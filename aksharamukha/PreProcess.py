# -*- coding: utf-8 -*-

from . import GeneralMap as GM
from . import ScriptRegistry as SR
import re
import string
import unicodedata
import functools
from . import PostProcess
from . import ConvertFix as CF
from aksharamukha.ScriptMap.EastIndic import PhagsPa, Burmese, Khmer
from aksharamukha.ScriptMap.MainIndic import Tamil, Malayalam, Limbu, Chakma
### Use escape char in all functions

def ItransLL(Strng):
    return Strng

def RomanLoCChandrabindu(Strng):
    Strng = re.sub('n̐', 'm̐', Strng)

    return Strng

def BalineseRomanLoCFix(Strng):
    Strng = Strng.replace('‘', 'ng̈')

    return Strng

def JavaneseRomanLoCFix(Strng):
    Strng = Strng.replace('‘', 'ng̈')

    return Strng

# RomanLoCDevanagari's own logic now lives in ScriptProcessing/RomanLoCDevanagari.py -
# consolidated there (batch migration).
from .ScriptProcessing.RomanLoCDevanagari import HindiMarathiRomanLoCFix_pre as HindiMarathiRomanLoCFix

def RomanLoCLaUnderscoreDoubleDot(Strng):
    Strng = Strng.replace('ḻ', 'l̤')

# reverse these in preprocess
def RomanLoCVaWa(Strng):
    Strng = Strng.replace('w', 'v')
    return Strng

def RomanLoCSasha(Strng):
    Strng = Strng.replace('sh', 'ṣ')

    return Strng

# IAST's own logic now lives in ScriptProcessing/IAST.py -
# consolidated there (batch migration).
from .ScriptProcessing.IAST import RomanLoCSLaDotLaUnderscore_pre as RomanLoCSLaDotLaUnderscore, joinVowelConsIAST

def RomanLoCLaUnderscoreDoubleDot(Strng):
    Strng = Strng.replace('l̤', 'ḻ')

    return Strng

def MalayalamRomanLoCFix(Strng):
    Strng = Strng.replace('ṯṯ', 'ṟṟ')
    Strng = Strng.replace('ȧ', 'ŭ')
    return Strng

def DevanagariRomanLoCFix(Strng):
    Strng = Strng.replace('g̳h̳', 'gḧ').replace('t̤', 'ṭ̈').replace('s̤', 's̈')\
        .replace('h̤', 'ḧ')

    return Strng

def IASTLDotRetroflex(Strng):
    Strng = Strng.replace('ḷ', 'l̤')

    return Strng

def ArchaicJnaSimplifyRomanLOC(Strng):
    Strng = Strng.replace('ꦘ', 'ꦚ')
    return Strng

def KhandaTaRomanLoC(Strng):
    Strng = Strng.replace('ৎ', 'ṯ')

    return Strng

def TibetanLoCRomanLoCFix(Strng):
    Strng = re.sub('t(?![ʹhs])', 'tʹ', Strng)
    Strng = re.sub('n(?![ʹy])', 'nʹ', Strng)

    return Strng

def BalineseJavaneseMoveRepha(Strng, tgt, reph):
    repha = '(' + reph + ')'

    cons = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, tgt)) + ')'
    vows = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSignsNV, tgt)) + ')'
    vir = GM.CrunchSymbols(GM.virama, tgt)[0]

    candAnu = '[' + ''.join(GM.CrunchSymbols(GM.CombiningSigns, tgt)[:2]) + ']'
    Strng = re.sub('(' + candAnu + ')' + repha, r'\2\1', Strng)

    Strng = re.sub('('+cons+')'+'('+ vir + cons +')*'+'(' + vows + ')?'+ repha, r'\7\1\3\5', Strng)

    return Strng

# DivesAkuru's own logic now lives in ScriptProcessing/DivesAkuru.py -
# consolidated there (batch migration).
from .ScriptProcessing.DivesAkuru import DivesAkuruAlternateIndVowels_pre as DivesAkuruAlternateIndVowels

# Kawi's own logic now lives in ScriptProcessing/Kawi.py -
# consolidated there (batch migration).
from .ScriptProcessing.Kawi import KawiMoveRepha_pre as KawiMoveRepha

# Javanese's own logic now lives in ScriptProcessing/Javanese.py -
# consolidated there (batch migration).
from .ScriptProcessing.Javanese import JavaneseMoveRepha_pre as JavaneseMoveRepha

# Balinese's own logic now lives in ScriptProcessing/Balinese.py -
# consolidated there (batch migration).
from .ScriptProcessing.Balinese import BalineseMoveRepha_pre as BalineseMoveRepha

# Oriya's own logic now lives in ScriptProcessing/Oriya.py -
# consolidated there (batch migration). Re-exported here so Options.py's PreProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Oriya import OriyaSubojinedVa, OriyaTargetVa

# Bengali's own logic now lives in ScriptProcessing/Bengali.py -
# consolidated there (batch migration). Re-exported here so Options.py's PreProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Bengali import BengaliSubojinedVa, BengaliTargetVa

def RetainDevangariDanda(Strng):
    Strng = Strng.replace('।', '│').replace('॥', '┃')
    return Strng

def RetainPipeDanda(Strng, src):
    Strng = Strng.replace("।", "|").replace("॥", "||")
    Strng = Strng.replace(".", "●")
    Strng = Strng.replace("||", "┃").replace("|", "│")

    return Strng

#ThamLoC
def ThamLoCRomanLoCTarget(Strng):
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'ThamLoC'))

    #Fix o
    Strng = Strng.replace('ᩮᩣ', 'ᩰ')

    #eo
    Strng = re.sub('ᩴ᩠ᨿ', '\u1A74\u1A7Fᨿ', Strng)

    #aiy
    Strng = re.sub('ᩱ᩠ᨿ', 'ᩱ\u1A7Fᨿ', Strng)

    #koi
    Strng = re.sub('᩠ᩅᩭ', '\u1A7Fᩅᩭ', Strng)

    #au
    Strng = re.sub('\u1A60\u1A45\u1A6B', '\u1A7F\u1A45\u1A6B', Strng)

    #close e/au
    Strng = re.sub('(᩠)(ᨿ|ᩅ)(?=(' + ListC + '))', '\u1A7F'+r'\2', Strng)

    # replace lue-karan with ra-haam
    Strng = Strng.replace('᩼', '᩺')

    #Mark Vowel Killer
    Strng = Strng.replace('᩺', '᩺''ʻ')

    return Strng

def ThamLoCRomanLoCSource(Strng):
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'ThamLoCRomanLoC'))
    ListV ='|'.join(GM.CrunchSymbols(GM.Vowels,'ThamLoCRomanLoC'))

    #a
    Strng = re.sub('(a|ǫḥ|ǫ|œ|ò)(?=(' + ListC + '))', r'\1''\u02BD', Strng)

    Strng = Strng.replace('ʻ', 'a''᩺')

    return Strng

# Khmer's own logic now lives in ScriptProcessing/Khmer.py -
# consolidated there (batch migration). Re-exported here so Options.py's PreProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Khmer import KhmerWordSplit

def KhmerLoCRomanLoCTarget(Strng):
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'Khmer'))
    ListV ='|'.join(GM.CrunchSymbols(GM.VowelSigns,'Khmer'))
    ListA ='|'.join(GM.CrunchSymbols(GM.CombiningSigns,'Khmer'))

    vir = Khmer.ViramaMap[0]

    #Mark im
    Strng = Strng.replace('ឹ', 'ិំ\u02BD')

    #move bantoc around
    Strng = re.sub('(.)(.(\u17D2.)*)(\u17CB)', r'\1\4\2', Strng)

    #mark consonant modifiers with subbase form
    Strng = re.sub('([ងញមបយរវ])(ុ)([ិឹីឺ])', r'\1''៉'r'\3', Strng)
    Strng = re.sub('([សហអ])(ុ)([ិឹីឺ])', r'\1''៊'r'\3', Strng)

    #move tonemarks around
    Strng = re.sub('('+ListC+')'+'([៎៏])''('+ListV+')''('+ListA+')?',r'\1\3\4\2',Strng)
    Strng = re.sub('('+ListC+')'+'('+ListV+')''([៎៏៊៉])''('+ListA+')?',r'\1\2\4\3',Strng)

    #fix oya to oy
    Strng = Strng.replace('ឲ្យ', 'ឱ្យ').replace('ឱ្យ', 'ឱ្យ' + vir)

    #ignore the following
    Strng = re.sub('[៙៚]', '', Strng)

    return Strng

