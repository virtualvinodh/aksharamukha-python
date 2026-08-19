# -*- coding: utf-8 -*-

### Introduce Nasal to Anusvara for scripts lacking nasal letters but having Anusvara/Chandrabindu

import importlib, string
import inspect
import re
from functools import reduce, lru_cache
from . import FallBack as fb

# Crunch Symbols

def ScriptPath(Script):
    if Script in MainIndic:
        return 'aksharamukha.ScriptMap.MainIndic.'+Script
    elif Script in EastIndic:
        return 'aksharamukha.ScriptMap.EastIndic.'+Script
    elif Script in Roman:
        return 'aksharamukha.ScriptMap.Roman.'+Script
    elif Script in NonIndic:
        return 'aksharamukha.ScriptMap.NonIndic.'+Script

def retCharList(charList):
    return globals()[charList]

@lru_cache(maxsize=None)
def _crunchSymbolsCached(Part,Script):
    ModScript = importlib.import_module(ScriptPath(Script))
    return reduce(lambda x,y : x+y,[getattr(ModScript,Var) for Var in Part])

def CrunchSymbols(Part,Script):
    # Part is a list (unhashable), so the cache key is built from a tuple;
    # a copy is returned so callers can't mutate the cached result.
    return list(_crunchSymbolsCached(tuple(Part),Script))

@lru_cache(maxsize=None)
def _crunchListCached(List,Script):
    try:
      ModScript = importlib.import_module(ScriptPath(Script))
    except:
      import logging
      logging.exception('The script ' + Script + ' cannot be found')
      return ''

    return getattr(ModScript,List)

def CrunchList(List,Script):
    result = _crunchListCached(List,Script)
    # copy on the way out for the same reason as CrunchSymbols above
    return list(result) if isinstance(result, list) else result

# Public (not module-local) since ConvertFix.FixIndicOutput's own
# globals()-based dispatch needs this same check and can't go through
# resolve() below (its "module" is obtained via globals(), a dict, which
# doesn't support the getattr() resolve() relies on).
@lru_cache(maxsize=None)
def accepts_ctx(fn):
    try:
        return 'ctx' in inspect.signature(fn).parameters
    except (TypeError, ValueError):
        return False

def resolve(module, name, txt, *extra, optional=False, ctx=None, **kwargs):
    # Single home for the reflection-dispatch pattern ("call the function
    # named by this string, if it exists") repeated ~9 times across the
    # codebase. optional=False (the default) preserves the plain-getattr
    # behaviour those call sites already had: an unknown name raises
    # AttributeError loudly, e.g. a typo'd pre/post-option name. optional=True
    # is for the sites that treat "no such function" as "this script has no
    # override, leave the text unchanged" - previously a try/except
    # AttributeError: pass wrapped around the call.
    #
    # ctx: passed through only to functions that actually declare a `ctx`
    # parameter (mirrors Options.py's call_pre_option/call_post_option) -
    # every existing Fix*/PreProcess/PostProcess function is untouched by
    # this, since none of them declare it yet.
    if optional:
        fn = getattr(module, name, None)
        if fn is None:
            return txt
    else:
        fn = getattr(module, name)
    if ctx is not None and accepts_ctx(fn):
        kwargs = dict(kwargs, ctx=ctx)
    return fn(txt, *extra, **kwargs)

#Introduce in all Latin Conversions
def EscapeChar(Strng):
    punct = "".join(['\\'+x for x in string.punctuation])

    return re.sub('('+punct+')',r'\\'+r'\1',Strng)


# Collection of Symbols

VedicSvaras = '('+ '|'.join(['᳚', '॑', '॒']) + ')?'
VedicSvarasList = ['᳚', '॑', '॒']

Vowels = ['VowelMap','SouthVowelMap','ModernVowelMap','SinhalaVowelMap']
VowelSignsNV = ['VowelSignMap','SouthVowelSignMap','ModernVowelSignMap','SinhalaVowelSignMap']
VowelSigns = ['ViramaMap','VowelSignMap','SouthVowelSignMap','ModernVowelSignMap','SinhalaVowelSignMap']
CombiningSigns = ['AyogavahaMap','NuktaMap']
Consonants = ['ConsonantMap','SouthConsonantMap','NuktaConsonantMap','SinhalaConsonantMap']

