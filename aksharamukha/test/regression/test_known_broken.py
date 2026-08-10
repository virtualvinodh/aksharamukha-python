# -*- coding: utf-8 -*-
"""
The 36 PreProcess/PostProcess functions that are NOT safely callable as a
bare pre_options=[name] / post_options=[name] value - either they're
internal multi-argument pipeline helpers that happen to live in the same
module namespace the by-name option dispatch reflects over (see the
refactor audit, pattern 01), or they're independently confirmed bugs
(removeZW, IPAIndic, the OriyaSubojinedVa regex typo), or a missing
optional dependency (khmernltk).

These tests assert the CURRENT failure mode, on purpose: if one of these
ever starts working (a fix lands) or starts failing differently (a
refactor changes what breaks), that's exactly the kind of change that
should stop a test suite, not pass silently. A newly-green test here means
"go update known_broken_options.json and, ideally, move that option into
test_postoptions.json/test_preoptions.json instead."
"""
import json
import os

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, 'known_broken_options.json'), 'r', encoding='utf-8') as f:
    BROKEN = json.load(f)

_EXCEPTION_TYPES = {
    'TypeError': TypeError,
    'AttributeError': AttributeError,
    'ModuleNotFoundError': ModuleNotFoundError,
    'ImportError': ImportError,
}


def _exception_class(name):
    if name in _EXCEPTION_TYPES:
        return _EXCEPTION_TYPES[name]
    import re
    if name == 'error':
        return re.error
    return Exception


@pytest.mark.parametrize("key", sorted(BROKEN.keys()))
def test_known_broken_option_fails_the_same_way(key):
    from aksharamukha import transliterate

    entry = BROKEN[key]
    kwargs = {'post_options': [entry['name']]} if entry['kind'] == 'post' else {'pre_options': [entry['name']]}
    sample = 'नमस्ते जगत्' if entry['source'] == 'Devanagari' else 'namaste jagat'

    with pytest.raises(_exception_class(entry['error_type'])):
        transliterate.process(entry['source'], entry['target'], sample, **kwargs)
