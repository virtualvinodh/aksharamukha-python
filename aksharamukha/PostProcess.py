# -*- coding: utf-8 -*-

from . import GeneralMap as GM
from . import ScriptRegistry as SR
from . import ScriptMap
from aksharamukha.ScriptMap.Roman import Avestan
from aksharamukha.ScriptMap.MainIndic import Ahom, Tamil,Malayalam,Gurmukhi,Oriya,Saurashtra,Sinhala,Urdu,Devanagari, Chakma, Limbu, Takri, TamilExtended, Kannada
from aksharamukha.ScriptMap.EastIndic import Tibetan, Thai, PhagsPa, ZanabazarSquare, Burmese, KhamtiShan, Khmer, Balinese, Javanese
from . import ConvertFix as CF
import re
import functools

### Rewrite all ListC, ListV as sorted(List,key=len,reverse=True).
### Consider Adding Options to ignore Nukta etc for Gujarati bengali by default

## order the functions by script ##

## This is the processing that's done immediately after calling the convert() function
## But before the post-processing steps
## removes extranous/artificial diacritics introduced
def default(Strng, langage=""):
    Strng = Strng.replace("\uF001", "").replace("\u05CC", "").\
        replace("ʻʻ", "").replace('\u05CD', '').replace('\u02C2', '') ## remove token characters for specialized processing

    return Strng

## This is processing that's done after the post-processing steps
## It's catch all function for all misc stuff
def defaultPost(src, tgt, Strng, nativize, preoptions, postoptions):
    Strng = Strng.replace('\u034F', '') ## remove token characters for specialized processing

    ## Fix Dandas & Numerals
    if 'romanNumerals' in postoptions:
        Strng = RetainIndicNumerals(Strng,tgt,reverse=True)
    if 'indicNumerals' in postoptions:
        Strng = RetainIndicNumerals(Strng,tgt,reverse=False)
    if 'romanFullStop' in postoptions:
        Strng = RetainDandasIndic(Strng, tgt, reverse=True)

    #Devanagari Dandas
    if not SR.get(tgt).is_transliteration:
        Strng = Strng.replace( '│', '।',).replace('┃', '॥')
    else:
        Strng = Strng.replace( '│', '|',).replace('┃', '||')
    #Pipe scripts as source
    Strng = Strng.replace( "●", ".",)

    return Strng

## Ahom ##

## Arabic ##

## Assamese ##

## Avestan ##

# Khojki's own logic now lives in ScriptProcessing/Khojki.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Khojki import KhojkiRRI, KhojkiQa, KhojkiRetainSpace

# Ahom's own logic now lives in ScriptProcessing/Ahom.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Ahom import removePaliAhom, AhomClosed

# Sinhala's own logic now lives in ScriptProcessing/Sinhala.py -
# consolidated there (batch migration).
from .ScriptProcessing.Sinhala import SinhalaDefaultConjuncts, SinhalaPali_post as SinhalaPali, SinhalaConjuncts, SinhalaChandrbinduAnusvara

# RomanLoC's own logic now lives in ScriptProcessing/RomanLoC.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.RomanLoC import LoCMarc8

def AnusvaraAsN(Strng):
    Strng = Strng.replace('m\u034F', 'n')
    return Strng

#show Schwa
def ShowSchwaHindi(Strng):
    from . import PreProcess as PreP
    Strng = PreP.RemoveSchwaHindi(Strng, True)
    return Strng

# Kannada's own logic now lives in ScriptProcessing/Kannada.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Kannada import KannadaSpacingCandrabindu, KannadaNotRepha, KannadaNakaraPollu

# Telugu's own logic now lives in ScriptProcessing/Telugu.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Telugu import TeluguRemoveNukta, TeluguRemoveAeAo, TeluguNakaraPollu, TeluguTamilZha, TeluguTamilRra, TeluguReph, TeluguArasunnaChandrabindu

#testcase todo
def syriacVowelsBelow(Strng):

    return Strng

#testcase todo
def syriacWesternOToU(Strng):

    return Strng

#testcase todo
# Dogra's own logic now lives in ScriptProcessing/Dogra.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Dogra import olddogra, DograShaKha

#testcase todo
def ISO259Target(Strng):
    replacements = [('b', 'ḃ'), ('p', 'ṗ'), ('k', 'k̇'), ('ḵ', 'k'), ('v', 'b'), ('f', 'p'), ('꞉', '\u0307'),\
         ('š̪', 'ś'), ('š̮', 'š'), ('š', 's̀'),
        ('ā', 'å'), ('e', 'ȩ'), ('ō', 'ŵ'), ('ū', 'ẇ'), ('\u033D', '°'), ('ĕ', 'ḝ')
    ]

    for x, y in replacements:
        Strng = Strng.replace(x, y)

    Strng = Strng.replace('\u00B0\u0307', '\u0307\u00B0')

    return Strng

#testcase todo
def HebrewSBLTarget(Strng):
    replacements = [('v', 'ḇ'), ('f', 'p̄'), ('d', 'ḏ'), ('ḏ꞉', 'd'), \
        ('g', 'ḡ'), ('ḡ꞉', 'g'),\
            ('t', 'ṯ'), ('ṯ꞉', 't'),
         ('š̪', 'ś'), ('š̮', 'š'),
        ('ō', 'ô'), ('o', 'ō'), ('ū', 'û'), ('\u033D', 'ĕ')
    ]

    for x, y in replacements:
        Strng = Strng.replace(x, y)

    Strng = Strng.replace('ĕ꞉', '꞉ĕ')

    if '\u05CE' in Strng:
        Strng = Strng.replace('ḏ', 'd').replace('ṯ', 't').replace('ḡ', 'g').replace('\u05CE', '')

    Strng = Strng.replace('\u00B0\u0307', '\u0307\u00B0')

    return Strng

#testcase todo
# HebrewSBL's own logic now lives in ScriptProcessing/HebrewSBL.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.HebrewSBL import removetddash

#testcase todo
def ISO259Source(Strng):

    return Strng

#testcase todo
def ISO233Source(Strng):

    return Strng

#testcase todo
def HebrewSBLSource(Strng):

    return Strng

#testcase todo
def PersianDMGSBLSource(Strng):

    return Strng

#testcase todo
def ISO233Target(Strng):
    replacements = [('j', 'ǧ'), ('g', 'ǧ'), ('ḧ', 'ẗ'), ('ḫ', 'ẖ'), ('a̮', 'ỳ'), ('ˀ', 'ˈ'), \
        ('aⁿ', 'á'), ('iⁿ', 'í'), ('uⁿ', 'ú'), ('ā̂', 'ʾâ'), ('\u033D', '')]

    for x, y in replacements:
        Strng = Strng.replace(x, y)

    return Strng

#todo add to frontend
def inherentAO(Strng):
    Strng = Strng.replace('a', 'ô')

    return Strng

# Bengali's own logic now lives in ScriptProcessing/Bengali.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Bengali import BengaliOldRA, BengaliConjunctVB, khandatabatova, BengaliRaBa, BengaliIntervocalicDDA

#testcase todo
def PersianDMGTarget(Strng):
    replacements = [('ḏ', 'ẕ'), ('ḍ', 'ż'), ('ṯ', 's̱'), ('j', 'ǧ'), ('ˀ','ʼ'), ('ʔ', 'ʼ'), ('ȳ', 'ye'), ("ā̂", "ā"), ('\u033D', '')]

    for x, y in replacements:
        Strng = Strng.replace(x, y)

    return Strng

#testcase todo
def arabizeLatn(Strng, target='semitic'):
    cons = '(' + '|'.join(GM.SemiticConsonants) + ')'

    # opt 1
    Strng = re.sub(cons + '(ʾ)', r'\1' + 'ā', Strng)
    ### implement ths as a preoption for all semitic scripts

    #print('Arabized string is', Strng)

    ## Strng = re.sub('ʾ[aiu]ⁿ', '')

    if target == 'indic':
        Strng = Strng.replace('ʾā', 'ā̂')

    # opt 2
    if target != 'indic':
        Strng = re.sub('ʾ', 'a', Strng)
    else:
        Strng = re.sub('ʾ', 'â', Strng)

    # opt 3
    Strng = re.sub('(a̮|ā̮)', 'ā', Strng)
    Strng = re.sub('ˀ?ā̮̂', 'ʼā', Strng)

    if target != 'indic':
        Strng = re.sub('[ˀʔ]', 'ʼ', Strng)
    else:
         Strng = re.sub('[ˀ]', '', Strng)

    if target != 'indic':
        Strng = LatnInitialVowels(Strng, 'ʾ') ## Check this

    if target != 'indic':
        Strng = re.sub('ʼʾ', 'ʼ', Strng)

    if target != 'indic':
        Strng = re.sub('\u033d', '', Strng)

    Strng = re.sub('(ā)([iau])(ⁿ)', r'\2\3', Strng)

    #print('Arabized string is', Strng)

    return Strng

#trigger - UI prompt to show "preserve source" must be enabled for this option
#testcase todo
def BengaliSwitchYaYYa(Strng):
    Strng = re.sub('(?<!\u09CD)য', '@#$', Strng)
    Strng = re.sub('য়', 'য', Strng)
    Strng = Strng.replace('@#$', 'য়')

    return Strng

#testcase todo
def AlephMaterLectionis(Strng, target='semitic'):
    cons = '(' + '|'.join(GM.SemiticConsonants) + ')'

    # opt 1
    Strng = re.sub(cons + '(ʾ)', r'\1' + 'ā', Strng)

    return Strng

#testcase todo
def urduizeLatn(Strng, target='semitic'):
    cons = '(' + '|'.join(GM.SemiticConsonants) + ')'

    # opt 1
    Strng = re.sub(cons + '(ʾ)', r'\1' + 'ā', Strng)

    if target == 'indic':
        Strng = Strng.replace('ʾā', 'ā̂') ## Check this

    # opt 2
    Strng = re.sub('ʾ', 'â', Strng)

    # opt 3
    Strng = re.sub('[ˀʔ]', 'ʾ', Strng)
    Strng = re.sub('(a̮|ā̮)', 'ā', Strng)
    Strng = re.sub('ˀ?ā̮̂', 'ʼā', Strng)

    if target != 'indic':
        Strng = re.sub('\u033d', '', Strng)

    if target != 'indic':
        Strng = LatnInitialVowels(Strng)

    Strng = re.sub('(ā)([iau])(ⁿ)', r'\2\3', Strng)

    return Strng

