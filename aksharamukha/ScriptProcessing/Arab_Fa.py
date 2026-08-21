# -*- coding: utf-8 -*-

# Arab-Fa's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# ConvertFix/PreProcess/PostProcess are imported LOCALLY inside each
# function that needs them (not at module level) - required to avoid a
# load-order-dependent circular import, since these three modules
# re-export names from here. See ScriptProcessing/Tamil.py.

import re

# ---- Fix (encode/decode conversion logic) ----

# internal
def FixArab_Fa(Strng, Source, reverse=False):

    """Applies the shared Perso-Arabic script fixes (via ConvertFix.FixArab) used for Farsi text."""
    from .. import Options
    Strng = Options.call_fix('FixArab', Strng, Source, reverse)

    return Strng

# ---- Post-processing options ----

# frontend
def persianPaGaFaJa(Strng):

    """Converts Persian-specific letters pe and gaf to Arabic fa and jim (/p g/ پ گ → /f j/ ف ج)."""
    Strng = Strng.replace('پ', 'ف').replace('گ', 'ج')

    return Strng
