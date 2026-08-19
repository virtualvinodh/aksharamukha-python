# -*- coding: utf-8 -*-

# Latn's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def _FixLatnEncode(Strng, Source):
    """Reorders visarga to precede an adjacent vowel or combining mark and strips a spurious 'a' before an aspiration marker when encoding to Latin."""
    vir = ''

    #print('here at last ')

    Strng = re.sub('([aiuāīū' + vir + '])(꞉)', r'\2\1', Strng)
    Strng = re.sub('(꞉)(\u033D)', r'\2\1', Strng)

    Strng = Strng.replace('aʰ', 'ʰ') ## Remove extraneous h
    #Strng = PostProcess.LatnInitialVowels(Strng)

    return Strng

def _FixLatnDecode(Strng, Source):
    """Reorders visarga back before a preceding vowel or combining mark when decoding out of Latin script."""
    vir = ''

    #print('here at last ')

    #print(Strng)
    Strng = re.sub('([aiuāīū' + vir + '])(꞉)', r'\2\1', Strng)
    Strng = re.sub('(\u033D)(꞉)', r'\2\1', Strng)
    #print(Strng)

    return Strng

def FixLatn(Strng, Source, reverse=False):
    """Dispatches to the Latin-script encode or decode fix-up routine based on the reverse flag."""
    return _FixLatnDecode(Strng, Source) if reverse else _FixLatnEncode(Strng, Source)

def alephAyinLatnAlternate(Strng):
    """Uses modifier-letter apostrophe symbols instead of aleph/ayin for glottal stop and voiced pharyngeal, e.g. ʾ ʿ → ʼ ʽ."""
    Strng = Strng.replace('ʾ', 'ʼ').replace('ʿ', 'ʽ')

    return Strng

def alephAyinLatnAlternate2(Strng):
    """Uses IPA glottal-stop and pharyngeal-fricative symbols instead of aleph/ayin, e.g. ʾ ʿ → ʔ ʕ."""
    Strng = Strng.replace('ʾ', 'ʔ').replace('ʿ', 'ʕ')

    return Strng
