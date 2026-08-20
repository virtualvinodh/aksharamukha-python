# -*- coding: utf-8 -*-

# Malayalam's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
#
# MalayalamPrakrit independently defines the SAME option name in both
# PreProcess.py and PostProcess.py as genuinely different functions -
# suffixed _pre/_post here (neither calls the other, so no cross-call
# rename needed, unlike some other collision pairs).
#
# MalayalamChillu/RetainDandasIndic/RetainIndicNumerals/
# ReverseGeminationSign/InsertGeminationSign all stay behind in
# PostProcess.py (genuinely shared/generic, or - for MalayalamChillu -
# also used by ShowChillus here) - calls to them stay/become qualified,
# each needing a local PostProcess import.

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.MainIndic import Malayalam

# ---- Fix (encode/decode conversion logic) ----

def _FixMalayalamEncode(Strng):
    """Converts chillu consonants to their Unicode chillu codepoints and retains Malayalam dandas and numerals when encoding into Malayalam."""
    from .. import PostProcess
    Strng = PostProcess.MalayalamChillu(Strng, False)

    Strng = PostProcess.RetainDandasIndic(Strng, 'Malayalam', True)
    Strng = PostProcess.RetainIndicNumerals(Strng, 'Malayalam', True)

    # fix n2ra
    #Strng = Strng.replace('ன்ற')

    Chillus=['\u0D7A','\u0D7B','\u0D7C','\u0D7D','\u0D7E', 'ഩ‍്']

    Anu = GM.CrunchSymbols(GM.CombiningSigns,'Malayalam')[1]


    return Strng

def _FixMalayalamDecode(Strng):
    """Expands chillu codepoints and archaic chillu letters back to consonant-plus-virama form and restores dandas/numerals when decoding out of Malayalam."""
    from .. import PostProcess
    Strng = PostProcess.MalayalamChillu(Strng, True)

    Strng = PostProcess.RetainIndicNumerals(Strng, 'Malayalam')
    Strng = PostProcess.RetainDandasIndic(Strng, 'Malayalam')

    #Fix Arachaic chillus
    chilluArch = ['\u0D54', '\u0D55', '\u0D56', '\u0D7F']
    chilluArchhVir = ['മ്', 'യ്', 'ഴ്', 'ക്']

    for ch, chvir in zip(chilluArch, chilluArchhVir):
        Strng = Strng.replace(ch, chvir)

    Chillus=['\u0D7A','\u0D7B','\u0D7C','\u0D7D','\u0D7E', 'ഩ‍്']

    Anu = GM.CrunchSymbols(GM.CombiningSigns,'Malayalam')[1]


    return Strng

def FixMalayalam(Strng, reverse=False):
    """Dispatches to the Malayalam encode or decode fix-up routine based on the reverse flag."""
    return _FixMalayalamDecode(Strng) if reverse else _FixMalayalamEncode(Strng)

# ---- Pre-processing options ----

def ShowChillus(Strng):
    """Displays chillu consonants with an explicit transliteration marker instead of collapsing them, e.g. ധർമൻ → /dharˍmanˍ/ not /dharman/."""
    from .. import PostProcess

    return PostProcess.MalayalamChillu(Strng, True, True)

def MalayalamHalfu(Strng):
    """Transcribes a word-final bare virama as the samvrutokara (extra-short u) sound, e.g. അവൻ അവന്‌ → avan avanŭ."""
    consu = '[കചടതറനണരലവഴളറ]'
    vir = GM.CrunchSymbols(GM.VowelSigns, 'Malayalam')[0]
    consAll = "(" + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Malayalam')) + ")"

    Strng = re.sub('(?<=' + consu + ')' + '(' + vir + ')' + '(?!' +  consAll + ')', r'\2' + 'ു്', Strng)

    return Strng