#testcase todo
def syricizeLatn(Strng, target='semitic'):
    cons = '(' + '|'.join(GM.SemiticConsonants) + ')'

    # opt 3
    if target != 'indic':
        Strng = re.sub('â', 'ʾa', Strng)
        Strng = re.sub('ā̂', 'ʾā', Strng)
        Strng = re.sub("ê", "ʾe", Strng)
        Strng = re.sub("ē̂", "ʾē", Strng)

    if target != 'indic':
        Strng = LatnInitialVowels(Strng)

    return Strng

#testcase todo
def hebraizeLatn(Strng, target='semitic'):
    #print('Hebraizing Latin')
    if target != 'indic':
        Strng = LatnInitialVowels(Strng, 'ʾ')

    return Strng

#testcase todo
def syriacRoman(Strng):
    Strng = Strng.replace('v', 'ḇ').replace('ġ','ḡ').replace('ḫ','ḵ').replace('f','p̄')

    return Strng

#testcase todo
# Latn's own logic now lives in ScriptProcessing/Latn.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Latn import alephAyinLatnAlternate, alephAyinLatnAlternate2

#testcase todo
#testcase todo
# Arab's own logic now lives in ScriptProcessing/Arab.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Arab import ArabRemoveAdditions, arabicRemoveAdditionsPhonetic, ArabAtoAleph

#testcase todo
#testcase todo
def removeSemiticLetters(Strng):
    Strng = Strng.replace('ṭ', 't').replace('ḥ', 'h').replace('ḍ', 'z').replace('ḏ', 'z').replace('ẓ', 'z')\
        .replace('w', 'v').replace('ʿ', 'ʾ').replace('ṣ', 's')

    return Strng

#testcase todo
# Hebrew's own logic now lives in ScriptProcessing/Hebrew.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Hebrew import removeNikkud, HebrewVetVav, HeberewQoph, HebewShortO, HebrewnonFinalShort

#testcase todo
def LatnInitialVowels(Strng, initLetter=''):
    initVow = 'â ā̂ î ī̂ û ū̂ ê ē̂ âŷ ô ō̂ âŵ'.split(' ')
    nonInitVow = 'a ā i ī u ū e ē aŷ o ō aŵ'.split(' ')

    for x, y in zip(initVow, nonInitVow):
        Strng = Strng.replace(x, initLetter+y)

    Strng = Strng.replace('\u0302', '')

    Strng = re.sub('\u033d', '', Strng)
    #Strng = 'Vinodh'
    return Strng

#testcase todo
def removeMajliyana(Strng):
    Strng = Strng.replace('\u0330', '')

    return Strng

#testcase todo
def removeRukkaka(Strng):
    Strng = Strng.replace('\u0741', '')

    return Strng

#testcase todo
def removeQussaya(Strng):
    Strng = Strng.replace('\u0742', '')

    return Strng

#testcase todo
def removeVowelsSyriac(Strng):
    Strng = re.sub('[\u0732\u0735\u073C\u0738\u0739\u073F]', '', Strng)

    Strng = re.sub('[ّܰܶܺܽܳ]', '', Strng)

    return Strng

#testcase todo
def removeDiacriticsArabic(Strng):
    diacrtics = ["\u0652", "\u064E", "\u0650", "\u064F"]

    for diacritic in diacrtics:
        Strng = Strng.replace(diacritic, '')

    return Strng

#testcase todo
def removeSukunEnd(Strng):
    Strng = re.sub('(\u0652)(\W|$)', r'\2', Strng)

    return Strng

#testcase todo
# Arab-Fa's own logic now lives in ScriptProcessing/Arab_Fa.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Arab_Fa import persianPaGaFaJa

#testcase todo
def removeDiacriticsPersian(Strng):

    return Strng

#testcase todo
def removeDiacriticsSyriac(Strng):

    return Strng

#testcase todo
def useKtivMale(Strng):

    return Strng

#testcase todo
def PhoneticMapping(Strng):

    return Strng

#testcase todo
def ArabicGimelGaGha(Strng):
    Strng = Strng.replace('ج', 'غ')

    return Strng

#testcase todo
def ArabicGimelPaBa(Strng):
    Strng = Strng.replace('ف', 'ب')

    return Strng

#testcase todo
def BurmeseRomanLoCSource(Strng):
    # remove marking for pure virama
    Strng = Strng.replace('ʻ', '')

    # restore superscript Ga into normal subjoined y, r , v, h
    yrvh = Burmese.ConsonantMap[25:27] + Burmese.ConsonantMap[28:29] + Burmese.ConsonantMap[32:33]
    yrvhPat = ''.join(yrvh)
    Strng = re.sub(f'(\u103A)(\u1039)([{yrvhPat}])', r'\2\3', Strng)

    # restrore special yrvh
    virsub = '\u1039'
    yrvhsub = ['\u103B','\u103C','\u103D','\u103E']

    for x,y in zip(yrvh,yrvhsub):
        # Undo Replace subjoining forms: exp-virama + y/r/v/h <- subjoining y/r/v/h
        Strng = Strng.replace(virsub + x, y)

    # reverse replace vowel + diac with vowels
    vowDep = 'အော် အော အိ အီ အု အူ အေ'.split(' ')
    vowIndep = 'ဪ ဩ ဣ ဤ ဥ ဦ ဧ'.split(' ')

    ## Fix modifier letter apostrephe to normal quotation mark
    Strng = Strng.replace('ʼ', '’')

    for x, y in zip(vowDep, vowIndep):
        Strng = Strng.replace('’' + y, x)

    # u-Indep-i -> u-dep-i
    Strng = Strng.replace('\u102Fဣ', '\u102D\u102F')

    # reverse mark a as glottalstop
    Strng = Strng.replace('’အ', 'အ')

    # swap tone + virama to proper order
    Strng = Strng.replace("့်", "့်")

    return Strng

#testcase todo
def removeSegmentSpacesBurmese(Strng):
    # segment text into syllables
    import regex

    Strng = regex.sub('(\p{L}\p{M}*) (\p{L})', r'\1\2', Strng)
    Strng = regex.sub('(\p{L}\p{M}*) (\p{L})', r'\1\2', Strng)

    return Strng

def UseAlternateo1(Strng):
    Strng = Strng.replace('ᩮᩣ', 'ᩰ')

    return Strng


def UseAlternateo2(Strng):
    Strng = Strng.replace('ᩰ', 'ᩮᩣ')

    return Strng

#ThamLoC
def ThamLoCRomanLoCTarget(Strng):
    return Strng

def ThamLoCRomanLoCSource(Strng):
    #cryptogammic dot to Sakot
    Strng = Strng.replace('\u1A7F', '᩠')

    #fixing aiy
    Strng = Strng.replace('\u1A71\u1A3F\u1A7A', '\u1A71᩠ᨿ')

    return Strng

# khmer
def KhmerLoCRomanLoCTarget(Strng):
    import unicodedata
    Strng = unicodedata.normalize('NFC', Strng)

    #move consonant modifiers
    #Strng = re.sub('(‛ʹ)(′?)(a)(?![ṃḥ])', r'\1\2', Strng)
    Strng = re.sub('(ʹ)(′?)(?=[aāiīuūẏȳeoăáâààáéíóúàèìòùă])', r'\2', Strng)
    #Strng = re.sub('(ʹ)(′?)(a)(?=[aāiīuūẏȳeoă])', r'\2', Strng)

    #fix Oh
    Strng = Strng.replace('oḥ', 'oaḥ')
    Strng = Strng.replace('  ', ' ')


    return Strng

def KhmerLoCRomanLoCSource(Strng):
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'Khmer'))
    ListV ='|'.join(GM.CrunchSymbols(GM.VowelSigns,'Khmer'))
    ListA ='|'.join(GM.CrunchSymbols(GM.CombiningSigns,'Khmer'))

    vir = Khmer.ViramaMap[0]

    #move bantoc around
    Strng = re.sub('(\u17CB)(.)', r'\2\1', Strng)

    #move tonemarks around
    Strng = re.sub('('+ListC+')'+'('+ListV+')''('+ListA+')?''([៎៏])',r'\1\4\2\3',Strng)

    #subjoined a
    #Strng = Strng.replace(vir + '‛', '\u17D2')

    #mark consonant modifiers with subbase form
    Strng = re.sub('([ងញមបយរវ])(៉)([ិឹីឺ])', r'\1''ុ'r'\3', Strng)
    Strng = re.sub('([សហអ])(៊)([ិឹីឺ])', r'\1''ុ'r'\3', Strng)

    #remove virama
    Strng = Strng.replace(vir, '')

    return Strng

# shan
def ShanLoCRomanLoCTarget(Strng):
    Strng = re.sub('(ʻ)([\u0310\u0322])', r'\2\1', Strng)
    Strng = re.sub('(ō)([\u0310\u0322]?)(ʻ)', r'\1\2', Strng)

    return Strng

def ShanLoCRomanLoCSource(Strng):
    # restrore special yrvh
    yrv = Burmese.ConsonantMap[25:27] + Burmese.ConsonantMap[28:29]
    vir = '်'
    yrvsub = ['\u103B','\u103C','\u1082']

    for x,y in zip(yrv,yrvsub):
        # Undo Replace subjoining forms: exp-virama + y/r/v/h <- subjoining y/r/v/h
        Strng = Strng.replace(vir + x, y)

    ## Fix modifier letter apostrephe to normal quotation mark
    Strng = Strng.replace('ʼ', '’')
    #remove purevowel marker
    Strng = Strng.replace('’', '')
    # remove marking for pure virama
    Strng = Strng.replace('ʻ', '')

    #ai reversal
    Strng = Strng.replace('\u036E', 'ႂ်')

    # closed vs open
    cons = "[ၵၶၷꧠငၸꧡꩡꧢၺꩦꩧꩨꩩꧣတထၻꩪၼပၽၿꧤမယရလဝသႁꩮၹၾႀဢ]"
    open = ['ႃ', 'ႄ', 'ေ']
    closed = ['ၢ', 'ႅ', 'ဵ']

    for o, c in zip(open, closed):
        pass
        Strng = re.sub('(' + cons + ')' + '(' + o + ')' + '(' + cons + ')', r'\1' + c + r'\3', Strng)

    return Strng

#testcase todo
def BurmeseRomanLoCTarget(Strng):
    #print(Strng)
    # mark tone
    Strng = Strng.replace('˳', 'ʹ')

    # mark depaend au -> o'
    Strng = Strng.replace('auʻ','oʻ')

    # mark visarga as tone
    Strng = Strng.replace('ḥ', 'ʺ')

    # sort subjoined consonants
    # Strng = Strng.replace('‘‘', '')

    # adhoc chars
    chars_misc = {
        "e*": "၏",
        'n*': "၌",
        'r*': '၍',
        'l*': '၎'
    }

    for lat, bur in chars_misc.items():
        Strng = Strng.replace(bur, lat)

    #Strng = Strng.replace('ṃ', 'ṁ')

    return Strng