def KhmerLoCRomanLoCSource(Strng):
    listdenormalize = ['å', 'ẙ', 'à', 'á', 'é', 'í', 'ó', 'ú', 'à', 'è', 'ì', 'ò', 'ù', 'ă']

    for let in listdenormalize:
        Strng = Strng.replace(let, unicodedata.normalize('NFD', let))

    Strng = re.sub('‛(?!ʹ)', '‛ʹ', Strng)
    Strng = re.sub('oaḥ', 'oḥ', Strng)

    return Strng

# shan
def ShanLoCRomanLoCTarget(Strng):
    #preserve ႂ်
    Strng = Strng.replace('ႂ်', '\u036E')

    # Shan normalize /aa/
    Strng = Strng.replace('ၢ', 'ႃ')
    Strng = Strng.replace('ါ', 'ႃ')

    Strng = Strng.replace('ႃႆ', 'ၢႆ').replace('ႆၢ', 'ၢႆ').replace('ႆႃ', 'ၢႆ')

    # asat + virma to just virama
    Strng = Strng.replace('\u103A\u1039', '\u1039')

    ## sort subjoined consonants
    yrv = Burmese.ConsonantMap[25:27] + Burmese.ConsonantMap[28:29]
    yrvsub = ['\u103B','\u103C','\u1082']
    vir = Burmese.ViramaMap[0]

    for x,y in zip(yrv,yrvsub):
        # Undo Replace subjoining forms: exp-virama + y/r/v/h <- subjoining y/r/v/h
        Strng = Strng.replace(y, vir + vir + x)

    # mark pure viramas
    aThat = r'်'
    Strng = re.sub('(?<!ႃ)'+aThat, aThat + 'ʻ', Strng)

    # mark a as glottalstop
    Strng = Strng.replace('ဢ','’ဢ')

    # changes for old shan
    Strng = Strng.replace('\u1039', '\u103A')

    # changes

    return Strng

# KhuenTham's own logic now lives in ScriptProcessing/KhuenTham.py -
# consolidated there (batch migration). Re-exported here so Options.py's PreProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.KhuenTham import KhuenRaHaamKaren

def ShanLoCRomanLoCSource(Strng):

    return Strng

def BurmeseRomanLoCSource(Strng):
    # adhoc chars
    chars_misc = {
        "e*": "၏",
        'n*': "၌",
        'r*': '၍',
        'l*': '၎'
    }

    for lat, bur in chars_misc.items():
        Strng = Strng.replace(lat, bur)

    Strng = Strng.replace('ṁ', 'ṃ')

    # reverse danda to comma and double danda to full stop
    Strng = Strng.replace(',', '၊').replace('.', '။')

    # restore visarga and fix incorrect diacritic character
    Strng = Strng.replace('˝', 'ʺ').replace('ʺ', 'ḥ')

    # restore visarga and fix incorrect diacritic character
    Strng = Strng.replace('´','ʹ').replace('ʹ', '˳')

    # replace modifier letter with quotation mark
    vowelSigns = '|'.join(GM.CrunchSymbols(GM.VowelSignsNV, 'IAST'))
    Strng = re.sub('(ʼ)(a|' + vowelSigns + ')', '’' + r'\2', Strng)

    # left quotation mark -> modifier letter comma
    consonants = '|'.join(GM.CrunchSymbols(GM.Consonants, 'IAST'))
    Strng = re.sub('(' + consonants + ')(‘)', r'\1' + 'ʻ', Strng)

    Strng = Strng.replace('o‘', 'oʻ')

    # reverse o' to au
    Strng = Strng.replace('oʻ', 'au')

    return Strng

def paliTham(Strng):

    return Strng

def segmentThamSyllabes(Strng):
    # segment text into syllables

    # https://github.com/ye-kyaw-thu/myWord/blob/main/syl_segment.py
    myConsonant = r"ᨠ-ᩌ"
    otherChar = r"ᩍ-ᩔ!-/:-@[-`{-~\s"
    ssSymbol = r'᩠'
    aThat = r'᩺'

    BreakPattern = re.compile(r"((?<!" + ssSymbol + r")["+ myConsonant + r"](?![" + aThat + ssSymbol + r"])" + r"|["  + otherChar + r"])", re.UNICODE)
    #Strng = Strng.replace("့်", "့်")
    Strng = BreakPattern.sub(' ' + r"\1", Strng)

    return Strng

# Burmese's own logic now lives in ScriptProcessing/Burmese.py -
# consolidated there (batch migration). Re-exported here so Options.py's PreProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Burmese import segmentBurmeseSyllables

# Shan's own logic now lives in ScriptProcessing/Shan.py -
# consolidated there (batch migration). Re-exported here so Options.py's PreProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Shan import segmentShanSyllables

def BurmeseRomanLoCTarget(Strng):
    # asat + virma to just virama
    Strng = Strng.replace('\u103A\u1039', '\u1039')

    # swap iu -> ui
    Strng = Strng.replace('\u102D\u102F', '\u102F\u102D')

    # mark Independent au -> o'
    Strng = Strng.replace('ဪ','ဩʻ')

    ## sort subjoined consonants
    yrvh = Burmese.ConsonantMap[25:27] + Burmese.ConsonantMap[28:29] + Burmese.ConsonantMap[32:33]
    yrvhsub = ['\u103B','\u103C','\u103D','\u103E']
    vir = Burmese.ViramaMap[0]

    for x,y in zip(yrvh,yrvhsub):
        # Undo Replace subjoining forms: exp-virama + y/r/v/h <- subjoining y/r/v/h
        Strng = Strng.replace(y, vir + vir + x)

    # swap tone + virama to proper order
    Strng = Strng.replace("့်", "့်")

    # mark pure viramas
    aThat = r'်'
    Strng = Strng.replace(aThat, aThat + 'ʻ')

    # mark a as glottalstop
    Strng = Strng.replace('အ','’အ')

    # replace vowel + diac with vowels
    vowDep = 'အော် အော အိ အီ အု အူ အေ'.split(' ')
    vowIndep = 'ဪ ဩ ဣ ဤ ဥ ဦ ဧ'.split(' ')

    for x, y in zip(vowDep, vowIndep):
        Strng = Strng.replace(x, y)

    # danda to comma and double danda to full stop
    Strng = Strng.replace('၊', ',').replace('။', '.')

    #print(Strng)

    return Strng

def insertViramaSyriac(Strng):
    Strng += "\uF001"
    return Strng

def BengaliSwitchYaYYa(Strng):
    Strng = re.sub('(?<!\u09CD)য', '@#$', Strng)
    Strng = re.sub('য়', 'য', Strng)
    Strng = Strng.replace('@#$', 'য়')

    return Strng


def removeFinalSchwaArab(Strng):
    #print('here', Strng)
    diacrtics = ["\u0652", "\u064E", "\u0650", "\u064F"]
    Strng = re.sub('([\u0628-\u0647])(?![\u0652\u064E\u0650\u064F\u0651\u064B\u064C\u064D\u0649])(?=(\W|$))', r'\1' + '\u0652', Strng)
    Strng = re.sub('([\u0628-\u0647]\u0651)(?![\u0652\u064E\u0650\u064F\u064B\u064C\u064D\u0649])(?=(\W|$))', r'\1' + '\u0652', Strng)
    Strng = re.sub('(?<!\u0650)([\u064A])(?![\u0651\u0652\u064E\u0650\u064F\u064B\u064C\u064D\u0649])(?=(\W|$))', r'\1' + '\u0652', Strng)
    Strng = re.sub('(?<!\u0650)([\u064A]\u0651)(?![\u0652\u064E\u0650\u064F\u064B\u064C\u064D\u0649])(?=(\W|$))', r'\1' + '\u0652', Strng)
    Strng = re.sub('(?<!\u064F)([\u0648])(?![\u0651\u0652\u064E\u0650\u064F\u064B\u064C\u064D\u0649])(?=(\W|$))', r'\1' + '\u0652', Strng)
    Strng = re.sub('(?<!\u064F)([\u0648]\u0651)(?![\u0652\u064E\u0650\u064F\u064B\u064C\u064D\u0649])(?=(\W|$))', r'\1' + '\u0652', Strng)

    #print(Strng)
    #print('here2', Strng)

    return Strng

