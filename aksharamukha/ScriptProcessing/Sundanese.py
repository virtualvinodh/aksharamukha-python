# -*- coding: utf-8 -*-

# Sundanese's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# ConvertFix/PreProcess/PostProcess are imported LOCALLY inside each
# function that needs them (not at module level) - required to avoid a
# load-order-dependent circular import, since these three modules
# re-export names from here. See ScriptProcessing/Tamil.py.

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.EastIndic import Sundanese

def _FixSundaneseEncode(Strng):

    """Converts ra-virama after a consonant to the Sundanese repha sign and subjoins virama-plus-ya/ra/la into their combining consonant forms when encoding."""
    from .. import PostProcess
    vir = Sundanese.ViramaMap[0]

    r = Sundanese.ConsonantMap[26] + vir
    ListC = '|'.join(GM.CrunchSymbols(GM.Consonants + GM.Vowels + GM.VowelSignsNV,'Sundanese'))
    #print(ListC)


    # Sundanese Repha
    Strng = re.sub('(' + ListC + ')' + r, r'\1' + '\u1B81', Strng)

    yrl = [vir+x for x in Sundanese.ConsonantMap[25:28]]
    yrlSub = ['\u1BA1','\u1BA2','\u1BA3']

    for x,y in zip(yrl,yrlSub):
        # Subjoined consonants
        Strng = Strng.replace(x,y)

    return Strng

def _FixSundaneseDecode(Strng):

    """Restores the Sundanese repha sign to ra-plus-virama, reverses historic conjuncts, and expands subjoined consonants back to virama-plus-consonant when decoding."""
    from .. import PostProcess
    vir = Sundanese.ViramaMap[0]

    r = Sundanese.ConsonantMap[26] + vir
    ListC = '|'.join(GM.CrunchSymbols(GM.Consonants + GM.Vowels + GM.VowelSignsNV,'Sundanese'))
    #print(ListC)


    # Reverse above
    Strng = Strng.replace('\u1B81',r)
    Strng = PostProcess.SundaneseHistoricConjuncts(Strng, True)

    yrl = [vir+x for x in Sundanese.ConsonantMap[25:28]]
    yrlSub = ['\u1BA1','\u1BA2','\u1BA3']

    for x,y in zip(yrl,yrlSub):
        # Reverse above
        Strng = Strng.replace(y,x)

    return Strng

def FixSundanese(Strng,reverse=False):

    """Dispatches to the Sundanese encode or decode fix-up routine based on the reverse flag."""
    from .. import PostProcess
    return _FixSundaneseDecode(Strng) if reverse else _FixSundaneseEncode(Strng)

def SundaneseHistoricConjuncts(Strng, reverse = False):

    """Converts to/from archaic Sundanese subjoined-consonant and word-final consonant forms, e.g. ᮊ᮪ᮙ ᮊ᮪ᮝ ᮃᮊ᮪ ᮃᮙ᮪ → ᮊᮬ ᮊᮭ ᮃᮾ ᮃᮿ."""
    from .. import PostProcess
    ListC = '|'.join(GM.CrunchSymbols(GM.Consonants + GM.Vowels + GM.VowelSignsNV,'Sundanese'))

    if not reverse:
        Strng = Strng.replace('᮪ᮙ', '\u1BAC') # Subjoined m
        Strng = Strng.replace('᮪ᮝ', '\u1BAD') # Subjoined w

        ListC = '|'.join(GM.CrunchSymbols(GM.Consonants + GM.Vowels + GM.VowelSignsNV,'Sundanese'))
        Strng = re.sub('(' + ListC + ')' + 'ᮊ᮪', r'\1' + 'ᮾ', Strng) # Final K
        Strng = re.sub('(' + ListC + ')' + 'ᮙ᮪', r'\1' + 'ᮿ', Strng) # Final M

    else:
        Strng = Strng.replace('\u1BAC', '᮪ᮙ') # Subjoined m
        Strng = Strng.replace('\u1BAD', '᮪ᮝ') # Subjoined w
        Strng = Strng.replace('ᮾ','ᮊ᮪') # Final K
        Strng = Strng.replace('ᮿ','ᮙ᮪') # Final M

    return Strng

def SundaneseRemoveHistoric(Strng):

    """Replaces historic Sundanese vocalic-r/l consonant letters and the archaic pamaeh sign with their modern letter-plus-panyecek combinations."""
    from .. import PostProcess
    Strng = Strng.replace('᮪ᮻ', 'ᮢᮩ')
    Strng = Strng.replace('᮪ᮼ', 'ᮣᮩ')
    Strng = Strng.replace('ᮻ', 'ᮛᮩ')
    Strng = Strng.replace('ᮼ', 'ᮜᮩ')
    Strng = Strng.replace('\u1BBD','\u1B98')

    return Strng
