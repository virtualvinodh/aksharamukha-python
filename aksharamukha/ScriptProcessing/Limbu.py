# -*- coding: utf-8 -*-

# Limbu's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
#
# LimbuSpellingSaI independently defines the SAME option name in both
# PreProcess.py and PostProcess.py, as two genuinely different functions
# (pre-side does roughly one direction of a transform, post-side roughly
# the inverse) - can't both be a bare top-level `def` of the identical
# name in one file. Suffixed _pre/_post here; PreProcess.py/PostProcess.py
# each re-export their own half under the ORIGINAL (unsuffixed) name via
# `import X_pre as X` / `import X_post as X`, so the public option name
# (post_options=['X']/pre_options=['X']) is completely unchanged.

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.MainIndic import Limbu

def _FixLimbuEncode(Strng):
    """Converts virama+ya/ra/va to subjoined consonant letters, maps consonant+virama to dedicated Limbu final-consonant letters, and substitutes punctuation with Limbu equivalents."""
    vir = Limbu.ViramaMap[0]

    SCons = [vir+x for x in [Limbu.ConsonantMap[x] for x in [25,26,28]]]  # /ya/, /ra/, /va/
    SubCons = ['\u1929','\u192A','\u192B']

    for x,y in zip(SCons,SubCons):
        # Replace Subjoined Consonants
        Strng = Strng.replace(x,y)

    signAll = '|'.join(GM.CrunchSymbols(GM.Consonants+GM.Vowels+GM.VowelSignsNV, "Limbu"))

    FCons = [x+vir for x in [Limbu.ConsonantMap[x] for x in[0,4,15,19,20,24,26,27]]]
    FinalCons = ['\u1930','\u1931','\u1933','\u1934','\u1935','\u1936','\u1937','\u1938']

    ### ZWNJ with finalcons + ya/ra/la/va (perhaps do this for other scripts)ˍ
    #Strng = Strng.replace("\u1922\u193A", "\u193A\u1922")
    Strng = Strng.replace('꞉', '᤺')

    for x,y in zip(FCons,FinalCons):
        # Replace Final pure consonants
        Strng = re.sub('('+signAll+')'+ '(\u193A?)' + '('+x+')',r'\1\2'+y,Strng)

    Strng = Strng.replace('ʔ','᤹')
    Strng = Strng.replace('!','᥄')
    Strng = Strng.replace('?','᥅')
    ## Add proper support for Limbu e,o to Devanagari
    ## Limbu Question mark and exclamation mark?
    ## LImbu to devanagari conventions
    ## Limbu Danda

    return Strng

def _FixLimbuDecode(Strng):
    """Reverses subjoined and dedicated final-consonant letters back to virama sequences, and restores Limbu punctuation to ASCII equivalents."""
    vir = Limbu.ViramaMap[0]

    SCons = [vir+x for x in [Limbu.ConsonantMap[x] for x in [25,26,28]]]  # /ya/, /ra/, /va/
    SubCons = ['\u1929','\u192A','\u192B']

    for x,y in zip(SCons,SubCons):
        # Reverse above
        Strng = Strng.replace(y,x)

    signAll = '|'.join(GM.CrunchSymbols(GM.Consonants+GM.Vowels+GM.VowelSignsNV, "Limbu"))

    FCons = [x+vir for x in [Limbu.ConsonantMap[x] for x in[0,4,15,19,20,24,26,27]]]
    FinalCons = ['\u1930','\u1931','\u1933','\u1934','\u1935','\u1936','\u1937','\u1938']

    ### ZWNJ with finalcons + ya/ra/la/va (perhaps do this for other scripts)ˍ
    #Strng = Strng.replace("\u193A\u1922", "\u1922\u193A")
    Strng = re.sub('(' + '|'.join(FinalCons) + ')' + '(?=[ᤕᤖᤘ])', r'\1' + '\u200C', Strng)
    Strng = re.sub('([ᤀᤁᤂᤃᤄᤅᤆᤇᤈᤉᤊᤋᤌᤍᤎᤏᤐᤑᤒᤓᤔᤕᤖᤗᤘᤚᤛᤜᤠᤣᤥᤧᤨᤩᤪᤫ])᤺', r'\1' + '꞉', Strng)
    ## Modifying letter colon ## Fix this only with aH ᤆᤠ᤺ᤣ

    for x,y in zip(FCons,FinalCons):
        # Reverse above
        Strng = Strng.replace(y,x)

    Strng = Strng.replace('᤹', 'ʔ')
    Strng = Strng.replace('᥄', '!')
    Strng = Strng.replace('᥅', '?')
    ## Add proper support for Limbu e,o to Devanagari
    ## Limbu Question mark and exclamation mark?
    ## LImbu to devanagari conventions
    ## Limbu Danda

    return Strng

def FixLimbu(Strng,reverse=False):
    """Dispatches to the Limbu encode or decode fix routine depending on conversion direction."""
    return _FixLimbuDecode(Strng) if reverse else _FixLimbuEncode(Strng)

def LimbuSpellingSaI_pre(Strng): ## Fix this not for all
    """Pre-processing step that prefixes Limbu final-consonant letters with the sa-i sign for an alternate spelling convention."""
    vir = Limbu.ViramaMap[0]

    FCons = [x+vir for x in [Limbu.ConsonantMap[x] for x in[0,4,15,19,20,24,26,27]]]
    FinalCons = ['\u1930','\u1931','\u1933','\u1934','\u1935','\u1936','\u1937','\u1938']

    for x, y in zip(FCons, FinalCons):
        Strng = Strng.replace(x, '\u193A' + y)

    return Strng

def LimbuSpellingSaI_post(Strng):
    """Post-processing step that removes the sa-i sign prefix from Limbu final-consonant letters, restoring the standard consonant+virama spelling."""
    vir = Limbu.ViramaMap[0]

    FCons = [x+vir for x in [Limbu.ConsonantMap[x] for x in[0,4,15,19,20,24,26,27]]]
    FinalCons = ['\u1930','\u1931','\u1933','\u1934','\u1935','\u1936','\u1937','\u1938']

    for x, y in zip(FCons, FinalCons):
        Strng = Strng.replace('\u193A' + y, x)
        Strng = Strng.replace('\u193A\u1922' + y, '\u1922' + x)

    return Strng

def LimburemoveHistorical(Strng):
    """Replaces obsolete/historical Limbu letter pairs with their modern equivalents."""
    removePairs = [("ᤉ", "ᤈ"), ("ᤊ","ᤏ"), ("ᤚ", "ᤙ"), ("ᤲ", "ᤱ")]

    for x,y in removePairs:
        Strng = Strng.replace(x,y)

    return Strng
