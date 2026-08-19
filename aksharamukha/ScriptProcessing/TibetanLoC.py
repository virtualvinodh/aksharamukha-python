# -*- coding: utf-8 -*-

# TibetanLoC's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re

def FixTibetanLoC(Strng,reverse=False):

    """Core Tibetan (LoC romanization variant) encode/decode logic: delegate to the shared Tibetan fixer without native-form swapping."""
    from .. import ConvertFix as CF
    return CF.FixTibetan(Strng,reverse, swapNative=False)
