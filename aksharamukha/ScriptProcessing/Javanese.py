# -*- coding: utf-8 -*-

# Javanese's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
#
# See ScriptProcessing/Balinese.py's header - same situation:
# JavaneseMoveRepha's own text is identical pre/post, but the shared
# BalineseJavaneseMoveRepha helper it calls genuinely differs by
# direction, so it still needs the _pre/_post split. AddRepha and
# BalineseJavaneseMoveRepha stay shared with Balinese, called via
# CF./PP./PostProcess. as before.

import re
from aksharamukha.ScriptMap.EastIndic import Javanese

def _FixJavaneseEncode(Strng):
    from .. import ConvertFix as CF
    Repha = '\uA982'
    vir = Javanese.ViramaMap[0]
    ra, ya = Javanese.ConsonantMap[26], Javanese.ConsonantMap[25]
    SubRa, SubYa = '\uA9BF','\uA9BE'

    Strng = CF.AddRepha(Strng,"Javanese",Repha,False)

    # Introduce subjoining Ra & Ya
    Strng = Strng.replace(vir+ra,SubRa).replace(vir+ya,SubYa)


    return Strng

def _FixJavaneseDecode(Strng):
    from .. import ConvertFix as CF
    Repha = '\uA982'
    vir = Javanese.ViramaMap[0]
    ra, ya = Javanese.ConsonantMap[26], Javanese.ConsonantMap[25]
    SubRa, SubYa = '\uA9BF','\uA9BE'

    Strng = CF.AddRepha(Strng,"Javanese",Repha,True)

    #Fix Archaic Jna
    Strng = Strng.replace('ꦘ', 'ꦗ꧀ꦚ')
    # Fix ra agang
    Strng = Strng.replace('ꦬ', ra)
    # Replace Subjoining forms with cons+vir
    Strng = Strng.replace(SubRa,vir+ra).replace(SubYa,vir+ya)
    # reversing archaic jna
    Strng = Strng.replace('ᭌ', 'ᬚ᭄ᬜ')
    # reverse a-based vowels
    vowelsA = ['ꦄꦶ', 'ꦄꦷ', 'ꦄꦸ', 'ꦄꦹ', 'ꦄꦽ', 'ꦄ꧀ꦉꦴ', 'ꦄ꧀ꦭꦼ', 'ꦄ꧀ꦭꦼꦴ', 'ꦄꦺ', 'ꦄꦻ', 'ꦄꦺꦴ', 'ꦄꦻꦴ']
    vowels = ['ꦆ', 'ꦇ', 'ꦈ', 'ꦈꦴ', 'ꦉ', 'ꦉꦴ', 'ꦊ', 'ꦋ', 'ꦌ', 'ꦍ', 'ꦎ', 'ꦎꦴ']

    for v, vA in zip(vowels, vowelsA):
        Strng = Strng.replace(vA, v)


    return Strng

def FixJavanese(Strng,reverse=False):
    return _FixJavaneseDecode(Strng) if reverse else _FixJavaneseEncode(Strng)

def JavaneseMoveRepha_pre(Strng):
    from .. import PreProcess as PP
    return PP.BalineseJavaneseMoveRepha(Strng, 'Javanese', 'ꦂ')

def JavaneseArchaicJNA(Strng):
    Strng = Strng.replace('ꦗ꧀ꦚ', 'ꦘ')
    return Strng

def JavaneseAvowels(Strng):
    vowelsA = ['ꦄꦶ', 'ꦄꦷ', 'ꦄꦸ', 'ꦄꦹ', 'ꦄꦽ', 'ꦄ꧀ꦉꦴ', 'ꦄ꧀ꦭꦼ', 'ꦄ꧀ꦭꦼꦴ', 'ꦄꦺ', 'ꦄꦻ', 'ꦄꦺꦴ', 'ꦄꦻꦴ']
    vowels = ['ꦆ', 'ꦇ', 'ꦈ', 'ꦈꦴ', 'ꦉ', 'ꦉꦴ', 'ꦊ', 'ꦋ', 'ꦌ', 'ꦍ', 'ꦎ', 'ꦎꦴ']

    for v, vA in zip(vowels, vowelsA):
        Strng = Strng.replace(v, vA)

    return Strng

def JavaneseMoveRepha_post(Strng):
    from .. import PostProcess
    return PostProcess.BalineseJavaneseMoveRepha(Strng, 'Javanese', 'ꦂ')