def AlephMaterLectionis(Strng, target='semitic'):
    Strng += "\u05CD"

    return Strng

# Indic Target
def FixSemiticRoman(Strng, Source):
    vir = '\u033D'

    if "\u05CD" in Strng:
        Strng = PostProcess.AlephMaterLectionis(Strng)

    if "\u05CC" in Strng:
        #print('before1', Strng)
        Strng = PostProcess.removeSemiticLetters(Strng)
        #print('after1', Strng)

        ## Fix Ayin -> Aleph approximation
        AyinAlephInitial = [('ʾa', 'ʾ'),('ʾā', 'ā̂'), ('ʾi', 'î'), ('ʾī', 'ī̂'), ('ʾu', 'û'), ('ʾū', 'ū̂'), ('ʾe', 'ê'), ('ʾē', 'ē̂'),\
                             ('ʾo', 'ô'), ('ʾō', 'ō̂')]

        for x, y in AyinAlephInitial:
            Strng = Strng.replace(x, y)

        ## Also make changes in PostOptionsLatn
        if Source == 'Arab':
            Strng = PostProcess.arabizeLatn(Strng, target="indic")
            #print('after2', Strng)
        elif Source == 'Arab-Ur' or Source == 'Arab-Pa' or Source == 'Arab-Fa':
            Strng = PostProcess.urduizeLatn(Strng, target="indic")
        elif Source == 'Syrn':
            Strng = PostProcess.syricizeLatn(Strng, target="indic")
        elif Source == 'Syrj' or Source == 'Hebr':
            Strng = PostProcess.hebraizeLatn(Strng, target="indic")

    # remove sin/shin dot
    Strng = Strng.replace('\u032A', '').replace('\u032E', '')

    # duplicate consonants
    ## move do chashmee ha + gemination sign
    ## tʰ꞉ -> t꞉ʰ
    Strng = re.sub('([ʰ])(꞉)', r'\2\1', Strng)

    Strng = re.sub('([aiuāīū])(꞉)', r'\2\1', Strng)
    Strng = re.sub('(.)(꞉)', r'\1' + vir + r'\1', Strng)

    # avoid fusion of Ayn
    Strng = Strng.replace("ʿ" + vir, "ʿ" + vir + "\u200B")

    cons_prev = '|'.join(GM.SemiticConsonants)

    if 'Syr' in Source: ## converting from Syriac through Latin
        consSyrc = "|".join(["ʾ", "b",  "v", "g", "ġ", "d", "ḏ", "h", "w", "z", "ḥ", "ṭ", "y", "k", "ḫ", "l", "m", "n", "s", "ʿ", "p", "f", "ṣ", "q", "r", "š", "t", "ṯ", "č", "ž", "j"])
        vowelSyrc = ["a", "ā", "e", "ē", "ū", "ō", "ī", "â", "ā̂", "ê", "ē̂"]

        vowelsDepSyrc = "|".join(["a", "ā", "e", "ē", "u", "i", "o"])
        vowelsInDepSyrc1 = ["i", "u", "o"]
        vowelsInDepSyrc2 = ["ī̂", "û", "ô"]

        if any([vow in Strng for vow in vowelSyrc]):
            #print(Strng)
            #print([(vow, vow in Strng) for vow in vowelSyrc])
            Strng = Strng.replace('ī', 'i').replace('ū', 'u').replace('ō', 'o')

            for vow1, vow2 in zip(vowelsInDepSyrc1, vowelsInDepSyrc2):
                Strng = re.sub('(?<!\w)' + vow1, vow2, Strng)

            Strng = Strng.replace('̂̂', '̂').replace('ô̂', 'ô') # [oi]^^ -> i^

            if "\uF001" in Strng:
                Strng = re.sub('(' + consSyrc + ')' + '(?!' + vowelsDepSyrc + ')', r'\1' + vir, Strng)

            # print(Strng)
            Strng = re.sub('(?<=' + cons_prev + ')' + 'a(?!\u0304)', '', Strng)

        Strng = Strng.replace("\uF001", "")

    ## Add scripts with vowels here
    if "Arab" in Source or Source == 'Latn' or Source == "Hebr" or Source == "Thaa" or Source == 'Type':
        basic_vowels = '(' + '|'.join(['a', 'ā', 'i', 'ī', 'u', 'ū', 'ē', 'ō', 'e', 'o', '#', vir]) + ')'
        Strng = re.sub('(ŵ)(?=' + basic_vowels + ')', "w", Strng)
        Strng = re.sub('(ŷ)(?=' + basic_vowels + ')', "y", Strng)

        Strng = re.sub('(?<=' + cons_prev + ')' + 'a(?!(ŵ|ŷ|\u0304|\u032E))', '', Strng)
        Strng = re.sub('(?<=ḧ)' + 'a(?!(ŵ|ŷ|\u0304|\u032E))', '', Strng)

        ## Hamza with vowels
        if 'Arab' in Source:
            simp_vow = 'a ā i ī u ū'.split(' ')
            init_vow = 'â ā̂ î ī̂ û ū̂'.split(' ')

            # Hamsa + vow -> indep vow
            for x, y in zip(simp_vow, init_vow):
                Strng = re.sub('ʔ' + x, y, Strng)

            # remove leftover hamza if nativizing
            if "\u05CC" in Strng:
                Strng = Strng.replace("ʔ", "")

    ## Semitic to Indic equivalents
    SemiticIndic=[('ṣ', 'sQ'), ('ʿ', 'ʾQ'), ('ṭ', 'tQ'), ('ḥ', 'hQ'), \
        ('ḍ', 'dQ'), ('p̣', 'pQ'), ('ž', 'šQ'), ('ẓ', 'jʰQ'), ('ḏ', 'dʰQ'), ('ṯ', 'tʰQ'),\
            ('w', 'vQ'), ('ḵ', 'k'), ('\u032A', ''), ('\u032E', ''),('a̮', "ā"),('\u0308', ""),\
                    ('ĕ\u0302', 'ê'), ('ă\u0302', 'â'), ('ŏ\u0302','ô'), ('ĕ', 'e'), ('ă', ''), ('ŏ','o'), ('ḵ', 'k'),\
                        ('ʾQā', 'ā̂Q'), ('ʾQi', 'îQ'), ('ʾQī', 'ī̂Q'), ('ʾQu', 'ûQ'), ('ʾQū', 'ū̂Q'), ('ʾQe', 'êQ'), ('ʾQē', 'ē̂Q'),\
                             ('ʾQo', 'ôQ'), ('ʾQō', 'ō̂Q'), ('ⁿ', 'n\u033D'), ('ʾā', 'ā̂')]

    for s, i in SemiticIndic:
        Strng = Strng.replace(s, i)

    if 'Arab' in Source:
        Strng = re.sub('(\u033D)([iuā])', r'\2', Strng)
        Strng = re.sub('(\u033D)([a])', '', Strng)

    ## Lone Aliph to Nukta
    Strng = Strng.replace('ʾ', 'â')

    return Strng

def perisanizeArab(Strng):
    arabKafYe = 'ك ي'.split(' ')
    persKafYe = 'ک ی'.split(' ')

    for x, y in zip(arabKafYe, persKafYe):
        Strng = Strng.replace(x, y)

    return Strng

