# -*- coding: utf-8 -*-
"""
Local web UI for the workbench. Same CSV files, same run_requests.py /
import_approved.py logic underneath - this is a UI layer on top, not a
replacement. Nothing here talks to the network except your own browser.

Run:  python app.py
Then open the URL it prints (defaults to http://127.0.0.1:8848).
"""
import csv
import io
import json
import os
import sys
import webbrowser

from flask import Flask, jsonify, request, send_from_directory

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import run_requests  # noqa: E402
import import_approved  # noqa: E402
import generate_options_catalog  # noqa: E402

app = Flask(__name__, static_folder=os.path.join(HERE, 'static'), static_url_path='')
app.config['JSON_SORT_KEYS'] = False  # preserve the fixtures' authored key order (source/target/cases,
                                        # not alphabetical) through the GET -> edit -> POST round trip

TABLES = {
    'source_texts': {
        'path': 'source_texts.csv',
        'columns': ['id', 'script', 'label', 'text'],
        'editable': True,
    },
    'fanout_requests': {
        'path': 'fanout_requests.csv',
        'columns': ['source_text_id', 'mode', 'target_script', 'nativize'],
        'editable': True,
    },
    'option_test_requests': {
        'path': 'option_test_requests.csv',
        'columns': ['kind', 'option_name', 'source_script', 'target_script', 'input_text', 'extra_args'],
        'editable': True,
    },
    'options_catalog': {
        'path': 'options_catalog.csv',
        'columns': ['kind', 'name', 'backend_status', 'in_frontend', 'applies_to_scripts', 'label'],
        'editable': False,
    },
    'fanout_results': {
        'path': 'fanout_results.csv',
        'columns': ['source_text_id', 'source_script', 'label', 'mode', 'target_script', 'nativize',
                    'output', 'roundtrip_output', 'matches_original', 'error', 'approve'],
        'editable': True,
    },
    'option_test_results': {
        'path': 'option_test_results.csv',
        'columns': ['kind', 'option_name', 'source_script', 'target_script', 'input', 'output',
                    'baseline_output', 'meaningful', 'how_called', 'error', 'approve'],
        'editable': True,
    },
}


def table_path(name):
    return os.path.join(HERE, TABLES[name]['path'])


def read_table(name):
    path = table_path(name)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def write_table(name, rows):
    columns = TABLES[name]['columns']
    path = table_path(name)
    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({c: row.get(c, '') for c in columns})


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/tables')
def api_tables():
    return jsonify({name: {'editable': cfg['editable'], 'columns': cfg['columns']} for name, cfg in TABLES.items()})


@app.route('/api/table/<name>', methods=['GET'])
def api_get_table(name):
    if name not in TABLES:
        return jsonify({'error': 'unknown table'}), 404
    return jsonify({'columns': TABLES[name]['columns'], 'rows': read_table(name)})


@app.route('/api/table/<name>', methods=['POST'])
def api_save_table(name):
    if name not in TABLES:
        return jsonify({'error': 'unknown table'}), 404
    if not TABLES[name]['editable']:
        return jsonify({'error': 'table is read-only'}), 400
    rows = request.get_json(force=True).get('rows', [])
    write_table(name, rows)
    return jsonify({'ok': True, 'count': len(rows)})


@app.route('/api/run', methods=['POST'])
def api_run():
    which = request.get_json(force=True).get('which', 'both')
    log = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = log
    try:
        if which in ('fanout', 'both'):
            run_requests.run_fanout()
        if which in ('options', 'both'):
            run_requests.run_options()
    finally:
        sys.stdout = old_stdout
    return jsonify({'ok': True, 'log': log.getvalue()})


@app.route('/api/regenerate_catalog', methods=['POST'])
def api_regenerate_catalog():
    log = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = log
    try:
        generate_options_catalog_main()
    finally:
        sys.stdout = old_stdout
    return jsonify({'ok': True, 'log': log.getvalue()})


def generate_options_catalog_main():
    # generate_options_catalog.py runs its body at import time under
    # `if __name__ == '__main__'`? no - it runs at module level, so re-import
    # won't re-run it. Re-execute the file directly instead.
    path = os.path.join(HERE, 'generate_options_catalog.py')
    with open(path, 'r', encoding='utf-8') as f:
        code = f.read()
    exec(compile(code, path, 'exec'), {'__name__': '__main__', '__file__': path})


def _load_json(*parts):
    with open(os.path.join(*parts), 'r', encoding='utf-8') as f:
        return json.load(f)


