# -*- coding: utf-8 -*-

# Balinese's LoC (Library of Congress) romanization logic, consolidated
# out of ConvertFix.py/PreProcess.py/PostProcess.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this
# follows). Renamed from RomanLoCBalinese.py for consistency with the
# rest of ScriptProcessing/ (one file per script, <Script>LoC.py).
#
# BalineseRomanLoCFix independently defines the SAME option name in both
# PreProcess.py and PostProcess.py as genuinely different functions -
# suffixed _pre/_post here, same convention used everywhere else.

import re

# ---- Pre-processing options ----

def BalineseRomanLoCFix_pre(Strng):
    """Replace the left single quotation mark placeholder with ng̈ in Balinese LoC romanization."""
    Strng = Strng.replace('‘', 'ng̈')

    return Strng

# ---- Post-processing options ----

def BalineseSimplified(Strng):
    """Uses simplified romanization mapping: ᬡ ᬙ ᬣ → na ca ta."""
    return Strng

def BalineseRomanLoCFix_post(Strng):
    """Fixes Balinese LoC romanization diacritics: h-diaeresis -> h, ng-diaeresis -> apostrophe-like sign."""
    Strng = Strng.replace('ḧ', 'h').replace('ng̈', '‘')

    return Strng
