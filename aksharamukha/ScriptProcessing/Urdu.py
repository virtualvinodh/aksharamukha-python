# -*- coding: utf-8 -*-

# Urdu's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re

def FixUrdu(Strng, reverse=False):

    """Core Urdu encode/decode logic: delegate to the shared Shahmukhi orthography fixer."""
    from .. import ConvertFix as CF
    return CF.FixUrduShahmukhi("Urdu", Strng, reverse)
