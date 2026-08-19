# -*- coding: utf-8 -*-

# Newa's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.MainIndic import Newa

def _FixNewaEncode(Strng):
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'Newa'))
    ra = Newa.ConsonantMap[26]
    vir = Newa.ViramaMap[0]
    ## The default behavior of Repha has been proposed to change
    # Strng = re.sub(ra + vir + '(' + ListC + ')', ra + vir + '\u200D' + r'\1', Strng)

    return Strng

def _FixNewaDecode(Strng):
    pass

    return Strng

def FixNewa(Strng, reverse=False):
    return _FixNewaDecode(Strng) if reverse else _FixNewaEncode(Strng)

def nepaldevafont(Strng):
    return Strng

def NewaMurmurConsonants(Strng):
    murmur = ['𑐓','𑐙','𑐤', '𑐪', '𑐭', '𑐯']
    connsh = ['𑐴𑑂𑐒', '𑐴𑑂𑐘', '𑐴𑑂𑐣', '𑐴𑑂𑐩', '𑐴𑑂𑐬', '𑐴𑑂𑐮']

    for x, y in zip(murmur, connsh):
        Strng = Strng.replace(y, x)

    return Strng

def NewaSpecialTa(Strng):

    Strng = Strng.replace('𑐟𑑂', '𑐟𑑂‍') #Ta+virama -> ta + virama + ZWJ

    return Strng

def NewaDisableRepha(Strng):
    Strng = Strng.replace('𑐬𑑂', '𑐬𑑂\u200D')

    return Strng