### Add new consonants here when added to gimeltra_data
#testcase todo
def insertARomanSemitic(Strng):
    Strng = Strng.replace('\u02BD', '')
    consonantsAll = '(' + '|'.join(sorted(GM.SemiticConsonants, key = len, reverse=True)) + ')'
    #above does not ocntain semitic consonants
    vowelsAll = '(' + '|'.join(GM.SemiticVowels) + ')'
    #print(Strng)
    Strng = re.sub(consonantsAll + '(?![꞉ʰ])(?!' + vowelsAll + ')', r'\1' + 'a', Strng)
    #print(Strng)
    Strng = re.sub('(꞉)(?!ʰ)(?!' + vowelsAll + ')', r'\1' + 'a', Strng)
    ## avoid double /a/ just in case
    #Strng = Strng.replace('aa', 'a')
    #Strng = re.sub(consonantsAll + '(?!' + vowelsAll + ')', r'\1' + 'a', Strng)

    #print(Strng)

    return Strng

# Semitic Target
#testcase todo
def FixSemiticRoman(Strng, Target):
    vir = '\u033D'
    Strng = re.sub('ō̂̄̂', 'ō̂', Strng)

    ## For Gemination
    if "Arab" in Target:
        consonantsAll = '(' + '|'.join(sorted(GM.CrunchSymbols(GM.Consonants, 'RomanSemitic'), key = len, reverse=True)) + ')'
        Strng = re.sub(consonantsAll + vir + r'\1', r'\1' + '꞉', Strng)
        #Strng = re.sub('(꞉)([aiuāīū])', r'\2\1', Strng)

    # create nukta equivalents
    # move nukta before /a/

    Strng = re.sub("âQ", "ʿ", Strng)
    Strng = re.sub('aQ', 'Qa', Strng)

    SemiticIndic=[('ʾQā', 'ā̂Q'), ('ʾQi', 'îQ'), ('ʾQī', 'ī̂Q'), ('ʾQu', 'ûQ'), ('ʾQū', 'ū̂Q'), ('ʾQe', 'êQ'), ('ʾQē', 'ē̂Q'),\
        ('ʾQo', 'ôQ'), ('ʾQō', 'ō̂Q'), ('ṣ', 'sQ'), ('ʿ', 'ʾQ'), \
                                 ('ṭ', 'tQ'), ('ḥ', 'hQ'), ('ḍ', 'dQ'), ('p̣', 'pQ'), ('ž', 'šQ'), ('ž', 'zQ'), ('ẓ', 'jʰQ'), ('ḏ', 'dʰQ'), ('ṯ', 'tʰQ'),
                                     ('w', 'vQ')
                        ]
    for s, i in SemiticIndic:
        Strng = Strng.replace(i, s)

    Strng = Strng.replace('\u033d\u033d', '\u033d')

    #print('Strng is ' + Strng)

    return Strng

#testcase todo
#testcase todo
def estrangelasyriac(Strng):

    return Strng

#testcase todo
def easternsyriac(Strng):

    return Strng

#testcase todo
def westernsyriac(Strng):

    return Strng


# Pallava's own logic now lives in ScriptProcessing/Pallava.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Pallava import kawitan, sundapura

# Itrans's own logic now lives in ScriptProcessing/Itrans.py -
# consolidated there (batch migration).
from .ScriptProcessing.Itrans import swapEeItrans_post as swapEeItrans, readableItrans

#todo change UI example : haMpi  ha~pi hA~s hAMs hU~ hUM -> hampi hAA hAs
def NasalTilde(Strng):
    Strng = AnusvaratoNasalASTISO(Strng)
    Strng = re.sub('(m̐|ṃ|ṁ)', '\u0303', Strng)

    return Strng

#todo feature
def siddhamBija(Strng):

    return Strng

#todo feature
def verticalKana(Strng):

    return Strng

#todo feature
def verticalSiddham(Strng):

    return Strng

#todo testcase
def vtobJapanese(txt):

    return txt

#todo testcase
# Sogd's own logic now lives in ScriptProcessing/Sogd.py -
# consolidated there (batch migration).
from .ScriptProcessing.Sogd import SogdReshAyin_post as SogdReshAyin

#todo testcase
# Sogo's own logic now lives in ScriptProcessing/Sogo.py -
# consolidated there (batch migration).
from .ScriptProcessing.Sogo import SogoReshAyinDaleth_post as SogoReshAyinDaleth

#todo testcase
def arabPaFa(Strng):

    return Strng.replace('پ','ف')


#todo testcase
def arabChaSa(Strng):

    return Strng.replace('چ', 'س')

#todo testcase
def gainGimel(Strng):
    return Strng.replace('עׄ','ג')

#todo testcase
# Hebr-Ar's own logic now lives in ScriptProcessing/Hebr_Ar.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Hebr_Ar import gainGimel, tavTwodot, tavThreedot

#todo testcase
#todo testcase
#todo testcase
def tokushuon(txt):
   txt = txt.replace('si', 'suxi').replace('zi', 'zuxi')
   txt = txt.replace('yi','ixi')
   txt = txt.replace('fy', 'fux')
   txt = txt.replace('nye', 'nixe')

   txt = re.sub('(?<![sc])hu', 'hoxu', txt)
   txt = re.sub('(?<![sc])hye', 'hixe', txt)

   return txt

#todo testcase
# --- JapanesePostProcess pipeline stages --------------------------------
# Extracted verbatim, one labeled block at a time - no logic changes, same
# variables in and out. Real test coverage exists for this function (80
# cases across vtobJapanese/eiaudipthongs/wasvnukta/verticalKana, both
# directions), verified the same way convert()'s staging was: A/B
# comparison against the pre-extraction implementation plus the full suite.

def _japanese_pivot_to_romankana(src, txt):
    from . import Convert
    txt = Convert.convertScript(txt, src, "Telugu")

    txt = txt.replace('ˆ', '')
    txt = Convert.convertScript(txt.lower(), "ISO", "Inter")

    txt = Convert.convertScript(txt, "Telugu", "RomanKana")

    return txt

def _japanese_visarga_nasalization_punctuation(txt):
    # Visarga
    txt = re.sub('([aiueo])' + r'\1' + 'H', r'\1' + r'\1' + 'h' + r'\1', txt)

    txt = re.sub('([aiueo])H', r'\1' + 'h' + r'\1', txt)

    # nasalization
    txt = txt.replace('Gk', 'nk').replace('Gg', 'ng').replace('Jc', 'nc').replace('Jj', 'nj').replace('mb', 'nb').replace('mp', 'np')

    txt = txt.replace("nn", 'nnn').replace('c', 'ch').replace('chch', 'cch').replace('shsh', 'ssh').replace("mm", "nm")

    txt = txt.replace(',', '、').replace('\uEA01', '。').replace('\uEA02', '。。')

    txt = txt.replace('JJ', 'nnny')
    txt = txt.replace('J', 'ny')

    return txt

def _japanese_empirical_consonant_fixes(txt, postoptions):
    if 'vtobJapanese' in postoptions:
        txt = txt.replace('v', 'b')

    # fix tra, dra
    txt = txt.replace('tr', 'tor').replace('dr', 'dor').replace('Dr', 'dor').replace('Tr', 'tor')

    ## how to satya, sadya, sahya, asya, ask the person
    txt = txt.replace('tya', 'tiya').replace('dya', 'diya').replace('sya', 'suya').replace('shya', 'shuya').replace('chya', 'chuya')#.replace('hya', 'hiya')
    txt = txt.replace('di', 'dexi').replace('du', 'doxu')#.replace('dyu','dexyu')
    txt = txt.replace('ti', 'texi').replace('tu', 'toxu')
    #txt = txt.replace('kwi', 'kuxi').replace('kwe', 'kuxwe').replace('kwo', 'kuxwo').replace('kwa', 'kuxwa')
    txt = txt.replace('mye', 'mixe').replace('pye', 'pixe').replace('bye', 'bixe')
    txt = txt.replace('ye', 'ixe')
    txt = txt.replace('vye', 'vuxixe').replace('vy', 'vuxy')
    txt = txt.replace('she', 'shixe')

    return txt

def _japanese_nativize_branch_fix(txt, nativize):
    if not nativize:
        txt = re.sub('(r)(r\u309A)', 'rur\u309A', txt)
        txt = re.sub('(r\u309A)(r\u309A)', 'rr' + '\u309A', txt)
        txt = re.sub('(k\u309A)(k\u309A)', 'kk' + '\u309A', txt)
        txt = re.sub('([rk])(\u309A)([aieou])', r'\1\3\2', txt)

        txt = tokushuon(txt)
    else:
        #txt = txt.replace('v', 'w')
        txt = txt.replace('r\u309A', 'r').replace('k\u309Ak' + '\u309A', 'ng').replace('k\u309A', 'ng')


        txt = txt.replace('yi', 'i').replace('ye', 'e').replace('wu', 'u')
        txt = txt.replace('wo', 'uxo')

        # she
        txt = txt.replace('she', 'shie')

    return txt

def _japanese_encode_to_kana(txt, tgt, nativize):
    from aksharamukha.ScriptMap.NonIndic import kana2roman

    if tgt == 'Hiragana':
        txt = kana2roman.to_hiragana(txt)

        txt = re.sub('(k|g|ch|j|p|b|m|y|r|w|sh|s|h|z|f)' + '(' + r'\1' + ')', r'\1' + 'u', txt)

        txt = re.sub('(d|t)' + '(' + r'\1' + ')', r'\1' + 'o', txt)

        if not nativize:
            txt = tokushuon(txt)

        txt = kana2roman.to_hiragana(txt)

        txt = re.sub('(k|g|ch|j|p|b|m|y|r|sh|s|h|z|f|v)', r'\1' + 'u', txt)
        txt = re.sub('(d|t)', r'\1' + 'o', txt)

        if not nativize:
            txt = tokushuon(txt)

        txt = kana2roman.to_hiragana(txt)

        txt = txt.replace('う゛', 'ゔ')

    if tgt == 'Katakana':
        txt = txt.replace('aa', 'a-').replace('ii', 'i-').replace('ee', 'e-').replace('oo', 'o-').replace('uu','u-')
        txt = txt.replace('a\u309Aa', 'a\u309A-').replace('i\u309Ai', 'i\u309A-').replace('e\u309Ae', 'e\u309A-').replace('o\u309Ao', 'o\u309A-').replace('u\u309Au','u\u309A-')

        txt = kana2roman.to_katakana(txt)

        txt = re.sub('(k|g|ch|j|p|b|m|y|r|sh|s|h|z|f|v)' + '(' + r'\1' + ')', r'\1' + 'u', txt)
        txt = re.sub('(d|t)' + '(' + r'\1' + ')', r'\1' + 'o', txt)

        if not nativize:
            txt = tokushuon(txt)

        txt = kana2roman.to_katakana(txt)
        txt = re.sub('(k|g|ch|j|p|b|m|y|r|sh|s|h|z|f|v)', r'\1' + 'u', txt)
        txt = re.sub('(d|t)', r'\1' + 'o', txt)

        if not nativize:
            txt = tokushuon(txt)

        txt = kana2roman.to_katakana(txt)

    return txt

