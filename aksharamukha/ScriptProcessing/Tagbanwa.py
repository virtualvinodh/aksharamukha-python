# -*- coding: utf-8 -*-

# Tagbanwa's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re

def _FixTagbanwaEncode(Strng):

    """Inserts the gemination sign for doubled consonants when encoding into Tagbanwa."""
    from .. import PostProcess
    Strng = PostProcess.InsertGeminationSign(Strng, 'Tagbanwa')

    return Strng

def _FixTagbanwaDecode(Strng):

    """No-op decode fix for Tagbanwa; no additional corrections are currently applied."""
    from .. import PostProcess
    pass

    return Strng

def FixTagbanwa(Strng, reverse=False):

    """Dispatches to the Tagbanwa encode or decode fix routine based on the reverse flag."""
    from .. import PostProcess
    return _FixTagbanwaDecode(Strng) if reverse else _FixTagbanwaEncode(Strng)
