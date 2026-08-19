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

def FixKhuenTham(Strng, reverse=False):

    """Applies the shared Tai Tham family fix-up, with ra-haam swap enabled, for Khuen Tham script conversion."""
    from .. import ConvertFix as CF
    return CF._FixTaiThamFamily(Strng, reverse, ['ᩅ', 'ᨴ', 'ᨵ', 'ᨣ'], marker_cleanup=False, ra_haam_swap=True)

# ---- Pre-processing options ----

def KhuenRaHaamKaren(Strng):

    """Expands ra-haam into an explicit ra consonant sign and reassigns the lue-karan mark to represent ra-haam, e.g. ᨠ᩺ → kar, ᨠ᩼ → k."""
    # replace ra ham with r+ra-haam ->
    Strng = Strng.replace('᩺', 'ᩁ\u1A60')

    # replace lue-karan with ra-haam
    Strng = Strng.replace('᩼', '᩺')

    return Strng

# KhuenTham overrides the shared ThamLoC RomanLocToPre with its own
# extra text-marker injection before delegating - see
# ScriptProcessing/HOW_TO_ADD_LOC.md and ScriptProcessing/ThamLoC.py.

def RomanLocToKhuenThamPre(Strng):
    """Injects the Khuen text marker, then applies the shared Tai Tham LoC pre-conversion fix, before converting LoC Roman text to Khuen Tham."""
    from .ThamLoC import RomanLocToThamLoCPre
    Strng = Strng + '\u02BE'  # indicator for Khuen text
    Strng = RomanLocToThamLoCPre(Strng)

    return Strng
