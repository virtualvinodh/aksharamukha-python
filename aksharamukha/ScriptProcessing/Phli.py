# -*- coding: utf-8 -*-

# Phli's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def PhliWawAyinResh(Strng):
    Strng = Strng.replace('𐭥', '[\uEA05-\uEA02-\uEA01]') # resh yin

    return Strng