@app.route('/api/script_lists')
def api_script_lists():
    """GeneralMap.py's script-category lists (IndicScripts, LatinScripts,
    SemiticScripts, ReversibleScripts, ...), regenerated fresh from the
    Python package on every request rather than served from the possibly-
    stale backend_script_lists.json snapshot on disk - this categorizes the
    Test Data tab's subtabs, so it should reflect the actual current
    GeneralMap.py, not whenever dump_backend_script_lists.py last ran."""
    reg_dir = os.path.dirname(HERE)
    sys.path.insert(0, os.path.abspath(os.path.join(reg_dir, '..', '..', '..')))
    from aksharamukha import GeneralMap as GM  # noqa: E402 (deliberately lazy - keeps this off the hot path)
    return jsonify({
        'IndicScripts': GM.IndicScripts,
        'LatinScripts': GM.LatinScripts,
        'SemiticScripts': GM.SemiticScripts,
        'NonIndic': GM.NonIndic,
        'ReversibleScripts': GM.ReversibleScripts,
        'RomanReversible': GM.RomanReversible,
    })


@app.route('/api/option_cases')
def api_option_cases():
    """The actual test-case data behind an option's green/red marking in the
    catalog - the catalog CSV only carries backend_status (a status word),
    never the cases themselves, so this is what backs the "cases" button."""
    kind = request.args.get('kind', '')
    name = request.args.get('name', '')
    paths = _fixture_paths()

    working_path = paths['post_path'] if kind == 'post' else paths['pre_path']
    working = _load_json(working_path)
    if name in working:
        return jsonify({'found': True, 'source': os.path.basename(working_path), 'blocks': working[name]})

    direct = _load_json(paths['direct_path'])
    key = kind + '::' + name
    if key in direct:
        entry = direct[key]
        return jsonify({'found': True, 'source': 'test_direct_options.json', 'blocks': [{
            'source': None, 'target': None, 'args': entry.get('args'), 'cases': entry['cases']
        }]})

    reg_dir = os.path.dirname(HERE)
    broken = _load_json(reg_dir, 'known_broken_options.json')
    if key in broken:
        return jsonify({'found': True, 'broken': broken[key]})

    return jsonify({'found': False})


def _fixture_paths():
    reg_dir = os.path.dirname(HERE)
    texts_dir = os.path.join(reg_dir, '..', 'test_texts')
    return {
        'post_path': os.path.join(texts_dir, 'test_postoptions.json'),
        'pre_path': os.path.join(texts_dir, 'test_preoptions.json'),
        'direct_path': os.path.join(reg_dir, 'test_direct_options.json'),
        'custom_path': os.path.join(texts_dir, 'test_custom_cases.json'),
    }


@app.route('/api/all_cases', methods=['GET'])
def api_all_cases():
    """The three trusted fixture files, verbatim - not flattened/rebuilt.

    An earlier version of this endpoint flattened every case into an
    independent row and reconstructed the JSON from scratch on save, which
    silently dropped anything not modeled in the row schema: a hand-written
    "comments" field on a block, an option with an empty cases list
    (AvestanConventions), the "custom_call" marker on JapanesePostProcess/
    defaultPost/JapanesePreProcess. Caught by diffing a no-op round-trip
    before it ever touched real data, but the fix is architectural, not a
    patch: never reconstruct. The client keeps exactly this object graph,
    mutates individual case pairs and block/entry lists in place, and saves
    the same structure back - so anything untouched survives byte-for-byte."""
    paths = _fixture_paths()
    return jsonify({
        'post': _load_json(paths['post_path']),
        'pre': _load_json(paths['pre_path']),
        'direct': _load_json(paths['direct_path']),
    })


@app.route('/api/all_cases', methods=['POST'])
def api_save_all_cases():
    """Writes back exactly what's posted - no reconstruction, no schema
    reduction. The client is expected to have started from what GET
    returned and only mutated it in place."""
    body = request.get_json(force=True)
    paths = _fixture_paths()
    with open(paths['post_path'], 'w', encoding='utf-8') as f:
        json.dump(body.get('post', {}), f, ensure_ascii=False, indent=4)
    with open(paths['pre_path'], 'w', encoding='utf-8') as f:
        json.dump(body.get('pre', {}), f, ensure_ascii=False, indent=4)
    with open(paths['direct_path'], 'w', encoding='utf-8') as f:
        json.dump(body.get('direct', {}), f, ensure_ascii=False, indent=1)
    return jsonify({'ok': True})