Signs = ['SignMap']
Numerals = ['NumeralMap']
Aytham =['Aytham']
om = ['OmMap']
virama = ['ViramaMap']

## Script Paths
MainIndic = ['GurmukhiLoC', 'LimbuLoC', 'BengaliRaBa', 'Nandinagari','Shahmukhi', 'TamilExtended','MasaramGondi','GunjalaGondi','Dogra', 'Ranjana', 'Khojki','GranthaGrantamil', 'Multani', 'Ahom', 'Mahajani','SiddhamDevanagari', 'Vatteluttu', 'GranthaPandya', 'Khudawadi', 'Bhaiksuki', 'Sharada', 'Newa', 'SylotiNagri', 'Takri', 'Tirhuta', 'Modi', 'Kaithi', 'Kharoshthi','Lepcha','Chakma','Brahmi','MeeteiMayek','Limbu','Assamese','Bengali','Devanagari','Grantha','Gujarati','Gurmukhi','Kannada','Malayalam','Oriya','Saurashtra','Sinhala','Tamil','TamilBrahmi','TamilGrantha','Telugu','Urdu']
EastIndic =['DivesAkuru', 'TibetanLoC', 'BatakLoC', 'ThamLoC', 'KhmerLoC', 'ShanLoC', 'Makasar', 'Kawi', 'Pallava', 'LaoTham', 'LueTham', 'KhuenTham', 'Marchen', 'Soyombo', 'KhomThai', 'KhamtiShan', 'TaiLaing', 'Mon', 'Shan', 'ZanabazarSquare','Rejang', 'Lao2','Buhid', 'Hanunoo', 'Siddham', 'Tibetan','Lao','TaiTham','Cham','BatakKaro','BatakPakpak','BatakSima','BatakToba','BatakManda','LaoPali','PhagsPa','Buginese','Tagbanwa','Tagalog','Sundanese','Balinese','Burmese','Javanese','Khmer','Siddham','Ranjana','Thaana','Thai', 'BurmeseALALC']
NonIndic = ['OldPersian', 'Hebrew']
Roman =['BatakLoCRomanLoC','GurmukhiLoCRomanLoC','TibetanLoCRomanLoC', 'LimbuLoCRomanLoC', 'BalineseSimpleRomanLoC', 'BalineseRomanLoC', 'JavaneseSimpleRomanLoC', 'JavaneseRomanLoC', 'BatakKaroRomanLoC', 'BatakMandaRomanLoC','BatakPakpakRomanLoC','BatakSimaRomanLoC','BatakTobaRomanLoC', 'GurmukhiRomanLoC', 'TibetanRomanLoC', 'LimbuRomanLoC', 'KannadaRomanLoC', 'TeluguRomanLoC', 'SinhalaRomanLoC', 'OriyaRomanLoC', 'AssameseRomanLoC', 'BengaliRomanLoC', 'GujaratiRomanLoC', 'DevanagariRomanLoC', 'ThamLoCRomanLoC', 'KhmerLoCRomanLoC', 'RomanLoC', 'ShanLoCRomanLoC', 'ThamLoCRomanLoC', 'KhmerLoCRomanLoC', 'ShanLoCRomanLoC', 'BurmeseRomanLoC', 'RomanSemitic', 'RomanColloquial', 'ISOPali', 'RomanKana', 'BarahaNorth', 'BarahaSouth', 'Mongolian', 'SLP1', 'Wancho', 'Mro', 'IASTPali', 'HanifiRohingya', 'Ariyaka', 'RomanReadable', 'Aksharaa', 'WarangCiti', 'SoraSompeng',"WX-kok",'Avestan','HK','IAST','ISO','Itrans','Titus','Titus','Velthuis','WX','Inter','IPA','TolongSiki','Santali','RussianCyrillic']
RomanDiacritic = ['IAST','Titus','ISO','IPA', 'IASTPali', 'ISOPali', 'BurmeseRomanLoC', 'ISOLOC', 'RomanSemitic', 'ShanLoCRomanLoC', 'KhmerLoCRomanLoC']

