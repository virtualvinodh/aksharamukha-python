# -*- coding: utf-8 -*-

# Chakma's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
#
# ChakmaPali independently defines the SAME option name in both
# PreProcess.py and PostProcess.py as two different functions - suffixed
# _pre/_post here, aliased back on re-export (see ScriptProcessing/
# DevanagariLimbu.py for the first script this pattern was used on).
#
# ChakmaGemination (a PostProcess.py private helper) had exactly 4
# callers total - ChakmaPali(post-side), ChakmaEnableAllConjuncts, and
# Chakma's own _FixChakmaEncode/_FixChakmaDecode - all four moved here
# in this same batch, so it was absorbed and de-qualified to a bare call
# rather than left behind pointlessly qualified.

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.MainIndic import Chakma

def _FixChakmaEncode(Strng):
    """Inserts the Chakma inherent vowel-A sign (Chakma's default vowel being AA), forms ai/ei ligatures, subjoins virama before y/r/l/n, and applies consonant gemination."""
    listC = '('+"|".join(sorted(GM.CrunchSymbols(GM.Consonants,"Chakma")+Chakma.VowelMap[:1],key=len,reverse=True))+')'
    listV = '('+"|".join(sorted(GM.CrunchSymbols(GM.VowelSigns,"Chakma")+Chakma.ViramaMap+['\U00011133'],key=len,reverse=True))+')'

    Strng = Strng.replace("\u02BD","")

    # Introduce vowel Sign A ; Chakma - Inharant vowel is AA
    Strng = re.sub("("+listC+")"+"(?!"+listV+")",r'\1''\u02BE',Strng)
    Strng = Strng.replace("\U00011127","")
    Strng = Strng.replace("\u02BE","\U00011127")

    Strng = Strng.replace('𑄣𑄳𑄦', '𑅄')
    Strng = Strng.replace('𑄣𑄴𑄦', '𑅄')

    ## Ai => kai
    Strng = re.sub("("+listC+")"+"(𑄃𑄨)", r'\1' + '\U0001112D', Strng)
    ## ei' => kei
    Strng = Strng.replace('\U0001112C𑄃𑄨ʼ', '\U00011146', )



    yrlvn = "("+"|".join(Chakma.ConsonantMap[19:20]+Chakma.ConsonantMap[26:29])+")"

    Strng = re.sub("\U00011134"+"(?="+yrlvn+")","\U00011133",Strng)

    Strng = ChakmaGemination(Strng)

    ###  O/Sub-va lookign similar; check

    return Strng

def _FixChakmaDecode(Strng):
    """Reverses Chakma inherent vowel-A insertion, ai/ei ligature formation, gemination, and y/r/l/n subjoining-virama rules back to their component forms."""
    listC = '('+"|".join(sorted(GM.CrunchSymbols(GM.Consonants,"Chakma")+Chakma.VowelMap[:1],key=len,reverse=True))+')'
    listV = '('+"|".join(sorted(GM.CrunchSymbols(GM.VowelSigns,"Chakma")+Chakma.ViramaMap+['\U00011133'],key=len,reverse=True))+')'

    Strng = Strng.replace("\u02BD","")

    Strng = ChakmaGemination(Strng, reverse = True)

    Strng = Strng.replace('𑅄', '𑄣𑄳𑄦')

    Strng = Strng.replace('\U00011133\U00011103', '\U00011145')
    Strng = Strng.replace('\U00011133\U00011104', '\U00011146')

    Strng = Strng.replace('\U0001112D', '𑄃𑄨')
    Strng = Strng.replace('\U00011146', '\U0001112C𑄃𑄨ʼ')

    Strng = Strng.replace("\U00011127","\u02BE")
    Strng = re.sub("("+listC+")"+"(?!"+listV+'|\u02BE'+")",r'\1''\U00011127',Strng)
    Strng = Strng.replace("\u02BE","")

    yrlvn = "("+"|".join(Chakma.ConsonantMap[19:20]+Chakma.ConsonantMap[26:29])+")"

    # Reverse above
    Strng = Strng.replace("\U00011133","\U00011134")

    # Reverse independetnet vowels to a-based vowels
    vowelDepA = ["𑄃𑄨", "𑄃𑄪", "𑄃𑄬"]
    vowelIndep = ["\U00011104", "\U00011105" , "\U00011106"]

    for x, y in zip(vowelDepA, vowelIndep):
        Strng = Strng.replace(y, x)

    ###  O/Sub-va lookign similar; check

    return Strng

def FixChakma(Strng, reverse=False):
    """Dispatches to the Chakma encode or decode fix routine depending on the reverse flag."""
    return _FixChakmaDecode(Strng) if reverse else _FixChakmaEncode(Strng)

