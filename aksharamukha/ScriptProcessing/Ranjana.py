# -*- coding: utf-8 -*-

# Ranjana's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def ranjanalantsa(Strng):
    Strng = Strng.replace('་', ' ')
    return Strng

def ranjanawartu(Strng):
    Strng = Strng.replace('་', '࿎ ')
    return Strng