@app.route('/api/custom_cases', methods=['GET'])
def api_custom_cases():
    """Free-form test cases: unlike Post-options/Pre-options (one option at a
    time, keyed by option name), a custom case is a full transliterate.process
    call - source, target, nativize, and any combination of pre_options AND
    post_options together - for the situations neither of those tabs can
    express. Backed by test_texts/test_custom_cases.json, a flat list, and
    exercised for real by TestCustomCases in testsuite.py."""
    paths = _fixture_paths()
    if not os.path.exists(paths['custom_path']):
        return jsonify({'rows': []})
    return jsonify({'rows': _load_json(paths['custom_path'])})


@app.route('/api/custom_cases', methods=['POST'])
def api_save_custom_cases():
    rows = request.get_json(force=True).get('rows', [])
    paths = _fixture_paths()
    with open(paths['custom_path'], 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=4)
    return jsonify({'ok': True, 'count': len(rows)})


@app.route('/api/preview_custom_case', methods=['POST'])
def api_preview_custom_case():
    """Computes (doesn't save) the output for one custom case, for the
    Autogenerate button on the Custom Cases tab - runs the real pipeline with
    whatever pre_options/post_options combination was specified."""
    sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..')))
    from aksharamukha import transliterate  # noqa: E402

    body = request.get_json(force=True)
    source = (body.get('source') or '').strip()
    target = (body.get('target') or '').strip()
    text = body.get('input') or ''
    nativize = body.get('nativize', True)
    pre_options = body.get('pre_options') or []
    post_options = body.get('post_options') or []
    if not source or not target or not text:
        return jsonify({'ok': False, 'error': 'source, target and input are all required'}), 400

    try:
        output = transliterate.process(source, target, text, nativize=nativize,
                                        pre_options=pre_options, post_options=post_options)
    except Exception as e:  # noqa: BLE001
        return jsonify({'ok': False, 'error': '%s: %s' % (type(e).__name__, str(e)[:300])})
    return jsonify({'ok': True, 'output': output})


CONVERSION_SAMPLES_PATH = os.path.join(HERE, 'conversion_samples.json')


def _script_categories():
    reg_dir = os.path.dirname(HERE)
    sys.path.insert(0, os.path.abspath(os.path.join(reg_dir, '..', '..', '..')))
    from aksharamukha import GeneralMap as GM  # noqa: E402
    return {
        'reversible': set(GM.ReversibleScripts),
        'roman_reversible': set(GM.RomanReversible),
        'indic': set(GM.IndicScripts),
        'latin': set(GM.LatinScripts),
        'semitic': set(GM.SemiticScripts),
    }, GM


def _categorize_script(script, cats):
    if script in cats['reversible']:
        return 'reversible_indic'
    if script in cats['indic']:
        return 'irreversible_indic'
    if script in cats['roman_reversible']:
        return 'roman_reversible'
    if script in cats['latin']:
        return 'roman_irreversible'
    if script in cats['semitic']:
        return 'semitic'
    return 'other'


def _load_conversion_samples():
    if not os.path.exists(CONVERSION_SAMPLES_PATH):
        return []
    return _load_json(CONVERSION_SAMPLES_PATH)


def _save_conversion_samples(records):
    with open(CONVERSION_SAMPLES_PATH, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=1)


@app.route('/api/conversion_samples', methods=['GET'])
def api_get_conversion_samples():
    return jsonify({'rows': _load_conversion_samples()})


@app.route('/api/conversion_samples', methods=['POST'])
def api_save_conversion_samples_route():
    rows = request.get_json(force=True).get('rows', [])
    _save_conversion_samples(rows)
    return jsonify({'ok': True, 'count': len(rows)})