ScriptCategory = {}

ScriptCategory['IndianMain'] = ['GranthaGrantamil','Assamese','Bengali','Devanagari','Gujarati','Gurmukhi','Kannada','Malayalam','Oriya','Sinhala','Tamil','Telugu','Urdu']
ScriptCategory['IndianMinority'] = ['Brahmi','Chakma','Grantha','Lepcha','Limbu','MeeteiMayek','Saurashtra','TamilBrahmi','TamilGrantha', 'Kaithi']
ScriptCategory['EastAsianPaliSans'] = ['Balinese','Burmese','Cham','Javanese','Khmer','LaoPali','Lao','PhagsPa','TaiTham','Thaana','Thai','Tibetan']
ScriptCategory['EastAsianIndFili'] = ['BatakKaro','BatakManda','BatakPakpak','BatakSima','BatakToba','Buginese','Sundanese','Tagalog','Tagbanwa']
ScriptCategory['IndianAlpha'] = ['Santali','TolongSiki']
ScriptCategory['RomanDiacritic'] = ['IAST','IPA','ISO','Titus', 'IASTPali']
ScriptCategory['RomanNonDiacritic'] = ['HK','Itrans','RussianCyrillic','Velthuis','WX']
ScriptCategory['NonIndic'] = ['Avestan','OldPersian']

Inter = "Inter"

Characters = Vowels + VowelSigns + CombiningSigns + Consonants
CharactersNV = Vowels + VowelSignsNV + CombiningSigns + Consonants

Diacritics = ['ʽ', '\u00B7', '\u00B9','\u00B2','\u00B3','\u2074','\u2081','\u2082','\u2083','\u2084']
DiacriticsRemovable = ['ʼ', 'ˇ', 'ˆ', '˘', '\u00B7']
DiacriticsRemovableTamil = ['ˇ', 'ˆ', '˘', '\u00B7']

ScriptAll = ['Aytham', 'Signs', 'CombiningSigns', 'VowelSigns', 'Vowels', 'Consonants', 'Numerals']

IndicScripts = [
               'DivesAkuru',
               'TibetanLoC',
               #'BatakLoC',
               'GurmukhiLoC',
               'LimbuLoC',
               'ThamLoC',
               'KhmerLoC',
               'ShanLoC',
               'BengaliRaBa',
               'RomanSemitic',
                'Makasar',
                'Nandinagari',
                'Kawi',
                'Shahmukhi',
                'Pallava',
                'Hebrew',
               'LaoTham',
               'LueTham',
               'KhuenTham',
               'TamilExtended',
               'Marchen',
               'MasaramGondi',
               'GunjalaGondi',
               'Soyombo',
               'Dogra',
               'KhomThai',
               'KhamtiShan',
               'TaiLaing',
               'Mon',
               'Khojki',
               'Shan',
               'Ranjana',
               'ZanabazarSquare',
               'Rejang',
               'GranthaGrantamil',
               'Devanagari',
               'Multani',
               'Ahom',
               'Mahajani',
               'Lao2',
               'Hanunoo',
               'Buhid',
               'Siddham',
               'SiddhamDevanagari',
               'GranthaPandya',
               'Vatteluttu',
               'Khudawadi',
               'Bhaiksuki',
               'Sharada',
               'Newa',
               'Takri',
               'SylotiNagri',
               'Tirhuta',
               'Modi',
               'Kaithi',
               'Kharoshthi',
               'Telugu',
               'Kannada',
               'Malayalam',
               'Gujarati',
               'Bengali',
               'Oriya',
               'Gurmukhi',
               'Tamil',
               'Assamese',
               'Saurashtra',
               'TamilBrahmi',
               'Grantha',
               'TamilGrantha',
               'Sinhala',
               'Khmer',
               'Burmese',
               'Urdu',
               'Balinese',
               'Javanese',
               'Thaana',
               'Tibetan',
               'Thai',
               'OldPersian',
               'Limbu',
               'Lepcha',
               'Sundanese',
               'Tagalog',
               'Tagbanwa',
               'Buginese',
               'Chakma',
               'PhagsPa',
               'MeeteiMayek',
               'LaoPali',
               'BatakKaro','BatakPakpak','BatakSima','BatakToba','BatakManda',
               'Cham',
               'TaiTham',
               'Lao',
               'Brahmi'
               ]

