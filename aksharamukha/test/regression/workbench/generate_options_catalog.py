# -*- coding: utf-8 -*-
"""Dumps frontend_backend_manifest.json's option lists to a spreadsheet-
friendly CSV - the read-only reference you browse to pick option names for
option_test_requests.csv. Regenerate whenever frontend_backend_manifest.json
changes (re-run ../build_frontend_backend_manifest.js first)."""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REG = os.path.dirname(HERE)

with open(os.path.join(REG, 'frontend_backend_manifest.json'), 'r', encoding='utf-8') as f:
    manifest = json.load(f)

rows = []
for kind, section in (('post', manifest['post_options']), ('pre', manifest['pre_options'])):
    for name, o in section.items():
        rows.append({
            'kind': kind,
            'name': name,
            'backend_status': o['backend_status'],
            'in_frontend': o['in_frontend'],
            'applies_to_scripts': '; '.join(o['applies_to_scripts']),
            'label': ' | '.join(o['labels'])[:200],
        })

rows.sort(key=lambda r: (r['kind'], r['name']))

out_path = os.path.join(HERE, 'options_catalog.csv')
with open(out_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['kind', 'name', 'backend_status', 'in_frontend', 'applies_to_scripts', 'label'])
    writer.writeheader()
    writer.writerows(rows)

print('wrote', out_path, '-', len(rows), 'options')
