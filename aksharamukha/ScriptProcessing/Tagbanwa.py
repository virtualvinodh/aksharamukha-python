# -*- coding: utf-8 -*-

# Tagbanwa's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re

def _FixTagbanwaEncode(Strng):

    from .. import PostProcess
    Strng = PostProcess.InsertGeminationSign(Strng, 'Tagbanwa')

    return Strng

def _FixTagbanwaDecode(Strng):

    from .. import PostProcess
    pass

    return Strng

def FixTagbanwa(Strng, reverse=False):

    from .. import PostProcess
    return _FixTagbanwaDecode(Strng) if reverse else _FixTagbanwaEncode(Strng)
