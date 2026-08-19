# -*- coding: utf-8 -*-

# WarangCiti's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from .. import GeneralMap as GM

# ---- Fix (encode/decode conversion logic) ----

def _FixWarangCitiEncode(Strng):
    """Marks consonant clusters with ZWJ, removes/restores the inherent and AA vowel signs, and merges the Warang Citi nukta letter sequence into its ligature when encoding."""
    ListC = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, 'WarangCiti')) + ')'
    ListV = "(" + "|".join(GM.CrunchSymbols(GM.Vowels, 'WarangCiti') + ['\u200D']) + ')'

    Strng = re.sub(ListC + ListC, r'\1' + '\u200D' + r'\2', Strng)

    # Remove the inherent vowel
    Strng = re.sub(ListC + '(\U000118C1\U000118D9\u02BE)', r'\1' + '\u00BD', Strng)

    Strng = re.sub(ListC + '(\U000118C1)', r'\1', Strng)

    Strng = re.sub(ListV + '(\U000118C0)', r'\1' + '\u200D' + r'\2', Strng)

    Strng = Strng.replace('\u02BE', '')

    Strng = Strng.replace("𑣟\u02BF", "𑣙𑣗") # Remove Warang Citi Nukta

    # Brining back 'AA'

    Strng = Strng.replace('\u00BD', '\U000118C1')

    # remove Nukta

    Strng = Strng.replace("\u02BF", "")


    return Strng

def _FixWarangCitiDecode(Strng):
    """Lowercases the text, reinserts the inherent vowel after bare consonants, restores the nukta ligature and AA vowel sign, and reorders vowel signs when decoding Warang Citi."""
    ListC = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, 'WarangCiti')) + ')'
    ListV = "(" + "|".join(GM.CrunchSymbols(GM.Vowels, 'WarangCiti') + ['\u200D']) + ')'

    Strng = Strng.lower()
    ## Replace hb -> vQ
    Strng = Strng.replace("𑣙𑣗", "𑣟\u02BF") # Introduce Warang Citi Nukta
    Strng = Strng.replace('\u00D7', '\u200D')

    ## Reintroduce vowel AA
    Strng = re.sub(ListC + '(\U000118C1)', r'\1' + '\u00BD',Strng)
    Strng = re.sub('(\u02BF)' + '(\U000118C1)', r'\1' + '\U000118C1\u00BD',Strng)

    # Introduce the inhernt  Vowel
    Strng = re.sub(ListC + '(?!' + ListV + ')', r'\1' + '\U000118C1', Strng)

    ## Retain Aspirates
    Strng = re.sub('([\U000118D4\U000118D5\U000118CC\U000118CB\U000118CF\U000118CE\U000118D2\U000118D1\U000118D5\U000118D4\U000118D8\U000118D7\U000118DB])(\u200D)(𑣙)', r'\1' + '\u00D6' + r'\3', Strng)
    Strng = Strng.replace('\u200D', '')
    Strng = Strng.replace('\u00D6', '\u200D')

    ## Move vowel signs and nUkta viQ -> vQi
    Strng = re.sub('(𑣁)' + '(\u02BF)' + ListV , r'\2\3', Strng)

    ## Remove a if necessary
    Strng = Strng.replace('𑣁' + '\u02BB', '')

    Strng = Strng.replace('\U000118C1\u00BD', '\U000118C1\U000118D9\u02BE')

    return Strng

def FixWarangCiti(Strng, reverse=False):
    """Dispatches to the Warang Citi encode or decode fix routine depending on conversion direction."""
    return _FixWarangCitiDecode(Strng) if reverse else _FixWarangCitiEncode(Strng)

# ---- Pre-processing options ----

def SchwaFinalWarangCiti(Strng):
    """Deletes the word-final inherent vowel (schwa) in Warang Citi text (𑣜𑣁𑣖 → rām)."""
    Target = "WarangCiti"

    VowI = "(" + '|'.join(GM.CrunchSymbols(GM.Vowels,Target)) + ")"
    VowS = "(" + '|'.join(GM.CrunchSymbols(GM.VowelSignsNV, Target)) + ")"
    Cons = "(" + '|'.join(GM.CrunchSymbols(GM.Consonants, Target)) + ")"
    Char = "(" + '|'.join(GM.CrunchSymbols(GM.Characters, Target)) + ")"

    Nas = "([" + '|'.join(GM.CrunchList('AyogavahaMap',Target)) + "]?)"

    ISyl = "((" + VowI + "|" + "(" + Cons + VowS + "?" + ")" + Nas + '))'
    Syl = "((" + Cons + VowS + ')' + Nas + ")"
    SylAny = "((" + Cons + VowS + "?" + ')' + Nas + ")"

    vir = '\u02BB'
    Cons2 = '((' + Cons + vir + ')?' + Cons + ')'

    Strng = re.sub(ISyl+Cons2+"(?!" + Char + ")", r'\1\8' + vir, Strng) # kama -> kam

    return Strng

# ---- Post-processing options ----

def WarangCitiModernOrthogaphy(Strng):
    """Converts to modern Warang Citi orthography by removing aspirate-ligature joiners and replacing the obsolete letter 𑣝 with 𑣞."""
    Strng = re.sub('([\U000118D4\U000118D5\U000118CC\U000118CB\U000118CF\U000118CE\U000118D2\U000118D1\U000118D5\U000118D4\U000118D8\U000118D7\U000118DB])(\u200D)(𑣙)', r'\1', Strng)
    Strng = Strng.replace('𑣝', '𑣞')

    Strng = Strng.replace('\u200D', '')

    return Strng