def ChakmaPali_pre(Strng):
    """Pre-processes Chakma text for Pali conversion by normalizing Ya/vA consonant forms and inserting the inherent vowel-A sign where absent."""
    Strng = Strng.replace('\U00011147', '𑄤') # Replace Ya
    Strng = Strng.replace('𑄠', '𑄡') # Replace vA

    listC = '('+"|".join(sorted(GM.CrunchSymbols(GM.Consonants,"Chakma")+Chakma.VowelMap[:1],key=len,reverse=True))+')'
    listV = '('+"|".join(sorted(GM.CrunchSymbols(GM.VowelSigns,"Chakma")+Chakma.ViramaMap+['\U00011133'],key=len,reverse=True))+')'

    Strng = Strng.replace("\u02BD","")

    Strng = Strng.replace('\U00011102', '\U00011127')

    # Introduce vowel Sign A ; Chakma - Inharant vowel is AA
    Strng = re.sub("("+listC+")"+"(?!"+listV+")",r'\1''\u02BE',Strng)
    Strng = Strng.replace("\U00011127","")
    Strng = Strng.replace("\u02BE","\U00011127")

    return Strng

def ChakmaPali_post(Strng):
    """Post-processes Chakma Pali text: reverses gemination and Ya/vA substitutions, then maps vowel-A to visarga and subjoined consonants to explicit virama per Pali convention."""
    listC = '('+"|".join(sorted(GM.CrunchSymbols(GM.Consonants,"Chakma")+Chakma.VowelMap[:1],key=len,reverse=True))+')'
    listV = '('+"|".join(sorted(GM.CrunchSymbols(GM.VowelSigns,"Chakma")+Chakma.ViramaMap+['\U00011133'],key=len,reverse=True))+')'

    Strng = ChakmaGemination(Strng, reverse = True)

    Strng = Strng.replace('𑄤', '\U00011147') # Replace Ya
    Strng = Strng.replace('𑄡', '𑄠') # Replace vA

    ## reverse A introduction

    Strng = Strng.replace("\U00011127","\u02BE")
    Strng = re.sub("("+listC+")"+"(?!"+listV+'|\u02BE'+")",r'\1''\U00011127',Strng)
    Strng = Strng.replace("\u02BE","")

    ## Replace A with Visarga as per Pali

    Strng = Strng.replace('\U00011127', '\U00011102')

    ## Replace subjoining with Explicit Virama

    Strng = Strng.replace('\U00011133', '\U00011134')

    return Strng

def ChakmaEnableAllConjuncts(Strng):
    """Enables all conjuncts: 𑄇𑄴𑄈𑄧 𑄉𑄴𑄊𑄧 𑄚𑄴𑄖𑄧 → 𑄇𑄳𑄈𑄧 𑄉𑄳𑄊𑄧 𑄚𑄳𑄖𑄧."""
    listC = '('+"|".join(sorted(GM.CrunchSymbols(GM.Consonants,"Chakma")+Chakma.VowelMap[:1],key=len,reverse=True))+')'
    Strng = re.sub("\U00011134"+'('+listC+')',"\U00011133"+r'\1',Strng)

    Strng = ChakmaGemination(Strng)

    return Strng

def ChakmaVowelsIndependent(Strng):
    """Enables independent i, u, and e vowel letters: 𑄃𑄨 𑄃𑄪 𑄃𑄬 → 𑄄 𑄅 𑄆."""
    vowelDepA = ["𑄃𑄨", "𑄃𑄪", "𑄃𑄬"]
    vowelIndep = ["\U00011104", "\U00011105" , "\U00011106"]

    for x, y in zip(vowelDepA, vowelIndep):
        Strng = Strng.replace(x, y)

    return Strng

def ChakmaGemination(Strng, reverse = False):
    """Applies or reverses Chakma consonant gemination rules involving explicit and subjoining virama forms before vowel signs."""
    ListC = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, 'Chakma')) + ")"
    virs = "([\U00011134\U00011133])"
    virExp = "\U00011134"
    virDep = "\U00011133"
    ListV = '('+"|".join(sorted(GM.CrunchSymbols(GM.VowelSignsNV,"Chakma"), key=len, reverse = True)) + ")"

    if not reverse:
        Strng = re.sub(ListC + virs + r'\1' + ListV, r'\1' + virExp + r'\3' , Strng)

        Strng = re.sub(ListC + virExp + r'\1' + virDep + ListC, r'\1' + virExp + virDep + r'\2' , Strng)
        Strng = re.sub(ListC + virDep + r'\1' + virDep + ListC, r'\1' + virExp + virDep + r'\2' , Strng)

        Strng = re.sub(virDep + ListC + virExp + ListV, virExp + r'\1' + virExp + r'\2' , Strng)

        # Strng = re.sub(ListC + virExp + virExp, r'\1' + virExp + r'\1' + virExp, Strng)
    else:
        Strng = re.sub(ListC + virExp + ListV, r'\1' + virExp + r'\1' + r'\2', Strng)
        Strng = re.sub(ListC + virExp + virDep, r'\1' + virExp + r'\1' + virDep, Strng)


    return Strng
