# -*- coding: utf-8 -*-

# Javanese's LoC (Library of Congress) romanization logic. See
# ScriptProcessing/HOW_TO_ADD_LOC.md for the naming convention this
# follows and how to add a new script. Renamed from RomanLoCJavanese.py
# for consistency with the rest of ScriptProcessing/ (one file per
# script, <Script>LoC.py).

import re

# ---- Pre-processing options ----

# internal
def RomanLocToJavanesePre(Strng):
    """Replace the left single quotation mark placeholder with ng̈ in Javanese LoC romanization."""
    Strng = Strng.replace('‘', 'ng̈')

    return Strng

# ---- Post-processing options ----

# frontend
def JavaneseSimplified(Strng):
    """Simplifies the jny consonant cluster to ny under the simplified Javanese romanization mapping."""
    Strng = Strng.replace('jny', 'ny')
    return Strng

# internal
def JavaneseToRomanLocPost(Strng):
    """Fixes Javanese LoC romanization diacritics: h-diaeresis -> h, ng-diaeresis -> apostrophe-like sign."""
    Strng = Strng.replace('ḧ', 'h').replace('ng̈', '‘')

    return Strng