SiddhamRanjana = ['Ranjana']

LatinScripts = [#'BatakLoCRomanLoC', 'BatakKaroRomanLoC', 'BatakMandaRomanLoC','BatakPakpakRomanLoC','BatakSimaRomanLoC','BatakTobaRomanLoC', 'GurmukhiRomanLoC' \
                'GurmukhiLoCRomanLoC', 'TibetanLoCRomanLoC', 'LimbuLoCRomanLoC', 'BalineseSimpleRomanLoC', 'BalineseRomanLoC', 'JavaneseSimpleRomanLoC', 'JavaneseRomanLoC', 'KannadaRomanLoC', 'TeluguRomanLoC', 'SinhalaRomanLoC', 'OriyaRomanLoC', 'AssameseRomanLoC', 'BengaliRomanLoC', 'GujaratiRomanLoC', 'DevanagariRomanLoC', 'ThamLoCRomanLoC', 'KhmerLoCRomanLoC', 'RomanLoC', 'ShanLoCRomanLoC', 'BurmeseRomanLoC', 'RomanColloquial', 'ISOPali', 'RomanKana', 'BarahaNorth', 'BarahaSouth', 'Mongolian', 'SLP1', 'Wancho', 'Mro', 'IASTPali', 'HanifiRohingya','Ariyaka', 'RomanReadable', 'Aksharaa', 'WarangCiti', 'SoraSompeng','WX-kok','Avestan','ISO','IAST','HK','Titus','Itrans','Velthuis','WX','Inter','IPA','TolongSiki','Santali','RussianCyrillic']

Gemination =  {
               'Gurmukhi' : '\u0A71',
               'Thaana' : '\u0787\u07B0',
               'Urdu': '\u0651',
               'Shahmukhi': '\u0651',
               'Grantha': '𑌂',
               'Malayalam': 'ം',
               'Khojki': '\U00011237',
               'Buginese': '',
               'Buhid': '',
               'Tagbanwa': '',
               'Makasar': ''
              }

pipeScripts = ["HK", "IASTPali", "IAST", "ISO", "Itrans", "ISOPali"]

Transliteration = ['IASTPali', 'RomanReadable', 'Aksharaa', 'ISO', 'IAST', 'HK','Titus','Itrans','Velthuis', 'WX', 'IPA', 'RussianCyrillic', 'IASTPali', 'ISOPali', 'RomanLoC']

## Indic scripts that use roman numerals
romanNumeralScripts = ['Tamil', 'Gurmukhi', 'Malayalam', 'Telugu']
## Indic scripts that use periods
romanPunctscripts = ['Tamil', 'Kannada', 'Malayalam', 'Telugu', 'Gujarati']

## List of supported LoC scripts
LoCScripts = ['Burmese', 'Shan', 'Khmer', 'KhuenTham', 'TaiTham', 'LaoTham', 'LueTham', 'Kannada', 'Tamil', 'Malayalam', 'Sinhala', 'Telugu', 'Kannada', 'Oriya', 'Assamese', 'Bengali', 'Gujarati', 'Devanagari', 'Balinese', 'Javanese', 'BatakKaro', 'BatakManda','BatakPakpak','BatakSima','BatakToba','Gurmukhi', 'Tibetan', 'Limbu']

