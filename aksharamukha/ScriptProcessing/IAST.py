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

# ---- Fix (encode/decode conversion logic) ----

def _FixIASTEncode(Strng):

    """No-op placeholder for IAST encoding; returns the string unchanged."""
    return Strng

def _FixIASTDecode(Strng):
    """Normalizes the alternate IAST anusvara spelling ṁ to the standard m-with-dot-below form."""
    Strng = Strng.replace("ṁ",IAST.AyogavahaMap[1])
    # ^ Some IAST publications use /ṁ/ instead of /m dot below/

    return Strng

def FixIAST(Strng,reverse=False):
    """Dispatches to the IAST encode or decode fix-up routine based on the reverse flag."""
    return _FixIASTDecode(Strng) if reverse else _FixIASTEncode(Strng)

# ---- Pre-processing options ----

def RomanLoCSLaDotLaUnderscore_pre(Strng):
    """Converts the IAST ḻ (la with dot below) to an l+diaeresis-below form and normalizes an l+underscore variant to ḻ, for LoC-style romanization."""
    Strng = Strng.replace('ḻ', 'l̤')
    Strng = Strng.replace( 'l̳', 'ḻ',)

    return Strng

def joinVowelConsIAST(Strng):
    """Joins separated vowel and consonant word boundaries into single words for IAST, e.g. tat tvam asi → tattvamasi."""
    from .. import PreProcess as PP
    return PP.joinVowelCons(Strng, 'IAST')

def IASTLDotRetroflex(Strng):
    """Convert IAST ḷ (retroflex l) to l̤ for Library of Congress-style romanization."""
    Strng = Strng.replace('ḷ', 'l̤')

    return Strng

def IASTPali_pre(Strng):
    """Convert IAST ḷ (retroflex l) to l̤ for Pali romanization."""
    Strng = Strng.replace('ḷ', 'l̤')

    return Strng

# ---- Post-processing options ----

def RomanLoCSLaDotLaUnderscore_post(Strng):
    """Reverses the LoC-style ḻ diacritic substitution, restoring the standard ḻ representation."""
    Strng = Strng.replace('ḻ', 'l̳')
    Strng = Strng.replace('l̤', 'ḻ')

    return Strng

def IASTPali_post(Strng):
    """Converts the IAST underlined-l (l with line below) used for retroflex l to the standard Pali l-underdot."""
    Strng = Strng.replace('l̤', 'ḷ')

    return Strng

