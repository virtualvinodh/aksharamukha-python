# -*- coding: utf-8 -*-

# Burmese's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.EastIndic import Burmese

# ---- Fix (encode/decode conversion logic) ----

def _FixBurmeseEncode(Strng):
    """Encodes Burmese script orthography: converts virama to subjoined forms, inserts kinzi/repha, forms tall-a, reorders medials, and applies script-specific ligatures."""
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'Burmese'))
    vir = Burmese.ViramaMap[0]

    AA = Burmese.VowelSignMap[0]
    E = Burmese.VowelSignMap[9]

    ## Check Rendering with Myanmar1 font buddho go gau

    yrvh = Burmese.ConsonantMap[25:27] + Burmese.ConsonantMap[28:29] + Burmese.ConsonantMap[32:33]
    yrvhsub = ['\u103B','\u103C','\u103D','\u103E']

    TallACons = '|'.join([Burmese.ConsonantMap[x] for x in [1,2,4,17,20,28]])

    Strng = re.sub('(?<!ာ)' + vir+'('+ListC+')','\u1039'+r'\1',Strng)

    # Introduce Kinzi: ga + NGA + sub-Virama -> ga + NGA + exp-Virama + sub-Virama
    Strng = re.sub('('+Burmese.ConsonantMap[4]+')'+'('+'\u1039'+')',r'\1'+vir+r'\2',Strng)

    # Introduce Repha
    Strng = re.sub('(ရ)'+'('+'\u1039'+')',r'\1'+vir+r'\2',Strng)

    # Introduce Tall A: ka + AA -> ka + Tall A
    Strng = re.sub('(?<!\u1039)('+TallACons+')'+'('+E+'?)'+AA,r'\1\2'+'\u102B',Strng)

    ## buddho --> Tall A
    Strng = re.sub('('+TallACons+')(\u1039)('+ListC +')'+'('+E+'?)'+AA,r'\1\2\3\4'+'\u102B',Strng)
    Strng = re.sub('('+TallACons+')(\u1039)('+ListC +')'+'(\u1039)('+ListC +')'+'('+E+'?)'+AA,r'\1\2\3\4\5\6'+'\u102B',Strng)

    Strng = re.sub('(?<=်္)' + '('+TallACons+')'+'('+E+'?)'+AA,r'\1\2'+'\u102B',Strng)

    # Remove Tall a Kinzi

    for x,y in zip(yrvh,yrvhsub):
        # Introduce subjoining forms: sub-virama + y/r/v/h -> subjoining y/r/v/h
        Strng = re.sub('(?<!်)\u1039'+x,y,Strng)

    Strng = re.sub('ျါ','ျာ', Strng)

    Strng = re.sub('(?<!ဂ)ြါ','ြာ', Strng)

    Strng = re.sub('ျေါ','ျော', Strng)

    Strng = re.sub('(?<!ဂ)ြေါ','ြော', Strng)


    Strng = Strng.replace("သ္သ", "ဿ")
    Strng = Strng.replace("ဉ္ဉ", "ည")

    Strng = Strng.replace("\u02F3", "့")
    Strng = Strng.replace("့်", "့်",)

    Strng = Strng.replace("ာ္", "ာ်")

    Strng = re.sub("(ရ်္င်္)" + "(" + ListC + ")", "ရ်္င္" + r'\2', Strng)

    Strng = Strng.replace("ါ္", "ါ်")

    Strng = Strng.replace("\u103A\u1039\u101A", "\u103B")
    Strng = Strng.replace('\u103C\u103A\u1039ဝ', "\u103Cွ")

    ## Maintain the order of the medials
    Strng = re.sub('(ှ)' + '([ျြွ])', r'\2\1', Strng)
    Strng = Strng.replace("\u103C\u103B", "\u103B\u103C")
    Strng = Strng.replace("\u103D\u103B", "\u103B\u103D")
    Strng = Strng.replace("ွ\u103C", "\u103Cွ")

    ## Introduce repha for ra and ga
    Strng = Strng.replace('ရျ', 'ရ်္ယ')
    Strng = Strng.replace('ငျ', 'င်္ယ')

    #Strng = Strng.replace("\u103A\u1039", "\u1039")

    return Strng

def _FixBurmeseDecode(Strng):
    """Reverses Burmese encoding fixes: expands subjoined consonants, kinzi, repha, tall-a, and medials back to explicit virama sequences."""
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'Burmese'))
    vir = Burmese.ViramaMap[0]

    AA = Burmese.VowelSignMap[0]
    E = Burmese.VowelSignMap[9]

    ## Check Rendering with Myanmar1 font buddho go gau

    yrvh = Burmese.ConsonantMap[25:27] + Burmese.ConsonantMap[28:29] + Burmese.ConsonantMap[32:33]
    yrvhsub = ['\u103B','\u103C','\u103D','\u103E']

    TallACons = '|'.join([Burmese.ConsonantMap[x] for x in [1,2,4,17,20,28]])

    ## Reverse the order of the medials
    Strng = re.sub('([ျြွ])' + '(ှ)', r'\2\1', Strng)
    Strng = Strng.replace("\u103B\u103C", "\u103C\u103B")
    Strng = Strng.replace("\u103B\u103D", "\u103D\u103B")
    Strng = Strng.replace("\u103Cွ", "ွ\u103C")

    Strng = Strng.replace("ဿ","သ္သ")
    Strng = Strng.replace("ည", "ဉ္ဉ")

    Strng = Strng.replace("့်", "့်")
    Strng = Strng.replace("့","\u02F3")

    # Replace sub Virama with explicit Virama
    Strng = Strng.replace('\u1039',vir)
    # Replace Tall AA with AA
    Strng = Strng.replace('\u102B',AA)
    # Replace Kinzi with NGA + Virama
    Strng = Strng.replace(Burmese.ConsonantMap[4]+vir+vir,Burmese.ConsonantMap[4]+vir)
    # Replace Repha
    Strng = Strng.replace('ရ'+vir+vir,'ရ'+vir)

    for x,y in zip(yrvh,yrvhsub):
        # Replace subjoining forms: exp-virama + y/r/v/h <- subjoining y/r/v/h
        Strng = Strng.replace(y,vir+x)

    return Strng

def FixBurmese(Strng, reverse=False):
    """Dispatches to the Burmese encode or decode fix routine depending on conversion direction."""
    return _FixBurmeseDecode(Strng) if reverse else _FixBurmeseEncode(Strng)

# ---- Pre-processing options ----

def segmentBurmeseSyllables(Strng):
    # segment text into syllables

    # https://github.com/ye-kyaw-thu/myWord/blob/main/syl_segment.py
    """Segments Burmese text into syllables by inserting spaces at syllable boundaries - လေထဲပျော် → လေ ထဲ ပျော်."""
    myConsonant = r"က-အ"
    otherChar = r"ဣဤဥဦဧဩဪဿ၌၍၏၀-၉၊။!-/:-@[-`{-~\s"
    ssSymbol = r'္'
    aThat = r'်'

    BreakPattern = re.compile(r"((?<!" + ssSymbol + r")["+ myConsonant + r"](?![" + aThat + ssSymbol + r"])" + r"|["  + otherChar + r"])", re.UNICODE)
    Strng = Strng.replace("့်", "့်")
    Strng = BreakPattern.sub(' ' + r"\1", Strng)

    return Strng
