# -*- coding: utf-8 -*-
"""Dumps GeneralMap.py's script-category lists to JSON, as input for
build_frontend_backend_manifest.js - lets the manifest builder cross-check
the frontend's script cards against what the backend actually recognizes,
without the JS side needing to import the Python package."""
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from aksharamukha import GeneralMap as GM  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

data = {
    'IndicScripts': GM.IndicScripts,
    'LatinScripts': GM.LatinScripts,
    'SemiticScripts': GM.SemiticScripts,
    'NonIndic': GM.NonIndic,
    'MainIndic': GM.MainIndic,
    'EastIndic': GM.EastIndic,
    'Roman': GM.Roman,
    'RomanDiacritic': GM.RomanDiacritic,
    'ReversibleScripts': GM.ReversibleScripts,
    'RomanReversible': GM.RomanReversible,
    'LoCScripts': GM.LoCScripts,
    'semiticISO': GM.semiticISO,
}

with open(os.path.join(HERE, 'backend_script_lists.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

print('wrote backend_script_lists.json:', {k: len(v) for k, v in data.items()})