def MalayalamTranscribe(Strng):
    """Phonetically transcribes Malayalam script, applying intervocalic/nasal consonant voicing and other sandhi rules, e.g. കൊടുങ്കാട് → kŏḍuṅgāḍŭ."""
    Strng = MalayalamHalfu(Strng)

    script = "Malayalam"

    ListC = GM.CrunchList('ConsonantMap',script)
    ListSC = GM.CrunchList('SouthConsonantMap',script)
    vir = GM.CrunchSymbols(GM.VowelSigns, script)[0]

    ConUnVoiced = [ListC[x] for x in [0,5,10,15,20]]
    ConVoicedJ =  [ListC[x] for x in [2,7,12,17,22]]
    ConVoicedS =  [ListC[x] for x in [2,5,12,17,22]]

    ConNasalsAll = '|'.join([ListC[x] for x in [4, 9, 14, 19, 24]])
    conNasalCa = '|'.join([ListC[x] for x in [9]])
    ConNasalsGroup = [ConNasalsAll, conNasalCa, ConNasalsAll, ConNasalsAll, ConNasalsAll]

    ConMedials = '|'.join(ListC[25:28]+ListSC[0:2]+ListSC[3:4])
    Vowels = '|'.join(GM.CrunchSymbols(GM.Vowels+GM.VowelSignsNV, script))
    Aytham = GM.CrunchList('Aytham',script)[0]
    Consonants = '|'.join(GM.CrunchSymbols(GM.Consonants,script))

    NRA =ListSC[3] + vir + ListSC[2]
    NDRA = ListC[14] + vir + ListC[12] + vir + ListC[26]

    ### Check Siva Siva Mails
    ### Do something about Eyelash ra in Transliterated text

    for i in range(len(ConUnVoiced)):
        pass
        #Strng = re.sub('('+Vowels+Consonants+')'+ConUnVoiced[i]+'('+Vowels+Consonants+')',r'\1'+ConVoicedS[i]+r'\2',Strng)
        Strng = re.sub('('+Vowels+'|'+Consonants+'|'+Aytham+')'+ConUnVoiced[i]+'(?!'+vir+')',r'\1'+ConVoicedS[i],Strng)
        Strng = re.sub('('+ConVoicedS[i]+')'+ConUnVoiced[i]+'(?!'+vir+')',r'\1'+ConVoicedS[i],Strng)

        # Nasals + Unvoiced -> voiced
        # Rule applied even if spaced -> ulakaJ cuRRu -> ulakaJ juRRu; cenJu -> senju
        # Strng = re.sub('('+ConNasalsSpace+')'+'('+vir+')'+'( ?)'+ConUnVoiced[i],r'\1\2\3'+ConVoicedJ[i],Strng)

        # Only without space : vampu -> vambu;  varim panam -> varim panam
        Strng = re.sub('('+ConNasalsGroup[i]+')'+'('+vir+')'+ConUnVoiced[i],r'\1\2'+ConVoicedJ[i],Strng)

        # Medials + Unvoiced -> Voiced
        Strng = re.sub('('+ConMedials+')'+'('+vir+')'+ConUnVoiced[i]+'(?!'+vir+')',r'\1\2'+ConVoicedS[i],Strng)

    #RRA NRA

    Strng = Strng.replace('റ്റ', 'ട്ട').replace('ന്റ', 'ണ്ഡ')

    #anusvara with m
    Strng = Strng.replace('ം', 'മ്')

    return Strng

def MalayalamPrakrit_pre(Strng):
    """Reverses gemination marks and converts the Prakrit anusvara-above character to a regular anusvara before Prakrit-specific processing."""
    from .. import PostProcess
    ## Reverse Gemination
    Strng = PostProcess.ReverseGeminationSign(Strng, 'Malayalam')
    Strng = Strng.replace("ഀ", "ം")

    return Strng

# ---- Post-processing options ----

def tradOrtho(Strng):
    """Traditional Malayalam orthography option, currently a no-op passthrough, e.g. തു തൂ → തു തൂ."""
    return Strng

def dotReph(Strng):
    """Converts ra-virama before a consonant into the dot-reph character, e.g. ധർമ → ധൎമ."""
    ListC = '('+"|".join(sorted(GM.CrunchSymbols(GM.Consonants,"Malayalam"))) + ')'

    Strng = re.sub('(?<!്)' + 'ർ' + ListC,'ൎ' + r'\1', Strng)
    Strng = re.sub('(?<!്)' +'ര്' + ListC,'ൎ' + r'\1', Strng)

    return Strng

def archaicAIAU(Strng):
    """Uses archaic vowel forms for long ī and au, e.g. ഈ കൗ → ൟ കൌ."""
    Strng = Strng.replace('ൗ', 'ൌ')
    Strng = Strng.replace('ഈ', 'ൟ')

    return Strng

