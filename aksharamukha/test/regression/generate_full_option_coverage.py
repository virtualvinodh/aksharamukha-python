# -*- coding: utf-8 -*-
"""
Fills the gap the previous regression pass found: only 34 of ~326
PostProcess functions (and 0 of ~129 PreProcess functions) have a real,
asserted test case anywhere in the repo. Every other option silently
no-ops in testsuite.py's TestPostOptions via a caught KeyError.

This script:
  1. Preserves every hand-authored entry already in test_texts/test_postoptions.json
     untouched (those are curated, minimal, presumably hand-verified cases -
     not overwritten).
  2. For every remaining callable single-arg option in PostProcess.py and
     PreProcess.py, generates real [input, output] cases by actually running
     transliterate.process() - i.e. characterization tests: current output
     becomes the asserted expected value. These are NOT a claim that the
     output is linguistically correct, only that it's what the option does
     today; that's what makes them useful as a regression trip-wire.
  3. Flags, per option, whether the generated case is "meaningful" (the
     option's output actually differs from the no-option baseline on that
     input) vs merely present-but-untriggered - and reports the split
     honestly instead of padding the count.
  4. Separately records every option that isn't safely callable as a bare
     post_options=[name]/pre_options=[name] value at all (crashes with
     TypeError/etc.) - these get a "does this still raise the same way"
     test instead of a bogus success case.

Outputs:
  test_texts/test_postoptions.json   (existing 34 entries preserved, ~292 added)
  test_texts/test_preoptions.json    (new, ~100+ entries)
  regression/known_broken_options.json (new, ~36 entries)
  regression/coverage_report.json     (summary stats)
"""
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from aksharamukha import transliterate  # noqa: E402
import generate_golden as gg  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TEST_TEXTS_DIR = os.path.abspath(os.path.join(HERE, '..', 'test_texts'))

TEXT_NAMES = ['heart', 'lalitavistara']

_sample_cache = {}


def get_sample(script, text_name):
    """Sample text in `script`. Devanagari/IAST load the static fixture files;
    every other script gets one derived on the fly (and cached) by converting
    the Devanagari original, so every option gets a real, script-appropriate
    input regardless of whether a static fixture exists for it."""
    key = (script, text_name)
    if key in _sample_cache:
        return _sample_cache[key]

    if script in ('Devanagari', 'IAST'):
        path = os.path.join(TEST_TEXTS_DIR, 'source_%s_%s.txt' % (script, text_name))
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        _sample_cache[key] = text
        return text

    base = get_sample('Devanagari', text_name)
    try:
        text = transliterate.process('Devanagari', script, base)
    except Exception:
        text = None
    _sample_cache[key] = text
    return text


_baseline_cache = {}


def get_baseline(source, target, text_name):
    key = (source, target, text_name)
    if key in _baseline_cache:
        return _baseline_cache[key]
    text = get_sample(source, text_name)
    if text is None:
        _baseline_cache[key] = None
        return None
    try:
        out = transliterate.process(source, target, text)
    except Exception:
        out = None
    _baseline_cache[key] = out
    return out


def build_for_option(kind, name, all_scripts_sorted_desc):
    matched = gg.infer_script_from_option_name(name, all_scripts_sorted_desc)
    if kind == 'post':
        source, target = 'Devanagari', (matched or 'IAST')
    else:
        source, target = (matched or 'IAST'), 'Devanagari'

    cases = []
    meaningful = False
    first_error = None

    for text_name in TEXT_NAMES:
        input_text = get_sample(source, text_name)
        if input_text is None:
            continue
        kwargs = {'post_options': [name]} if kind == 'post' else {'pre_options': [name]}
        try:
            output = transliterate.process(source, target, input_text, **kwargs)
        except Exception as e:  # noqa: BLE001
            if first_error is None:
                first_error = {'error_type': type(e).__name__, 'error': str(e)[:300]}
            continue

        cases.append([input_text, output])
        baseline = get_baseline(source, target, text_name)
        if baseline is not None and output != baseline:
            meaningful = True

    if cases:
        return {
            'status': 'working',
            'source': source, 'target': target,
            'cases': cases, 'meaningful': meaningful,
        }
    else:
        return {
            'status': 'broken',
            'source': source, 'target': target,
            'error': first_error or {'error_type': 'Unknown', 'error': 'no case produced output'},
        }


