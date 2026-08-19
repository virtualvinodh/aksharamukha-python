# -*- coding: utf-8 -*-

# ThamLoC's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re

# ---- Fix (encode/decode conversion logic) ----

def FixThamLoC(Strng, reverse=False):

    """Core Tai Tham (LoC variant) encode/decode logic: delegate to the shared Tai Tham family fixer with marker cleanup enabled and ra-haam swapping disabled."""
    from .. import ConvertFix as CF
    return CF._FixTaiThamFamily(Strng, reverse, ['ᩅ', 'ᨴ', 'ᨵ', 'ᨣ', 'ᨷ'], marker_cleanup=True, ra_haam_swap=False)
