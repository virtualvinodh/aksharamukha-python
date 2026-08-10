# -*- coding: utf-8 -*-
"""
Golden-output regression corpus generator for aksharamukha.

Captures CURRENT behavior (bugs included) across three axes so that a future
refactor/migration can be diffed against a known baseline instead of trusted
on faith:

  1. baseline_hash.json   - hashes of the 622 existing test_texts/test_*.txt
                             fixtures (Devanagari/IAST -> every target script,
                             no options), so drift in the *existing* fixtures
                             is detected too.
  2. roundtrip.json        - NEW: for every target script, forward conversion
                             from Devanagari/IAST AND the reverse round-trip
                             back, under both nativize=True and nativize=False.
                             The existing suite only ever tested the forward
                             direction.
  3. options.json           - NEW: every function in PreProcess.py and
                             PostProcess.py that is reachable as a
                             pre_options=[...] / post_options=[...] value,
                             exercised at least once through the public API.
                             The existing test_postoptions.json fixture only
                             covers 34 of ~327 PostProcess functions; every
                             other option silently no-ops in that suite via
                             a caught KeyError. This covers all of them.

Every record stores the *result* (output text, or exception type + message)
rather than an assertion of correctness - this is a snapshot of current
behavior, warts and all, to diff against, not a claim that the current
behavior is right.

Run:  python generate_golden.py
Compare a later run against this one with compare_golden.py.
"""
import hashlib
import inspect
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from aksharamukha import transliterate, GeneralMap, PreProcess, PostProcess  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TEST_TEXTS_DIR = os.path.abspath(os.path.join(HERE, '..', 'test_texts'))
OUT_DIR = HERE

# Tamil -> IPA makes a live, unbounded, timeout-less HTTP call to a third
# party endpoint (transliterate.py:524-527, flagged in the earlier audit).
# Excluded here so the suite stays offline and finite.
EXCLUDE_TARGETS = {'IPA'}

SAMPLE_TEXT_NAME = 'heart'


def load_sample(script):
    path = os.path.join(TEST_TEXTS_DIR, 'source_%s_%s.txt' % (script, SAMPLE_TEXT_NAME))
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def safe_call(fn, *args, **kwargs):
    """Run fn, capturing either the result or a compact error description."""
    try:
        result = fn(*args, **kwargs)
        return {'ok': True, 'output': result}
    except Exception as e:  # noqa: BLE001 - intentionally broad, this is a probe
        return {'ok': False, 'error_type': type(e).__name__, 'error': str(e)[:300]}


# ---------------------------------------------------------------------------
# Part 1: hash the 622 existing baseline fixtures already in test_texts/
# ---------------------------------------------------------------------------
def hash_existing_baseline():
    records = []
    for fname in sorted(os.listdir(TEST_TEXTS_DIR)):
        if not fname.startswith('test_') or not fname.endswith('.txt'):
            continue
        path = os.path.join(TEST_TEXTS_DIR, fname)
        with open(path, 'rb') as f:
            content = f.read()
        records.append({
            'file': fname,
            'sha256': hashlib.sha256(content).hexdigest(),
            'bytes': len(content),
        })
    return records


# ---------------------------------------------------------------------------
# Part 2: forward + round-trip matrix, both nativize states, every script
# ---------------------------------------------------------------------------
def all_target_scripts():
    names = list(dict.fromkeys(
        GeneralMap.IndicScripts + GeneralMap.Roman + GeneralMap.SemiticScripts + GeneralMap.NonIndic
    ))
    return [n for n in names if n not in EXCLUDE_TARGETS]


