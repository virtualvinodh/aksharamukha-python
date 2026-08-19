# -*- coding: utf-8 -*-

# Shahmukhi's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re

# ---- Fix (encode/decode conversion logic) ----

def FixShahmukhi(Strng, reverse=False):

    """Applies the shared Perso-Arabic Shahmukhi/Urdu fix routine to encode or decode Shahmukhi text based on the reverse flag."""
    from .. import ConvertFix as CF
    return CF.FixUrduShahmukhi('Shahmukhi', Strng, reverse)