def ArabizePersian(Strng):
    ## how to deal with ga
    arabKafYe = 'ك ي'.split(' ')
    persKafYe = 'ک ی'.split(' ')

    for x, y in zip(arabKafYe, persKafYe):
        Strng = Strng.replace(y, x)

    return Strng

def semiticizeUrdu(Strng):
    urduSpecific = 'ے ڈ ٹ ہ'.split(' ')
    semitic = 'ي د ت ه'.split(' ')

    for x, y in zip(urduSpecific, semitic):
        Strng = Strng.replace(x, y)

    ## remove Do chashme he
    Strng = Strng.replace('ھ', '')

    return Strng

def ShowChillus(Strng):

    return PostProcess.MalayalamChillu(Strng, True, True)

def ShowKhandaTa(Strng):
    Strng = Strng.replace('ৎ', 'ত্ˍ')

    return Strng

def eiaudipthongs(Strng):

    return Strng

def wasvnukta(Strng):

    return Strng

def default(Strng):

    return Strng

# Sogd's own logic now lives in ScriptProcessing/Sogd.py -
# consolidated there (batch migration).
from .ScriptProcessing.Sogd import SogdReshAyin_pre as SogdReshAyin

# Sogo's own logic now lives in ScriptProcessing/Sogo.py -
# consolidated there (batch migration).
from .ScriptProcessing.Sogo import SogoReshAyinDaleth_pre as SogoReshAyinDaleth

# Phlp's own logic now lives in ScriptProcessing/Phlp.py -
# consolidated there (batch migration). Re-exported here so Options.py's PreProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Phlp import PhlpMemQoph, PhlpWawAyinResh

# Phli's own logic now lives in ScriptProcessing/Phli.py -
# consolidated there (batch migration). Re-exported here so Options.py's PreProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Phli import PhliWawAyinResh

# Hatr's own logic now lives in ScriptProcessing/Hatr.py -
# consolidated there (batch migration). Re-exported here so Options.py's PreProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Hatr import HatrDalethResh

def MalayalamHalfu(Strng):
    consu = '[കചടതറനണരലവഴളറ]'
    vir = GM.CrunchSymbols(GM.VowelSigns, 'Malayalam')[0]
    consAll = "(" + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Malayalam')) + ")"

    Strng = re.sub('(?<=' + consu + ')' + '(' + vir + ')' + '(?!' +  consAll + ')', r'\2' + 'ു്', Strng)

    return Strng

def MalayalamTranscribe(Strng):
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

def retainLatin(Strng, reverse=False):
    latn_basic_lower = 'a b c d e f g h i j k l m n o p q r s t u v w x y z ḥ ṭ ṣ ʾ ʿ š ā ī ū ē ō'
    latn_basic_upper = latn_basic_lower.upper()
    latn_all = latn_basic_lower + latn_basic_upper
    latn_all = latn_all.split(' ')

    if not reverse:
        for i, c in enumerate(latn_all):
            Strng = Strng.replace(c, chr(60929+i))

        # for disambiguating preprocessed consonants
        Strng = Strng.replace('\uEA01', 'r').replace('\uEA02', 'ʿ').replace('\uEA03', 'm').replace('\uEA04', 'q').replace('\uEA05', 'w').replace('\uEA06', 'd')

    else:
        # print('I am trying to reverse Lating')
        for i, c in enumerate(latn_all):
            Strng = Strng.replace(chr(60929+i), c)

    return Strng

# --- JapanesePreProcess pipeline stages ---------------------------------
# Extracted verbatim, no logic changes. Real test coverage exists (the
# eiaudipthongs/wasvnukta preoptions each have 20 cases across both
# Hiragana and Katakana sources), verified the same way as everywhere
# else in this session: A/B comparison plus the full suite.

@functools.lru_cache(maxsize=None)
def _get_kakasi():
    # pykakasi.kakasi() was previously constructed fresh on every single
    # Hiragana/Katakana->other conversion - real, measurable per-call cost
    # for no benefit, since the converter itself holds no per-call state.
    import pykakasi
    return pykakasi.kakasi()

def _japanese_kakasi_romanize(txt):
    from . import Convert

    kks = _get_kakasi()

    txt = Convert.convertScript(txt.lower(), "ISO", "Devanagari")
    #print(txt)

    cv = kks.convert(txt)
    txt = ''

    for item in cv:
        txt = txt + ' ' + item['hepburn']

    return txt

def _japanese_normalize_romanization(txt, preoptions):
    if 'eiaudipthongs' in preoptions:
        txt = txt.replace('ou', 'o\u02BDu').replace('ei', 'e\u02BDi')

    txt = re.sub('(r)([aiueo])(\u309A\u309A)', 'l' + r'\2\2', txt)
    txt = re.sub('(r)([aāiīuūeēoō])(\u309A)', 'l' + r'\2', txt)

    txt = re.sub('(k)([aiueo])(\u309A\u309A)', 'ṅ' + r'\2\2', txt)
    txt = re.sub('(k)([aāiīuūeēoō])(\u309A)', 'ṅ' + r'\2', txt)

    txt = txt.replace('aa', 'ā').replace('ii', 'ī').replace('ee', 'ē').replace('oo', 'ō').replace('uu','ū')
    txt = txt.replace('a-', 'ā').replace('i-', 'ī').replace('e-', 'ē').replace('o-', 'ō').replace('u-','ū')
    txt = txt.replace("n'", 'n_').replace('ch', 'c').replace('sh', 'ṣ').replace('sṣ', 'ṣṣ').replace('ai', 'a_i').replace('au', 'a_u')
    txt = txt.replace('w', 'v')
    txt = txt.replace('ou', 'ō').replace('ei', 'ē')
    txt = txt.replace('、', ',').replace('。', '.')

    # Nasalization of n

    txt= txt.replace('ng', 'ṅg').replace('nk', 'ṅk').replace('nk', 'ṅk').replace('np', 'mp').replace('nb', 'mb').replace('nm', 'mm')

    if 'wasvnukta' in preoptions:
        txt = txt.replace('v', 'v̈')

    #print(txt)

    txt = txt.replace('、', ',').replace('。', '.')

    return txt

def JapanesePreProcess(src, txt, preoptions):
    if src == 'Hiragana' or src == 'Katakana':
        # preserve roman words
        txt = _japanese_kakasi_romanize(txt)
        txt = _japanese_normalize_romanization(txt, preoptions)

    return txt
# Hebrew's own logic now lives in ScriptProcessing/Hebrew.py -
# consolidated there (batch migration). Re-exported here so Options.py's PreProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Hebrew import holamlong, novowelshebrewIndic, novowelshebrewSemitic, shvanakhall

# ISO's own logic now lives in ScriptProcessing/ISO.py -
# consolidated there (batch migration). Re-exported here so Options.py's PreProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.ISO import longEOISO, joinVowelConsISO

def SanskritLexicaizeHK(Strng):

    return Strng

# Thai's own logic now lives in ScriptProcessing/Thai.py -
# consolidated there (batch migration).
from .ScriptProcessing.Thai import ThaiOrthography, ThaiPhonetic, ThaiSajjhayaOrthography_pre as ThaiSajjhayaOrthography, ThaiSajjhayawithA_pre as ThaiSajjhayawithA

# LaoPali's own logic now lives in ScriptProcessing/LaoPali.py -
# consolidated there (batch migration).
from .ScriptProcessing.LaoPali import LaoTranscription_pre as LaoTranscription, LaoPhonetic_pre as LaoPhonetic, LaoSajhayaOrthography, LaoSajhayaOrthographywithA

# TamilSaurashtra's own logic now lives in ScriptProcessing/TamilSaurashtra.py -
# consolidated there (batch migration). Re-exported here so Options.py's PreProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.TamilSaurashtra import SaurastraHaaruColonTamil

# Chakma's own logic now lives in ScriptProcessing/Chakma.py -
# consolidated there (batch migration).
from .ScriptProcessing.Chakma import ChakmaPali_pre as ChakmaPali

# Takri's own logic now lives in ScriptProcessing/Takri.py -
# consolidated there (batch migration).
from .ScriptProcessing.Takri import TakriArchaicKha_pre as TakriArchaicKha

