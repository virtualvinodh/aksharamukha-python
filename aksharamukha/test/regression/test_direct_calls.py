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
    entry = DIRECT[key]
    inp, expected = entry['cases'][case_index]

    if entry.get('custom_call'):
        # JapanesePostProcess / defaultPost / JapanesePreProcess: Strng is
        # not their first parameter, so they're exercised through the exact
        # same lambda used to generate their expected output.
        import promote_direct_call_options as pdc
        fn = pdc.CUSTOM_CALLS[(entry['kind'], entry['name'])]
        actual = fn(inp)
    else:
        # Options.call_pre_option/call_post_option resolve through
        # Options.py's own PRE_OPTION_FUNCS/POST_OPTION_FUNCS dicts (which
        # include every auto-discovered ScriptProcessing option, not just
        # ones re-exported into PreProcess.py/PostProcess.py) instead of
        # getattr(PreProcess/PostProcess, name) against the raw module -
        # same *args shape this already needed, so a straight swap. Was
        # the getattr version, which broke this whole test file (578
        # failures) the moment a re-export it depended on got removed in
        # an earlier attempt at this cleanup.
        from aksharamukha import Options
        call = Options.call_post_option if entry['kind'] == 'post' else Options.call_pre_option
        actual = call(entry['name'], inp, *entry['args'])

    assert actual == expected
