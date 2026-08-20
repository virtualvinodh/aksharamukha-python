# -*- coding: utf-8 -*-

# Thaana's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re
from .. import GeneralMap as GM

# ---- Fix (encode/decode conversion logic) ----

# internal
def _FixThaanaEncode(Strng):

    """Applies Thaana encoding fixes: gemination-sign insertion, removal of redundant inherent-vowel sign before vowel signs, and Arabic-to-Thaana punctuation mapping."""
    from .. import PostProcess
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'Thaana'))
    VowelVS = '|'.join(GM.CrunchSymbols(GM.VowelSigns,'Thaana'))
    aBase = '\u0787'

    # Replace VS-A + Vowel Sign -> Vowel Sign :
    Strng = PostProcess.InsertGeminationSign(Strng, 'Thaana')
    Strng = re.sub("(\u07A6)"+"(?=("+VowelVS+"))","",Strng)
    Strng = Strng.replace("\u02BE","")

    for x,y in zip([',','?',';'],['،','؟','؛']):
        Strng = Strng.replace(x,y)

    Strng = Strng.replace('ʔ', 'އް')


    return Strng

# internal
def _FixThaanaDecode(Strng):

    """Reverses Thaana encoding fixes: approximates Arabic-loan consonants to native Thaana letters, inserts sukun on bare consonants, restores the inherent-vowel sign before vowel signs, and reverses gemination/punctuation mapping."""
    from .. import PostProcess
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'Thaana'))
    VowelVS = '|'.join(GM.CrunchSymbols(GM.VowelSigns,'Thaana'))
    aBase = '\u0787'

    # Add VS-A to all VowelSigns
    # Approximate
    Strng = Strng.replace('ޢ','އ')
    Strng = Strng.replace('ޡ','ތ')
    Strng = Strng.replace('ޥ','ވ') # waav to va
    Strng = Strng.replace('ޠ','ތ') # To to ta
    Strng = Strng.replace('ޟ','ސ')
    Strng = Strng.replace('ޞ','ސ')
    Strng = Strng.replace('ޜ','ށ')
    Strng = Strng.replace('ޛ','ދ')
    Strng = Strng.replace('ޘ','ތ')
    Strng = Strng.replace('ޛ','ދ')
    Strng = Strng.replace('ޙ', 'ހ')

    Strng = re.sub('(' + ListC.replace('ަ','') + ')' + '(?!' + VowelVS + '|ަ' + ')', r'\1' + 'ް', Strng)

    Strng = re.sub('(?<!'+aBase+')(?<!'+'\u02BD\u02BD\u02BD'+')('+VowelVS+')',"\u07A6"+r'\1',Strng)
    Strng = PostProcess.ReverseGeminationSign(Strng, 'Thaana')

    Strng = Strng.replace('އް','ʔ')

    for x,y in zip([',','?',';'],['،','؟','؛']):
        Strng = Strng.replace(y,x)

    return Strng

# internal
def FixThaana(Strng, reverse=False):

    """Dispatches to the Thaana encode or decode fix routine depending on the reverse flag."""
    return _FixThaanaDecode(Strng) if reverse else _FixThaanaEncode(Strng)

# ---- Post-processing options ----

# internal
def ThaanaRemoveHistorical(Strng):
    """Replaces the historical Thaana letter naa (retroflex n) with the modern noonu letter."""
    return Strng.replace('ޱ','ނ')

