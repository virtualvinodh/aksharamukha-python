// Builds frontend_backend_manifest.json: one file combining every script,
// pre-option, and post-option the *frontend* (aksharamukha-front's
// ScriptMixin.js - labels, descriptions, per-script option groupings) knows
// about with what the *backend* (this repo's regression suite - see
// generate_full_option_coverage.py / promote_direct_call_options.py) has
// confirmed actually exists and works.
//
// Cross-references both directions:
//   - scripts/options the frontend lists that the backend doesn't recognize
//     (dead UI references - e.g. this run found 'qafTwodot')
//   - scripts/options the backend supports that the frontend never exposes
//
// Requires Node (no npm deps) and a checkout of the frontend repo. Adjust
// FRONTEND_ROOT below if your sibling checkout lives somewhere else.
//
// Run: node dump_backend_script_lists.py's Python counterpart first
//   (python dump_backend_script_lists.py), then:
//   node build_frontend_backend_manifest.js

const fs = require('fs');
const path = require('path');

const FRONTEND_ROOT = 'c:\\Users\\vinod\\Projects\\aksharamukha\\aksharamukha-front';
const MIXIN_PATH = path.join(FRONTEND_ROOT, 'src', 'mixins', 'ScriptMixin.js');

const HERE = __dirname;
const TEXTS = path.join(HERE, '..', 'test_texts');

