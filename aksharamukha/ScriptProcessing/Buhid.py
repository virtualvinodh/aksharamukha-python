# -*- coding: utf-8 -*-

# Buhid's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re

def _FixBuhidEncode(Strng):

    from .. import PostProcess
    Strng = PostProcess.InsertGeminationSign(Strng, 'Buhid')

    return Strng

def _FixBuhidDecode(Strng):

    from .. import PostProcess
    pass

    return Strng

def FixBuhid(Strng, reverse=False):

    from .. import PostProcess
    return _FixBuhidDecode(Strng) if reverse else _FixBuhidEncode(Strng)
