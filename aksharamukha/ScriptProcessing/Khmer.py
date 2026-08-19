# -*- coding: utf-8 -*-

# Khmer's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.EastIndic import Khmer

def _FixKhmerEncode(Strng, target):
    """Converts virama+consonant sequences to the subjoining coeng form, introduces the ra-repha ligature, and merges the i vowel sign with anusvara into their ligature."""
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,target))
    ListV ='|'.join(GM.CrunchSymbols(GM.VowelSigns,target))
    ListA ='|'.join(GM.CrunchSymbols(GM.CombiningSigns,target))

    ra = Khmer.ConsonantMap[26]
    vir = Khmer.ViramaMap[0]

    Strng = re.sub(vir+'('+ListC+')','\u17D2'+r'\1',Strng)
    # Introduce Repha : ra + sub Virama + Cons -> Cons + Repha
    Strng = re.sub('(?<!\u17D2)('+ra+')'+'\u17D2'+'('+ListC+')',r'\2'+'\u17CC',Strng)
    # i + Anusara -> i-Anusvara ligature
    Strng = Strng.replace('\u17B7\u17C6','\u17B9')


    return Strng

def _FixKhmerDecode(Strng, target):
    """Expands the subjoining coeng mark back to explicit virama, restores the ra-repha ligature to ra+virama+consonant, and splits the i-anusvara ligature apart."""
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,target))
    ListV ='|'.join(GM.CrunchSymbols(GM.VowelSigns,target))
    ListA ='|'.join(GM.CrunchSymbols(GM.CombiningSigns,target))

    ra = Khmer.ConsonantMap[26]
    vir = Khmer.ViramaMap[0]

    # Replace Subjoining Virama with Explicit Virama
    Strng = Strng.replace('\u17D2',vir)
    Strng = re.sub(vir+'(?=[\u17AB\u17AC\u17AD\u17AE])','\u17D2',Strng)
    # Remove Repha : ra + sub Virama + Cons <- Cons + Repha
    Strng = re.sub('('+ListC+')'+'\u17CC',ra+vir+r'\1',Strng)
    # i + Anusara -> i-Anusvara ligature
    Strng = Strng.replace('\u17B9','\u17B7\u17C6')

    return Strng

def FixKhmer(Strng,reverse=False, target="Khmer"):
    """Dispatches to the Khmer encode or decode fix routine depending on conversion direction."""
    return _FixKhmerDecode(Strng, target) if reverse else _FixKhmerEncode(Strng, target)

def KhmerWordSplit(Strng):
    """Segments unspaced Khmer text into words using the khmernltk tokenizer (មនុស្សទាំងអស់ → មនុស្ស ទាំងអស់)."""
    from khmernltk import word_tokenize
    sents = Strng.split('\n')
    sent_token = []
    for sent in sents:
        sent_token.append(' '.join(word_tokenize(sent)))
    Strng = '\n'.join(sent_token)
    Strng = Strng.replace('  ', ' ')

    return Strng