def JapanesePostProcess(src, tgt, txt, nativize, postoptions):
    from . import Convert

    txt = _japanese_pivot_to_romankana(src, txt)
    txt = _japanese_visarga_nasalization_punctuation(txt)
    txt = _japanese_empirical_consonant_fixes(txt, postoptions)
    txt = _japanese_nativize_branch_fix(txt, nativize)
    txt = _japanese_encode_to_kana(txt, tgt, nativize)

    txt = Convert.convertScript(txt, "Inter", "ISO")

    return txt
def urduRemoveInherent(Strng):
    Strng = re.sub('\Ba', '', Strng)

    return Strng

#todo testcase
def devanagariuttara(Strng):

    return Strng

def devanagarinepali(Strng):

    return Strng

def devanagaribalbodh(Strng):

    return Strng

def devanagarijain(Strng):

    return Strng

def HiraganaaunotDipthong(Strng):

    return Strng

#not used
def IASTISONasalTilde(Strng):

    return Strng

#todo testcase
#todo testcase
#todo testcase
def HebrewKatevMalei(Strng):
    Strng = Strng.replace('ָ', 'א') # long aa
    Strng = Strng.replace('ַ', 'א') # short a

    return Strng

#todo testcase
def DevanagariAnusvara(Strng):

    return NasalToAnusvara(Strng, 'Devanagari')

def jainomDevangari(Strng):
    Strng = Strng.replace('ॐ', 'ꣽ')

    return Strng

# Gurmukhi's own logic now lives in ScriptProcessing/Gurmukhi.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Gurmukhi import GurmukhiCandrabindu, GurmukhiYakaash, GurmukhiTippiBindu, GurmukhiTippiGemination

#misnomer
def mDotAboveToBelow(Strng):
    Strng = Strng.replace('ṃ', 'ṁ')

    return Strng

#misnomer
def mDotBelowToAbove(Strng):
    Strng = Strng.replace('ṁ', 'ṃ')

    return Strng

#todo : ISOPali postoptions empty todo

# ISO's own logic now lives in ScriptProcessing/ISO.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.ISO import noLongEO

# TamilExtended's own logic now lives in ScriptProcessing/TamilExtended.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.TamilExtended import TamilStyleUUCore, TamilStyleUUOther, TamilpredictDentaNaExtended, TamilExtendedNNA, TamilExtendedAnusvara

# Tamil's post-options (and its default-bundle TamilNaToNNa/
# TamilpredictDentaNa) now live in ScriptProcessing/Tamil.py, consolidated
# there with its Fix logic and pre-options too. Re-exported here so
# Options.py's getmembers(PostProcess, isfunction) discovery still finds
# them, and so PostOptions.py's default bundle for Tamil keeps resolving.
from .ScriptProcessing.Tamil import (TamilNaToNNa, TamilpredictDentaNa, ContextualLLa,
    FinalNNa, TamilAddFirstVarga, TamilDisableSHA, TamilGranthaVisarga, TamilOmDisable,
    TamilRemoveApostrophe, TamilRemoveNumbers, TamilSubScript, oldtamilortho)

# Thai's own logic now lives in ScriptProcessing/Thai.py -
# consolidated there (batch migration).
from .ScriptProcessing.Thai import ThaiNativeConsonants, ThaiSajjhayaOrthography_post as ThaiSajjhayaOrthography, ThaiSajjhayawithA_post as ThaiSajjhayawithA, ThaiTranscription, ThaiVisargaSaraA

# KhamtiShan's own logic now lives in ScriptProcessing/KhamtiShan.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.KhamtiShan import KhamiShanMyanmarNumerals, KhamtiShanRa

# Grantha's own logic now lives in ScriptProcessing/Grantha.py -
# consolidated there (batch migration).
from .ScriptProcessing.Grantha import GranthaOldau, GranthaPrakrit, granthafinal, granthaserif, egrantamil

def Dot2Dandas(Strng):
    Strng = Strng.replace('..', '॥')
    Strng = Strng.replace('.', '।')

    return Strng

def Dot2Pipes(Strng):
    Strng = Strng.replace('..', '||')
    Strng = Strng.replace('.', '|')

    return Strng

# TamilSaurashtra's own logic now lives in ScriptProcessing/TamilSaurashtra.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.TamilSaurashtra import SaurastraHaaruColon

# Takri's own logic now lives in ScriptProcessing/Takri.py -
# consolidated there (batch migration).
from .ScriptProcessing.Takri import TakriArchaicKha_post as TakriArchaicKha, TakriRemoveGemination

# Mongolian's own logic now lives in ScriptProcessing/Mongolian.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Mongolian import MongolianSyllabize

# Tibetan's own logic now lives in ScriptProcessing/Tibetan.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Tibetan import TibetanSyllabize, TibetanSanskritPalatals, tibetandbumed, TibetanNada, TibetanTsheg, TibetanRemoveVirama, TibetanRemoveBa

# Soyombo's own logic now lives in ScriptProcessing/Soyombo.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Soyombo import SoyomboSyllabize, SoyomboSanskritPalatals, SoyomboFinals, SoyomboInitials, SoyomboSpaceTscheg


# PhagsPa's own logic now lives in ScriptProcessing/PhagsPa.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.PhagsPa import PhagsPaTib, PhagsPaSeal

# RomanReadable's own logic now lives in ScriptProcessing/RomanReadable.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.RomanReadable import RomanReadableLongEO

# Marchen's own logic now lives in ScriptProcessing/Marchen.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Marchen import MarchenSanskritPalatals


# ZanabazarSquare's own logic now lives in ScriptProcessing/ZanabazarSquare.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.ZanabazarSquare import ZanabazarSanskritPalatals, ZanzabarSpaceTsheg, ZanabazarSquareContextual, ZanabazarSquareAiAu, ZanabazarSquareMongolianFinal

def KhandaTaRomanLoC(Strng):
    Strng = Strng.replace('ṯ', 'ৎ')

    return Strng

# reverse these in preprocess
def RomanLoCVaWa(Strng):
    Strng = Strng.replace('v', 'w')
    return Strng

def RomanLoCSasha(Strng):
    Strng = Strng.replace('ṣ', 'sh')
    return Strng

# IAST's own logic now lives in ScriptProcessing/IAST.py -
# consolidated there (batch migration).
from .ScriptProcessing.IAST import RomanLoCSLaDotLaUnderscore_post as RomanLoCSLaDotLaUnderscore

def RomanLoCLaUnderscoreDoubleDot(Strng):
    Strng = Strng.replace('ḻ', 'l̤')

    return Strng

# RomanLoCDevanagari's own logic now lives in ScriptProcessing/RomanLoCDevanagari.py -
# consolidated there (batch migration).
from .ScriptProcessing.RomanLoCDevanagari import HindiMarathiRomanLoCFix_post as HindiMarathiRomanLoCFix

# DivesAkuru's own logic now lives in ScriptProcessing/DivesAkuru.py -
# consolidated there (batch migration).
from .ScriptProcessing.DivesAkuru import DivesAkuruAlternateIndVowels_post as DivesAkuruAlternateIndVowels, DivesAkuruHomoOrganNasal, UseAlternateYA

# Kawi's own logic now lives in ScriptProcessing/Kawi.py -
# consolidated there (batch migration).
from .ScriptProcessing.Kawi import KawiAltAiAU, KawiArchaicJNA, KawiDecomposedVowel, KawiMoveRepha_post as KawiMoveRepha

# Javanese's own logic now lives in ScriptProcessing/Javanese.py -
# consolidated there (batch migration).
from .ScriptProcessing.Javanese import JavaneseArchaicJNA, JavaneseAvowels, JavaneseMoveRepha_post as JavaneseMoveRepha

def TibetanLoCRomanLoCFix(Strng):
    Strng = re.sub('tʹ(?!s)', 't', Strng)
    Strng = re.sub('nʹ(?!y)', 'n', Strng)
    Strng = re.sub('j_h', 'jh', Strng)

    return Strng

# RomanLoCJavanese's own logic now lives in ScriptProcessing/RomanLoCJavanese.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.RomanLoCJavanese import JavaneseSimplified

# RomanLoCBalinese's own logic now lives in ScriptProcessing/RomanLoCBalinese.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.RomanLoCBalinese import BalineseSimplified

def BalineseRomanLoCFix(Strng):
    Strng = Strng.replace('ḧ', 'h').replace('ng̈', '‘')

    return Strng

def JavaneseRomanLoCFix(Strng):
    Strng = Strng.replace('ḧ', 'h').replace('ng̈', '‘')

    return Strng

# Balinese's own logic now lives in ScriptProcessing/Balinese.py -
# consolidated there (batch migration).
from .ScriptProcessing.Balinese import BalineseArchaicJNA, BalineseAvowels, BalineseMoveRepha_post as BalineseMoveRepha

def BalineseJavaneseMoveRepha(Strng, tgt, reph):
    repha = '(' + reph + ')'

    cons = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, tgt)) + ')'
    vows = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSignsNV, tgt)) + ')'
    vir = GM.CrunchSymbols(GM.virama, tgt)[0]

    Strng = re.sub(repha+'('+cons+')'+'('+ vir + cons +')*'+'(' + vows + ')?', r'\2\4\6\1', Strng)

    candAnu = '[' + ''.join(GM.CrunchSymbols(GM.CombiningSigns, tgt)[:2]) + ']'
    Strng = re.sub(repha+'(' + candAnu + ')', r'\2\1', Strng)

    return Strng

