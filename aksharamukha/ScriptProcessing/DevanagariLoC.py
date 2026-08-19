# -*- coding: utf-8 -*-

# Devanagari's LoC (Library of Congress) romanization logic, consolidated
# out of ConvertFix.py/PreProcess.py/PostProcess.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this
# follows). Renamed from RomanLoCDevanagari.py for consistency with the
# rest of ScriptProcessing/ (one file per script, <Script>LoC.py).
#
# HindiMarathiRomanLoCFix and DevanagariRomanLoCFix each independently
# define the SAME option name in both PreProcess.py and PostProcess.py,
# as genuinely different functions - can't both be a bare top-level
# `def` of the identical name in one file. Suffixed _pre/_post here;
# PreProcess.py/PostProcess.py each re-export their own half under the
# ORIGINAL (unsuffixed) name via `import X_pre as X` / `import X_post as
# X`, so the public option name (post_options=['X']/pre_options=['X'])
# is completely unchanged.

import re

# ---- Pre-processing options ----

def HindiMarathiRomanLoCFix_pre(Strng):
    """Substitutes 'sh'→ṣ, ḷ→ḻ, and l̤→l̳ before Hindi/Marathi Library of Congress romanization."""
    Strng = Strng.replace('sh', 'ṣ')
    Strng = Strng.replace('ḷ', 'ḻ')
    Strng = Strng.replace('l̤', 'l̳')

    return Strng

def DevanagariRomanLoCFix_pre(Strng):
    """Normalize nukta-marked digraphs (g̳h̳, t̤, s̤, h̤) to their LoC diacritic forms for Devanagari romanization."""
    Strng = Strng.replace('g̳h̳', 'gḧ').replace('t̤', 'ṭ̈').replace('s̤', 's̈')\
        .replace('h̤', 'ḧ')

    return Strng

# ---- Post-processing options ----

def HindiMarathiRomanLoCFix_post(Strng):
    """Reverses the Hindi/Marathi LoC substitutions: ṣ→'sh', ḻ→ḷ, l̳→l̤."""
    Strng = Strng.replace('ṣ', 'sh')
    Strng = Strng.replace('ḻ', 'ḷ')
    Strng = Strng.replace('l̳', 'l̤')

    return Strng

def DevanagariRomanLoCFix_post(Strng):
    """Fixes Devanagari LoC romanization diaeresis-marked digraphs: g-h-diaeresis -> g-underdot h-underdot, t-diaeresis -> t-underdot, s-diaeresis -> s-underdot, h-diaeresis -> h-underdot."""
    Strng = Strng.replace('gḧ', 'g̳h̳').replace('ṭ̈', 't̤').replace('s̈', 's̤')\
        .replace('ḧ', 'h̤')

    return Strng