#Modified Src Input Map for LoC script
#speicalpostpre process
LocPostPre = ['Burmese', 'Shan', 'Khmer', 'ThamLoC', 'ShanLoC', 'KhmerLoC']
#spcial Loc source
LoCSrcMap =  ['Shan', 'Khmer', 'Gurmukhi', 'Limbu', 'Tibetan']
#Sepcial Map for RomanLoC target
LoCTgtMap = ['Burmese', 'Shan', 'Khmer', 'KhuenTham', 'TaiTham', 'LaoTham', 'LueTham', 'ThamLoC', 'ShanLoC', 'KhmerLoC', 'Kannada', 'Telugu', 'Sinhala', 'Oriya', 'Assamese', 'Bengali', 'Gujarati', 'Devanagari', 'Balinese', 'Javanese', 'Batak', 'Gurmukhi', 'GurmukhiLoC', 'Tibetan', 'Limbu', 'LimbuLoC', 'Tibetan', 'TibetanLoC']

#They're basically modified ISO
LoCTgtISO = ['Tamil', 'Malayalam']

##
LoCTgtPostOptions = {
    'Telugu': ['AnusvaratoNasalASTISO', 'RomanLoCChandrabindu'],
    'Kannada': ['AnusvaratoNasalASTISO', 'RomanLoCChandrabindu'],
    'Malayalam': ['AnusvaratoNasalASTISO', 'RomanLoCChandrabindu', 'MalayalamRomanLoCFix', 'mDotBelowToAbove'],
    'Sinhala': ['AnusvaratoNasalASTISO',  'SinhalaSannakaNasalization', 'RomanLoCChandrabindu'],
    'Oriya': ['AnusvaratoNasalASTISO', 'RomanLoCChandrabindu'],
    'Assamese': ['RomanLoCChandrabindu'],
    'GurmukhiLoC': ['GurmukhiRomanLoCFix'],
    'Bengali': ['RomanLoCChandrabindu'],
    'Gujarati': ['AnusvaratoNasalASTISO', 'RomanLoCChandrabindu'],
    'Devanagari': ['AnusvaratoNasalASTISO', 'RomanLoCChandrabindu', 'DevanagariRomanLoCFix'],
    'Balinese': ['BalineseRomanLoCFix'],
    'Javanese': ['JavaneseRomanLoCFix'],
    'TibetanLoC': ['TibetanLoCRomanLoCFix']
}

##
LoCTgtPreOptions = {
    'Assamese': ['KhandaTaRomanLoC'],
    'Bengali': ['KhandaTaRomanLoC', 'BengaliSubojinedVa'],
}

##
LoCSrcPostOptions = {
    'Assamese': ['KhandaTaRomanLoC'],
    'Bengali': ['KhandaTaRomanLoC'],
    'Telugu':['TeluguArasunnaChandrabindu']
}

##
LoCSrcPreOptions = {
    'Telugu': ['RomanLoCChandrabindu'],
    'Kannada': ['RomanLoCChandrabindu'],
    'Malayalam': ['RomanLoCChandrabindu', 'MalayalamRomanLoCFix'],
    'Sinhala': ['RomanLoCChandrabindu'],
    'Oriya': ['RomanLoCChandrabindu'],
    'Assamese': ['RomanLoCChandrabindu'],
    'Bengali': ['RomanLoCChandrabindu'],
    'Gujarati': [ 'RomanLoCChandrabindu'],
    'Devanagari': ['RomanLoCChandrabindu', 'DevanagariRomanLoCFix'],
    'Balinese': ['BalineseRomanLoCFix'],
    'Javanese': ['JavaneseRomanLoCFix'],
    'TibetanLoC': ['TibetanLoCRomanLoCFix']
}

SemiticScripts = ['Arab-Pa', 'Syrj', 'Syrn', 'Syre', 'Thaa', 'Arab-Ur', 'Type', 'Hebr-Ar', 'Arab-Fa', 'Latn', 'Arab', 'Ethi', 'Armi', 'Brah', 'Chrs', 'Egyp', 'Elym', 'Grek', 'Hatr', 'Hebr', 'Mani', 'Narb', 'Nbat', 'Palm', 'Phli', 'Phlp', 'Phnx', 'Prti', 'Samr', 'Sarb', 'Sogd', 'Sogo', 'Ugar']