def build_roundtrip_matrix():
    records = []
    targets = all_target_scripts()
    sources = ['Devanagari', 'IAST']
    sample = {s: load_sample(s) for s in sources}

    total = len(sources) * len(targets) * 2
    done = 0
    t0 = time.time()
    for source in sources:
        src_text = sample[source]
        for target in targets:
            for nativize in (True, False):
                done += 1
                fwd = safe_call(transliterate.process, source, target, src_text, nativize=nativize)
                rec = {
                    'source': source, 'target': target, 'nativize': nativize,
                    'forward': fwd,
                }
                if fwd['ok']:
                    rev = safe_call(transliterate.process, target, source, fwd['output'], nativize=nativize)
                    rec['roundtrip'] = rev
                    rec['roundtrip_matches_source'] = rev.get('ok') and rev.get('output') == src_text
                else:
                    rec['roundtrip'] = None
                    rec['roundtrip_matches_source'] = False
                records.append(rec)
                if done % 100 == 0:
                    print('  roundtrip %d/%d (%.0fs elapsed)' % (done, total, time.time() - t0))
    return records


# ---------------------------------------------------------------------------
# Part 3: exercise every Pre/PostProcess option at least once
# ---------------------------------------------------------------------------
def own_functions(module):
    return [
        name for name, obj in inspect.getmembers(module, inspect.isfunction)
        if obj.__module__ == module.__name__ and not name.startswith('_')
    ]


def infer_script_from_option_name(option_name, all_scripts_sorted_desc):
    for script in all_scripts_sorted_desc:
        if script in option_name:
            return script
    return None


def build_options_matrix():
    all_scripts = sorted(set(all_target_scripts()), key=len, reverse=True)
    dev_heart = load_sample('Devanagari')
    iast_heart = load_sample('IAST')

    records = []

    post_fns = own_functions(PostProcess)
    pre_fns = own_functions(PreProcess)

    print('  %d PostProcess functions, %d PreProcess functions to exercise' % (len(post_fns), len(pre_fns)))

    for name in post_fns:
        target = infer_script_from_option_name(name, all_scripts)
        source, tgt = ('Devanagari', target) if target else ('Devanagari', 'IAST')
        res = safe_call(transliterate.process, source, tgt, dev_heart, post_options=[name])
        records.append({'kind': 'post_option', 'name': name, 'source': source, 'target': tgt, 'result': res})

    for name in pre_fns:
        matched = infer_script_from_option_name(name, all_scripts)
        source, tgt = (matched, 'Devanagari') if matched else ('IAST', 'Devanagari')
        text = dev_heart if source == 'Devanagari' else iast_heart
        res = safe_call(transliterate.process, source, tgt, text, pre_options=[name])
        records.append({'kind': 'pre_option', 'name': name, 'source': source, 'target': tgt, 'result': res})

    return records


def git_commit():
    try:
        return subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'],
            cwd=os.path.join(HERE, '..', '..', '..'), text=True
        ).strip()
    except Exception:
        return None


def main():
    t0 = time.time()
    print('== Part 1: hashing existing baseline fixtures ==')
    baseline = hash_existing_baseline()
    print('  %d existing fixture files hashed' % len(baseline))
    with open(os.path.join(OUT_DIR, 'baseline_hash.json'), 'w', encoding='utf-8') as f:
        json.dump(baseline, f, ensure_ascii=False, indent=1)

    print('== Part 2: forward + round-trip matrix ==')
    roundtrip = build_roundtrip_matrix()
    with open(os.path.join(OUT_DIR, 'roundtrip.json'), 'w', encoding='utf-8') as f:
        json.dump(roundtrip, f, ensure_ascii=False, indent=1)

    print('== Part 3: per-option exercise ==')
    options = build_options_matrix()
    with open(os.path.join(OUT_DIR, 'options.json'), 'w', encoding='utf-8') as f:
        json.dump(options, f, ensure_ascii=False, indent=1)

    manifest = {
        'generated_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'git_commit': git_commit(),
        'python_version': sys.version,
        'counts': {
            'baseline_fixtures': len(baseline),
            'roundtrip_records': len(roundtrip),
            'option_records': len(options),
        },
        'elapsed_seconds': round(time.time() - t0, 1),
    }
    with open(os.path.join(OUT_DIR, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)

    print('== done in %.0fs ==' % (time.time() - t0))
    print(json.dumps(manifest, indent=1))


if __name__ == '__main__':
    main()
