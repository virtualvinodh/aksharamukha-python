# -*- coding: utf-8 -*-

# Takri's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
#
# TakriArchaicKha independently defines the SAME option name in both
# PreProcess.py and PostProcess.py as two different functions - suffixed
# _pre/_post here, aliased back on re-export (see ScriptProcessing/
# DevanagariLimbu.py for the first script this pattern was used on).

import re
from aksharamukha.ScriptMap.MainIndic import Takri

def TakriArchaicKha_pre(Strng):

    return Strng.replace('𑚋', '𑚸')

def TakriArchaicKha_post(Strng):

    return Strng.replace('𑚸', '𑚋')

def TakriRemoveGemination(Strng):

    Strng = re.sub('(.)' + Takri.ViramaMap[0] + r'\1', r'\1', Strng)

    return Strng
