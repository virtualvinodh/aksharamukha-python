# -*- coding: utf-8 -*-

# Mongolian's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from .. import GeneralMap as GM

# ---- Fix (encode/decode conversion logic) ----

# internal
def _FixMongolianEncode(Strng):
    """Removes redundant free-variation-selector markers before consonants/vowels, reorders consonant clusters before vowels with the Mongolian bowed-tooth marker, and converts the modifier apostrophe to a zero-width joiner."""
    vowels = '(' + '|'.join(GM.CrunchSymbols(GM.Vowels, 'Mongolian')) + ')'
    consonants = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Mongolian')) + ')'

    #Strng = re.sub(consonants + '?' + vowels + '([\u1880\u1881])?', r'\1\2\3 ', Strng)
    Strng = re.sub('(\u180B)' + consonants, r'\2', Strng)
    Strng = re.sub('(\u180B)' + vowels, r'\2', Strng)

    Strng = re.sub(consonants + consonants + consonants + vowels + '(\u1880)', r'\5\1\2\3\4', Strng)
    Strng = re.sub(consonants + consonants + vowels + '(\u1880)', r'\4\1\2\3', Strng)
    Strng = re.sub(consonants + '?' + vowels + '(\u1880)', r'\3\1\2', Strng)
    Strng = Strng.replace(' \u02BC', '\u200B')
    Strng = Strng.replace('\u02BC', '\u200B')


    return Strng

# internal
def _FixMongolianDecode(Strng):
    """Inserts the free-variation selector after a bare aleph-vowel (ᠠ) when it is not already present."""
    vowels = '(' + '|'.join(GM.CrunchSymbols(GM.Vowels, 'Mongolian')) + ')'
    consonants = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Mongolian')) + ')'

    ## add variation seelct one
    #print(Strng)
    Strng = re.sub('(ᠠ)(?!\u180B)', r'\1' + '\u180B', Strng)
    #print(Strng)

    return Strng

# internal
def FixMongolian(Strng, reverse=False):
    """Dispatches to the Mongolian encode or decode fix routine based on the reverse flag."""
    return _FixMongolianDecode(Strng) if reverse else _FixMongolianEncode(Strng)

# ---- Post-processing options ----

# frontend
def MongolianSyllabize(Strng):
    """Inserts syllable-boundary spaces between consonant-vowel units in Mongolian text, e.g. ᠮᠠᢏᢈ → ᠮᠠ᠋ ᢏᢈ."""
    vowels = '(' + '|'.join(GM.CrunchSymbols(GM.Vowels, 'Mongolian')+['\u1820']) + ')'
    consonants = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Mongolian')) + ')'

    Strng = re.sub(consonants + '?' + vowels, r'\1\2' + ' ', Strng)
    Strng = re.sub('(\u180E\u1820)' + consonants, r'\1 \2', Strng)
    Strng = re.sub('\u1820 ', '\u1820\u180B ', Strng)
    Strng = Strng.replace('ᠣᠸᠠ᠋', 'ᠣᠸᠠ')
    Strng = Strng.replace('ᠣᠸᠸᠠ᠋', 'ᠣᠸᠸᠠ')
    Strng = Strng.replace(' \u180E', '\u180E')
    Strng = Strng.replace(' ' + '\u200B', '')
    Strng = Strng.replace(' ᢁ', 'ᢁ')

    return Strng
