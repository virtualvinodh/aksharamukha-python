# -*- coding: utf-8 -*-
"""
Reads source_texts.csv / fanout_requests.csv / option_test_requests.csv and
runs every request for real through transliterate.process(), writing
fanout_results.csv and option_test_results.csv. Nothing here touches the
real test fixtures - review the results CSVs (there's an empty 'approve'
column to fill in 'yes'/'no'), then run import_approved.py to merge the
approved rows into test_texts/test_postoptions.json etc.

Run:  python run_requests.py
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REG = os.path.dirname(HERE)
sys.path.insert(0, os.path.abspath(os.path.join(REG, '..', '..', '..')))

from aksharamukha import transliterate, GeneralMap as GM, PreProcess, PostProcess  # noqa: E402

sys.path.insert(0, REG)
import generate_golden as gg  # noqa: E402
import promote_direct_call_options as pdc  # noqa: E402


def read_csv(name):
    path = os.path.join(HERE, name)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def write_csv(name, rows, fieldnames):
    path = os.path.join(HERE, name)
    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print('wrote', path, '-', len(rows), 'rows')


def safe_convert(source, target, text, **kwargs):
    try:
        return {'ok': True, 'output': transliterate.process(source, target, text, **kwargs)}
    except Exception as e:  # noqa: BLE001
        return {'ok': False, 'error': '%s: %s' % (type(e).__name__, str(e)[:200])}


def error_str(res):
    return '' if res['ok'] else res['error']


# ---------------------------------------------------------------------------
# fan-out / round-trip
# ---------------------------------------------------------------------------
def run_fanout():
    texts = {row['id']: row for row in read_csv('source_texts.csv')}
    requests_ = read_csv('fanout_requests.csv')
    results = []

    for req in requests_:
        src_row = texts.get(req['source_text_id'])
        if not src_row:
            print('  skip: unknown source_text_id', req.get('source_text_id'))
            continue
        source, text, label = src_row['script'], src_row['text'], src_row['label']
        nativize = req.get('nativize', 'true').strip().lower() != 'false'
        mode = req['mode'].strip()

        if mode == 'all_scripts':
            for target in gg.all_target_scripts():
                if target == source:
                    continue
                res = safe_convert(source, target, text, nativize=nativize)
                results.append({
                    'source_text_id': req['source_text_id'], 'source_script': source, 'label': label,
                    'mode': mode, 'target_script': target, 'nativize': nativize,
                    'output': res.get('output', ''), 'roundtrip_output': '', 'matches_original': '',
                    'error': error_str(res), 'approve': ''
                })

        elif mode == 'round_trip':
            target_field = (req.get('target_script') or '').strip()
            targets = [target_field] if target_field else sorted(set(GM.ReversibleScripts + GM.RomanReversible))
            for target in targets:
                fwd = safe_convert(source, target, text, nativize=nativize)
                if not fwd['ok']:
                    results.append({
                        'source_text_id': req['source_text_id'], 'source_script': source, 'label': label,
                        'mode': mode, 'target_script': target, 'nativize': nativize,
                        'output': '', 'roundtrip_output': '', 'matches_original': '',
                        'error': error_str(fwd), 'approve': ''
                    })
                    continue
                rev = safe_convert(target, source, fwd['output'], nativize=nativize)
                matches = rev['ok'] and rev['output'] == text
                results.append({
                    'source_text_id': req['source_text_id'], 'source_script': source, 'label': label,
                    'mode': mode, 'target_script': target, 'nativize': nativize,
                    'output': fwd['output'], 'roundtrip_output': rev.get('output', ''),
                    'matches_original': matches, 'error': error_str(rev), 'approve': ''
                })
        else:
            print('  skip: unknown mode', mode)

    write_csv('fanout_results.csv', results,
              ['source_text_id', 'source_script', 'label', 'mode', 'target_script', 'nativize',
               'output', 'roundtrip_output', 'matches_original', 'error', 'approve'])


# ---------------------------------------------------------------------------
# option test cases
# ---------------------------------------------------------------------------
def parse_extra_args(field):
    parts = [p.strip() for p in field.split(',') if p.strip() != '']
    out = []
    for p in parts:
        if p.lower() == 'true':
            out.append(True)
        elif p.lower() == 'false':
            out.append(False)
        else:
            out.append(p)
    return out


def run_option(kind, name, source, target, text, extra_args):
    """Mirrors the real investigation from promote_direct_call_options.py:
    try the public single-arg path first, fall back to a direct call with
    known (or user-supplied) extra arguments if that's what it needs."""
    module = PostProcess if kind == 'post' else PreProcess

    if extra_args:
        try:
            return {'ok': True, 'output': getattr(module, name)(text, *extra_args), 'how': 'direct-call (user extra_args)'}
        except Exception as e:  # noqa: BLE001
            return {'ok': False, 'error': '%s: %s' % (type(e).__name__, str(e)[:200]), 'how': 'direct-call (user extra_args)'}

    kwargs = {'post_options': [name]} if kind == 'post' else {'pre_options': [name]}
    res = safe_convert(source, target, text, **kwargs)
    if res['ok']:
        return {**res, 'how': 'post_options=[]/pre_options=[]'}

    if not res['ok'] and 'TypeError' in res['error'] and 'positional argument' in res['error']:
        table = pdc.GENERIC_POST if kind == 'post' else pdc.GENERIC_PRE
        if name in table:
            try:
                out = getattr(module, name)(text, *table[name])
                return {'ok': True, 'output': out, 'how': 'direct-call (known args from promote_direct_call_options.py)'}
            except Exception as e:  # noqa: BLE001
                return {'ok': False, 'error': '%s: %s' % (type(e).__name__, str(e)[:200]), 'how': 'direct-call (known args)'}
        custom = pdc.CUSTOM_CALLS.get((kind, name))
        if custom:
            try:
                return {'ok': True, 'output': custom(text), 'how': 'direct-call (custom shape)'}
            except Exception as e:  # noqa: BLE001
                return {'ok': False, 'error': '%s: %s' % (type(e).__name__, str(e)[:200]), 'how': 'direct-call (custom shape)'}
        return {**res, 'how': 'post_options=[]/pre_options=[] - needs extra_args, none known; fill in the extra_args column'}

    return {**res, 'how': 'post_options=[]/pre_options=[]'}


