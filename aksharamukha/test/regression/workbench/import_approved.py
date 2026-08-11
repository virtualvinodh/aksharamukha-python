# -*- coding: utf-8 -*-
"""
Merges rows marked approve=yes in fanout_results.csv / option_test_results.csv
into the real fixtures:

  - option_test_results.csv (approve=yes) -> test_texts/test_postoptions.json
    / test_preoptions.json, in the same {name: [{source,target,cases:[[in,out]]}]}
    schema TestPostOptions/TestPreOptions already read - so they run under
    plain `pytest testsuite.py` immediately, no separate runner needed.
  - fanout_results.csv (approve=yes) -> regression/roundtrip_user.json, a
    sibling to the auto-generated roundtrip.json, kept separate so your
    hand-picked cases never get silently overwritten by a re-run of
    generate_golden.py.

Defaults to --dry-run (prints what WOULD change, writes nothing). Pass
--apply to actually write.

Run:  python import_approved.py            # preview
      python import_approved.py --apply    # write for real
"""
import argparse
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REG = os.path.dirname(HERE)
TEXTS = os.path.join(REG, '..', 'test_texts')


def read_csv(name):
    path = os.path.join(HERE, name)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def is_approved(row):
    return (row.get('approve') or '').strip().lower() in ('yes', 'y', 'true')


def import_options(apply_):
    rows = [r for r in read_csv('option_test_results.csv') if is_approved(r) and not r.get('error')]
    if not rows:
        print('option_test_results.csv: 0 approved rows to import')
        return

    post_path = os.path.join(TEXTS, 'test_postoptions.json')
    pre_path = os.path.join(TEXTS, 'test_preoptions.json')
    with open(post_path, 'r', encoding='utf-8') as f:
        post_fixture = json.load(f)
    with open(pre_path, 'r', encoding='utf-8') as f:
        pre_fixture = json.load(f)

    changed_post, changed_pre = False, False
    for row in rows:
        fixture = post_fixture if row['kind'] == 'post' else pre_fixture
        name = row['option_name']
        entry_list = fixture.setdefault(name, [])
        block = next((b for b in entry_list if b['source'] == row['source_script'] and b['target'] == row['target_script']), None)
        if block is None:
            block = {'source': row['source_script'], 'target': row['target_script'], 'cases': []}
            entry_list.append(block)
        case = [row['input'], row['output']]
        if case not in block['cases']:
            block['cases'].append(case)
            print(('[apply] ' if apply_ else '[dry-run] ') + 'add case for %s::%s (%s->%s)' %
                  (row['kind'], name, row['source_script'], row['target_script']))
            if row['kind'] == 'post':
                changed_post = True
            else:
                changed_pre = True

    if apply_:
        if changed_post:
            with open(post_path, 'w', encoding='utf-8') as f:
                json.dump(post_fixture, f, ensure_ascii=False, indent=4)
        if changed_pre:
            with open(pre_path, 'w', encoding='utf-8') as f:
                json.dump(pre_fixture, f, ensure_ascii=False, indent=4)
    elif changed_post or changed_pre:
        print('(dry-run - nothing written; re-run with --apply)')


def import_fanout(apply_):
    rows = [r for r in read_csv('fanout_results.csv') if is_approved(r) and not r.get('error')]
    if not rows:
        print('fanout_results.csv: 0 approved rows to import')
        return

    out_path = os.path.join(REG, 'roundtrip_user.json')
    existing = []
    if os.path.exists(out_path):
        with open(out_path, 'r', encoding='utf-8') as f:
            existing = json.load(f)

    for row in rows:
        existing.append({
            'source_script': row['source_script'], 'label': row['label'], 'mode': row['mode'],
            'target_script': row['target_script'], 'nativize': row['nativize'] == 'True',
            'output': row['output'], 'roundtrip_output': row['roundtrip_output'],
            'matches_original': row.get('matches_original', '')
        })
        print(('[apply] ' if apply_ else '[dry-run] ') + 'add fanout case %s->%s (%s)' %
              (row['source_script'], row['target_script'], row['label']))

    if apply_:
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(existing, f, ensure_ascii=False, indent=1)
    else:
        print('(dry-run - nothing written; re-run with --apply)')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true', help='actually write changes (default is dry-run preview)')
    args = parser.parse_args()

    import_options(args.apply)
    import_fanout(args.apply)