def UrduShortNotShown(Strng):
    Strng += "\u02BB\u02BB"

    return Strng

def AnuChandraEqDeva(Strng):

    return AnuChandraEq(Strng, 'Devanagari')

def AnuChandraEq(Strng, script):
    Chandrabindu = GM.CrunchList('AyogavahaMap', script)[0]
    Anusvara = GM.CrunchList('AyogavahaMap', script)[1]

    Strng = Strng.replace(Chandrabindu, Anusvara)

    return Strng

# Tamil's pre-options now live in ScriptProcessing/Tamil.py, consolidated
# there with its Fix logic and post-options too. Re-exported here so
# Options.py's getmembers(PreProcess, isfunction) discovery still finds them.
from .ScriptProcessing.Tamil import TamilNumeralSub, TamilTranscribeCommon, TamilTranscribe, TamilTranscribeDialect

def swapEe(Strng):
    Strng = Strng.replace('E', 'X@X@')
    Strng = Strng.replace('e', 'E')
    Strng = Strng.replace('X@X@','e')

    Strng = Strng.replace('O', 'X@X@')
    Strng = Strng.replace('o', 'O')
    Strng = Strng.replace('X@X@','o')

    return Strng

# Itrans's own logic now lives in ScriptProcessing/Itrans.py -
# consolidated there (batch migration).
from .ScriptProcessing.Itrans import swapEeItrans_pre as swapEeItrans

# Grantha's own logic now lives in ScriptProcessing/Grantha.py -
# consolidated there (batch migration).
from .ScriptProcessing.Grantha import egrantamil

# Siddham's own logic now lives in ScriptProcessing/Siddham.py -
# consolidated there (batch migration).
from .ScriptProcessing.Siddham import siddhammukta

def TaiKuen(Strng):
    return Strng

def TaiThamLao(Strng):
    return Strng

# consider adding an optional NUkta to the post consonantal position
def RemoveSchwaHindi(Strng, showschwa=False):
    VowI = "(" + '|'.join(GM.CrunchSymbols(GM.Vowels,'Devanagari')) + ")"
    VowS = "(" + '|'.join(GM.CrunchSymbols(GM.VowelSignsNV, 'Devanagari')) + ")"
    Cons = "(" + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Devanagari')) + ")"
    Char = "(" + '|'.join(GM.CrunchSymbols(GM.Characters, 'Devanagari')) + ")"
    Nas = "([ंःँ]?)"
    ISyl = "((" + VowI + "|" + "(" + Cons + VowS + "?" + "))" + Nas +')'
    Syl = "((" + Cons + VowS + ')' + Nas + ")"
    SylAny = "((" + Cons + VowS + "?" + ')' + Nas + ")"

    if not showschwa:
        vir = '्'
        vir2 = '्'
    else:
        vir = '\u0954'
        vir2 = '\u0954'

    Strng = re.sub(ISyl+Cons+Cons+SylAny+"(?!" + Char + ")", r'\1\8' + vir + r'\9\10', Strng) # bhAratIya --> bhArtIy
    Strng = re.sub(ISyl+Cons+Syl+SylAny+"(?!" + Char + ")", r'\1\8' + vir + r'\9\15', Strng) # bhAratIya --> bhArtIy
    Strng = re.sub(ISyl+Cons+Syl+"(?!" + Char + ")", r'\1\8' + vir + r'\9', Strng) # namakIn -> namkIn

    Strng = re.sub(ISyl+Cons+"(?!" + Char + ")", r'\1\8' + vir, Strng) # kama -> kam

    Cons_sss = '((' + Cons + vir + ')' +'([शषस]))' # delete if double ends with s, sh, s
    Strng = re.sub(ISyl+Cons_sss+"(?!" + Char + ")", r'\1\8' + vir, Strng)

    ## remove from geminated consonants
    Target = 'Devanagari'

    ConUnAsp = [GM.CrunchList('ConsonantMap', Target)[x] for x in [0,2,5,7,10,12,15,17,20,22,4,9,14,19,24,25,26,27,28,29,30,31,32]]
    ConUnAsp = ConUnAsp + GM.CrunchList('SouthConsonantMap',Target) + GM.CrunchList('NuktaConsonantMap',Target)
    ConAsp   = [GM.CrunchList('ConsonantMap', Target)[x] for x in [1,3,6,8,11,13,16,18,21,23]]

    Strng = re.sub(ISyl + '('+'|'.join(ConUnAsp)+')'+'('+vir+')('+r'\8'+")(?!" + Char + ")", r'\1\8\9\10' + vir,Strng)

    for i in range(len(ConAsp)):
        Strng = re.sub(ISyl +'('+ConUnAsp[i]+')'+'('+vir+')'+'('+ConAsp[i]+')'+'(?!" + Char + ")', r'\1\8\9\10' + vir,Strng)

    #Strng = re.sub(VowI + Nas + Cons2+"(?!" + Char + ")", r'\1\2\3' + vir, Strng)

    cons_pyramid = ['[यरलव]', '[नमण]', '[शषस]', '[कखपफगघबभ]', '[टठतथडढदध]', '[चछजझज़]']
    for c1, cons1 in enumerate(cons_pyramid):
        for c2, cons2 in enumerate(cons_pyramid):
            if c1 < c2: # delete if ascending order
                Cons_pyr = '((' + cons1 + vir + ')' +'('+cons2+'))'
                Strng = re.sub(ISyl+Cons_pyr+"(?!" + Char + ")", r'\1\8' + vir, Strng)


    Strng = Strng.replace(vir, vir2)

    return Strng

# consider adding an optional NUkta to the post consonantal position
def RemoveFinal(Strng, Target):
    if Target == 'Bengali':
        Strng = PostProcess.KhandaTa(Strng, Target, True)

    VowI = "(" + '|'.join(GM.CrunchSymbols(GM.Vowels,Target)) + ")"
    VowS = "(" + '|'.join(GM.CrunchSymbols(GM.VowelSignsNV, Target)) + ")"
    Cons = "(" + '|'.join(GM.CrunchSymbols(GM.Consonants, Target)) + ")"
    Char = "(" + '|'.join(GM.CrunchSymbols(GM.Characters, Target)) + ")"
    Nas = "([" + '|'.join(GM.CrunchList('AyogavahaMap',Target)) + "]?)"

    ISyl = "((" + VowI + "|" + "(" + Cons + VowS + "?" + ")" + Nas + '))'
    Syl = "((" + Cons + VowS + ')' + Nas + ")"
    SylAny = "((" + Cons + VowS + "?" + ')' + Nas + ")"

    vir = GM.CrunchList("ViramaMap", Target)[0]
    if Target != 'Bengali':
        Cons2 = '((' + Cons + vir + ')?' + Cons + ')'
    else:
        Cons2 = '(()?' + Cons + ')'

    if Target == 'Khmer' or Target == 'KhmerLoC':
        ListC ='|'.join(GM.CrunchSymbols(sorted(GM.Consonants, key=len, reverse=True),Target))
        ra = Khmer.ConsonantMap[26]
        Strng = re.sub('('+ListC+')'+'\u17CC',ra+'\u17D2'+r'\1',Strng)

        Strng = re.sub(ISyl + '('+ListC +')' + '(((\u17D2)' + '('+ListC +'))*)([៍៎៏]?)(?=[\s\n])', r'\1\8\9' + vir + r'\13', Strng) # kama -> kam
        Strng = re.sub(ISyl + '('+ListC +')' + '(((\u17D2)' + '('+ListC +'))*)([៍៎៏]?)$', r'\1\8\9' + vir + r'\13', Strng) # kama -> kam
    else:
        Strng = re.sub(ISyl + Cons2+"(?!" + Char + ")", r'\1\8' + vir, Strng) # kama -> kam
        Strng = re.sub(ISyl + Cons2+"(?!" + Char + ")", r'\1\8' + vir, Strng) # kama -> kam

    #Strng = re.sub(VowI + Nas + Cons2+"(?!" + Char + ")", r'\1\2\3' + vir, Strng)

    return Strng

