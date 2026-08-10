# -*- coding: utf-8 -*-
"""
Re-runs the same matrix generate_golden.py captured, against the CURRENT
code, and reports every place output differs from the saved golden snapshot.

This is the actual regression check to run after any refactor step (e.g.
each phase of the pipeline-restructure proposal): it doesn't judge whether
a change is correct, only whether behavior moved - so an intentional bug
fix will show up here too and needs a human to confirm it's the change
they meant to make.

Usage:
    python compare_golden.py            # summary only
    python compare_golden.py --verbose  # print every diff
"""
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

import generate_golden as gg  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    with open(os.path.join(HERE, name), 'r', encoding='utf-8') as f:
        return json.load(f)


def compare_baseline_hashes():
    old = {r['file']: r['sha256'] for r in load('baseline_hash.json')}
    new = {r['file']: r['sha256'] for r in gg.hash_existing_baseline()}
    changed = [f for f in old if f in new and old[f] != new[f]]
    added = [f for f in new if f not in old]
    removed = [f for f in old if f not in new]
    return changed, added, removed


def compare_roundtrip():
    old = load('roundtrip.json')
    new_by_key = {}
    for r in gg.build_roundtrip_matrix():
        key = (r['source'], r['target'], r['nativize'])
        new_by_key[key] = r

    diffs = []
    for r in old:
        key = (r['source'], r['target'], r['nativize'])
        n = new_by_key.get(key)
        if n is None:
            diffs.append((key, 'missing in new run'))
            continue
        if r['forward'] != n['forward']:
            diffs.append((key, 'forward output changed'))
        elif r.get('roundtrip') != n.get('roundtrip'):
            diffs.append((key, 'roundtrip output changed'))
    return diffs


def compare_options():
    old = {(r['kind'], r['name']): r for r in load('options.json')}
    new = {(r['kind'], r['name']): r for r in gg.build_options_matrix()}

    diffs = []
    for key, r in old.items():
        n = new.get(key)
        if n is None:
            diffs.append((key, 'missing in new run'))
            continue
        if r['result'] != n['result']:
            was_ok, now_ok = r['result']['ok'], n['result']['ok']
            if was_ok and not now_ok:
                diffs.append((key, 'NEW FAILURE: ' + n['result'].get('error_type', '?')))
            elif not was_ok and now_ok:
                diffs.append((key, 'FIXED (was: ' + r['result'].get('error_type', '?') + ')'))
            else:
                diffs.append((key, 'output changed'))
    return diffs


def main():
    verbose = '--verbose' in sys.argv

    print('Comparing against golden snapshot from', load('manifest.json')['generated_at'])
    print()

    changed, added, removed = compare_baseline_hashes()
    print('[existing test_texts fixtures] changed=%d added=%d removed=%d' % (len(changed), len(added), len(removed)))
    if verbose:
        for f in changed:
            print('  CHANGED:', f)

    rt_diffs = compare_roundtrip()
    print('[roundtrip matrix] %d / difference(s)' % len(rt_diffs))
    if verbose or rt_diffs:
        for key, why in rt_diffs[:50 if not verbose else None]:
            print('  ', key, '-', why)

    opt_diffs = compare_options()
    print('[option sweep] %d difference(s)' % len(opt_diffs))
    if verbose or opt_diffs:
        for key, why in opt_diffs[:50 if not verbose else None]:
            print('  ', key, '-', why)

    total = len(changed) + len(added) + len(removed) + len(rt_diffs) + len(opt_diffs)
    print()
    print('TOTAL DIFFERENCES:', total)
    sys.exit(1 if total else 0)


if __name__ == '__main__':
    main()
