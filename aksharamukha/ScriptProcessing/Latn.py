# -*- coding: utf-8 -*-

# Latn's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def _FixLatnEncode(Strng, Source):
    vir = ''

    #print('here at last ')

    Strng = re.sub('([aiuāīū' + vir + '])(꞉)', r'\2\1', Strng)
    Strng = re.sub('(꞉)(\u033D)', r'\2\1', Strng)

    Strng = Strng.replace('aʰ', 'ʰ') ## Remove extraneous h
    #Strng = PostProcess.LatnInitialVowels(Strng)

    return Strng

def _FixLatnDecode(Strng, Source):
    vir = ''

    #print('here at last ')

    #print(Strng)
    Strng = re.sub('([aiuāīū' + vir + '])(꞉)', r'\2\1', Strng)
    Strng = re.sub('(\u033D)(꞉)', r'\2\1', Strng)
    #print(Strng)

    return Strng

def FixLatn(Strng, Source, reverse=False):
    return _FixLatnDecode(Strng, Source) if reverse else _FixLatnEncode(Strng, Source)

def alephAyinLatnAlternate(Strng):
    Strng = Strng.replace('ʾ', 'ʼ').replace('ʿ', 'ʽ')

    return Strng

def alephAyinLatnAlternate2(Strng):
    Strng = Strng.replace('ʾ', 'ʔ').replace('ʿ', 'ʕ')

    return Strng