# Gurmukhi's own logic now lives in ScriptProcessing/Gurmukhi.py -
# consolidated there (batch migration). Re-exported here so Options.py's PreProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Gurmukhi import SchwaFinalGurmukhi

# Gujarati's own logic now lives in ScriptProcessing/Gujarati.py -
# consolidated there (batch migration). Re-exported here so Options.py's PreProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Gujarati import SchwaFinalGujarati

def SchwaFinalBengali(Strng):

    Strng = RemoveFinal(Strng, 'Bengali')

    return Strng

def SchwaFinalKhmerLoC(Strng):

    Strng = RemoveFinal(Strng, 'KhmerLoC')

    return Strng

def SchwaFinalKhmer(Strng):

    Strng = RemoveFinal(Strng, 'Khmer')

    return Strng

# WarangCiti's own logic now lives in ScriptProcessing/WarangCiti.py -
# consolidated there (batch migration). Re-exported here so Options.py's PreProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.WarangCiti import SchwaFinalWarangCiti

def siddhamUnicode(Strng):
    return Strng

# DevanagariLimbu's own logic now lives in ScriptProcessing/DevanagariLimbu.py -
# consolidated there (batch migration).
from .ScriptProcessing.DevanagariLimbu import LimbuDevanagariConvention_pre as LimbuDevanagariConvention

# Limbu's own logic now lives in ScriptProcessing/Limbu.py -
# consolidated there (batch migration).
from .ScriptProcessing.Limbu import LimbuSpellingSaI_pre as LimbuSpellingSaI


def removeChillus(Strng):
    Chillus=['\u0D7A','\u0D7B','\u0D7C','\u0D7D','\u0D7E']

    vir = Malayalam.ViramaMap[0]
    ConVir =[
             Malayalam.ConsonantMap[14]+vir,
             Malayalam.ConsonantMap[19]+vir,
             Malayalam.ConsonantMap[26]+vir,
             Malayalam.ConsonantMap[27]+vir,
             Malayalam.SouthConsonantMap[0]+vir,
            ]

    for x,y in zip(Chillus, ConVir):
        Strng = Strng.replace(x, y)

    return Strng

# Sinhala's own logic now lives in ScriptProcessing/Sinhala.py -
# consolidated there (batch migration).
from .ScriptProcessing.Sinhala import SinhalaPali_pre as SinhalaPali

def IASTPali(Strng):
    Strng = Strng.replace('ḷ', 'l̤')

    return Strng

# RussianCyrillic's own logic now lives in ScriptProcessing/RussianCyrillic.py -
# consolidated there (batch migration).
from .ScriptProcessing.RussianCyrillic import CyrillicPali_pre as CyrillicPali

def MalayalamPrakrit(Strng):
    ## Reverse Gemination
    Strng = PostProcess.ReverseGeminationSign(Strng, 'Malayalam')
    Strng = Strng.replace("ഀ", "ം")

    return Strng

def GranthaPrakrit(Strng):
    ## Reverse Gemination
    Strng = PostProcess.ReverseGeminationSign(Strng, 'Grantha')

    Strng = Strng.replace("𑌀", "𑌂")

    return Strng

def RomanPreFix(Strng,Source):
    DepV = '\u1E7F'
    Asp = '\u02B0'

    Vir = GM.CrunchList("ViramaMap", Source)[0]
    Nuk = GM.CrunchList("NuktaMap", Source)[0]
    VowelA = GM.CrunchSymbols(['VowelMap'],Source)[0]

    ListV = '|'.join(GM.CrunchSymbols(GM.VowelSigns,Source))
    ListC = '|'.join(GM.CrunchSymbols(GM.Consonants,Source))

    Strng = re.sub('('+ListC+')'+'(?!'+ListV+'|'+VowelA+')',r'\1'+DepV+Vir,Strng)

    Strng = re.sub('('+ListC+'|'+Nuk+')'+'('+ListV+')',r'\1'+DepV+r'\2',Strng)
    #print Strng

    Strng = re.sub('(?<='+ListC+')'+'('+VowelA+')',r'',Strng)
    #print Strng

    #Fix Nukta त़् त़्अ त़्ा -->  त़् त़ त़ा
    Strng = Strng.replace(DepV+Vir+Nuk+VowelA,Nuk)
    Strng = re.sub(DepV+Vir+Nuk+'(?=['+DepV+'])',Nuk,Strng)
    Strng = Strng.replace(DepV+Vir+Nuk,Nuk+DepV+Vir)

    #print Strng

    return Strng

def joinVowelCons(Strng, script):
    consonantsAll = '(' + '|'.join(sorted(GM.CrunchSymbols(GM.Consonants, script), key = len, reverse=True)) + ')'
    vowelsAll = '(' + '|'.join(sorted(GM.CrunchSymbols(GM.Vowels, script), key = len, reverse=True)) + ')'

    Strng = re.sub(consonantsAll + ' ' + vowelsAll, r'\1\2', Strng)
    Strng = re.sub(consonantsAll + ' ' + consonantsAll, r'\1\2', Strng)

    return Strng

