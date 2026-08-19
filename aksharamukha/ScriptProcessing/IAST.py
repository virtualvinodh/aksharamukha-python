# -*- coding: utf-8 -*-

# IAST's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
#
# RomanLoCSLaDotLaUnderscore independently defines the SAME option name in
# both PreProcess.py and PostProcess.py as two different functions -
# suffixed _pre/_post here; PreProcess.py/PostProcess.py each re-export
# their own half aliased back to the original name (see ScriptProcessing/
# DevanagariLimbu.py for the first script this pattern was used on).
#
# joinVowelCons is called via PP. because it stays shared with
# joinVowelConsISO (ScriptProcessing/ISO.py) - genuinely one function used
# by two different scripts' own preoptions, not something to duplicate.

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.Roman import IAST

def _FixIASTEncode(Strng):

    return Strng

def _FixIASTDecode(Strng):
    Strng = Strng.replace("ṁ",IAST.AyogavahaMap[1])
    # ^ Some IAST publications use /ṁ/ instead of /m dot below/

    return Strng

def FixIAST(Strng,reverse=False):
    return _FixIASTDecode(Strng) if reverse else _FixIASTEncode(Strng)

def RomanLoCSLaDotLaUnderscore_pre(Strng):
    Strng = Strng.replace('ḻ', 'l̤')
    Strng = Strng.replace( 'l̳', 'ḻ',)

    return Strng

def RomanLoCSLaDotLaUnderscore_post(Strng):
    Strng = Strng.replace('ḻ', 'l̳')
    Strng = Strng.replace('l̤', 'ḻ')

    return Strng

def joinVowelConsIAST(Strng):
    from .. import PreProcess as PP
    return PP.joinVowelCons(Strng, 'IAST')
