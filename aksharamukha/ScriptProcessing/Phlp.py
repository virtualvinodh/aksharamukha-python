# -*- coding: utf-8 -*-

# Phlp's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

# ---- Pre-processing options ----

# frontend
def PhlpMemQoph(Strng):
    """Disambiguates the Psalter Pahlavi Mem-Qoph ligature by expanding it to a bracketed [m-q] marker (𐮋 → [m-q])."""
    Strng = Strng.replace('𐮋', '[\uEA03-\uEA04]') # mem qoph

    return Strng

# frontend
def PhlpWawAyinResh(Strng):
    """Disambiguates the Psalter Pahlavi Waw-Ayin-Resh ligature by expanding it to a bracketed [w-ʿ-r] marker (𐮅)."""
    Strng = Strng.replace('𐮅', '[\uEA05-\uEA02-\uEA01]') # resh yin

    return Strng
