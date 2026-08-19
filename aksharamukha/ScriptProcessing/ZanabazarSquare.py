# -*- coding: utf-8 -*-

# ZanabazarSquare's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.EastIndic import ZanabazarSquare

def _FixZanabazarSquareEncode(Strng):
    """Applies Zanabazar Square encoding fixes: converts virama+consonant to subjoining form and merges the KSSA conjunct sequence into its dedicated character."""
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'ZanabazarSquare'))
    yrlv = ZanabazarSquare.ConsonantMap[25:29]
    yrlv_sub = ['\U00011A3B', '\U00011A3C', '\U00011A3D', '\U00011A3E']

    vir = ZanabazarSquare.ViramaMap[0]

    Strng = re.sub(vir+'('+ListC+')','\U00011A47'+r'\1',Strng)
    # KSSA
    Strng = Strng.replace('𑨋𑩇𑨯','𑨲')

    return Strng

def _FixZanabazarSquareDecode(Strng):
    """Reverses Zanabazar Square encoding fixes: expands subjoining virama and repha, TSA-series to CA-series consonants, contextual y/r/l/v forms, alternate ai/au, the KSSA conjunct, and the Mongolian final mark."""
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'ZanabazarSquare'))
    yrlv = ZanabazarSquare.ConsonantMap[25:29]
    yrlv_sub = ['\U00011A3B', '\U00011A3C', '\U00011A3D', '\U00011A3E']

    vir = ZanabazarSquare.ViramaMap[0]

    Strng = Strng.replace('\U00011A41', ' ')

    tsaSeries = ['𑨣', '𑨤', '𑨥']
    caSeries = ['𑨐','𑨑','𑨒']

    for x, y in zip(tsaSeries,caSeries):
        Strng = Strng.replace(y, x)

    # subjoining contextual y/r/l/v
    for x, y in zip(yrlv, yrlv_sub):
        Strng = Strng.replace(y, '\U00011A47' + x)

    # Repha
    Strng = Strng.replace('\U00011A3A', yrlv[1] + '\U00011A47')

    # KSSA
    Strng = Strng.replace('𑨲', '𑨋𑩇𑨯')

    # Alternate ai/au
    Strng = Strng.replace('\U00011A07', '\U00011A04\U00011A0A')
    Strng = Strng.replace('\U00011A08', '\U00011A06\U00011A0A')

    # Mongolian final -> Virama
    Strng = Strng.replace('\U00011A33', vir)

    # Subojin to Normal vir
    Strng = Strng.replace('\U00011A47', vir)

    return Strng

def FixZanabazarSquare(Strng, reverse=False):
    """Dispatches to the Zanabazar Square encode or decode fix routine depending on the reverse flag."""
    return _FixZanabazarSquareDecode(Strng) if reverse else _FixZanabazarSquareEncode(Strng)

def ZanabazarSanskritPalatals(Strng):
    """Converts TSA-series letters to Sanskrit palatal (CA-series) forms: 𑨣 𑨤 𑨥 → 𑨐 𑨑 𑨒."""
    tsaSeries = ['𑨣', '𑨤', '𑨥']
    caSeries = ['𑨐','𑨑','𑨒']

    for x, y in zip(tsaSeries,caSeries):
        Strng = Strng.replace(x, y)

    return Strng

def ZanzabarSpaceTsheg(Strng):
    """Replaces spaces with the Zanabazar Square tsheg (syllable separator) mark: 𑨝 𑨢𑨆 → 𑨝𑩁𑨢𑨆."""
    Strng = Strng.replace(' ', '\U00011A41')

    return Strng

def ZanabazarSquareContextual(Strng):
    """Applies contextual subjoined ya/ra/la/va forms and the repha ligature: 𑨋𑩇𑨪 𑨋𑩇𑨫 𑨋𑩇𑨬 𑨋𑩇𑨭 𑨫𑩇𑨋 → 𑨋𑨻 𑨋𑨼 𑨋𑨽 𑨋𑨾 𑨺𑨋."""
    yrlv = ZanabazarSquare.ConsonantMap[25:29]
    yrlv_sub = ['\U00011A3B', '\U00011A3C', '\U00011A3D', '\U00011A3E']

    for x, y in zip(yrlv, yrlv_sub):
        Strng = Strng.replace('\U00011A47' + x, y)
    # Repha
    Strng = re.sub('(?<!\U00011A47)' + yrlv[1] + '\U00011A47', '\U00011A3A', Strng)

    return Strng

def ZanabazarSquareAiAu(Strng):
    """Uses alternate ai/au vowel ligatures: 𑨀𑨄𑨊 𑨀𑨆𑨊 → 𑨀𑨇 𑨀𑨈."""
    Strng = Strng.replace('\U00011A04\U00011A0A', '\U00011A07')
    Strng = Strng.replace('\U00011A06\U00011A0A', '\U00011A08')

    return Strng

def ZanabazarSquareMongolianFinal(Strng):
    """Uses the Mongolian final consonant mark in place of virama: 𑨀𑨋𑨴 → 𑨀𑨋𑨳."""
    Strng = Strng.replace(ZanabazarSquare.ViramaMap[0], '\U00011A33')

    return Strng