def GurmukhiRomanLoCFix(Strng):
    Strng = re.sub('(m̆|ṃ)(k|g)', 'ṅ' + r'\2', Strng)
    Strng = re.sub('(m̆|ṃ)(c|j)', 'ñ' + r'\2', Strng)
    Strng = re.sub('(m̆|ṃ)(ṭ|ḍ)', 'ṇ' + r'\2', Strng)
    Strng = re.sub('(m̆|ṃ)(t|d)', 'n' + r'\2', Strng)
    Strng = re.sub('(m̆|ṃ)(p|b)', 'm' + r'\2', Strng)

    return Strng

def DevanagariRomanLoCFix(Strng):
    Strng = Strng.replace('gḧ', 'g̳h̳').replace('ṭ̈', 't̤').replace('s̈', 's̤')\
        .replace('ḧ', 'h̤')

    return Strng

def MalayalamRomanLoCFix(Strng):
    Strng = Strng.replace('ṟṟ', 'ṯṯ')
    Strng = Strng.replace('ŭ', 'ȧ')
    return Strng

def MalayalamNTA(Strng):
    Strng = Strng.replace('nṟ', 'nṯ')
    return Strng

def MalayalamTTNTA(Strng):
    Strng = Strng.replace('ṟṟ', 'ṯṯ')
    Strng = Strng.replace('nṟ', 'nṯ')
    return Strng

def SinhalaSannakaNasalization(Strng):
    #Strng = Strng.replace('ṁ', 'ṃ')

    Strng = re.sub('(n̆)(k|g)', 'ṅ' + r'\2', Strng)
    Strng = re.sub('(n̆)(c|j)', 'ñ' + r'\2', Strng)
    Strng = re.sub('(n̆)(ṭ|ḍ)', 'ṇ' + r'\2', Strng)
    Strng = re.sub('(n̆)(t|d)', 'n' + r'\2', Strng)
    Strng = re.sub('(m̆)(p|b)', 'm' + r'\2', Strng)

    return Strng

def RomanLoCChandrabindu(Strng):
    #Strng = Strng.replace('ṁ', 'ṃ')

    Strng = re.sub('(m̐)(k|g)', 'n̐' + r'\2', Strng)
    Strng = re.sub('(m̐)(c|j)', 'n̐' + r'\2', Strng)
    Strng = re.sub('(m̐)(ṭ|ḍ)', 'n̐' + r'\2', Strng)
    Strng = re.sub('(m̐)(t|d)', 'n̐' + r'\2', Strng)
    Strng = re.sub('(m̐)(p|b)', 'n̐' + r'\2', Strng)

    return Strng

def AnusvaratoNasalASTISO(Strng):
    #Strng = Strng.replace('ṁ', 'ṃ')

    Strng = re.sub('(ṃ|ṁ)(k|g)', 'ṅ' + r'\2', Strng)
    Strng = re.sub('(ṃ|ṁ)(c|j)', 'ñ' + r'\2', Strng)
    Strng = re.sub('(ṃ|ṁ)(ṭ|ḍ)', 'ṇ' + r'\2', Strng)
    Strng = re.sub('(ṃ|ṁ)(t|d)', 'n' + r'\2', Strng)
    Strng = re.sub('(ṃ|ṁ)(p|b)', 'm' + r'\2', Strng)

    return Strng


# RussianCyrillic's own logic now lives in ScriptProcessing/RussianCyrillic.py -
# consolidated there (batch migration).
from .ScriptProcessing.RussianCyrillic import CyrillicPali_post as CyrillicPali, removeDiacritics

# Ranjana's own logic now lives in ScriptProcessing/Ranjana.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Ranjana import ranjanalantsa, ranjanawartu

def TaiKuen(Strng):
    return Strng

def TaiThamLao(Strng):
    return Strng

# Newa's own logic now lives in ScriptProcessing/Newa.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Newa import nepaldevafont, NewaMurmurConsonants, NewaSpecialTa, NewaDisableRepha

# Chakma's own logic now lives in ScriptProcessing/Chakma.py -
# consolidated there (batch migration).
from .ScriptProcessing.Chakma import ChakmaPali_post as ChakmaPali, ChakmaEnableAllConjuncts, ChakmaVowelsIndependent, ChakmaGemination

# LaoPali's own logic now lives in ScriptProcessing/LaoPali.py -
# consolidated there (batch migration).
from .ScriptProcessing.LaoPali import LaoTranscription_post as LaoTranscription, LaoPhonetic_post as LaoPhonetic, LaoSajjhaya, LaoSajjhayawithA

# Siddham's own logic now lives in ScriptProcessing/Siddham.py -
# consolidated there (batch migration).
from .ScriptProcessing.Siddham import UseAlternateI1, UseAlternateI2, UseAlternateII, UseAlternateU, UseAlternateVSU, UseAlternateVSUU, siddhammukta

def DevanagariACandra(Strng):
    Strng = Strng.replace('ऍ', 'ॲ')

    return Strng

# WarangCiti's own logic now lives in ScriptProcessing/WarangCiti.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.WarangCiti import WarangCitiModernOrthogaphy

def MultaniAbjad(Strng):
    ListAll = "(" + "|".join(GM.CrunchSymbols(GM.Characters, 'Multani') + ["𑊓", "𑊍"]) + ")"
    ListC = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, 'Multani') + ["𑊓", "𑊍"]) + ")"
    ListV = "(" + "|".join(GM.CrunchSymbols(GM.Vowels, 'Multani') + ["𑊓", "𑊍"]) + ")"

    Strng = re.sub(ListC + ListV + ListC, r'\1\3', Strng)
    Strng = re.sub('('+ ListC + '{2,})' + ListV, r'\1', Strng)
    Strng = re.sub(ListV + ListC + ListV, r'\1\2', Strng)


    return Strng

# Lao's own logic now lives in ScriptProcessing/Lao.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Lao import LaoNative

# Sundanese's own logic now lives in ScriptProcessing/Sundanese.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Sundanese import SundaneseHistoricConjuncts, SundaneseRemoveHistoric

# Limbu's own logic now lives in ScriptProcessing/Limbu.py -
# consolidated there (batch migration).
from .ScriptProcessing.Limbu import LimbuSpellingSaI_post as LimbuSpellingSaI, LimburemoveHistorical

def tradOrtho(Strng):
    return Strng

def siddhamap(Strng):
    return Strng

# Bhaiksuki's own logic now lives in ScriptProcessing/Bhaiksuki.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Bhaiksuki import BhaiksukiRetainSpace

# Kaithi's own logic now lives in ScriptProcessing/Kaithi.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Kaithi import KaithiRetainSpace

def MedievalTamilOrthography(Strng):
    OldEO = ['எ்', 'ெ்', 'ஒ்', 'ெ்ா', 'எ', 'ெ', 'ஒ', 'ொ']
    NewEO = ['எ', 'ெ', 'ஒ', 'ொ', 'ஏ', 'ே', 'ஓ', 'ோ']

    for x,y in zip(NewEO, OldEO):
        Strng = Strng.replace(x,y)

    return Strng

def AmbigousTamilOrthography(Strng):

    return Strng

def ModiRemoveLong(Strng):
    Strng = Strng.replace('𑘂', '𑘃')
    Strng = Strng.replace('𑘅','𑘄')
    Strng = Strng.replace('𑘱', '𑘲')
    Strng = Strng.replace('𑘴','𑘳')

    Strng = Strng.replace('𑘆', '𑘨𑘲')
    Strng = Strng.replace('𑘇', '𑘨𑘲')
    Strng = Strng.replace('𑘈', '𑘩𑘲')
    Strng = Strng.replace('𑘉', '𑘩𑘲')

    Strng = Strng.replace('𑘵', '𑘿𑘨𑘲')
    Strng = Strng.replace('𑘶', '𑘿𑘨𑘲')
    Strng = Strng.replace('𑘷', '𑘿𑘩𑘲')
    Strng = Strng.replace('𑘸', '𑘿𑘩𑘲')

    return Strng

# DevanagariLimbu's own logic now lives in ScriptProcessing/DevanagariLimbu.py -
# consolidated there (batch migration).
from .ScriptProcessing.DevanagariLimbu import LimbuDevanagariConvention_post as LimbuDevanagariConvention

# Nandinagari's own logic now lives in ScriptProcessing/Nandinagari.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Nandinagari import NandinagariPrishtamatra

def DevanagariPrishtamatra(Strng, reverse = False):
    if not reverse:
        Strng = Strng.replace('े','ॎ')
        Strng = Strng.replace('ै','ॎे')
        Strng = Strng.replace('ो','ॎा')
        Strng = Strng.replace('ौ','ॎो')
    else:
        Strng = Strng.replace('ॎे', 'ै')
        Strng = Strng.replace('ॎो', 'ौ')
        Strng = Strng.replace('ॎा', 'ो')
        Strng = Strng.replace('ॎ', 'े')

    return Strng

def ThaanaRemoveHistorical(Strng):
    return Strng.replace('ޱ','ނ')

# Oriya's own logic now lives in ScriptProcessing/Oriya.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Oriya import OriyaVaAlt, OriyaYYA, OriyaVa

def dotReph(Strng):
    ListC = '('+"|".join(sorted(GM.CrunchSymbols(GM.Consonants,"Malayalam"))) + ')'

    Strng = re.sub('(?<!്)' + 'ർ' + ListC,'ൎ' + r'\1', Strng)
    Strng = re.sub('(?<!്)' +'ര്' + ListC,'ൎ' + r'\1', Strng)

    return Strng

def archaicAIAU(Strng):
    Strng = Strng.replace('ൗ', 'ൌ')
    Strng = Strng.replace('ഈ', 'ൟ')

    return Strng

def MalayalamremoveHistorical(Strng):
    Strng = Strng.replace('\u0D29','\u0D28')
    Strng = Strng.replace('ന‍്', 'ൻ')

    return Strng

def MalayalamPrakrit(Strng):
    ## Replace Anusvara with Anusvara above
    Strng = Strng.replace("ം", "ഀ")
    Strng = InsertGeminationSign(Strng, 'Malayalam')

    return Strng

    ## Insert Gemination Sign

def MeeteiMayekremoveHistorical(Strng):
    removePairs = [('ꫢ', 'ꯆ'), ('ꫣ', 'ꯅ'), ('ꫤ','ꯇ'), ('ꫥ','ꯊ'), ('ꫦ','ꯗ'), ('ꫧ','ꯙ'), ('ꫨ','ꯅ'),
                   ('ꫩ','ꯁ'), ('ꫪ','ꯁ'), ('\uAAF5','ꯍ꯭'), ('ꯑꫫ','ꯏ'), ('ꯑꫬ','ꯎ'), ('ꫫ','ꯤ'), ('ꫬ','ꯨ')]

    for x,y in removePairs:
        Strng = Strng.replace(x,y)

    return Strng