def MalayalamPrakrit_post(Strng):
    """Converts anusvara to the Prakrit anusvara-above character and inserts gemination marks after Prakrit-specific processing."""
    from .. import PostProcess
    ## Replace Anusvara with Anusvara above
    Strng = Strng.replace("ം", "ഀ")
    Strng = PostProcess.InsertGeminationSign(Strng, 'Malayalam')

    return Strng

def historicChillu(Strng):
    """Converts consonant-plus-virama sequences to historic/archaic chillu letters, e.g. ൿ ൔ ൕ ൖ."""
    chilluArch = ['\u0D54', '\u0D55', '\u0D56', '\u0D7F']
    chilluArchhVir = ['മ്', 'യ്', 'ഴ്', 'ക്']

    ListC = '(' + '|'.join(GM.CrunchSymbols(GM.CharactersNV,'Malayalam') + ['ഽ']) + ')'

    vir = Malayalam.ViramaMap[0]

    for ch, chvir in zip(chilluArch, chilluArchhVir):
        Strng = re.sub('(?<!' + vir + ')' + chvir + '(?!' + ListC + ')', ch, Strng)

    return Strng

def MalayalamLineVirama(Strng):
    #ListC = '(' + '|'.join(GM.CrunchSymbols(GM.CharactersNV,'Malayalam') + ['ഽ']) + ')'
    #Strng = re.sub('\u0D4D'+'(?!'+ListC +')', '\u0D3B', Strng)
    """Uses the line-form (vertical bar) virama instead of the standard virama, e.g. ക് → ക഻."""
    Strng = Strng.replace('\u0D4D', '\u0D3B')

    return Strng

def MalayalamCircVirama(Strng):
    """Uses the circle-form virama instead of the standard virama, e.g. ക് → ക഼."""
    Strng = Strng.replace('\u0D4D', '\u0D3C')

    return Strng

def RephaDoubleMalayalam(Strng):
    """Geminates the consonant following a reph/dot-reph, e.g. ധർമ → ധർമ്മ."""
    repha = '[ർൎ]'

    Target = 'Malayalam'

    vir = GM.CrunchSymbols(GM.VowelSigns,Target)[0]
    ConUnAsp = [GM.CrunchList('ConsonantMap', Target)[x] for x in [0,2,5,7,10,12,15,17,20,22,4,9,14,19,24,25,28,29,31]]
    ConUnAsp = ConUnAsp + ['ള']
    ConAsp   = [GM.CrunchList('ConsonantMap', Target)[x] for x in [1,3,6,8,11,13,16,18,21]]

    # don't replace after virma
    # arka -> arkka but arkya -> arkya
    Strng = re.sub('(' + repha + ')' + '('+'|'.join(ConUnAsp)+')' +'(?!' + vir +')', r'\1\2' + vir + r'\2', Strng)

    # ardha -> arddha but ardya -> ardya
    for i in range(len(ConAsp)):
        Strng = re.sub('(' + repha + ')' + '(' + ConAsp [i] +')' +'(?!' + vir +')', r'\1' +  ConUnAsp[i] + vir + r'\2', Strng)

    # Dot reph with ya

    # Strng = Strng.replace('ൎയ', 'ൎയ്യ')

    return Strng

def MalayalamAnusvaraNasal(Strng):
    """Converts anusvara to/from homorganic nasal consonants for Malayalam-specific consonant clusters, accounting for chillu letters."""
    ListCAll = '(' + '|'.join(GM.CrunchSymbols(GM.Characters, 'Malayalam')) + ')'

    ListNNasal = [Malayalam.ConsonantMap[x] for x in [4,9,14,19,24]]
    ListCNasal = [
             '|'.join(Malayalam.ConsonantMap[0:1]),
             '|'.join(Malayalam.ConsonantMap[5:8]),
             '|'.join(Malayalam.ConsonantMap[10:14]),
             '|'.join(Malayalam.ConsonantMap[15:19]),
             '|'.join(Malayalam.ConsonantMap[20:21]),
            ]

    ListNAnu = [Malayalam.ConsonantMap[x] for x in [4,24]]
    ListCAnu = [
             '|'.join(Malayalam.ConsonantMap[1:4]),
             '|'.join(Malayalam.ConsonantMap[21:24]),
            ]

    vir = Malayalam.ViramaMap[0]
    Anu = Malayalam.AyogavahaMap[1]

    Chillus=['\u0D7A','\u0D7B','\u0D7C','\u0D7D','\u0D7E', 'ഩ‍്']

    for i in range(len(ListNNasal)):
        Strng = re.sub('('+Anu+')'+'('+ListCNasal[i]+')',ListNNasal[i]+vir+r'\2',Strng)

    for i in range(len(ListNAnu)):
        Strng = re.sub(ListCAll + GM.VedicSvaras + '(?<!' + vir + ')'+'(?<![' + ".".join(Chillus) + '])(?<!' + vir +')' + '('+ListNAnu[i]+')'+'('+vir+')'+'('+ListCAnu[i]+')',r'\1\2'+Anu+r'\5',Strng)

    return Strng

