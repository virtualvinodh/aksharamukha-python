# -*- coding: utf-8 -*-

# Lao2's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re

def FixLao2(Strng, reverse = False):

    """Delegates Lao2 script fix-up to the shared Lao encode/decode logic."""
    from .. import ConvertFix as CF
    return CF.FixLao(Strng, reverse)
