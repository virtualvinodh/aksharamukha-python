# -*- coding: utf-8 -*-

# Hatr's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def HatrDalethResh(Strng):
    Strng = Strng.replace('𐣣', '[\uEA06-\uEA01]') # resh yin

    return Strng
