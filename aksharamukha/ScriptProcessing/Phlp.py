# -*- coding: utf-8 -*-

# Phlp's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def PhlpMemQoph(Strng):
    Strng = Strng.replace('𐮋', '[\uEA03-\uEA04]') # mem qoph

    return Strng

def PhlpWawAyinResh(Strng):
    Strng = Strng.replace('𐮅', '[\uEA05-\uEA02-\uEA01]') # resh yin

    return Strng