// ---------- extract the plain-data part of ScriptMixin.js's data() ----------
function extractFrontendData (mixinPath) {
  const src = fs.readFileSync(mixinPath, 'utf8');
  const lines = src.split('\n');

  const dataStart = lines.findIndex(l => /^\s*data \(\) \{/.test(l));
  const computedStart = lines.findIndex(l => /^  computed:/.test(l));
  if (dataStart === -1 || computedStart === -1) {
    throw new Error('Could not locate data()/computed: boundaries - ScriptMixin.js structure changed, update this script');
  }
  // skip the "return {" opening line, and the two closing lines below the
  // last real key ("    }" closing the return-object, "  }," closing data())
  const body = lines.slice(dataStart + 2, computedStart - 2).join('\n');

  const stripped = body
    .replace(/apiCall: this\.\$axios\.create\(\{[\s\S]*?\}\),\r?\n/, '')
    .replace(/wikipediaCall: this\.\$axios\.create\(\{[\s\S]*?\}\),\r?\n/, '')
    .replace(/scriptSourceCall: this\.\$axios\.create\(\{[\s\S]*?\}\),\r?\n/, '');

  // eslint-disable-next-line no-new-func
  return new Function('return {\n' + stripped + '\n};')();
}

const fe = extractFrontendData(MIXIN_PATH);
const backendScripts = JSON.parse(fs.readFileSync(path.join(HERE, 'backend_script_lists.json'), 'utf8'));
const postWorking = JSON.parse(fs.readFileSync(path.join(TEXTS, 'test_postoptions.json'), 'utf8'));
const preWorking = JSON.parse(fs.readFileSync(path.join(TEXTS, 'test_preoptions.json'), 'utf8'));
const direct = JSON.parse(fs.readFileSync(path.join(HERE, 'test_direct_options.json'), 'utf8'));
const broken = JSON.parse(fs.readFileSync(path.join(HERE, 'known_broken_options.json'), 'utf8'));

// ---------- SCRIPTS ----------
const scriptFamilies = {
  scriptsIndic: 'Indic',
  scriptsSemitic: 'Semitic',
  scriptsLatin: 'Latin',
  scriptsRomanization: 'Romanization',
  scriptsIME: 'IME'
};

const scripts = {};
for (const [arrKey, family] of Object.entries(scriptFamilies)) {
  for (const entry of (fe[arrKey] || [])) {
    const value = entry.value;
    if (!value) continue;
    if (!scripts[value]) {
      scripts[value] = {
        value,
        label: entry.label || value,
        families: [],
        description: entry.ssdesc || entry.miscdesc || '',
        region: entry.region || [],
        status: entry.status || [],
        language: entry.language || [],
        derivation: entry.invented || [],
        font: entry.font || null,
        codes: {
          scriptSource: entry.sscode || '',
          omniglot: entry.omnicode || '',
          wikipedia: entry.wikicode || ''
        },
        misc_source: entry.miscsrc || ''
      };
    }
    if (!scripts[value].families.includes(family)) scripts[value].families.push(family);
  }
}

const inList = (name, list) => backendScripts[list].includes(name);
for (const value of Object.keys(scripts)) {
  const mappedSemitic = backendScripts.semiticISO[value]; // e.g. ISO259 -> Hebrew, not a script of its own
  scripts[value].backend = {
    in_IndicScripts: inList(value, 'IndicScripts'),
    in_LatinScripts: inList(value, 'LatinScripts'),
    in_SemiticScripts: inList(value, 'SemiticScripts'),
    in_NonIndic: inList(value, 'NonIndic'),
    is_reversible: inList(value, 'ReversibleScripts') || inList(value, 'RomanReversible'),
    supports_LoC: inList(value, 'LoCScripts'),
    semitic_iso_variant_of: mappedSemitic || null
  };
  const b = scripts[value].backend;
  scripts[value].found_in_backend = b.in_IndicScripts || b.in_LatinScripts || b.in_SemiticScripts ||
    b.in_NonIndic || !!mappedSemitic;
}

const allBackendScripts = new Set([
  ...backendScripts.IndicScripts, ...backendScripts.LatinScripts,
  ...backendScripts.SemiticScripts, ...backendScripts.NonIndic
]);
const frontendOnly = Object.keys(scripts).filter(v => !scripts[v].found_in_backend);
const backendOnly = [...allBackendScripts].filter(v => !scripts[v]);

// ---------- OPTIONS ----------
function backendStatus (kind, name) {
  const workingMap = kind === 'post' ? postWorking : preWorking;
  if (Object.prototype.hasOwnProperty.call(workingMap, name)) return 'working';
  if (Object.prototype.hasOwnProperty.call(direct, kind + '::' + name)) return 'working-multi-arg';
  if (Object.prototype.hasOwnProperty.call(broken, kind + '::' + name)) return 'broken';
  return 'unknown-to-backend';
}

function collectFrontendOptions (groups) {
  const out = {};
  for (const [scriptName, entries] of Object.entries(groups || {})) {
    for (const e of entries) {
      if (!e || !e.value) continue;
      if (!out[e.value]) out[e.value] = { labels: new Set(), applies_to: [] };
      if (e.label) out[e.value].labels.add(e.label);
      out[e.value].applies_to.push(scriptName);
    }
  }
  return out;
}

function collectFrontendOptionsFromList (list, scriptName) {
  const out = {};
  for (const e of (list || [])) {
    if (!e || !e.value) continue;
    if (!out[e.value]) out[e.value] = { labels: new Set(), applies_to: [] };
    if (e.label) out[e.value].labels.add(e.label);
    out[e.value].applies_to.push(scriptName || '(all semitic)');
  }
  return out;
}

function mergeInto (target, src) {
  for (const [k, v] of Object.entries(src)) {
    if (!target[k]) target[k] = { labels: new Set(), applies_to: [] };
    v.labels.forEach(l => target[k].labels.add(l));
    target[k].applies_to.push(...v.applies_to);
  }
}

const feProAll = {};
mergeInto(feProAll, collectFrontendOptions(fe.preOptionsGroup));
mergeInto(feProAll, collectFrontendOptions(fe.preOptionsIndic));
mergeInto(feProAll, collectFrontendOptions(fe.preOptionsGroupSpecific));
mergeInto(feProAll, collectFrontendOptionsFromList(fe.preOptionSemiticAllIndic, '(all semitic->indic)'));
mergeInto(feProAll, collectFrontendOptions(fe.preOptionsSemitic));

const fePostAll = {};
mergeInto(fePostAll, collectFrontendOptions(fe.postOptionsGroup));
mergeInto(fePostAll, collectFrontendOptions(fe.postOptionsIndic));
mergeInto(fePostAll, collectFrontendOptions(fe.postOptionsSemitic));
mergeInto(fePostAll, collectFrontendOptions(fe.postOptionsGroupSpecific));

const postRadioGroups = fe.postOptionsRadioGroup || {};

function buildOptionSection (kind, feMap, workingMap) {
  const names = new Set([
    ...Object.keys(workingMap),
    ...Object.keys(direct).filter(k => k.startsWith(kind + '::')).map(k => k.slice(kind.length + 2)),
    ...Object.keys(broken).filter(k => k.startsWith(kind + '::')).map(k => k.slice(kind.length + 2)),
    ...Object.keys(feMap)
  ]);
  const out = {};
  for (const name of [...names].sort()) {
    const fe_ = feMap[name];
    out[name] = {
      name,
      backend_status: backendStatus(kind, name),
      in_frontend: !!fe_,
      labels: fe_ ? [...fe_.labels] : [],
      applies_to_scripts: fe_ ? [...new Set(fe_.applies_to)] : []
    };
  }
  return out;
}

const pre_options = buildOptionSection('pre', feProAll, preWorking);
const post_options = buildOptionSection('post', fePostAll, postWorking);

function counts (section) {
  const vals = Object.values(section);
  return {
    total: vals.length,
    working: vals.filter(o => o.backend_status === 'working').length,
    working_multi_arg: vals.filter(o => o.backend_status === 'working-multi-arg').length,
    broken: vals.filter(o => o.backend_status === 'broken').length,
    unknown_to_backend: vals.filter(o => o.backend_status === 'unknown-to-backend').length,
    in_frontend: vals.filter(o => o.in_frontend).length,
    not_in_frontend: vals.filter(o => !o.in_frontend).length
  };
}

const manifest = {
  _generated_by: 'build_frontend_backend_manifest.js',
  _generated_at: new Date().toISOString(),
  _sources: {
    frontend: MIXIN_PATH,
    backend_scripts: 'GeneralMap.py, via dump_backend_script_lists.py',
    backend_options: 'test_texts/test_postoptions.json, test_texts/test_preoptions.json, ' +
      'regression/test_direct_options.json, regression/known_broken_options.json'
  },
  summary: {
    scripts_total: Object.keys(scripts).length,
    scripts_in_frontend_but_not_backend: frontendOnly,
    scripts_in_backend_but_not_frontend: backendOnly,
    pre_options: counts(pre_options),
    post_options: counts(post_options)
  },
  scripts,
  pre_options,
  post_options,
  post_options_radio_groups: postRadioGroups
};

const outPath = path.join(HERE, 'frontend_backend_manifest.json');
fs.writeFileSync(outPath, JSON.stringify(manifest, null, 1), 'utf8');
console.log('wrote', outPath);
console.log(JSON.stringify(manifest.summary, null, 1));
