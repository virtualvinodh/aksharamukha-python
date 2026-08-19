# -*- coding: utf-8 -*-

# Hatr's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

# ---- Pre-processing options ----

def HatrDalethResh(Strng):
    """Disambiguates the Hatran letter daleth-resh (𐣣) by expanding it into its [d-r] transliteration form."""
    Strng = Strng.replace('𐣣', '[\uEA06-\uEA01]') # resh yin

    return Strng
