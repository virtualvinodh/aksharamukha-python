# -*- coding: utf-8 -*-

# Javanese's LoC (Library of Congress) romanization logic, consolidated
# out of ConvertFix.py/PreProcess.py/PostProcess.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this
# follows). Renamed from RomanLoCJavanese.py for consistency with the
# rest of ScriptProcessing/ (one file per script, <Script>LoC.py).
#
# JavaneseRomanLoCFix independently defines the SAME option name in both
# PreProcess.py and PostProcess.py as genuinely different functions -
# suffixed _pre/_post here, same convention used everywhere else.

import re

# ---- Pre-processing options ----

def JavaneseRomanLoCFix_pre(Strng):
    """Replace the left single quotation mark placeholder with ng̈ in Javanese LoC romanization."""
    Strng = Strng.replace('‘', 'ng̈')

    return Strng

# ---- Post-processing options ----

def JavaneseSimplified(Strng):
    """Simplifies the jny consonant cluster to ny under the simplified Javanese romanization mapping."""
    Strng = Strng.replace('jny', 'ny')
    return Strng

def JavaneseRomanLoCFix_post(Strng):
    """Fixes Javanese LoC romanization diacritics: h-diaeresis -> h, ng-diaeresis -> apostrophe-like sign."""
    Strng = Strng.replace('ḧ', 'h').replace('ng̈', '‘')

    return Strng
