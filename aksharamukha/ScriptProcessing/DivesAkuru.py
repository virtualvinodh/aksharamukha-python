# -*- coding: utf-8 -*-

# DivesAkuru's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
#
# DivesAkuruAlternateIndVowels independently defines the SAME option name
# in both PreProcess.py and PostProcess.py as two different functions -
# suffixed _pre/_post here, aliased back on re-export (see
# ScriptProcessing/DevanagariLimbu.py for the first script this pattern
# was used on).

import re
from .. import GeneralMap as GM

# ---- Fix (encode/decode conversion logic) ----

# internal
def _FixDivesAkuruEncode(Strng):
    """Converts explicit virama+consonant into subjoining virama and forms special ra/ya conjuncts (repha, subjoined ya) for Dives Akuru."""
    target = 'DivesAkuru'

    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,target)+['\U00011926'])
    ListV ='|'.join(GM.CrunchSymbols(GM.VowelSigns,target))
    ListA ='|'.join(GM.CrunchSymbols(GM.CombiningSigns,target))

    ra = GM.CrunchSymbols(GM.Consonants,target)[26]
    ya = GM.CrunchSymbols(GM.Consonants,target)[25]
    vir = GM.CrunchSymbols(GM.virama,target)[0]
    combVir = '\U0001193E'
    aVS = '\U00011F34'

    Strng = re.sub(vir+'('+ListC+')', combVir+r'\1',Strng)
    # Replace Explicit Virama + Cons -> Subjoining Virama + Cons
    Strng = re.sub(combVir +ra, '\U00011942',Strng)
    # Replace Explicit Virama + Cons -> Subjoining Virama + Cons
    Strng = re.sub(combVir +ya, '\U00011940',Strng)
    # Introduce Repha : ra + sub Virama + Cons -> Cons + Repha
    Strng = re.sub('(?<!\U0001193E)'+ra+'\U0001193E'+'('+ListC+')','\U00011941'+r'\1',Strng)


    return Strng

# internal
def _FixDivesAkuruDecode(Strng):
    """Reverses Dives Akuru homorganic nasal signs, subjoining virama, alternate ya, and repha/subjoined-ya conjuncts back to explicit sequences."""
    target = 'DivesAkuru'

    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,target)+['\U00011926'])
    ListV ='|'.join(GM.CrunchSymbols(GM.VowelSigns,target))
    ListA ='|'.join(GM.CrunchSymbols(GM.CombiningSigns,target))

    ra = GM.CrunchSymbols(GM.Consonants,target)[26]
    ya = GM.CrunchSymbols(GM.Consonants,target)[25]
    vir = GM.CrunchSymbols(GM.virama,target)[0]
    combVir = '\U0001193E'
    aVS = '\U00011F34'

    # reverse homonasal
    homoNasal = '\U0001193F'

    Strng = re.sub(homoNasal+'(?=[𑤌𑤍𑤎𑤏])', '𑤐\U0001193E', Strng)
    Strng = re.sub(homoNasal+'(?=[𑤑𑤒𑤓])', '𑤕\U0001193E', Strng)
    Strng = re.sub(homoNasal+'(?=[𑤖𑤘𑤙])', '𑤚\U0001193E', Strng)
    Strng = re.sub(homoNasal+'(?=[𑤛𑤜𑤝𑤞])', '𑤟\U0001193E', Strng)
    Strng = re.sub(homoNasal+'(?=[𑤠𑤡𑤢𑤣])', '𑤤\U0001193E', Strng)

    # reverse the joning virama
    Strng = Strng.replace(combVir, vir)
    # replace alter. ya
    Strng = Strng.replace("\U00011926", "\U00011925")
    # Reverse : Replace Explicit Virama + Cons -> Subjoining Virama + Cons
    Strng = re.sub(combVir, vir, Strng)
    # Reverse : Replace Explicit Virama + Cons -> Subjoining Virama + Cons
    Strng = re.sub('\U00011942', vir +ra, Strng)
    # Reverse : Replace Explicit Virama + Cons -> Subjoining Virama + Cons
    Strng = re.sub('\U00011940', vir +ya, Strng)
    # Reverse : Introduce Repha : ra + sub Virama + Cons -> Cons + Repha
    Strng = re.sub('\U00011941', vir +ra, Strng)


    return Strng

# internal
def FixDivesAkuru(Strng, reverse=False):
    """Dispatches to the Dives Akuru encode or decode fix-up routine based on the reverse flag."""
    return _FixDivesAkuruDecode(Strng) if reverse else _FixDivesAkuruEncode(Strng)

# ---- Pre-processing options ----

# frontend
def DivesAkuruAlternateIndVowels_pre(Strng):
    # use alt /y/
    #Strng = Strng.replace("\U00011925", "\U00011926")

    # replace ind. vow with /y/

    """Collapses y-based vowel sequences (e.g. 𑤥𑤰) into their standalone Dives Akuru independent vowel letters (e.g. 𑤁)."""
    vow = "𑤁 𑤂 𑤃 𑤄 𑤅 𑤆 𑤆𑤵 𑤉 𑤀".split(" ")
    vowy = "𑤥𑤰 𑤥𑤱 𑤥𑤲 𑤥𑤳 𑤥𑤴 𑤥𑤵 𑤥𑤷 𑤥𑤸 𑤥".split(" ")

    for v, vy in zip(vow, vowy):
        Strng = Strng.replace(vy, v)

    return Strng

# ---- Post-processing options ----

# frontend
def DivesAkuruAlternateIndVowels_post(Strng):
    # use alt /y/
    """Expands standalone Dives Akuru independent vowels into y-based sequences and switches to the alternate ya glyph (e.g. 𑤁→𑤥𑤰)."""
    Strng = Strng.replace("\U00011925", "\U00011926")

    # replace ind. vow with /y/

    vow = "𑤀 𑤁 𑤂 𑤃 𑤄 𑤅 𑤆 𑤆𑤵 𑤉".split(" ")
    vowy = "𑤥 𑤥𑤰 𑤥𑤱 𑤥𑤲 𑤥𑤳 𑤥𑤴 𑤥𑤵 𑤥𑤷 𑤥𑤸".split(" ")

    for v, vy in zip(vow, vowy):
        Strng = Strng.replace(v, vy)

    return Strng

# frontend
def DivesAkuruHomoOrganNasal(Strng):
    """Uses the homorganic nasal sign in place of virama+nasal before a matching consonant, e.g. 𑤐𑤾𑤎 → 𑤿𑤎."""
    homoNasal = '\U0001193F'

    Strng = re.sub('(𑤐\U0001193E)(?=[𑤌𑤍𑤎𑤏])', homoNasal, Strng)
    Strng = re.sub('(𑤕\U0001193E)(?=[𑤑𑤒𑤓])', homoNasal, Strng)
    Strng = re.sub('(𑤚\U0001193E)(?=[𑤖𑤘𑤙])', homoNasal, Strng)
    Strng = re.sub('(𑤟\U0001193E)(?=[𑤛𑤜𑤝𑤞])', homoNasal, Strng)
    Strng = re.sub('(𑤤\U0001193E)(?=[𑤠𑤡𑤢𑤣])', homoNasal, Strng)


    return Strng

# frontend
def UseAlternateYA(Strng):
    """Uses the alternate Dives Akuru ya glyph in place of the standard one, 𑤥 → 𑤦."""
    Strng = Strng.replace("\U00011925", "\U00011926")

    return Strng
