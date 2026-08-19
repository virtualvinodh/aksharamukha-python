# -*- coding: utf-8 -*-

# Balinese's LoC (Library of Congress) romanization logic. See
# ScriptProcessing/HOW_TO_ADD_LOC.md for the naming convention this
# follows and how to add a new script. Renamed from RomanLoCBalinese.py
# for consistency with the rest of ScriptProcessing/ (one file per
# script, <Script>LoC.py).

import re

# ---- Pre-processing options ----

def RomanLocToBalinesePre(Strng):
    """Replace the left single quotation mark placeholder with ng̈ in Balinese LoC romanization."""
    Strng = Strng.replace('‘', 'ng̈')

    return Strng

# ---- Post-processing options ----

def BalineseSimplified(Strng):
    """Uses simplified romanization mapping: ᬡ ᬙ ᬣ → na ca ta."""
    return Strng

def BalineseToRomanLocPost(Strng):
    """Fixes Balinese LoC romanization diacritics: h-diaeresis -> h, ng-diaeresis -> apostrophe-like sign."""
    Strng = Strng.replace('ḧ', 'h').replace('ng̈', '‘')

    return Strng
