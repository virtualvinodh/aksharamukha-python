# -*- coding: utf-8 -*-

# KhuenTham's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# ConvertFix/PreProcess/PostProcess are imported LOCALLY inside each
# function that needs them (not at module level) - required to avoid a
# load-order-dependent circular import, since these three modules
# re-export names from here. See ScriptProcessing/Tamil.py.

import re

# ---- Fix (encode/decode conversion logic) ----

# internal
def FixKhuenTham(Strng, reverse=False, ctx=None):

    """Applies the shared Tai Tham family fix-up, with ra-haam swap enabled, for Khuen Tham script conversion."""
    from .. import ConvertFix as CF
    return CF._FixTaiThamFamily(Strng, reverse, ['ᩅ', 'ᨴ', 'ᨵ', 'ᨣ'], marker_cleanup=False, ra_haam_swap=True, ctx=ctx)

# ---- Pre-processing options ----

# frontend
def KhuenRaHaamKaren(Strng):

    """Expands ra-haam into an explicit ra consonant sign and reassigns the lue-karan mark to represent ra-haam, e.g. ᨠ᩺ → kar, ᨠ᩼ → k."""
    # replace ra ham with r+ra-haam ->
    Strng = Strng.replace('᩺', 'ᩁ\u1A60')

    # replace lue-karan with ra-haam
    Strng = Strng.replace('᩼', '᩺')

    return Strng

# KhuenTham overrides the shared ThamLoC RomanLocToPre with its own
# ctx.is_khuen_target flag before delegating - see
# ScriptProcessing/HOW_TO_ADD_LOC.md and ScriptProcessing/ThamLoC.py.
# (Formerly a literal '\u02BE' marker appended to the text itself and
# grepped for later in ConvertFix._FixTaiThamFamily - see MARKERS.md.)

# internal
def RomanLocToKhuenTham_pre(Strng, ctx=None):
    """Marks this text as Khuen (via ctx), then applies the shared Tai Tham LoC pre-conversion fix, before converting LoC Roman text to Khuen Tham."""
    from .ThamLoC import RomanLocToThamLoC_pre
    if ctx is not None:
        ctx.is_khuen_target = True
    Strng = RomanLocToThamLoC_pre(Strng)

    return Strng
