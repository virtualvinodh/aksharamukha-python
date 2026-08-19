# -*- coding: utf-8 -*-

# RomanLoC's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def LoCMarc8(Strng):
    import unicodedata
    Strng = unicodedata.normalize('NFD', Strng)
    Strng = Strng.replace('\u02DA', '\u02D9')
    return Strng
