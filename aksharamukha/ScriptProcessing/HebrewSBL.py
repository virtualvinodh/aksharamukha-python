# -*- coding: utf-8 -*-

# HebrewSBL's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def removetddash(Strng):
    Strng += '\u05CE'

    Strng = Strng.replace('d', 'd꞉').replace('t', 't꞉').replace('g', 'g꞉')
    Strng = Strng.replace('ḏ', 'd').replace('ṯ', 't').replace('ḡ', 'g').replace('\u05CE', '')

    return Strng
