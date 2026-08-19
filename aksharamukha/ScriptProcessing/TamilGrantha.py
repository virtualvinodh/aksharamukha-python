# -*- coding: utf-8 -*-

# TamilGrantha's own Fix logic, consolidated out of ConvertFix.py
# (batch migration - see ScriptProcessing/Tamil.py for the pattern
# this follows). No pre/post options exist for this script. Distinct
# from the already-migrated Tamil and Grantha scripts.

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.MainIndic import TamilGrantha, Tamil

# ---- Fix (encode/decode conversion logic) ----

def _FixTamilGranthaEncode(Strng):
    """Reorders Tamil Grantha pre-base vowel signs (e/E/ai, o/O/au) to precede their consonant using joiner marks, matching Tamil script visual ordering."""
    ListC = '|'.join(GM.CrunchSymbols(GM.Consonants, 'TamilGrantha'))
    ListEAI = '|'.join(TamilGrantha.VowelSignMap[9:11]+TamilGrantha.SouthVowelSignMap[0:1])
    ListOAU = TamilGrantha.VowelSignMap[11:13]+TamilGrantha.SouthVowelSignMap[1:2]

    # k + VS e/E/ai -> Joiners + VS e/E/ai + k
    Strng = re.sub('('+ListC+')'+'('+ListEAI+')','\u200B\u200C\u200D\u200C'+r'\2\1',Strng)
    # k + VS o/O/au -> Joiners + VS e/E + k + VS AA/La
    Strng = re.sub('('+ListC+')'+'('+ListOAU[0]+')','\u200B\u200C\u200D\u200C'+TamilGrantha.VowelSignMap[9]+r'\1'+TamilGrantha.VowelSignMap[0],Strng)
    Strng = re.sub('('+ListC+')'+'('+ListOAU[2]+')','\u200B\u200C\u200D\u200C'+TamilGrantha.SouthVowelSignMap[0]+r'\1'+TamilGrantha.VowelSignMap[0],Strng)
    Strng = re.sub('('+ListC+')'+'('+ListOAU[1]+')','\u200B\u200C\u200D\u200C'+TamilGrantha.SouthVowelSignMap[0]+r'\1'+Tamil.SouthConsonantMap[0],Strng)

    ## Reversing நே்ˆদ
    Strng = re.sub('(\u200B\u200C\u200D\u200C.)'+'('+ListC+')'+'(்ˆ)',r'\2\3\1',Strng)


    return Strng

def _FixTamilGranthaDecode(Strng):
    """Reverses the Tamil Grantha pre-base vowel-sign reordering, restoring consonant+vowel-sign order from the joiner-marked visual sequence."""
    ListC = '|'.join(GM.CrunchSymbols(GM.Consonants, 'TamilGrantha'))
    ListEAI = '|'.join(TamilGrantha.VowelSignMap[9:11]+TamilGrantha.SouthVowelSignMap[0:1])
    ListOAU = TamilGrantha.VowelSignMap[11:13]+TamilGrantha.SouthVowelSignMap[1:2]

    #print('I am here')
    # k + VS o/O/au <- Joiners + VS e/E + k + VS AA/La
    Strng = re.sub('\u200B'+TamilGrantha.VowelSignMap[9]+'('+ListC+')'+TamilGrantha.VowelSignMap[0],r'\1'+ListOAU[0],Strng)
    Strng = re.sub('\u200B'+TamilGrantha.SouthVowelSignMap[0]+'('+ListC+')'+TamilGrantha.VowelSignMap[0],r'\1'+ListOAU[2],Strng)
    Strng = re.sub('\u200B'+TamilGrantha.SouthVowelSignMap[0]+'('+ListC+')'+Tamil.SouthConsonantMap[0],r'\1'+ListOAU[1],Strng)
    # k + VS e/E/ai <- Joiners + VS e/E/ai + k
    Strng = re.sub('\u200B'+'('+ListEAI+')'+'('+ListC+')',r'\2\1',Strng)

    return Strng

def FixTamilGrantha(Strng, reverse=False):
    """Dispatches to the Tamil Grantha encode or decode fix routine depending on the reverse flag."""
    return _FixTamilGranthaDecode(Strng) if reverse else _FixTamilGranthaEncode(Strng)
