# -*- coding: utf-8 -*-

# Ahom's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.MainIndic import Ahom

# ---- Fix (encode/decode conversion logic) ----

def _FixAhomEncode(Strng):
    """Reorders Ahom vowel signs and anusvara into correct visual order and merges two consonant+vowel sequences into single ligature characters."""
    ListVS = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSignsNV, 'Ahom')) + ')'
    Anu = '('+ GM.CrunchList('AyogavahaMap', 'Ahom')[1] + ')'

    Strng = Strng.replace('\U0001172B\U0001170D', '\U0001171E')
    Strng = Strng.replace('\U0001172B\U0001170E', '\U0001171D')

    Strng = re.sub(ListVS + Anu, r'\2\1', Strng)
    Strng = re.sub(Anu + '(𑜦)', r'\2\1', Strng)


    return Strng

def _FixAhomDecode(Strng):
    """Reverses Ahom encoding fixes: splits merged ligatures, reconstructs closed-syllable e/o forms, and restores vowel-before-anusvara order."""
    ListVS = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSignsNV, 'Ahom')) + ')'
    Anu = '('+ GM.CrunchList('AyogavahaMap', 'Ahom')[1] + ')'

    Strng = Strng.replace('\U0001171E', '\U0001172B\U0001170D')
    Strng = Strng.replace('\U0001171D', '\U0001172B\U0001170E')

    vir = Ahom.ViramaMap[0]
    anu = Ahom.AyogavahaMap[1]

    #reverse closed syllable e
    Strng = re.sub(anu + '\U00011727' + '(?!\U00011728)', '\U00011726\U00011727\U0001172A', Strng)
    Strng = re.sub('(\U00011726)(.)('+vir+')', '\U00011726\U00011727'+r'\2\3', Strng)

    #rever closed syllable o
    Strng = re.sub('(\U00011728)(.)('+vir+')', '\U00011726\U00011721'+r'\2\3', Strng)

    Strng = Strng.replace(anu + '\U00011728', '\U00011726\U00011721\U0001172A')

    Strng = re.sub(Anu + ListVS, r'\2\1', Strng)

    return Strng

def FixAhom(Strng, reverse=False):
    """Dispatches to the Ahom encode or decode fix-up routine based on the reverse flag."""
    return _FixAhomDecode(Strng) if reverse else _FixAhomEncode(Strng)

# ---- Post-processing options ----

def removePaliAhom(Strng):
    """Replaces Pali-specific Ahom characters with their standard non-Pali equivalents, e.g. 𑝁 𑝂 𑝃 𑝄 𑝅 𑝆 → 𑜄 𑜌 𑜓 𑜔 𑜃 𑜎."""
    pali = "𑝁 𑝂 𑝃 𑝄 𑝅 𑝆".split(" ")
    nonPali ="𑜄 𑜌 𑜓 𑜔 𑜃 𑜎".split(" ")

    for p, np in zip(pali, nonPali):
        Strng = Strng.replace(p, np)

    return Strng

def AhomClosed(Strng):
    """Converts open Ahom vowel signs for i, u, e, and o into their closed-syllable forms before a final consonant or anusvara."""
    vir = Ahom.ViramaMap[0]
    anu = Ahom.AyogavahaMap[1]

    #closed i
    Strng = Strng.replace('\U00011722', '\U00011723')
    Strng = re.sub('(\U00011723)(.)('+vir+')', '\U00011722'+r'\2\3', Strng)
    Strng = Strng.replace(anu + '\U00011723', anu + '\U00011722')

    #closed u
    Strng = Strng.replace('\U00011724', '\U00011725')
    Strng = re.sub('(\U00011725)(.)('+vir+')', '\U00011724'+r'\2\3', Strng)
    Strng = Strng.replace(anu + '\U00011725', anu + '\U00011724')

    #closed e
    Strng = re.sub('(\U00011726\U00011727)(.)('+vir+')', '\U00011726'+r'\2\3', Strng)
    Strng = Strng.replace('\U00011726\U0001172A\U00011727', anu + '\U00011727')

    #closed o
    Strng = re.sub('(\U00011726\U00011721)(.)('+vir+')', '\U00011728'+r'\2\3', Strng)
    Strng = Strng.replace('\U00011726\U0001172A\U00011721', anu + '\U00011728')

    return Strng