def main():
    all_scripts = sorted(set(gg.all_target_scripts()), key=len, reverse=True)

    post_names = gg.own_functions(__import__('aksharamukha.PostProcess', fromlist=['x']))
    pre_names = gg.own_functions(__import__('aksharamukha.PreProcess', fromlist=['x']))

    existing_post_path = os.path.join(TEST_TEXTS_DIR, 'test_postoptions.json')
    with open(existing_post_path, 'r', encoding='utf-8') as f:
        post_fixture = json.load(f)
    preserved = set(post_fixture.keys())

    broken = {}
    report = {'post': {'preserved': len(preserved), 'added_working': 0, 'added_meaningful': 0,
                        'added_not_meaningful': 0, 'broken': 0},
              'pre': {'added_working': 0, 'added_meaningful': 0, 'added_not_meaningful': 0, 'broken': 0}}

    print('Building POST options (%d total, %d already have hand-authored cases)...' % (len(post_names), len(preserved)))
    for i, name in enumerate(post_names):
        if name in preserved:
            continue
        result = build_for_option('post', name, all_scripts)
        if result['status'] == 'working':
            post_fixture[name] = [{'source': result['source'], 'target': result['target'], 'cases': result['cases']}]
            report['post']['added_working'] += 1
            if result['meaningful']:
                report['post']['added_meaningful'] += 1
            else:
                report['post']['added_not_meaningful'] += 1
        else:
            broken['post::' + name] = {'kind': 'post', 'name': name, 'source': result['source'],
                                        'target': result['target'], **result['error']}
            report['post']['broken'] += 1
        if (i + 1) % 50 == 0:
            print('  post %d/%d' % (i + 1, len(post_names)))

    print('Building PRE options (%d total)...' % len(pre_names))
    pre_fixture = {}
    for i, name in enumerate(pre_names):
        result = build_for_option('pre', name, all_scripts)
        if result['status'] == 'working':
            pre_fixture[name] = [{'source': result['source'], 'target': result['target'], 'cases': result['cases']}]
            report['pre']['added_working'] += 1
            if result['meaningful']:
                report['pre']['added_meaningful'] += 1
            else:
                report['pre']['added_not_meaningful'] += 1
        else:
            broken['pre::' + name] = {'kind': 'pre', 'name': name, 'source': result['source'],
                                       'target': result['target'], **result['error']}
            report['pre']['broken'] += 1
        if (i + 1) % 50 == 0:
            print('  pre %d/%d' % (i + 1, len(pre_names)))

    with open(existing_post_path, 'w', encoding='utf-8') as f:
        json.dump(post_fixture, f, ensure_ascii=False, indent=4)

    with open(os.path.join(TEST_TEXTS_DIR, 'test_preoptions.json'), 'w', encoding='utf-8') as f:
        json.dump(pre_fixture, f, ensure_ascii=False, indent=4)

    with open(os.path.join(HERE, 'known_broken_options.json'), 'w', encoding='utf-8') as f:
        json.dump(broken, f, ensure_ascii=False, indent=1)

    report['totals'] = {
        'post_options_total': len(post_names),
        'pre_options_total': len(pre_names),
        'post_with_test_case': len(post_fixture),
        'pre_with_test_case': len(pre_fixture),
        'known_broken': len(broken),
        'grand_total_options': len(post_names) + len(pre_names),
        'grand_total_with_case_or_tracked_break': len(post_fixture) + len(pre_fixture) + len(broken),
    }
    with open(os.path.join(HERE, 'coverage_report.json'), 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=1)

    print(json.dumps(report, indent=1))


if __name__ == '__main__':
    main()