def run_options():
    requests_ = read_csv('option_test_requests.csv')
    results = []
    for req in requests_:
        kind, name = req['kind'].strip(), req['option_name'].strip()
        source, target, text = req['source_script'].strip(), req['target_script'].strip(), req['input_text']
        extra_args = parse_extra_args(req.get('extra_args', '') or '')

        res = run_option(kind, name, source, target, text, extra_args)

        # A direct call's output is still in the option's own input space (e.g.
        # a PreProcess function returns modified *source*-script text, not the
        # final converted target-script text) - so "meaningful" there means
        # "did it change the text at all", not "does it differ from the full
        # pipeline's target-script output", which would always be true/false
        # for the wrong reason (comparing across scripts).
        if res.get('how', '').startswith('direct-call'):
            baseline_output = text
        else:
            baseline = safe_convert(source, target, text)
            baseline_output = baseline.get('output', '')

        meaningful = res['ok'] and res.get('output') != baseline_output
        results.append({
            'kind': kind, 'option_name': name, 'source_script': source, 'target_script': target,
            'input': text, 'output': res.get('output', ''), 'baseline_output': baseline_output,
            'meaningful': meaningful, 'how_called': res.get('how', ''), 'error': error_str(res),
            'approve': ''
        })

    write_csv('option_test_results.csv', results,
              ['kind', 'option_name', 'source_script', 'target_script', 'input', 'output',
               'baseline_output', 'meaningful', 'how_called', 'error', 'approve'])


if __name__ == '__main__':
    print('== fan-out / round-trip requests ==')
    run_fanout()
    print('== option test requests ==')
    run_options()