## Add new consonants here

SemiticConsonants = ['ʾ','b','v','g','j','d','h','w','z','ḥ','ṭ','y','k','l','m','n','s','ʿ','f','ṣ','q','r','š','t','ḍ','ḏ','ḫ','ġ','ṯ','ẓ','p','č','ž','ɖ','ʈ','ʂ','ɭ','ɲ','ɳ','ɽ','ʰ'] # make a list

SemiticVowels = ['a', 'ā', 'i', 'ī', 'u', 'ū', 'ē', 'ō', 'e', 'o', '#', '\u033D']

semiticVowelsAll = '꞉ a ā i ī u ū e ē o ō a̮ ̽ ā̮ ĕ ă ŏ aŷ aŵ a aⁿ uⁿ iⁿ'.split(' ')
vowelsInitialAll = 'ˀā̮̂ ā̮̂ â ā̂ î ī̂ û ū̂ ê ē̂ ô ō̂ âŷ âŵ ˀâ ˀî'.split(' ')

semiticISO = {
                'ISO259': 'Hebrew',
                'HebrewSBL': 'Hebrew',
                'ISO233': 'Arab',
                'PersianDMG': 'Arab-Fa'
}

ReversibleScripts = ['Devanagari', 'Tamil', 'Telugu', 'Kannada', 'Sinhala', 'Oriya', 'Gujarati', 'Bengali', 'Assamese', 'Malayalam', 'Gurmukhi']

RomanReversible = ['IAST', 'HK', 'Itrans', 'Velthuis', 'Titus', 'WX', 'RussianCyrillic', 'ISO']

CharmapLists = ['VowelMap', 'VowelSignMap', 'ConsonantMap', 'SignMap', 'AyogavahaMap', 'ModernVowelMap', 'ModernVowelSignMap']
# VowelMap/VowelSignMap (and ModernVowelMap/ModernVowelSignMap) deliberately
# SHARE a base codepoint. convertScript's Latin->Indic path builds the
# 'Inter' pivot representation of a vowel using only the VowelMap mapping
# (convertInter's ScriptAll has no VowelSigns group - Latin vowels are always
# "independent" going in), then RomanPreFix inserts a DepV marker in front of
# syllable-medial occurrences and _build_char_pairs looks those up as
# DepV + <VowelSignMap's Inter placeholder>. That lookup only hits because
# VowelSignMap's placeholder for a given vowel equals VowelMap's placeholder
# for the same vowel - the shared base isn't a leftover collision, it's what
# makes the independent/dependent-vowel disambiguation trick work. (Given
# separate bases instead, per category, RomanLoC->Khmer/Shan/TaiTham
# round-trips broke - confirmed empirically, not just by reasoning.)
InterAdd = {'VowelMap': '\U000F0000', 'VowelSignMap': '\U000F0000', 'ConsonantMap':'\U000F2000', 'SignMap':'\U000F3000', 'AyogavahaMap':'\U000F4000', 'ModernVowelMap': '\U000F5000', 'ModernVowelSignMap':'\U000F5000'}

# Canonical per-category letter orders, used to resolve the mnemonic HK-style
# names FallBack.py's OthersRev/OthersNonRev/Others base index can use
# instead of a raw integer (e.g. 'u' instead of 4). These match HK.py's own
# literal base-list definitions exactly (VOWEL_SIGN_NAMES = VOWEL_NAMES[1:]
# because HK.py itself defines VowelSignMap = VowelMap[1:]; MODERN_VOWEL_NAMES
# covers both Modern forms because HK.py defines ModernVowelSignMap =
# ModernVowelMap[:], unshifted) - not an independently-maintained guess.
VOWEL_NAMES = ['a', 'A', 'i', 'I', 'u', 'U', 'R', 'RR', 'lR', 'lRR', 'e', 'ai', 'o', 'au']
VOWEL_SIGN_NAMES = VOWEL_NAMES[1:]
MODERN_VOWEL_NAMES = ['aE', 'aO']
CONSONANT_NAMES = ['k', 'kh', 'g', 'gh', 'G', 'c', 'ch', 'j', 'jh', 'J', 'T', 'Th', 'D', 'Dh', 'N',
                    't', 'th', 'd', 'dh', 'n', 'p', 'ph', 'b', 'bh', 'm', 'y', 'r', 'l', 'v', 'z', 'S', 's', 'h']