@app.route('/api/generate_conversion_samples', methods=['POST'])
def api_generate_conversion_samples():
    """Generates baseline (no-option) conversion samples for ONE source text -
    the (script, text, label) sent directly by the caller, i.e. a single row's
    button on the Source Texts tab, not a scan of the whole source_texts.csv.

    mode='all_fanout': the source text -> every script, one direction,
      ALWAYS both nativize=True and nativize=False (2 records per script,
      regardless of whether that script is documented reversible - the
      variant count is a property of which button generated it, not of the
      individual script).
    mode='reverse': the source text -> every REVERSIBLE script only
      (GeneralMap.ReversibleScripts / RomanReversible) -> back, checking the
      round trip, nativize=False only (1 record per script) - reversibility
      is a property of the raw mapping, not the nativized/stylized one.

    Optional 'target': restricts either mode to that ONE script instead of
    looping the whole list - the "generate just this pair" control on the
    Source Texts tab uses this so a single Arabic->Hebrew style pair doesn't
    require a full fanout.

    Existing records are keyed by (source, target, nativize, mode, label); a
    matching key gets replaced with the freshly-generated result, anything
    else already in conversion_samples.json is left alone.
    """
    sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..')))
    from aksharamukha import transliterate, GeneralMap as GM  # noqa: E402

    body = request.get_json(force=True)
    mode = body.get('mode', 'all_fanout')
    source = (body.get('script') or '').strip()
    text = body.get('text') or ''
    label = body.get('label') or ''
    single_target = (body.get('target') or '').strip() or None
    if not source or not text:
        return jsonify({'ok': False, 'error': 'script and text are required'}), 400

    cats, _ = _script_categories()

    existing = _load_conversion_samples()
    # label is part of the key: two source_texts.csv rows can share a script
    # (e.g. two Devanagari samples) and must produce independent records, not
    # overwrite each other just because source/target/nativize/mode match.
    index = {(r['source'], r['target'], r['nativize'], r['mode'], r.get('label')): i for i, r in enumerate(existing)}

    def safe_convert(src, tgt, txt, nativize):
        try:
            return {'ok': True, 'output': transliterate.process(src, tgt, txt, nativize=nativize)}
        except Exception as e:  # noqa: BLE001
            return {'ok': False, 'error': '%s: %s' % (type(e).__name__, str(e)[:200])}

    all_scripts = [s for s in set(GM.IndicScripts + GM.LatinScripts + GM.SemiticScripts + GM.NonIndic) if s != 'IPA']
    reversible_scripts = sorted(set(GM.ReversibleScripts) | set(GM.RomanReversible))
    if single_target:
        all_scripts = [single_target]
        reversible_scripts = [single_target]

    new_or_updated = 0

    if mode == 'all_fanout':
        for target in all_scripts:
            if target == source:
                continue
            for nativize in (True, False):
                res = safe_convert(source, target, text, nativize)
                record = {
                    'source': source, 'target': target, 'nativize': nativize, 'label': label,
                    'mode': 'fanout', 'category': _categorize_script(target, cats),
                    'input': text, 'output': res.get('output', ''), 'error': res.get('error', ''),
                }
                key = (source, target, nativize, 'fanout', label)
                if key in index:
                    existing[index[key]] = record
                else:
                    index[key] = len(existing)
                    existing.append(record)
                new_or_updated += 1

    elif mode == 'reverse':
        for target in reversible_scripts:
            if target == source:
                continue
            # Reversibility is a property of the raw/ISO-style mapping, not
            # the nativized (script-stylized) one - nativize=True applies
            # lossy per-script defaults (nukta removal, va/ba swaps, ...)
            # that are never guaranteed to round-trip. This matches how the
            # pytest suite itself checks reversibility (text_compare_reversible
            # / text_compare_reversible_2 in testsuite.py both use
            # nativize=False), so a round trip generated here with
            # nativize=True would fail for reasons that have nothing to do
            # with whether the script is actually reversible.
            fwd = safe_convert(source, target, text, False)
            rev = safe_convert(target, source, fwd.get('output', ''), False) if fwd['ok'] else {'ok': False, 'output': '', 'error': 'forward conversion failed'}
            record = {
                'source': source, 'target': target, 'nativize': False, 'label': label,
                'mode': 'roundtrip', 'category': _categorize_script(target, cats),
                'input': text, 'output': fwd.get('output', ''), 'error': fwd.get('error', '') or rev.get('error', ''),
                'roundtrip_output': rev.get('output', ''),
                'matches_original': bool(fwd['ok'] and rev['ok'] and rev.get('output', '') == text),
            }
            key = (source, target, False, 'roundtrip', label)
            if key in index:
                existing[index[key]] = record
            else:
                index[key] = len(existing)
                existing.append(record)
            new_or_updated += 1

    _save_conversion_samples(existing)
    return jsonify({'ok': True, 'generated_or_updated': new_or_updated, 'total': len(existing)})


