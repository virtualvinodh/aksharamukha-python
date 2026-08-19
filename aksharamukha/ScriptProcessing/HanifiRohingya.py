# -*- coding: utf-8 -*-

# HanifiRohingya's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from .. import GeneralMap as GM

# ---- Fix (encode/decode conversion logic) ----

def _hanifi_rohingya_lookups():
    """Builds regex character-class strings for Hanifi Rohingya consonants and vowels used by the encode/decode fixers."""
    consList = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'HanifiRohingya')+['\U00010D17', '\U00010D19']) + ')'
    vowList = '(' + '|'.join(GM.CrunchSymbols(GM.Vowels, 'HanifiRohingya')) + ')'

    vowListNotA = '(' + '|'.join(GM.CrunchSymbols(GM.Vowels, 'HanifiRohingya')[1:]) + ')'

    consListLookBehind = ''.join(map(lambda x: '(?<!' + x + ')', GM.CrunchSymbols(GM.Consonants, 'HanifiRohingya')))
    return consList, vowList, vowListNotA, consListLookBehind

def _FixHanifiRohingyaEncode(Strng):
    """Encodes Hanifi Rohingya orthography: inserts vowel carriers, gemination marks, diphthong signs, tone letters, sukun, and Perso-Arabic punctuation."""
    consList, vowList, vowListNotA, consListLookBehind = _hanifi_rohingya_lookups()

    Strng = re.sub(consListLookBehind + vowList, '\U00010D00' + r'\1', Strng ) # Add Vowel Carrier
    Strng = re.sub(consList + r'\1', r'\1' + '\U00010D27', Strng) # Add Gemination

    Strng = re.sub(vowListNotA + '𐴀𐴟', r'\1' + '\U00010D17', Strng) # koi, kui etc
    Strng = re.sub(vowListNotA + '𐴀𐴞', r'\1' + '\U00010D19', Strng) # kou etc. using the dipthong character

    Strng = Strng.replace('\U00010D24\\', '\U00010D25') #swap tone 2
    Strng = Strng.replace('\U00010D24/', '\U00010D26') #swap tone 3

    Strng = Strng.replace('_', '\U00010D22') # Map Sukun

    for x,y in zip([',','?',';'],['،','؟','؛']):
        Strng = Strng.replace(x,y)

    return Strng

def _FixHanifiRohingyaDecode(Strng):
    """Reverses Hanifi Rohingya encoding: removes vowel carriers, expands gemination and diphthongs, and restores tone marks and punctuation."""
    consList, vowList, vowListNotA, consListLookBehind = _hanifi_rohingya_lookups()

    tones = '([\U00010D24\U00010D25\U00010D26])'
    Strng = re.sub('(\U00010D00)' + tones + vowList, r'\1\3\2', Strng) # Swap Vowel-carrier + tone + vowelsign
    Strng = re.sub(consList + tones + vowList, r'\1\3\2', Strng) # swap cons + tone + vowel sign

    Strng = re.sub(vowListNotA.replace('\U00010D00', '') + '\U00010D17' , r'\1' + '𐴀𐴟', Strng) #swap tone 2
    Strng = re.sub(vowListNotA.replace('\U00010D00', '') +'\U00010D19', r'\1' + '𐴀𐴞' , Strng) #swap tone 3

    Strng = Strng.replace('\U00010D00', '') # remove vowel carrier
    Strng = re.sub('(.)' + '\U00010D27', r'\1\1' , Strng) # reverse gemination

    Strng = Strng.replace('\U00010D25', '\U00010D24\\') #swap tone 2
    Strng = Strng.replace('\U00010D26', '\U00010D24/') # swap tone 3

    Strng = re.sub(consList + '\U00010D17' , r'\1' + '\U00010D16\u02BE', Strng) # cons + dipth.y -> y + nukta

    Strng = re.sub(consList +'\U00010D19', r'\1' + '\U00010D18\u02BE', Strng) # cons + dipth.w -> v + nukta

    Strng = Strng.replace('\U00010D22', '_') #remove Sukun

    Strng = Strng.replace('𐴜', '𐴖') # v -> w; Archaic v is not used anyway

    for x,y in zip([',','?',';'],['،','؟','؛']):
        Strng = Strng.replace(y,x)

    return Strng

def FixHanifiRohingya(Strng, reverse=False):
    """Dispatches to the Hanifi Rohingya encode or decode fix routine depending on conversion direction."""
    return _FixHanifiRohingyaDecode(Strng) if reverse else _FixHanifiRohingyaEncode(Strng)
