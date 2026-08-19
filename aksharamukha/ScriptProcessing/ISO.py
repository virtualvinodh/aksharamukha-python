# -*- coding: utf-8 -*-

# ISO's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# ConvertFix/PreProcess/PostProcess are imported LOCALLY inside each
# function that needs them (not at module level) - required to avoid a
# load-order-dependent circular import, since these three modules
# re-export names from here. See ScriptProcessing/Tamil.py.

import re

def longEOISO(Strng):

    """Treats plain e/o as long vowels by converting them to ē/ō in ISO-15919 transliteration."""
    from .. import PreProcess as PP
    Strng = Strng.replace('e', 'ē').replace('o', 'ō')

    return Strng

def joinVowelConsISO(Strng):

    """Joins a consonant-final word with a following vowel-initial word in ISO-15919 text, e.g. tat tvam asi → tattvamasi."""
    from .. import PreProcess as PP
    return PP.joinVowelCons(Strng, 'ISO')

def noLongEO(Strng):

    """Converts long ē/ō vowels back to plain e/o in ISO-15919 transliteration."""
    from .. import PreProcess as PP
    Strng = Strng.replace('ē', 'e').replace('ō', 'o')

    return Strng