def TamilSHADisable(Strng):
    return Strng.replace("ஶ", "ஸ²")

# കൽന് കത്ല് ക്ഷേത്ര് കൻല് - Check this

def MalayalamChillu(Strng, reverse=False, preserve=False):

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

def historicChillu(Strng):
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
    Strng = Strng.replace('\u0D4D', '\u0D3B')

    return Strng

def MalayalamCircVirama(Strng):
    Strng = Strng.replace('\u0D4D', '\u0D3C')

    return Strng

def RemoveSchwa(Strng,Target):

    vir = GM.CrunchSymbols(GM.VowelSigns,Target)[0] + GM.CrunchSymbols(GM.VowelSigns,Target)[0]
    ListC = '|'.join(GM.CrunchSymbols(GM.Consonants,Target))
    ListV = '|'.join(GM.CrunchSymbols(GM.Vowels,Target))
    ListVS = '|'.join(GM.CrunchSymbols(GM.VowelSignsNV,Target))
    ListAll = '|'.join(GM.CrunchSymbols(GM.Vowels+GM.VowelSigns+GM.Consonants+GM.CombiningSigns,Target))

    # Fix अपमही अपमाही

    Strng = re.sub('('+ListAll+')'+'('+ListC+')'+'(?!'+ListAll+')',r'\1\2'+vir,Strng)
    Strng = re.sub('('+ListAll+')'+'(?<!'+vir+')'+'('+ListC+')'+'('+ListC+')'+'('+ListVS+')',r'\1\2'+vir+r'\3\4',Strng)

    return Strng

def InsertGeminationSign(Strng,Target): #Fix this

    vir = GM.CrunchSymbols(GM.VowelSigns,Target)[0]
    ConUnAsp = [GM.CrunchList('ConsonantMap', Target)[x] for x in [0,2,5,7,10,12,15,17,20,22,4,9,14,19,24,25,26,27,28,29,30,31,32]]
    ConUnAsp = ConUnAsp + GM.CrunchList('SouthConsonantMap',Target) + GM.CrunchList('NuktaConsonantMap',Target)
    ConAsp   = [GM.CrunchList('ConsonantMap', Target)[x] for x in [1,3,6,8,11,13,16,18,21,23]]
    ConOthrs = [GM.CrunchList('ConsonantMap', Target)[x] for x in [0,2,5,7,10,12,15,17,20,22,4,9,14,19,24]]

    Strng = re.sub('('+'|'.join(ConUnAsp)+')'+'('+vir+')'+r'\1',GM.Gemination[Target]+r'\1',Strng)

    for i in range(len(ConAsp)):
        Strng = re.sub('('+ConUnAsp[i]+')'+'('+vir+')'+'('+ConAsp[i]+')',GM.Gemination[Target]+r'\3',Strng)

    return Strng

def ReverseGeminationSign(Strng,Target): #Fix this

    vir = GM.CrunchSymbols(GM.VowelSigns,Target)[0]
    ConUnAsp = [GM.CrunchList('ConsonantMap', Target)[x] for x in [0,2,5,7,10,12,15,17,20,22,4,9,14,19,24,25,26,27,28,29,30,31,32]]
    ConUnAsp = ConUnAsp + GM.CrunchList('SouthConsonantMap',Target) + GM.CrunchList('NuktaConsonantMap',Target)
    ConAsp   = [GM.CrunchList('ConsonantMap', Target)[x] for x in [1,3,6,8,11,13,16,18,21,23]]
    ConOthrs = [GM.CrunchList('ConsonantMap', Target)[x] for x in [0,2,5,7,10,12,15,17,20,22,4,9,14,19,24]]

    if Target == 'Gurmukhi':
        Strng = Strng.replace('ੱਸ਼਼', 'ਸ਼਼੍ਸ਼਼')

    Strng = re.sub('(' + GM.Gemination[Target] + ')' + '('+'|'.join(ConUnAsp)+')', r'\2' + vir + r'\2', Strng)

    for i in range(len(ConAsp)):
        Strng = re.sub('(' + GM.Gemination[Target] + ')' + '(' + ConAsp [i] +')', ConUnAsp[i] + vir + r'\2', Strng)

    return Strng

def KhandaTa(Strng,Target, reverse=False): #Check for Bhakt - Khanda Ta not formed

    ta = GM.CrunchSymbols(GM.Consonants, Target)[15]
    khandata = '\u09CE'
    vir = GM.CrunchSymbols(GM.VowelSigns,Target)[0]
    ListC = '|'.join([GM.CrunchList('ConsonantMap', Target)[x] for x in [15,16,19,27,24,25,26,28]] + ['ব', 'ৰ', 'য়'])
    #print(ListC)
    if not reverse:
        Strng = re.sub('(?<!' + vir + ')' + '('+ta+')'+'('+vir+')'+'(?!'+ListC+')',khandata, Strng)
        Strng = Strng.replace('ৎˍ', 'ৎ')
    else:
        Strng = Strng.replace(khandata, ta + vir)

    return Strng

def NasalToAnusvara(Strng,Target):

    ListN = [GM.CrunchSymbols(GM.Consonants, Target)[x] for x in [4,9,14,19,24]]
    ListC = [
             '|'.join(GM.CrunchList('ConsonantMap', Target)[0:4]),
             '|'.join(GM.CrunchList('ConsonantMap', Target)[5:9]),
             '|'.join(GM.CrunchList('ConsonantMap', Target)[10:14]),
             '|'.join(GM.CrunchList('ConsonantMap', Target)[15:19]),
             '|'.join(GM.CrunchList('ConsonantMap', Target)[20:24]),
            ]
    ListCAll = '(' + '|'.join(GM.CrunchSymbols(GM.Characters, Target)) + ')'

    vir = GM.CrunchSymbols(GM.VowelSigns,Target)[0]
    Anu = GM.CrunchSymbols(GM.CombiningSigns,Target)[1]

    for i in range(len(ListN)):
        #print '('+ListN[i]+')'+'('+vir+')'+'('+ListC[i]+')'
        Strng = re.sub(ListCAll + GM.VedicSvaras + '(?<!' + vir + ')' + '('+ListN[i]+')' +'('+vir+')'+'('+ListC[i]+')',r'\1\2'+Anu+r'\5',Strng)
        Strng = re.sub(ListCAll + GM.VedicSvaras + '(?<!' + vir + ')' + '('+ListN[i]+')' +'('+vir+')'+'('+ListC[i]+')',r'\1\2'+Anu+r'\5',Strng)

    for svara in GM.VedicSvarasList:
        Strng = Strng.replace(svara + Anu, Anu + svara)

    return Strng

def AnusvaraToNasal(Strng,Target):
    nukta = GM.CrunchList('NuktaMap', Target)[0]

    ListN = [GM.CrunchSymbols(GM.Consonants, Target)[x] for x in [4,9,14,19,24]]
    ListC = [
             '|'.join(GM.CrunchList('ConsonantMap', Target)[0:4]),
             '|'.join(GM.CrunchList('ConsonantMap', Target)[5:9]),
             '|'.join(GM.CrunchList('ConsonantMap', Target)[10:14]),
             '|'.join(GM.CrunchList('ConsonantMap', Target)[15:19]),
             '|'.join(GM.CrunchList('ConsonantMap', Target)[20:24]),
            ]
    vir = GM.CrunchSymbols(GM.VowelSigns,Target)[0]
    Anu = GM.CrunchSymbols(GM.CombiningSigns,Target)[1]

    for i in range(len(ListN)):
        Strng = re.sub('('+Anu+')'+ GM.VedicSvaras + '('+ListC[i]+')(?!' + nukta + ')',ListN[i]+vir+r'\2\3',Strng)

        if Target == "Tamil":
            Strng = re.sub('(ம்)'+ GM.VedicSvaras + '(ʼ)' + '('+ListC[i]+')',ListN[i]+vir+r'\2\4',Strng)

    return Strng

def MalayalamAnusvaraNasal(Strng):
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

## Check Namna, ramya -> Malayalam; fix
def MToAnusvara(Strng,Target):

    M = GM.CrunchList('ConsonantMap', Target)[24] + GM.CrunchList('ViramaMap',Target)[0]
    vir = GM.CrunchList('ViramaMap',Target)[0]
    Anusvara = GM.CrunchList('AyogavahaMap',Target)[1]
    ListC = '|'.join(GM.CrunchSymbols(GM.Characters, Target))

    Chillus= '|'.join([vir, '\u0D7A','\u0D7B','\u0D7C','\u0D7D','\u0D7E'])

    ListCAll = '(' + '|'.join(GM.CrunchSymbols(GM.Characters, Target)) + ')'

    Strng = re.sub(ListCAll + GM.VedicSvaras + '(?<!' + vir + ')'+'('+M+')'+'(?!'+ListC+')',r'\1\2'+Anusvara,Strng)

    for svara in GM.VedicSvarasList:
        Strng = Strng.replace(svara + Anusvara, Anusvara + svara)

    #Strng = Strng.replace(M,Anusvara)

    return Strng

def BengaliYYA(Strng):
    return YYAEverywhere(Strng, 'Bengali')

def YYAEverywhere(Strng, Target):
    Ya = GM.CrunchList('ConsonantMap', Target)[25]
    YYa = GM.CrunchList('NuktaConsonantMap',Target)[7]

    Strng = Strng.replace(Ya, YYa)

    return Strng

def YaToYYa(Strng,Target):
    YYa = GM.CrunchList('NuktaConsonantMap',Target)[7]

    ListC = '|'.join(GM.CrunchSymbols(GM.Characters, Target)+[GM.CrunchList('SignMap',Target)[0]] + ['ৰ'])

    ListS = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSignsNV,Target)) + ')'

    Ya = GM.CrunchList('ConsonantMap', Target)[25]
    vir = GM.CrunchSymbols(GM.VowelSigns,Target)[0]

    ListVarga = '|'.join(GM.CrunchList('ConsonantMap',Target)[0:25])

    if Target in ['Assamese','Bengali', 'Oriya', "Chakma"]:
        Strng = re.sub('('+ListC+')'+ GM.VedicSvaras + Ya,r'\1\2'+YYa,Strng)

        if Target in ['Assamese', 'Bengali']:
            Strng = Strng.replace(vir+YYa,vir+Ya)

        if Target == "Chakma":
            Strng = Strng.replace("𑄠𑄡", "𑄠𑄠")
            Strng = Strng.replace(vir + YYa, "\U00011133" + YYa)

    #print(Target)
    '''
    if Target == 'Oriya':
        #print('I am here for you')
        Strng = re.sub('('+ListVarga+')'+ Ya+'('+ListC+')',r'\1'+YYa+r'\2',Strng)
        Strng = re.sub('('+ListVarga+')'+ ListS + Ya+'('+ListC+')',r'\1'+ r'\2' + YYa+r'\3',Strng)
        Strng = re.sub(Ya + '(?!' + ListC + ')', YYa, Strng)

        Strng = Strng.replace(vir+Ya,vir+YYa)
    '''

    return Strng