def MalayalamChillu(Strng, reverse=False, preserve=False):

    """Forms Malayalam chillu (pure, vowelless) consonant letters from consonant+virama in appropriate contexts, or reverses chillus back to consonant+virama when reverse=True."""
    Chillus=['\u0D7A','\u0D7B','\u0D7C','\u0D7D','\u0D7E', 'ഩ‍്']

    ListC = '(' + '|'.join(GM.CrunchSymbols(GM.CharactersNV,'Malayalam') + ['ഽ']) + ')'

    vir = Malayalam.ViramaMap[0]
    ConVir =[
             Malayalam.ConsonantMap[14]+vir,
             Malayalam.ConsonantMap[19]+vir,
             Malayalam.ConsonantMap[26]+vir,
             Malayalam.ConsonantMap[27]+vir,
             Malayalam.SouthConsonantMap[0]+vir,
             'ഩ്'
            ]

    ## may be include ha ?
    CList = [
            Malayalam.ConsonantMap[10:15]+Malayalam.ConsonantMap[24:26]+Malayalam.ConsonantMap[28:29],
            Malayalam.ConsonantMap[15:20]+Malayalam.ConsonantMap[24:27]+Malayalam.ConsonantMap[28:29]+['റ'],
            Malayalam.ConsonantMap[25:27],
            Malayalam.ConsonantMap[20:21] + Malayalam.ConsonantMap[24:26] + Malayalam.ConsonantMap[27:29],
            Malayalam.SouthConsonantMap[0:1]+Malayalam.ConsonantMap[25:27],
            Malayalam.ConsonantMap[15:20]+Malayalam.ConsonantMap[24:27]+Malayalam.ConsonantMap[28:29]+['റ']
            ]

    if not reverse:
        for i in range(len(Chillus)):
            #print '(?<!'+'['+vir+''.join(Chillus)+']'+')'+'('+ConVir[i]+')'+'(?!['+''.join(CList[i])+'])'
            Strng = re.sub(ListC + GM.VedicSvaras + '('+ConVir[i]+')'+'(?!['+''.join(CList[i])+'])',r'\1\2' + Chillus[i],Strng)
            Strng = re.sub(ListC + GM.VedicSvaras + '('+ConVir[i]+')'+'(?=(['+''.join(CList[i])+'])' + vir + r'\4' + ')',r'\1\2' + Chillus[i],Strng)

        ## remove _ appearing due to the preserve chillu option
        Strng = re.sub('(?<!ത്)ˍ', '', Strng)

    else:
        if preserve:
            for x,y in zip(Chillus, ConVir):
                Strng = Strng.replace(x, y +'ˍ') ## Fix the reversal of characters of this
        else:
            for x,y in zip(Chillus, ConVir):
                Strng = Strng.replace(x, y) ## Fix the reversal of characters of this

    return Strng

def MalayalamNTA(Strng):
    """Converts the n+ra sequence into n+t-line (Malayalam nta orthographic convention)."""
    Strng = Strng.replace('nṟ', 'nṯ')
    return Strng

def MalayalamTTNTA(Strng):
    """Doubled ra (tta) & n+ra (nta) -> t-line doubled & n+t-line."""
    Strng = Strng.replace('ṟṟ', 'ṯṯ')
    Strng = Strng.replace('nṟ', 'nṯ')
    return Strng

def MalayalamremoveHistorical(Strng):
    """Replaces the historical Malayalam na letter with the modern na, and the virama-joined na-chillu sequence with the standalone chillu-n."""
    Strng = Strng.replace('\u0D29','\u0D28')
    Strng = Strng.replace('ന‍്', 'ൻ')

    return Strng

