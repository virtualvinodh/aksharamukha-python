# -*- coding: utf-8 -*-

# Hebr-Ar's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def gainGimel(Strng):
    return Strng.replace('ק','ק̈')

def tavTwodot(Strng):
    return Strng.replace('ת','ת̈')

def tavThreedot(Strng):
    return Strng.replace('תׄ','ת֒')
