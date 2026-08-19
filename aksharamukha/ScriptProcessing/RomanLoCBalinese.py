# -*- coding: utf-8 -*-

# RomanLoCBalinese's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

# ---- Post-processing options ----

def BalineseSimplified(Strng):
    """Uses simplified romanization mapping: ᬡ ᬙ ᬣ → na ca ta."""
    return Strng
