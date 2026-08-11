# -*- coding: utf-8 -*-
"""
One-off import: the 'heart' (Heart Sutra / Prajnaparamita Hridaya) and
'lalitavistara' corpora are already fully transliterated to every script by
testsuite.py's TestOverall (test_texts/test_<src>_<tgt>_<text>.txt,
nativize=True default) - no need to regenerate them through the workbench UI.
This reads those existing files directly and:
  1. adds 4 rows to source_texts.csv (Devanagari/IAST x heart/lalitavistara)
  2. merges the corresponding conversion samples into conversion_samples.json,
     using the same (source, target, nativize, mode, label) dedup key the
     app's own generation endpoints use, so re-running this is a no-op.

Run once from this directory: python import_existing_corpus.py
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEST_TEXTS_DIR = os.path.abspath(os.path.join(HERE, '..', '..', 'test_texts'))
SOURCE_TEXTS_CSV = os.path.join(HERE, 'source_texts.csv')
CONVERSION_SAMPLES_JSON = os.path.join(HERE, 'conversion_samples.json')

sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..', '..')))
from aksharamukha import GeneralMap as GM  # noqa: E402

CATS = {
    'reversible': set(GM.ReversibleScripts),
    'roman_reversible': set(GM.RomanReversible),
    'indic': set(GM.IndicScripts),
    'latin': set(GM.LatinScripts),
    'semitic': set(GM.SemiticScripts),
}


def categorize(script):
    if script in CATS['reversible']:
        return 'reversible_indic'
    if script in CATS['indic']:
        return 'irreversible_indic'
    if script in CATS['roman_reversible']:
        return 'roman_reversible'
    if script in CATS['latin']:
        return 'roman_irreversible'
    if script in CATS['semitic']:
        return 'semitic'
    return 'other'


TARGET_SCRIPTS = GM.IndicScripts + GM.Roman + GM.SemiticScripts
SOURCE_SCRIPTS = ['Devanagari', 'IAST']
LABELS = ['heart', 'lalitavistara']


def read_source_texts_csv():
    with open(SOURCE_TEXTS_CSV, 'r', encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def write_source_texts_csv(rows):
    with open(SOURCE_TEXTS_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'script', 'label', 'text'])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main():
    rows = read_source_texts_csv()
    existing_keys = {(r['script'], r['label']) for r in rows}
    next_id = max((int(r['id']) for r in rows if r['id'].strip().isdigit()), default=0) + 1

    added_source_rows = 0
    source_text_cache = {}
    for label in LABELS:
        for script in SOURCE_SCRIPTS:
            path = os.path.join(TEST_TEXTS_DIR, 'source_%s_%s.txt' % (script, label))
            if not os.path.exists(path):
                print('missing source file, skipping:', path)
                continue
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
            source_text_cache[(script, label)] = text
            if (script, label) in existing_keys:
                continue
            rows.append({'id': str(next_id), 'script': script, 'label': label, 'text': text})
            next_id += 1
            added_source_rows += 1

    write_source_texts_csv(rows)
    print('Added %d new Source Texts rows (%d already present).' % (added_source_rows, len(rows) - added_source_rows))

    existing = []
    if os.path.exists(CONVERSION_SAMPLES_JSON):
        with open(CONVERSION_SAMPLES_JSON, 'r', encoding='utf-8') as f:
            existing = json.load(f)
    index = {(r['source'], r['target'], r['nativize'], r['mode'], r.get('label')): i for i, r in enumerate(existing)}

    added_or_updated = 0
    missing_outputs = 0
    for label in LABELS:
        for source in SOURCE_SCRIPTS:
            input_text = source_text_cache.get((source, label))
            if input_text is None:
                continue
            for target in TARGET_SCRIPTS:
                if target == source:
                    continue
                out_path = os.path.join(TEST_TEXTS_DIR, 'test_%s_%s_%s.txt' % (source, target, label))
                if not os.path.exists(out_path):
                    missing_outputs += 1
                    continue
                with open(out_path, 'r', encoding='utf-8') as f:
                    output_text = f.read()
                record = {
                    'source': source, 'target': target, 'nativize': True, 'label': label,
                    'mode': 'fanout', 'category': categorize(target),
                    'input': input_text, 'output': output_text, 'error': '',
                }
                key = (source, target, True, 'fanout', label)
                if key in index:
                    existing[index[key]] = record
                else:
                    index[key] = len(existing)
                    existing.append(record)
                added_or_updated += 1

    with open(CONVERSION_SAMPLES_JSON, 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, indent=1)

    print('Added/updated %d conversion samples (%d output files were missing on disk).' % (added_or_updated, missing_outputs))
    print('conversion_samples.json now has %d total records.' % len(existing))


if __name__ == '__main__':
    main()
