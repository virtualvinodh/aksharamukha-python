# -*- coding: utf-8 -*-

# Sharada's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re
from .. import GeneralMap as GM

def _FixSharadaEncode(Strng):

    from .. import PostProcess
    Strng = PostProcess.KhandaTa(Strng, 'Assamese', False)

    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'Sharada'))
    Nukta = '|'.join(GM.CrunchSymbols(GM.CombiningSigns,'Sharada')[-1])
    Virama = ''.join(GM.CrunchSymbols(['ViramaMap'], 'Sharada'))

    Strng = Strng.replace( Nukta + Virama, Nukta + Virama + '\u200C')
    Strng = re.sub('(' + Virama + ')' + '(' + ListC + ')' + '(' + Nukta + ')', r'\1' + '\u200C' + r'\2\3', Strng)

    '''Strng = Strng.replace('𑆇ʼ','\U00011183\U000111CB\U000111B6').replace('𑆈ʼ','\U00011183\U000111CB\U000111B7')\
        .replace('𑆶ʼ','\U000111CB\U000111B6').replace('𑆷ʼ','\U000111CB\U000111B7')

    Strng = Strng.replace('\U00011184ʼ', '𑆃𑇋𑆳')
    Strng = re.sub('(?<!\U000111BE)\U000111B3ʼ', '\U000111CB\U000111B3', Strng)

    Strng = Strng.replace('𑆃ʼ', '𑆃𑇋', )
    Strng = re.sub('(' + ListC + ')'+ 'ʼ', r'\1' + '\U000111CB', Strng)'''






    return Strng

def _FixSharadaDecode(Strng):

    from .. import PostProcess
    Strng = PostProcess.KhandaTa(Strng, 'Assamese', True)

    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'Sharada'))
    Nukta = '|'.join(GM.CrunchSymbols(GM.CombiningSigns,'Sharada')[-1])
    Virama = ''.join(GM.CrunchSymbols(['ViramaMap'], 'Sharada'))

    pass
    # u^ u^^ to vriaama
    # Fix Devanagari as well u^ u^^ to devanagri vowels

    # half-u and half-long-u
    #Strng = Strng.replace('\U00011183\U000111CB\U000111B6', '𑆇ʼ').replace('\U00011183\U000111CB\U000111B7', '𑆈ʼ').\
    #    replace('\U000111CB\U000111B6', '𑆶ʼ').replace('\U000111CB\U000111B7', '𑆷ʼ')

    #Strng = Strng.replace('𑆃𑇋𑆳', '\U00011184ʼ')
    #Strng = re.sub('(?<!\U000111BE)\U000111CB\U000111B3', '\U000111B3ʼ', Strng)

    #Strng = Strng.replace('𑆃𑇋', '𑆃ʼ')
    #Strng = re.sub('(' + ListC + ')'+ '\U000111CB', r'\1' +  'ʼ', Strng)

    return Strng

def FixSharada(Strng,reverse=False):

    from .. import PostProcess
    return _FixSharadaDecode(Strng) if reverse else _FixSharadaEncode(Strng)