def PreProcess(Strng,Source,Target,postoptions,preoptions):
    if SR.get(Source).is_roman_diacritic or Source == 'Latn':
        Strng = Strng.lower()

    if SR.get(Source).is_pipe_script:
        if '|' in Strng:
            Strng = Strng.replace(".", "●")
            Strng = Strng.replace("।", "|").replace("॥", "||")
            Strng = Strng.replace("|", ".").replace("||", "..")
        if Source == "Itrans":
            Strng = re.sub("●([acCDN])", "."+r'\1', Strng)
        elif Source == "Velthuis":
            Strng = re.sub("●([rRlLmhtdnTDsyg])", "."+r'\1', Strng)
            Strng = re.sub("●●([lr])", "."+r'\1', Strng)

    if 'Arab' in Source:
        Strng = re.sub('([وي])(?=[\u064E\u0650\u064F\u0651\u064B\u064C\u064D])', '\u02DE' + r'\1', Strng)
        #Strng = re.sub('((\u064E|\u0650|\u0652|\u064F))(\u0651)', r'\2', Strng)

    if Source in ["Syrj", "Syrn"]:
        Strng = Strng.replace('\u0323', '\u0742')


    if Source == 'Itrans':
        sOm = 'OM'
        tOm = 'oM'

        punc =  '(' + '|'.join(["\u005C"+x for x in list(string.punctuation)]+ ['\s']
                    + [x.replace('.', '\.') for x in GM.CrunchSymbols(GM.Signs,Source)[1:3]]) + ')'

        Strng = re.sub(punc + sOm + punc, r'\1' + tOm + r'\2', Strng)
        Strng = re.sub('^' + sOm + punc, tOm + r'\1', Strng)
        Strng = re.sub(punc + sOm + '$', r'\1' + tOm, Strng)
        Strng = re.sub('^' + sOm + '$', tOm, Strng)

        punc = '(\s)'

        Strng = re.sub(punc + sOm + punc, r'\1' + tOm + r'\2', Strng)
        Strng = re.sub('^' + sOm + punc, tOm + r'\1', Strng)
        Strng = re.sub(punc + sOm + '$', r'\1' + tOm, Strng)
        Strng = re.sub('^' + sOm + '$', tOm, Strng)


        # kaRRi -> katri etc. not kaVoc.R
        Strng = re.sub('([aAiuUeoEO])([R]){2}([iI])', r'\1'+r'\2'+'_'+r'\2'+r'\3', Strng)
        Strng = re.sub('([aAiuUeoEO])([L]){2}([iI])', r'\1'+r'\2'+'_'+r'\2'+r'\3', Strng)

        AltForm = ['O', 'aa','ii','uu','RRi','RRI','LLi','LLI','N^','JN','chh','shh','x','GY','.n','.m','.h', 'AUM', 'E', 'J', 'c.o', 'c.e']
        NormForm = ['^o', 'A','I','U','R^i','R^I','L^i','L^I','~N','~n','Ch','Sh','kSh','j~n','M','M','','oM', '^e', 'z', 'A.c', 'e.c']

        for x,y in zip(AltForm,NormForm):
            Strng = Strng.replace(x,y)

        AltForms = [('ee', 'I'), ('dny', 'j~n'), ('oo', 'U'), ('kS', 'kSh'), ('w', 'v'), ('|', '.'), ('kShh', 'kSh')]

        for x,y in AltForms:
            Strng = Strng.replace(x,y)

        Strng = Strng.replace('OM', 'oM')


    if Source == 'BarahaNorth' or Source == 'BarahaSouth':
        # alternate representations

        alt_baraha = [('A', 'aa'), ('I', 'ee'), ('U', 'oo'), ('~loo', '~lU'), ('Roo', 'RU'), ('ou', 'au'), ('K', 'kh'), ('G','gh'), ('ch', 'c'), ('Ch', 'C'), ('J','jh'), ('P', 'ph'), ('B', 'bh'), ('w', 'v'), ('sh', 'S'), ('~h', '_h'), ('Y', 'yx'), ('^^', '{}'), ('^', '()'), ('tx', 'rx'), ('zh', 'Lx'), ('~e', '~a'), ('q', '\_'), ('#', "\\'"), ('$', '\\"')]

        for alt, norm in alt_baraha:
            Strng = Strng.replace(alt, norm)

        if Target == 'Tamil':
            Strng = Strng.replace('n', 'nx').replace('~nx', 'n')

    if 'IAST' in Source:
        Strng = Strng.replace("aï", "a_i")
        Strng = Strng.replace("aü", "a_u")
        Strng = Strng.replace('\u0303', 'ṃ')

    if "ISO" in Source:
        Strng = Strng.replace('a:i', 'a_i')
        Strng = Strng.replace('a:u', 'a_u')
        Strng = Strng.replace('\u0303', 'ṁ')
        ## People use the wrong convention sometimes
        Strng = Strng.replace('ṃ', 'ṁ')

    if Source == "Titus":
        Strng = Strng

    if Source == "ISO" or Source == "IAST" or Source == "Titus" or Source == "RussianCyrillic":
        Strng = CF.VedicSvarasNonDiacritic(Strng)

    if Source == "Latn" and 'Syr' in Target:
        Strng = Strng.replace('ḇ', 'v').replace('ḡ', 'ḡ').replace('ḵ', 'ḫ').replace('p̄', 'f')

    if ('↓' in Strng or '↑' in Strng) and SR.get(Target).is_indic :
        Strng = Strng.replace('↓', '॒')
        Strng = Strng.replace('↑↑', '᳚')
        Strng = Strng.replace('↑', '॑')

    if ('↓' in Strng or '↑' in Strng) and SR.get(Target).is_latin :
        Strng = Strng.replace('↓', '\\_')
        Strng = Strng.replace('↑↑', '\\"')
        Strng = Strng.replace('↑', '\\\'')

    if Source == "WarangCiti":
        Strng = Strng.replace('\u200D', '\u00D7')

    if Source == "Hebr-Ar":
        # accept variants with dotes
        dot_var = [('עׄ','ג'), ('תׄ','ת֒'), ('ת','ת̈'), ('ק','ק̈')]

        for char, char_var in dot_var:
            Strng = Strng.replace(char_var, char)

    ## Normalize Input Strings

    Strng = normalize(Strng,Source)

    ## Remove unsupported letters and replace with supported ones

    #Fix Udata + Avagraha combination
    # नमो॑ऽयम् --> namo̍​'yam
    if SR.get(Source).is_indic and SR.get(Target).is_transliteration:
        udatta = '\u0951'
        avagrahaSrc = GM.CrunchList('SignMap', Source)[0]
        avagrahaTgt = GM.CrunchList('SignMap', Target)[0]

        if avagrahaTgt == "'":
            Strng = Strng.replace(udatta + avagrahaSrc, udatta + '\u200B' + avagrahaSrc)

    return Strng

def ISO259Target(Strng):
    Strng = Strng.replace('א', 'ʾ').replace('׳', '’')

    return Strng

def ISO233Target(Strng):
    replacements = [('أ', 'ˈʾ'), ('ء', '¦'), ('إ', 'ˌʾ')]

    for x, y in replacements:
        Strng = Strng.replace(x, y)

    return Strng

def PersianDMGTarget(Strng):
    replacements = [('ا', 'ʾ')]

    for x, y in replacements:
        Strng = Strng.replace(x, y)

    return Strng

def ISO233Source(Strng):
    replacements = [('أ', 'ˈʾ'), ('ء', '¦'), ('إ', 'ˌʾ')]

    for x, y in replacements:
        Strng = Strng.replace(y, x)

    replacements = [('j', 'ǧ'), ('g', 'ǧ'), ('ḧ', 'ẗ'), ('ḫ', 'ẖ'), ('a̮', 'ỳ'), \
        ('aⁿ', 'á'), ('iⁿ', 'í'), ('uⁿ', 'ú'), ('ā̂', 'ʾâ'), ('ˀ', 'ˈ')]

    for x, y in replacements:
        Strng = Strng.replace(y, x)

    return Strng

def HebrewSBLTarget(Strng):
    Strng = Strng.replace('א', 'ʾ').replace('׳', '’')

    return Strng

def HebrewSBLSource(Strng):
    Strng = Strng.replace('ʾ', 'א',).replace('’', '׳')
    Strng = Strng.replace('\u0307\u00B0', '\u00B0\u0307')

    replacements = [('v', 'ḇ'), ('f', 'p̄'), ('d꞉', 'd'), ('d', 'ḏ'), \
        ('g꞉', 'g'), ('g', 'ḡ'), \
            ('t꞉', 't'), ('t', 'ṯ'),
         ('š̮', 'š'), ('š̪', 'ś'),
        ('o', 'ō'), ('ō', 'ô'), ('ū', 'û'), ('\u033D', 'ĕ')
    ]

    for x, y in replacements:
        Strng = Strng.replace(y, x)

    return Strng

def ISO259Source(Strng):
    Strng = Strng.replace('ʾ', 'א',).replace('’', '׳')
    Strng = Strng.replace('\u0307\u00B0', '\u00B0\u0307')

    replacements = [('ḵ', 'k'), ('v', 'b'), ('f', 'p'), ('b', 'ḃ'), ('p', 'ṗ'), ('k', 'k̇'), ('꞉', '\u0307'),\
        ('š̮', 'š'), ('š', 's̀'), ('š̪', 'ś'),
        ('ā', 'å'), ('e', 'ȩ'), ('ō', 'ŵ'), ('ū', 'ẇ'), ('\u033D', '°'), ('ĕ', 'ḝ')
    ]

    for x, y in replacements:
        Strng = Strng.replace(y, x)

    Strng = unicodedata.normalize('NFD', Strng)
    Strng = Strng.replace('\u0307', '꞉')
    Strng = unicodedata.normalize('NFC', Strng)

    return Strng

def UnSupThaana(Strng):

    return Strng

def RemoveJoiners(Strng):
    Strng = Strng.replace("\u200D", "")
    Strng = Strng.replace("\u200C", "")

    return Strng

# Arab's own logic now lives in ScriptProcessing/Arab.py -
# consolidated there (batch migration). Re-exported here so Options.py's PreProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Arab import ArabicGimelJa

