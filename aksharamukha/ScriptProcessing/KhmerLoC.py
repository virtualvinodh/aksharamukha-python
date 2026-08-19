# -*- coding: utf-8 -*-

# KhmerLoC's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re

# ---- Fix (encode/decode conversion logic) ----

def FixKhmerLoC(Strng,reverse=False):

    """Applies the shared Khmer fix-up logic (via ConvertFix.FixKhmer) targeting the Library of Congress romanization scheme."""
    from .. import ConvertFix as CF
    return CF.FixKhmer(Strng, reverse, target="KhmerLoC")
