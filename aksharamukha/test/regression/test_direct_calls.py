# -*- coding: utf-8 -*-
"""
The ~32 PreProcess/PostProcess functions that take more than just `Strng` -
they're real, correctly-designed options (per-script defaults wired through
PostOptions.py's elif chain, or internal pipeline steps called with a fixed
extra argument from Convert.py/ConvertFix.py/transliterate.py), just not
reachable through the single-argument post_options=[name]/pre_options=[name]
mechanism transliterate.process() offers directly (see transliterate.py:455
and :522 - both call getattr(module, name)(txt) with exactly one argument).

See promote_direct_call_options.py for how each function's real extra
argument(s) were sourced (grepped from an actual call site wherever one
exists, extracted via `ast` for the couple of cases needing a non-ASCII
script character so it's never hand-retyped) and generate_full_option_coverage.py's
sibling test_postoptions.json/test_preoptions.json for the ~419 options that
*are* reachable that way.
"""
import json
import os

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, 'test_direct_options.json'), 'r', encoding='utf-8') as f:
    DIRECT = json.load(f)


def _params():
    for key, entry in DIRECT.items():
        for i, (inp, out) in enumerate(entry['cases']):
            yield pytest.param(key, i, id='%s-case%d' % (key, i))


@pytest.mark.parametrize("key,case_index", list(_params()))
def test_direct_call_option(key, case_index):
    from aksharamukha import PreProcess, PostProcess

    entry = DIRECT[key]
    module = PostProcess if entry['kind'] == 'post' else PreProcess
    inp, expected = entry['cases'][case_index]

    if entry.get('custom_call'):
        # JapanesePostProcess / defaultPost / JapanesePreProcess: Strng is
        # not their first parameter, so they're exercised through the exact
        # same lambda used to generate their expected output.
        import promote_direct_call_options as pdc
        fn = pdc.CUSTOM_CALLS[(entry['kind'], entry['name'])]
        actual = fn(inp)
    else:
        fn = getattr(module, entry['name'])
        actual = fn(inp, *entry['args'])

    assert actual == expected
