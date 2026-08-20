# -*- coding: utf-8 -*-

# LaoTham's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re

# ---- Fix (encode/decode conversion logic) ----

def FixLaoTham(Strng, reverse=False):

    """Applies the shared Tai Tham script orthographic fixes (via ConvertFix.FixTaiTham) used for the Lao Tham variant."""
    from .. import ConvertFix as CF
    Strng = CF.FixTaiTham(Strng, reverse)

    return Strng

# ---- Pre-processing options ----

def TaiThamLao_pre(Strng):
    """Placeholder Tai Tham Lao pre-processing hook (currently a no-op passthrough)."""
    return Strng

# ---- Post-processing options ----

def TaiThamLao_post(Strng):
    """No-op placeholder (reserved for Tai Tham Lao-variant post-processing)."""
    return Strng

