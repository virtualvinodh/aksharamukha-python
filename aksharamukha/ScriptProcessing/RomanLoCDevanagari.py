# -*- coding: utf-8 -*-

# RomanLoCDevanagari's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
#
# HindiMarathiRomanLoCFix independently defines the SAME option name in both
# PreProcess.py and PostProcess.py, as two genuinely different functions
# (pre-side does roughly one direction of a transform, post-side roughly
# the inverse) - can't both be a bare top-level `def` of the identical
# name in one file. Suffixed _pre/_post here; PreProcess.py/PostProcess.py
# each re-export their own half under the ORIGINAL (unsuffixed) name via
# `import X_pre as X` / `import X_post as X`, so the public option name
# (post_options=['X']/pre_options=['X']) is completely unchanged.

import re

def HindiMarathiRomanLoCFix_pre(Strng):
    """Substitutes 'sh'→ṣ, ḷ→ḻ, and l̤→l̳ before Hindi/Marathi Library of Congress romanization."""
    Strng = Strng.replace('sh', 'ṣ')
    Strng = Strng.replace('ḷ', 'ḻ')
    Strng = Strng.replace('l̤', 'l̳')

    return Strng

def HindiMarathiRomanLoCFix_post(Strng):
    """Reverses the Hindi/Marathi LoC substitutions: ṣ→'sh', ḻ→ḷ, l̳→l̤."""
    Strng = Strng.replace('ṣ', 'sh')
    Strng = Strng.replace('ḻ', 'ḷ')
    Strng = Strng.replace('l̳', 'l̤')

    return Strng
