# -*- coding: utf-8 -*-

### Introduce Nasal to Anusvara for scripts lacking nasal letters but having Anusvara/Chandrabindu

import importlib, string
import re
from functools import reduce
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

def CrunchSymbols(Part,Script):
    ModScript = importlib.import_module(ScriptPath(Script))
    return reduce(lambda x,y : x+y,[getattr(ModScript,Var) for Var in Part])

def CrunchList(List,Script):
    try:
      ModScript = importlib.import_module(ScriptPath(Script))
    except:
      import logging
      logging.exception('The script ' + Script + ' cannot be found')
      return ''

    return getattr(ModScript,List)

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
InterAdd = {'VowelMap': '\U000F0000', 'VowelSignMap': '\U000F0000', 'ConsonantMap':'\U000F2000', 'SignMap':'\U000F3000', 'AyogavahaMap':'\U000F4000', 'ModernVowelMap': '\U000F5000', 'ModernVowelSignMap':'\U000F5000'}

def add_additional_chars(script_char_map, file_script):
    for charlist in CharmapLists:
        mapping_char = getattr(fb, charlist)
        #print('vinodh')
        #print(file_script)
        ModScript = importlib.import_module(ScriptPath(file_script))
        InterAddIndex = ord(InterAdd[charlist])
        for num, mapng in enumerate(mapping_char.items()):
                char, mapping = mapng
                if file_script in mapping.keys():
                        script_char_map[charlist].append(mapping[file_script])
                elif file_script == 'Inter':
                        script_char_map[charlist].append(chr(InterAddIndex+num))
                else:
                    if file_script in ReversibleScripts:
                        mapchar = 'OthersRev'
                    else:
                        mapchar = 'OthersNonRev'

                    if mapping[mapchar][0] == -1:
                         first_char = ''
                    else:
                         #print(charlist)
                         #print(mapping[mapchar][0])
                         first_char= script_char_map[charlist][mapping[mapchar][0]]

                    if len(mapping[mapchar]) > 1:
                        if 'nukta' in mapping[mapchar]:
                            second_char = ModScript.NuktaMap[0]
                        else:
                            second_char = mapping[mapchar][1]

                    if len(mapping[mapchar]) == 1:
                        script_char_map[charlist].append(first_char)
                    else:
                        script_char_map[charlist].append(first_char+second_char)