#def TamilTranscribe(Strng,Target):
#
#    CM = GM.CrunchList('ConsonantMap',Target)
#    SM = GM.CrunchList('SouthConsonantMap',Target)
#    vir = GM.CrunchSymbols(GM.VowelSigns,Target)[0]
#
#    ConUnVoiced = [CM[x] for x in [0,5,10,15,20]]
#    ConVoicedJ =  [CM[x] for x in [2,7,12,17,22]]
#    ConVoicedS =  [CM[x] for x in [2,31,12,17,22]]
#    ConNasals = '|'.join([CM[x] for x in [4,9,14,19,24]])
#    ConMedials = '|'.join(CM[25:28]+SM[0:2]+SM[3:4])
#    Vowels = '|'.join(GM.CrunchSymbols(GM.Vowels+GM.VowelSignsNV, Target))
#    Aytham = GM.CrunchList('Aytham',Target)[0]
#    Consonants = '|'.join(GM.CrunchSymbols(GM.Consonants,Target))
#    NRA =SM[3] + vir + SM[2]
#    NDRA = CM[14] + vir + CM[12] + vir + CM[26]
#
#    ### Check Siva Siva Mails
#    ### Do something about Eyelash ra in Transliterated text
#
#    for i in range(len(ConUnVoiced)):
#        #Strng = re.sub('('+Vowels+Consonants+')'+ConUnVoiced[i]+'('+Vowels+Consonants+')',r'\1'+ConVoicedS[i]+r'\2',Strng)
#        Strng = re.sub('('+Vowels+'|'+Consonants+'|'+Aytham+')'+ConUnVoiced[i]+'(?!'+vir+')',r'\1'+ConVoicedS[i],Strng)
#        Strng = re.sub('('+ConNasals+')'+'('+vir+')'+'( ?)'+ConUnVoiced[i],r'\1\2\3'+ConVoicedJ[i],Strng)
#        Strng = re.sub('('+ConMedials+')'+'('+vir+')'+ConUnVoiced[i]+'(?!'+vir+')',r'\1\2'+ConVoicedS[i],Strng)
#
#    Strng = Strng.replace(NRA,NDRA)
#    Strng = re.sub('(?<!'+'('+CM[5]+'|'+SM[2]+')'+vir+')'+CM[5]+'(?!'+vir+')',CM[31],Strng)
#
#    Strng = Strng.replace(CM[5]+vir+' '+CM[31],CM[5]+vir+' '+CM[5])
#
#    return Strng

def VaToBa(Strng,Target):

    va = GM.CrunchSymbols(GM.Consonants, Target)[28]
    ba = GM.CrunchSymbols(GM.Consonants, Target)[22]

    if Target == 'Bengali':
        #Strng = Strng.replace('ৎৱ', 'ত্ব')
        pass

    Strng = Strng.replace(va,ba)

    return Strng

def tbadiff(Strng,Target):

    Strng = Strng.replace('ৎব', 'ত্ব')

    return Strng

def RetainDandasIndic(Strng, Target, reverse=False):
    Dandas = GM.CrunchList('SignMap', Target)[1:3]

    if not reverse:
        Strng = Strng.replace('..', Dandas[1])
        Strng = Strng.replace('.', Dandas[0])
    else:
        Strng = Strng.replace(Dandas[0], '.')
        Strng = Strng.replace(Dandas[1], '..')

    return Strng

def RetainIndicNumerals(Strng,Target, reverse=False):
    NativeNumerals = GM.CrunchList('NumeralMap', Target)
    ArabicNumerals = GM.CrunchList('NumeralMap', 'ISO')

    if not reverse:
        for x,y in zip(ArabicNumerals, NativeNumerals):
            Strng = re.sub('(?<!h)' + x, y, Strng)
    else:
        for x,y in zip(NativeNumerals, ArabicNumerals):
            Strng = Strng.replace(x, y)

    return Strng

def RetainRomanNumerals(Strng,Target, reverse=False):
    NativeNumerals = GM.CrunchList('NumeralMap', Target)
    ArabicNumerals = GM.CrunchList('NumeralMap', 'ISO')

    if not reverse:
        for y,x in zip(ArabicNumerals, NativeNumerals):
            Strng = re.sub('(?<!h)' + x, y, Strng)
    else:
        for y,x in zip(NativeNumerals, ArabicNumerals):
            Strng = Strng.replace(x, y)

    return Strng

def indicNumerals(Strng):
    return Strng

def romanFullStop(Strng):
    return Strng

def indicDandas(Strng):
    return Strng

def romanNumerals(Strng):
    return Strng

def RetainTeluguDanda(Strng):
    return RetainDandasIndic(Strng, 'Telugu')

def RetainTeluguNumerals(Strng):
    return RetainIndicNumerals(Strng, 'Telugu')

def RetainTamilDanda(Strng):
    return RetainDandasIndic(Strng, 'Tamil')

def RetainTamilNumerals(Strng):
    return RetainIndicNumerals(Strng, 'Tamil')

def RetainKannadaDanda(Strng):
    return RetainDandasIndic(Strng, 'Kannada')

def RetainKannadaNumerals(Strng):
    return RetainIndicNumerals(Strng, 'Kannada')

def RetainMalayalamDanda(Strng):
    return RetainDandasIndic(Strng, 'Malayalam')

def RetainMalayalamNumerals(Strng):
    return RetainIndicNumerals(Strng, 'Malayalam')

def RetainGujaratiDanda(Strng):
    return RetainDandasIndic(Strng, 'Gujarati')

def RetainGurmukhiNumerals(Strng):
    return RetainIndicNumerals(Strng, 'Gurmukhi')

def RemoveDiacritics(Strng):
    for x in GM.DiacriticsRemovable:
        Strng = Strng.replace(x,'')

    return Strng

def RemoveDiacriticsTamil(Strng):
    for x in GM.DiacriticsRemovableTamil:
        Strng = Strng.replace(x,'')

    return Strng

def SaurashtraHaru(Strng):

    ListC = '|'.join([Saurashtra.ConsonantMap[x] for x in [19,24,26,27]])
    vir = Saurashtra.ViramaMap[0]
    ha = Saurashtra.ConsonantMap[32]

    Strng = re.sub('('+ListC+')'+vir+ha,r'\1'+'\uA8B4',Strng)

    return Strng

def IASTPali(Strng):
    Strng = Strng.replace('l̤', 'ḷ')

    return Strng

def UrduAlternateUU(Strng):
    Strng = Strng.replace("\\u064F\\u0648","\u0648\u0657")

    return Strng

def ThaiLaoTranscription(Strng,Script,shortA,shortAconj,reverse=False, anusvaraChange=True):
    ## For Native lao: aMDa give an'da as intermediate (N doesn't exist in Native Lao )
    ## Hence issues with nasal conversion

    Strng = Strng.replace("\u02BD","")

    cons = "|".join(GM.CrunchSymbols(GM.Consonants, Script)+GM.CrunchList('VowelMap',Script)[0:1])

    if Script == 'Thai':
        cons = "|".join(GM.CrunchSymbols(GM.Consonants, Script)+GM.CrunchList('VowelMap',Script)[0:1] + ['ฮ', 'บ', 'ฝ', 'ด'])

    if Script == 'Lao':
        cons = "|".join(GM.CrunchSymbols(GM.Consonants, Script) + GM.CrunchList('VowelMap',Script)[0:1] + ['ດ','ບ','ຟ'])

    consnA = cons[:-2]
    listVS = "|".join(GM.CrunchSymbols(GM.VowelSignsNV,Script))
    vir = GM.CrunchList('ViramaMap',Script)[0]
    AIUVir = "".join(GM.CrunchList('VowelSignMap',Script)[0:5]+[vir])
    EAIO = "".join(GM.CrunchList('VowelSignMap',Script)[9:12]+GM.CrunchList('SinhalaVowelSignMap',Script)[:])
    Anu = GM.CrunchList('AyogavahaMap',Script)[1]
    ng = GM.CrunchList('ConsonantMap',Script)[4]

    vowA = GM.CrunchList('VowelMap',Script)[0]

    if anusvaraChange:
        Strng = AnusvaraToNasal(Strng,Script)

    if not reverse:
        if Script == 'Thai':
            Strng = re.sub("(["+EAIO+"])"+"("+cons+")"+"("+vir+")",r'\2\3\1',Strng) #Reverse bre, bro etc
            Strng = Strng.replace("\u0E33","\u0E32\u0E4D").replace("\u0E36","\u0E34\u0E4D") # reverse AM, iM
        if Script == 'LaoPali':
            Strng = Strng.replace('ຳ', 'າໍ')

        if anusvaraChange:
            Strng = Strng.replace(Anu, ng + vir)

        Strng = re.sub("(?<!["+EAIO+"])"+"("+cons+")"+"(?!["+AIUVir+"])",r'\1'+shortA,Strng)
        Strng = re.sub("("+shortA+")"+"(?=("+cons+")"+"("+vir+"))",shortAconj,Strng)


        # prahlada -> ประหลาทะ
        Strng = Strng.replace(shortAconj + 'ห'+vir, shortA + 'ห'+vir)
        # katra -> กะตระ
        Strng = re.sub("("+shortAconj+")"+ "(.)("+vir+")([รล])",shortA + r'\2\3\4',Strng)

        ## swap rl
        consswap = "|".join(GM.CrunchSymbols(GM.Consonants, "Thai"))
        Strng = re.sub("("+consswap+")"+"("+vir+")"+"(["+EAIO+"])"+"([รล])",r"\3\1\2\4",Strng)

        ## katro -> กะโตร
        Strng = re.sub(shortAconj +"(["+EAIO+"])", shortA + r'\1', Strng)

        Strng = Strng.replace(vir, '')

        ## Fix sarva --> srrva ; สัรวะ ->
        Strng = Strng.replace(shortAconj + 'ร', 'รร')


        ## Fix Purevowels

    else:
        consOnly = "|".join(GM.CrunchSymbols(GM.Consonants, Script))
        aVow = GM.CrunchList('VowelMap',Script)[0]

        Strng = re.sub('('+consnA+')'+'(?!'+listVS+'|'+shortA+'|'+shortAconj+')',r'\1'+vir,Strng)

        if Script == "Lao":
            Strng = re.sub('(?<!ໂ)' + '(?<!ແ)'+'(?<!ເ)' + '('+aVow+')' + '(?<!ເ)' + shortA+"|"+shortAconj, r"\1",Strng)
            Strng = re.sub('(' + consOnly + ')' + '(?<!າ|ໂ|ແ|ເ)' + shortA+"|"+shortAconj, r"\1",Strng)

            Strng = Strng.replace("຺ຳ", "ຳ") ## Fixing for Lao

        else:
            Strng = re.sub('(?<!โ)' + '(?<!แ)'+'(?<!เ)' + '('+aVow+')' + '(?<!เ)' + shortA+"|"+shortAconj, r"\1",Strng)
            Strng = re.sub('(' + consOnly + ')' + '(?<!า|โ|แ|เ)' + shortA+"|"+shortAconj, r"\1",Strng)

            # ธรรมะ -> dharma
            Strng = re.sub(vir + 'รฺรฺ', 'รฺ', Strng)

            # พรหมา  -> Brahma
            Strng = re.sub(vir + 'หฺ', 'หฺ', Strng)

    return Strng