@app.route('/api/generate_option_cases', methods=['POST'])
def api_generate_option_cases():
    """For every working single-argument option of the given kind, generate
    a case for EVERY script it applies to (per the catalog's applies_to_scripts,
    not just the one default pair the original coverage pass used), always at
    nativize=True. TestPostOptions/TestPreOptions call transliterate.process()
    without a nativize argument (default True) - generating nativize=False
    cases here would record a second, different expected output for the same
    input text under the same option, which the test can never satisfy since
    it only ever exercises nativize=True. Only touches options whose
    backend_status is already 'working' (single source_texts.csv sample text
    already known to succeed) - the 32 multi-arg options and the 4 broken
    ones are out of scope for this bulk pass; they're handled individually
    via the Direct Options tab / known_broken_options.json.

    The Devanagari base text is sent directly by the caller - a single
    Source Texts row's button - rather than auto-picked from source_texts.csv,
    so which row drives generation is explicit and visible in the UI."""
    sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..')))
    from aksharamukha import transliterate  # noqa: E402

    body = request.get_json(force=True)
    kind = body.get('kind', 'post')
    dev_text = body.get('text') or ''
    if not dev_text:
        return jsonify({'ok': False, 'error': 'text is required (send a Devanagari row from Source Texts)'}), 400

    catalog_rows = read_table('options_catalog')
    paths = _fixture_paths()
    working_path = paths['post_path'] if kind == 'post' else paths['pre_path']
    working = _load_json(working_path)

    sample_cache = {'Devanagari': dev_text}

    def get_sample(script):
        if script in sample_cache:
            return sample_cache[script]
        try:
            sample_cache[script] = transliterate.process('Devanagari', script, dev_text)
        except Exception:  # noqa: BLE001
            sample_cache[script] = None
        return sample_cache[script]

    added = 0
    for row in catalog_rows:
        if row['kind'] != kind or row['backend_status'] != 'working':
            continue
        name = row['name']
        scripts = [s.strip() for s in row['applies_to_scripts'].split(';') if s.strip() and 'all semitic' not in s]
        for script in scripts:
            source, target = ('Devanagari', script) if kind == 'post' else (script, 'Devanagari')
            text = get_sample(source)
            if not text:
                continue
            kwargs = {'post_options': [name]} if kind == 'post' else {'pre_options': [name]}
            try:
                output = transliterate.process(source, target, text, nativize=True, **kwargs)
            except Exception:  # noqa: BLE001
                continue
            blocks = working.setdefault(name, [])
            # nativize is part of the block's identity now, not just
            # source/target - a block's cases only make sense checked under
            # the ONE nativize value that produced them (see testsuite.py,
            # which reads testcase.get('nativize', True) per block). Matching
            # on source/target alone could silently merge this bulk-generated
            # nativize=True case into a manually-added nativize=False block.
            block = next((b for b in blocks if b.get('source') == source and b.get('target') == target
                          and b.get('nativize', True) is True), None)
            if block is None:
                block = {'source': source, 'target': target, 'nativize': True, 'cases': []}
                blocks.append(block)
            if [text, output] not in block['cases']:
                block['cases'].append([text, output])
                added += 1

    with open(working_path, 'w', encoding='utf-8') as f:
        json.dump(working, f, ensure_ascii=False, indent=4)
    return jsonify({'ok': True, 'added': added})


@app.route('/api/preview_option_case', methods=['POST'])
def api_preview_option_case():
    """Computes (doesn't save) the output for one manually-specified option
    case, for the 'Autogenerate' button on the Add Case form - lets you type
    the input yourself and have the expected output filled in by actually
    running the option, instead of copy-pasting a result computed elsewhere.
    nativize defaults to True (matching every existing case, and what
    TestPostOptions/TestPreOptions assume when a stored case has no nativize
    field) but can be set False - testsuite.py now reads a per-block
    'nativize' field back out and passes it through explicitly."""
    sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..')))
    from aksharamukha import transliterate  # noqa: E402

    body = request.get_json(force=True)
    kind = body.get('kind', 'post')
    name = (body.get('name') or '').strip()
    source = (body.get('source') or '').strip()
    target = (body.get('target') or '').strip()
    text = body.get('input') or ''
    nativize = body.get('nativize', True)
    if not name or not source or not target or not text:
        return jsonify({'ok': False, 'error': 'option name, source, target and input are all required'}), 400

    kwargs = {'post_options': [name]} if kind == 'post' else {'pre_options': [name]}
    try:
        output = transliterate.process(source, target, text, nativize=nativize, **kwargs)
    except Exception as e:  # noqa: BLE001
        return jsonify({'ok': False, 'error': '%s: %s' % (type(e).__name__, str(e)[:300])})
    return jsonify({'ok': True, 'output': output})


@app.route('/api/import', methods=['POST'])
def api_import():
    apply_ = bool(request.get_json(force=True).get('apply', False))
    log = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = log
    try:
        import_approved.import_options(apply_)
        import_approved.import_fanout(apply_)
    finally:
        sys.stdout = old_stdout
    return jsonify({'ok': True, 'applied': apply_, 'log': log.getvalue()})


if __name__ == '__main__':
    port = 8848
    url = 'http://127.0.0.1:%d' % port
    print('Workbench running at', url)
    try:
        webbrowser.open(url)
    except Exception:
        pass
    app.run(host='127.0.0.1', port=port, debug=False)