AYOGAVAHA_NAMES = ['~', 'M', 'H']
NAME_TABLES = {
    'VowelMap': VOWEL_NAMES,
    'VowelSignMap': VOWEL_SIGN_NAMES,
    'ConsonantMap': CONSONANT_NAMES,
    'SignMap': None,
    'AyogavahaMap': AYOGAVAHA_NAMES,
    'ModernVowelMap': MODERN_VOWEL_NAMES,
    'ModernVowelSignMap': MODERN_VOWEL_NAMES,
}

def _resolve_base_index(charlist, base):
    # base is normally an HK-style name (str) resolved against this
    # category's own canonical order. None (no base character) is handled by
    # the caller before this is even reached. One FallBack.py entry
    # (VowelPairs['Thamclosedau']'s dependent form) still carries a raw int
    # past the canonical range - it's always meant a previously-synthesized
    # fallback character at that position in whichever script requests it,
    # existing order-dependent behavior predating this naming scheme, left
    # as-is rather than silently reinterpreted.
    if isinstance(base, str):
        return NAME_TABLES[charlist].index(base)
    return base

def add_additional_chars(script_char_map, file_script):
    for charlist in CharmapLists:
        mapping_char = getattr(fb, charlist)
        ModScript = importlib.import_module(ScriptPath(file_script))
        InterAddIndex = ord(InterAdd[charlist])
        for num, mapng in enumerate(mapping_char.items()):
                char, mapping = mapng
                # A key can be a single script name, or (when several
                # scripts share the same value) a tuple of script names.
                direct = mapping.get(file_script)
                if direct is None:
                    for k in mapping:
                        if isinstance(k, tuple) and file_script in k:
                            direct = mapping[k]
                            break
                if direct is not None:
                        script_char_map[charlist].append(direct)
                elif file_script == 'Inter':
                        script_char_map[charlist].append(chr(InterAddIndex+num))
                else:
                    if file_script in ReversibleScripts:
                        mapchar = 'OthersRev'
                    else:
                        mapchar = 'OthersNonRev'

                    # 'Others' is the single spec used for both reversible and
                    # non-reversible scripts, when they don't need to differ -
                    # OthersRev/OthersNonRev only appear explicitly for the
                    # rare entries where the two genuinely need different
                    # suffixes.
                    spec = mapping.get(mapchar, mapping.get('Others'))

                    base_raw = spec[0]
                    if base_raw is None:
                         first_char = ''
                    else:
                         base_index = _resolve_base_index(charlist, base_raw)
                         if base_index >= len(script_char_map[charlist]):
                             raise ValueError(
                                 "FallBack.py entry %r's %s base %r is out of range "
                                 "for %s's own %s (only %d entries so far) - a bad fallback "
                                 "index in FallBack.py, not a problem with %s itself."
                                 % (char, mapchar, base_raw, file_script, charlist,
                                    len(script_char_map[charlist]), file_script))
                         first_char = script_char_map[charlist][base_index]

                    if len(spec) > 1:
                        # fb.NUKTA is a sentinel object, not a literal suffix - checked
                        # by identity, so no real suffix string could ever collide with it.
                        if spec[1] is fb.NUKTA:
                            second_char = ModScript.NuktaMap[0]
                        else:
                            second_char = spec[1]

                    if len(spec) == 1:
                        script_char_map[charlist].append(first_char)
                    else:
                        script_char_map[charlist].append(first_char+second_char)

