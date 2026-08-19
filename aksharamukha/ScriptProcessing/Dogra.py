# -*- coding: utf-8 -*-

# Dogra's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def olddogra(Strng):

    return Strng

def DograShaKha(Strng):
    Strng = Strng.replace('𑠨', '𑠋')

    return Strng
