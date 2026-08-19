# -*- coding: utf-8 -*-

# Kawi's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
#
# KawiMoveRepha independently defines the SAME option name in both
# PreProcess.py and PostProcess.py as two different functions (near-
# inverse regex passes) - suffixed _pre/_post here, aliased back on
# re-export (see ScriptProcessing/DevanagariLimbu.py for the first
# script this pattern was used on). Self-contained - no shared helper
# involved here, unlike Balinese/Javanese's BalineseJavaneseMoveRepha.

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.EastIndic import Kawi

# ---- Fix (encode/decode conversion logic) ----

def FixKawi(Strng, reverse=False):
    """Dispatches to the Kawi encode or decode fix routine depending on the reverse flag."""
    return _FixKawiDecode(Strng) if reverse else _FixKawiEncode(Strng)

def _FixKawiEncode(Strng):
    """Applies Kawi encoding rules: subjoining virama+consonant, ra-repha formation, and disambiguating the tall-A vowel sign after specific consonant clusters."""
    target = 'Kawi'

    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,target))
    ListV ='|'.join(GM.CrunchSymbols(GM.VowelSigns,target))
    ListA ='|'.join(GM.CrunchSymbols(GM.CombiningSigns,target))

    ra = Kawi.ConsonantMap[26]
    vir = Kawi.ViramaMap[0]
    aVS = '\U00011F34'
    aVSAlt = '\U00011F35'
    E = '\U00011F3E'
    AA = '\U00011F34'

    Strng = re.sub(vir+'('+ListC+')','\U00011F42'+r'\1',Strng)
    # Introduce Repha : ra + sub Virama + Cons -> Cons + Repha
    Strng = re.sub('(?<!\U00011F42)'+ra+'\U00011F42'+'('+ListC+')','\U00011F02'+r'\1',Strng)
    #special AA
    TallACons = '|'.join(['\U00011F26', '\U00011F16', '\U00011F1C'])

    Strng = re.sub('(?<!\U00011F42)('+TallACons+')'+'('+E+'?)'+AA,r'\1\2'+'\U00011F35',Strng)

     ## buddho --> Tall A
    Strng = re.sub('('+TallACons+')(\U00011F42)('+ListC +')'+'('+E+'?)'+AA,r'\1\2\3\4'+'\U00011F35',Strng)
    Strng = re.sub('('+TallACons+')(\U00011F42)('+ListC +')'+'(\U00011F42)('+ListC +')'+'('+E+'?)'+AA,r'\1\2\3\4\5\6'+'\U00011F35',Strng)

    ## post-base consonant signs do not need disambiguating AA
    postBaseCons = '|'.join(['\U00011F1A', '\U00011F26', '\U00011F27', '\U00011F2B', '\U00011F31'])
    Strng = re.sub('(\U00011F42)('+postBaseCons+')'+'(\U00011F35)', r'\1\2' + AA, Strng)



    return Strng

def _FixKawiDecode(Strng):
    """Reverses Kawi encoding rules: expands subjoining virama and repha, normalizes alternate tall-A, decomposes JÑA and independent i/u/e vowels, and splits alternate ai/au ligatures."""
    target = 'Kawi'

    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,target))
    ListV ='|'.join(GM.CrunchSymbols(GM.VowelSigns,target))
    ListA ='|'.join(GM.CrunchSymbols(GM.CombiningSigns,target))

    ra = Kawi.ConsonantMap[26]
    vir = Kawi.ViramaMap[0]
    aVS = '\U00011F34'
    aVSAlt = '\U00011F35'
    E = '\U00011F3E'
    AA = '\U00011F34'

    # Replace Subjoining Virama with Explicit Virama
    Strng = Strng.replace('\U00011F42',vir)
    # Replace Repha
    Strng = Strng.replace('\U00011F02', ra + vir)
    # reverse AltA
    Strng = Strng.replace(aVSAlt, aVS)
    # reverse JNA
    Strng = Strng.replace('\U00011F33', '𑼙𑽂𑼛')
    # decompose ind.vowels
    Strng = Strng.replace('\U00011F04\U00011F34', '\U00011F05').replace('\U00011F06\U00011F34', '\U00011F07').replace('\U00011F08\U00011F34', '\U00011F09')
    # reverse Alt ai, alt au
    Strng = Strng.replace('\U00011F3E\U00011F3E', '\U00011F3F')

    return Strng

# ---- Pre-processing options ----

def KawiMoveRepha_pre(Strng):
    """Moves the Kawi repha (superscript RA) mark from before to after the consonant/vowel cluster it modifies, for correct rendering order."""
    tgt = 'Kawi'
    repha = '\U00011F02'

    cons = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants + GM.Vowels, tgt)) + ')'
    vows = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSignsNV, tgt)) + ')'
    vir = '\U00011F42'

    Strng = re.sub(repha + '(('+cons+')' + '('+ vir + cons +')*'+'(' + vows + ')?)', r'\1' + repha, Strng)

    return Strng

# ---- Post-processing options ----

def KawiAltAiAU(Strng):
    #  Alt ai, alt au
    """Uses the alternate AI/AU vowel form: 𑼒𑼿 𑼒𑼿𑼴 → 𑼒𑼾𑼾 𑼒𑼾𑼾𑼴."""
    Strng = Strng.replace('\U00011F3F', '\U00011F3E\U00011F3E')

    return Strng

def KawiArchaicJNA(Strng):
    """Uses the archaic JÑA conjunct form: 𑼙𑽂𑼛 → 𑼳."""
    Strng = Strng.replace('𑼙𑽂𑼛', '\U00011F33')
    return Strng

def KawiDecomposedVowel(Strng):
    """Uses decomposed independent vowel forms: 𑼅 𑼇 𑼉 → 𑼄𑼴 𑼆𑼴 𑼈𑼴."""
    Strng = Strng.replace('\U00011F05', '\U00011F04\U00011F34').replace('\U00011F07', '\U00011F06\U00011F34').replace('\U00011F09', '\U00011F08\U00011F34')

    return Strng

def KawiMoveRepha_post(Strng):
    """Moves the Kawi repha (superscript RA) mark from after back to before the consonant/vowel cluster it modifies, reversing the rendering-order adjustment."""
    tgt = 'Kawi'
    repha = '\U00011F02'

    cons = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants + GM.Vowels, tgt)) + ')'
    vows = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSignsNV, tgt)) + ')'
    vir = '\U00011F42'

    Strng = re.sub('(('+cons+')' + '('+ vir + cons +')*'+'(' + vows + ')?)' + repha , repha + r'\1', Strng)

    return Strng