def ThamTallADisable(Strng):
    Strng = Strng.replace('\u1A64', '\u1A63')

    return Strng

def ThamTallAOthers(Strng):
    TallACons = '|'.join(['ᨧ', 'ᨻ', 'ᩁ', 'ᨽ']) ## ca ba ra bha

    Strng = FixTallA(Strng, TallACons)

    return Strng

#start here

def RephaDoubleMalayalam(Strng):
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

def ThamShiftMaiKangLai(Strng):
    Strng = re.sub('(\u1A58)(.)', r'\2\1', Strng)
    ListV = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns,'TaiTham') + ['ᩤ']) + ')'

    Strng = re.sub('(\u1A58)([\u1A55\u1A56])', r'\2\1', Strng)
    Strng = re.sub('(\u1A58)(\u1A60.)', r'\2\1', Strng)
    Strng = re.sub('(\u1A58)' + ListV, r'\2\1', Strng)
    Strng = re.sub('(\u1A58)' + ListV, r'\2\1', Strng)

    #Strng = Strng.replace('\u1A63\u1A58', '\u1A58\u1A63')

    return Strng

# not used
def FixTallA(Strng, TallACons):
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'TaiTham'))
    Sub =['\u1A55','\u1A56'] # Subjoined Forms of /ra/ and /la/

    E = "ᩮ"
    AA = 'ᩣ'

    # Introduce Tall A: ka + AA -> ka + Tall A
    Strng = re.sub('(?<!᩠)('+TallACons+')'+'('+E+'?)'+AA,r'\1\2'+'ᩤ',Strng)

    ## buddho --> Tall A
    Strng = re.sub('('+TallACons+')(᩠)('+ListC +')'+'('+E+'?)'+AA,r'\1\2\3\4'+'ᩤ',Strng)
    Strng = re.sub('('+TallACons+')(᩠)('+ListC +')'+'(᩠)('+ListC +')'+'('+E+'?)'+AA,r'\1\2\3\4\5\6'+'ᩤ',Strng)

    ### Subjoined
    Strng = re.sub('('+TallACons+')' + "(" + "|".join(Sub) + ")" + '('+E+'?)'+AA, r'\1\2\3' + 'ᩤ', Strng)

    ### reverse Tall-A for those with protruding subCons forms
    reverseSub = '([' + ''.join(['ᨥ', 'ᨫ', 'ᨬ', 'ᨰ', 'ᨸ', 'ᩈ', 'ᨿ', 'ᩇ', 'ᨹ']) + '])'
    Strng = re.sub('(\u1A60)'+ reverseSub + '(\u1A6E\u1A64)', r'\1\2' + '\u1A6E\u1A63', Strng) ## vyo (Tall) to vyo (normal)
    Strng = re.sub('(\u1A60)'+ reverseSub + '(\u1A64)', r'\1\2' + '\u1A63', Strng) ## vyA (Tall) to vyA (normal)

    return Strng


def AvestanConventions(Strng):
    # Fix Nasalization, hma etc

    extraCons = ["\U00010B33","\U00010B32","\U00010B1D","\U00010B12", '𐬣', '𐬝']
    ListC = "|".join(GM.CrunchSymbols(GM.Consonants, "Avestan")+extraCons)
    ListV = "|".join(GM.CrunchSymbols(GM.Vowels,"Avestan"))
    ListA = "|".join(GM.CrunchSymbols(GM.Vowels + GM.Consonants,"Avestan")+extraCons+ ['𐬄','𐬅'])


    ii = Avestan.VowelMap[2] * 2
    uu = Avestan.VowelMap[4] * 2
    i = Avestan.VowelMap[2]
    a = Avestan.VowelMap[0]

    kha = Avestan.ConsonantMap[1]
    nga = Avestan.ConsonantMap[4]
    ya = Avestan.ConsonantMap[25]
    va = Avestan.ConsonantMap[28]
    ta = Avestan.ConsonantMap[15]
    tha = Avestan.ConsonantMap[16]
    dha = Avestan.ConsonantMap[18]
    na = Avestan.ConsonantMap[19]
    ma = Avestan.ConsonantMap[24]
    kb = "|".join([Avestan.ConsonantMap[0], Avestan.ConsonantMap[22]])
    nna = Avestan.ConsonantMap[14]
    sha = Avestan.ConsonantMap[29]

    VelarDental = "|".join(Avestan.ConsonantMap[0:4]+Avestan.ConsonantMap[15:19])

    Strng = Strng.replace(nga+i, '𐬣'+ i)

    ## Conventions from AVestan Combined Grammer

    Strng = re.sub(a + '([' + na + ma + '])' + '(?!' +  ListA + ')', '𐬆' + r'\1' , Strng) ## Soft -Ta end of words

    Strng = re.sub("("+na+")"+"("+VelarDental+")",nna+r'\2',Strng) ##

    Strng = re.sub("("+kha+")"+"(?="+ii+")","\U00010B12",Strng)
    Strng = re.sub("("+sha+")"+"(?="+ii+")","\U00010B33",Strng)

    Strng = re.sub("("+tha+"|"+dha+")"+"("+uu+")",r'\1'"𐬡",Strng)

    Strng = re.sub("("+ta+")"+"(?!"+"(("+ListV+")"+"|"+"("+ListC+"))"+")","\U00010B1D",Strng)
    Strng = re.sub("("+ta+")"+"(?="+"("+kb+")"+")",'\U00010B1D',Strng)

    return Strng

# not used
def TaiThamO(Strng):
    Strng = Strng.replace("\u1A6E\u1A63","\u1A70")

    return Strng

# not used
def TaiThamHighNga(Strng):
    Strng = Strng.replace('\u1A58','\u1A59')

    return Strng

# not used
def TaiThamMoveNnga(Strng):
    Strng = re.sub('(.)(\u1A58)',r'\2\1',Strng) # Probably its u1A59

    return Strng

def UrduRemoveShortVowels(Strng):
    ShortVowels = ['\u0652','\u064E','\u0650','\u064F', '\u0658']

    for vow in ShortVowels:
        Strng = Strng.replace(vow,"")

    return Strng

def LatinPipes(Strng):
    ###

    return Strng

# not used
def PhagsPaRearrange(Strng,Target):
    vir = GM.CrunchList('ViramaMap', Target)[0]
    ListC = '|'.join(GM.CrunchSymbols(GM.Consonants,Target))
    ListV = '|'.join(GM.CrunchSymbols(GM.Vowels,Target))
    ListVS = '|'.join(GM.CrunchSymbols(GM.VowelSignsNV,Target))

    Strng = re.sub("(?<!( |"+vir+"))"+"("+ListC+")"+"(?= )",r'\2'+vir,Strng)
    #print Strng

    Strng = Strng.replace(" ","").replace("᠂"," ").replace("᠃"," ")
    return Strng

# not used
def DevanagariAVowels(Strng):
    oldVowels = Devanagari.VowelMap[2:12]+Devanagari.SouthVowelMap[:1]
    a = Devanagari.VowelMap[0]
    newAVowels = [a+x for x in Devanagari.VowelSignMap[1:11]+Devanagari.SouthVowelSignMap[:1]]

    for x,y in zip(oldVowels,newAVowels):
        Strng = Strng.replace(x,y)

    return Strng

# not used
def AnusvaraToNasalIPA(Strng):

    Strng = Strng.replace("̃k","ŋk")
    Strng = Strng.replace("̃g","ŋg")

    Strng = Strng.replace("̃c","ɲc")
    Strng = Strng.replace("̃j","ɲj")

    Strng = Strng.replace("̃t̪","n̪t̪")
    Strng = Strng.replace("̃d̪","n̪d̪")

    Strng = Strng.replace("̃ɖ","ɳɖ")
    Strng = Strng.replace("̃ʈ","ɳʈ")

    Strng = Strng.replace("̃ːk","ːŋk")
    Strng = Strng.replace("̃ːg","ːŋg")

    Strng = Strng.replace("̃ːc","ːɲc")
    Strng = Strng.replace("̃ːj","ːɲj")

    Strng = Strng.replace("̃ːt̪","ːn̪t̪")
    Strng = Strng.replace("̃ːd̪","ːn̪d̪")

    Strng = Strng.replace("̃ːɖ","ːɳɖ")
    Strng = Strng.replace("̃ːʈ","ːɳʈ")

    return Strng

# not used
def IPARemoveCross(Strng):

    Strng = Strng.replace('×','')

    return Strng

# not used
def ChakmaAVowels(Strng):

    return Strng

def swapEe(Strng):
    Strng = Strng.replace('E', 'X@X@')
    Strng = Strng.replace('e', 'E')
    Strng = Strng.replace('X@X@', 'e')

    Strng = Strng.replace('O', 'X@X@')
    Strng = Strng.replace('o', 'O')
    Strng = Strng.replace('X@X@', 'o')

    return Strng

def capitalizeSentence(Strng):
    Strng = re.sub(r"(\A\w)|"+            # start of string
             "(?<!\.\w)([\.?!]\s*)\w|"+     # after a ?/!/. and a space,
             "\w(?:\.\w)|"+
             "(\n)\w|"+               # start/middle of acronym
             "(\n(\"|\“|\'|\‘))\w|"+
             "(?<=\w\.)\w",               # end of acronym
             lambda x: x.group().upper(),
             Strng)

    Strng = re.sub(r"(@)(.)", lambda x: x.groups()[1].upper(), Strng)

    return Strng