# Normalize Input
# ka + <nukta> -> qa etc
def normalize(Strng,Source):

    # Replace Decomposed Nukta Characters by pre-composed Nukta consonants

    #nuktaDecom = [u"क़",u"ख़",u"ग़",u"ज़",u"ड़",u"ढ़",u"फ़",u"य़",u"ਲ਼",u"ਸ਼",u"ਖ਼",u"ਗ਼",u"ਜ਼",u"ਫ਼",u"ড়",u"ঢ়",u"য়",u"ଡ଼",u"ଢ଼"]
    #nuktaPrecom = [u"क़",u"ख़",u"ग़",u"ज़",u"ड़",u"ढ़",u"फ़",u"य़",u"ਲ਼",u"ਸ਼",u"ਖ਼",u"ਗ਼",u"ਜ਼",u"ਫ਼",u"ড়",u"ঢ়",u"য়",u"ଡ଼",u"ଢ଼"]

    nuktaDecom = ["\u0915\u093C","\u0916\u093C","\u0917\u093C","\u091C\u093C","\u0921\u093C","\u0922\u093C","\u092B\u093C","\u092F\u093C","\u0A32\u0A3C","\u0A38\u0A3C","\u0A16\u0A3C","\u0A17\u0A3C","\u0A1C\u0A3C","\u0A2B\u0A3C","\u09A1\u09BC","\u09A2\u09BC","\u09AF\u09BC","\u0B21\u0B3C","\u0B22\u0B3C"]
    nuktaPrecom = ["\u0958","\u0959","\u095A","\u095B","\u095C","\u095D","\u095E","\u095F","\u0A33","\u0A36","\u0A59","\u0A5A","\u0A5B","\u0A5E","\u09DC","\u09DD","\u09DF","\u0B5C","\u0B5D"]

    if Source not in ["Grantha","TamilGrantha"]:
        for x,y in zip(nuktaDecom,nuktaPrecom):
            Strng = Strng.replace(x,y)

    if Source in ['IAST', 'ISO', 'ISOPali', 'Titus', 'IASTPali']:
        Strng = Strng.replace("ü", "uʼ").replace("ǖ", "ūʼ").replace( 'ö', 'aʼ',).replace('ȫ', 'āʼ')

    if Source in ['IAST', 'ISO', 'ISOPali', 'IASTPali', 'Titus'] or 'RomanLoC' in Source:
        Strng = unicodedata.normalize('NFC', Strng)
        Strng = Strng.replace("ẗ", "ẗ").replace("ÿ", "ÿ").replace("ḧ", "ḧ")

        if 'RomanLoC' in Source:
            Strng = Strng.replace('\u02D9', '\u02DA')

    if Source == 'Arab-Ur' or Source == 'Arab-Pa':
        Strng = Strng.replace('ك', 'ک')
        Strng = Strng.replace('ي', 'ی')

    if Source == "Hebr":
        vowels = ['ְ','ֱ','ֲ','ֳ','ִ','ֵ','ֶ','ַ','ָ','ֹ','ֺ','ֻ','ׇ']
        vowelsR = '(' + '|'.join(vowels + ['וֹ', 'וּ']) + ')'

        # Swap the order of diacritics
        Strng = re.sub(vowelsR + '([ּׁׂ])', r'\2\1', Strng)
        Strng = Strng.replace('\u05BC\u05B0\u05C1', '\u05C1\u05BC\u05B0')

    # Sindhi C+Anudatta <- Sindhi Underscore characters
    # For easy Transliteration

    # Malayalam Chillu Characters

    chilluZwj=["ണ്‍","ന്‍","ര്‍","ല്‍","ള്‍","ക്‍"]
    chilluAtom=["ൺ","ൻ","ർ","ൽ","ൾ","ൿ"]

    for x,y in zip(chilluZwj,chilluAtom):
        Strng = Strng.replace(x,y)

    Strng = Strng.replace('ൌ', 'ൗ')
    Strng = Strng.replace('ൟ', 'ഈ')
    Strng = Strng.replace('ൎ', 'ര്')

    # Malayalam chill + virama to just letter + virama

    Strng = Strng.replace('ൻ്റ', 'ന്റ')

    # Telugu/Kananda Nakaarapollu

    Strng = Strng.replace('ೝ', 'ನ್') # Kannada
    Strng = Strng.replace('ౝ', 'న్') # Telugu

    # Bengali Khanda Ta

    # Strng = Strng.replace("ৎ","ত্‍")

    # Tamil

    tamAlt = ["ஸ்ரீ","க்‌ஷ","ர‌ி","ர‌ீ"]
    tamNorm = ["ஶ்ரீ","க்ஷ","ரி","ரீ"]

    # Burmese

    Strng = Strng.replace("ဿ", "သ္သ")

    # Tamil

    Strng.replace("ஸ²", "ஶ")

    ## The following is a reversal of custom options check !!!!

    subNum = ["¹","₁","₂","₃","₄"]
    supNum = ["","","²","³","⁴"]

    for x,y in zip(tamAlt+subNum,tamNorm+supNum):
        Strng = Strng.replace(x,y)

    # Tibetan Vowels

    oldVow = ["ྲྀ","ཷ","ླྀ","ཹ","ཱི","ཱུ","ཀྵ","ྐྵ"]
    newVow= ["ྲྀ","ྲཱྀ","ླྀ","ླཱྀ","ཱི","ཱུ","ཀྵ","ྐྵ"]

    for x,y in zip(oldVow,newVow):
        Strng = Strng.replace(x,y)

    # Decomposed to Precomposed Roman Characters

    latinDecom= ["ā","ī","ū","ē","ō","ṃ","ṁ","ḥ","ś","ṣ","ṇ","ṛ","ṝ","ḷ","ḹ","ḻ","ṉ","ṟ"]
    latinPrecom = ["ā","ī","ū","ē","ō","ṃ","ṁ","ḥ","ś","ṣ","ṇ","ṛ","ṝ","ḷ","ḹ","ḻ","ṉ","ṟ"]

    for x,y in zip(latinDecom,latinPrecom):
        Strng = Strng.replace(x,y)

    # Thai Decomposed AM to Precomposed AM

    Strng = Strng.replace("ํา","ำ")

    # For Lao

    Strng  = Strng.replace("ໍາ", 'ຳ')

    ## Two Single Danda to Double Danda

    Strng = Strng.replace("।।","॥")

    ## Decomposed Limbu to precomposed

    Strng = Strng.replace("ᤠ᤺ᤣ", "ᤠᤣ᤺")
    Strng = Strng.replace("᤺ᤣ", "ᤣ᤺")
    Strng = Strng.replace("ᤠᤣ", "ᤥ")

    ## Replace Thai ฎ

    Strng = Strng.replace("ฎ", "ฏ")

    ## Replace Grantha old au with new au

    Strng = Strng.replace('𑍌', '𑍗')

    ## Replace Tibetan Chandra with Nada to the normal one

    Strng = Strng.replace('\u0F82', '\u0F83')

    ## Replace Candra A iwht regualr AE

    Strng = Strng.replace('ॲ', 'ऍ')

    #Strng = Strng.replace('', "ຣ\uE00A")

    ## Normalization for Bengali, Tamil, Malayalam and Grantha

    # Bengali o/au

    Strng = Strng.replace('ো', 'ো')
    Strng = Strng.replace('াে', 'ো')

    Strng = Strng.replace('ৌ', 'ৌ')
    Strng = Strng.replace('ৗে', 'ৌ')

    # Tamil o, O, au

    Strng = Strng.replace('ொ', 'ொ')
    Strng = Strng.replace('ாெ', 'ொ')

    Strng = Strng.replace('ோ', 'ோ')
    Strng = Strng.replace('ாே', 'ோ')

    Strng = Strng.replace('ௌ', 'ௌ')
    Strng = Strng.replace('ௗெ', 'ௌ')

    # Malayalam

    Strng = Strng.replace('ൊ', 'ൊ')
    Strng = Strng.replace('ാെ', 'ൊ')

    Strng = Strng.replace('ോ', 'ോ')
    Strng = Strng.replace('ാേ', 'ോ')

    # Grantha

    Strng = Strng.replace('𑍋', '𑍋')
    Strng = Strng.replace('𑌾𑍇', '𑍋')

    return Strng

# Remove ZWJ/ZWNJ characters
def removeZW(Strng):
    Strng = Strng.replace("\u200C").replace("\u200D")

    return Strng

# PhagsPa's own logic now lives in ScriptProcessing/PhagsPa.py -
# consolidated there (batch migration). Re-exported here so Options.py's PreProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.PhagsPa import PhagsPaArrange

def IPAIndic(Strng):
    Strng = Strng.replace("ʊ","u")
    Strng = Strng.replace("ɛ","e")

    return
