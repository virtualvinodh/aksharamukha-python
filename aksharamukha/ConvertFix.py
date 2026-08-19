# -*- coding: utf-8 -*-
from . import GeneralMap as GM
from aksharamukha.ScriptMap.Roman import Avestan, IAST
from aksharamukha.ScriptMap.MainIndic import Ahom, Tamil,TamilGrantha, Limbu, MeeteiMayek, Urdu, Lepcha, Chakma, Kannada, Gurmukhi, Newa
from aksharamukha.ScriptMap.EastIndic import Lao, TaiTham,Tibetan,Burmese,Khmer,Balinese,Javanese,Thai, Sundanese, PhagsPa, Cham, Thaana, Rejang, ZanabazarSquare, Makasar, Kawi
from . import PostProcess
import re

## Test Syllable initial conjunct

## ListC check.. if LLA is there in ListC... just now it has only Consonant Map
### Rewrite all ListC, ListV as sorted(List,key=len,reverse=True)

def lenSort(x,y):
    if(len(x[0]) > len(y[0])):
        return -1
    else:
        return 0

def OriyaIPAFixPre(Strng):
    Strng = Strng.replace('ଂ', 'ଙ୍')
    Strng = Strng.replace('ଃ', 'ହ୍')

    return Strng

def SinhalaIPAFix(Strng):
    consonants = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'IPA')) + ')'

    Strng = re.sub('^' + consonants + '(ə)', r'\1ʌ', Strng)
    Strng = re.sub('(\s)' + consonants + '(ə)', r'\1\2ʌ', Strng)

    Strng = re.sub('^' + consonants + consonants +'(ə)', r'\1ʌ', Strng)
    Strng = re.sub('(\s)' + consonants + consonants +'(ə)', r'\1\2ʌ', Strng)

    Strng = re.sub('^' + consonants + consonants + consonants +'(ə)', r'\1ʌ', Strng)
    Strng = re.sub('(\s)' + consonants + consonants + consonants +'(ə)', r'\1\2ʌ', Strng)


    return Strng

def OriyaIPAFix(Strng):
    Strng = Strng.replace('ə', 'ɔ')
    Strng = Strng.replace('j', 'd͡ʒ')
    Strng = Strng.replace('\u1E8F', 'j')
    Strng = Strng.replace('kʂ', 'kʰ')
    Strng = Strng.replace('ʂ', 's̪')
    Strng = Strng.replace('ʃ', 's̪')
    Strng = Strng.replace('ʋ', 'u̯')

    Strng = Strng.replace('t͡s', 't͡ʃ')

    Strng = Strng.replace('ɪ', 'i')
    Strng = Strng.replace('iː', 'i')
    Strng = Strng.replace('uː', 'u')
    Strng = Strng.replace('eː', 'e')
    Strng = Strng.replace('oː', 'o')
    Strng = Strng.replace('ɾɨ', 'ɾu')
    Strng = Strng.replace('ɾɨː', 'ɾu')
    Strng = Strng.replace('lɨ', 'lu')
    Strng = Strng.replace('lɨː', 'lu')

    return Strng

def VedicSvarasLatinIndic(Strng, Source):
    ## Vedic Svaras
    Strng = Strng.replace('{\\m+}', 'ꣳ')
    Strng = Strng.replace('\\m++', 'ꣴ')
    Strng = Strng.replace('\\m+', 'ꣳ')

    Strng = Strng.replace('\\`', '\\_') ## Alternate form of Anudatta
    Strng = Strng.replace('\\\'\'', '\\"') ## Alternate form of Dirdha udatta

    Ayogavaha = GM.CrunchList('AyogavahaMap', Source)
    Svaras = ['\\_', '\\"', '\\\'']

    ## Svap the order of Svara + Ayogavaha -> Ayogaaha + Svara
    ## Indic syllable boundaries
    for x in Ayogavaha:
        for y in Svaras:
            Strng = Strng.replace(y + x, x + y)

    ### Introduce Vedic Svaras
    Strng = Strng.replace('\\"', '᳚')
    Strng = Strng.replace('\\\'', '॑')
    Strng = Strng.replace('\\_', '॒')

    return Strng

def VedicSvarsIndicLatin(Strng):
    Strng = Strng.replace('᳚', '\\"')
    Strng = Strng.replace('॑', '\\\'')
    Strng = Strng.replace('॒', '\\_')
    Strng = Strng.replace('ꣳ', '\\m+')
    Strng = Strng.replace('ꣴ', '\\m++')

    return Strng

def VedicSvarasOthers(Strng, Target):
    Strng = Strng.replace('\\"','↑↑').replace("\\_", '↓').replace("\\\'",'↑')
    anu = GM.CrunchList('AyogavahaMap', Target)[1]
    Strng = Strng.replace('\\m++', 'ꣴ')
    Strng = Strng.replace('\\m+', 'ꣳ')

    Ayogavaha = GM.CrunchList('AyogavahaMap', Target)

    return Strng

def VedicSvarasDiacrtics(Strng, Target):
    Strng = Strng.replace('\\\'', '̍')
    Strng = Strng.replace('\\"', '̎')
    Strng = Strng.replace('\\_', '̱')
    Strng = Strng.replace('\\m++', 'gͫ̄')
    Strng = Strng.replace('\\m+', 'gͫ')

    if (Target == 'ISO' or Target == 'ISOPali'):
        Strng = Strng.replace('\\’’', '̎')
        Strng = Strng.replace('\\’', '̍')


    Ayogavaha = GM.CrunchList('AyogavahaMap', Target)
    Svaras = ['̍', '̎', '̱']

    ## Svap the order of Svara + Ayogavaha -> Ayogaaha + Svara
    ## Indic syllable boundaries
    for x in Ayogavaha:
        for y in Svaras:
            Strng = Strng.replace(x + y, y + x)

    return Strng

def VedicSvarasCyrillic(Strng, Target):
    Strng = Strng.replace('\\\'', '̍')
    Strng = Strng.replace('\\"', '̎')
    Strng = Strng.replace('\\_', '̱')
    Strng = Strng.replace('\\м++', 'г\u0361м')
    Strng = Strng.replace('\\м+', 'г\u035Cм')
    Strng = Strng.replace('\\m++', 'г\u0361м')
    Strng = Strng.replace('\\m+', 'г\u035Cм')
    Ayogavaha = GM.CrunchList('AyogavahaMap', Target)
    Svaras = ['̍', '̎', '̱']

    ## Svap the order of Svara + Ayogavaha -> Ayogaaha + Svara
    ## Indic syllable boundaries
    for x in Ayogavaha:
        for y in Svaras:
            Strng = Strng.replace(x + y, y + x)

    return Strng

def VedicSvarasNonDiacritic(Strng):
    Strng = Strng.replace('̍', '\\\'')
    Strng = Strng.replace('̎', '\\"')
    Strng = Strng.replace('̱', '\\_')
    Strng = Strng.replace('gͫ̄', '\\m++')
    Strng = Strng.replace('gͫ', '\\m+')

    Strng = Strng.replace('г\u0361м', '\\m++')
    Strng = Strng.replace('г\u035Cм', '\\m+')


    return Strng

def FixRomanOutput(Strng,Target):

    # Input:Devanagari & Output:ISO
    # Input: क् क्अ क का कृ क्ह ब़् ब़ ब़ो भ् भ भा कि कइ कई
    # Output: kʌ× kʌ×a kʌ kʌā kʌr̥ kʌ×hʌ bʌ̄× bʌ̄ bʌ̄ō bhʌ× bhʌ bhʌā kʌi kʌṿi kʌṿī

    Schwa = '\uF000'
    DepV = '\u1E7F'

    # Creating RegEx matches
    #Escape ^,. which appear in ITRANS & Velthuis
    VowelSignList = '|'.join(GM.CrunchSymbols(GM.VowelSigns,Target)).replace('^','\^').replace('.','\.') # OR of all Consonants - k|kh etc
    VowelList = '|'.join(GM.CrunchSymbols(GM.Vowels,Target)).replace('^','\^').replace('.','\.') # OR of all Vowels - a|A etc

    Virama = ''.join(GM.CrunchSymbols(['ViramaMap'],Target))
    Nukta = ''.join(GM.CrunchSymbols(['NuktaMap'],Target))

    VowelA = GM.CrunchSymbols(['VowelMap'],Target)[0] # Vowel Letter 'a'
    VowelIU = '|'.join(GM.CrunchSymbols(['VowelMap'],Target)[2]+GM.CrunchSymbols(['VowelMap'],Target)[4])

    TargetCons = GM.CrunchSymbols(['ConsonantMap'],Target)
    ConsH = TargetCons[32] # Consonant H
    UnAspCons = '|'.join([TargetCons[i] for i in [0,2,5,7,10,12,15,17,20,22]]).replace('^','\^').replace('.','\.') # All Unaspirated Plosives

    #Transcribe Malayalam half-u
    if Target in ['IAST', 'ISO', 'ISOPali', 'Titus']:
        Strng = Strng.replace('u' + Virama, Virama + 'ŭ')

    # कि कइ - ki -> k_i
    Strng = re.sub('(?<='+Schwa+DepV+')'+'('+VowelIU+')',r'_\1',Strng)
    # Output: kʌ× kʌ×a kʌ kʌā kʌr̥ kʌ×hʌ bʌ̄× bʌ̄ bʌ̄ō bhʌ× bhʌ bhʌā kʌi kʌṿ_i kʌṿī

    # अइ अउ --> a_i a_u
    # print(Strng)
    Strng = re.sub('(?<=ṿ'+VowelA+'ṿ)'+'('+VowelIU+')',r'_\1',Strng)

    # ब्ह -> b_h not bh
    Strng = re.sub('('+UnAspCons+')''('+Schwa+Virama+')('+ConsH+')',r'\1_\3',Strng)
    # Output: kʌ× kʌ×a kʌ kʌā kʌr̥ k_hʌ bʌ̄× bʌ̄ bʌ̄ō bhʌ× bhʌ bhʌā kʌi kʌṿ_i kʌṿī

    # क्अ -> k_a not ka
    Strng = re.sub('('+Schwa+')('+Virama+')(?='+VowelList+')',r'_\2',Strng)
    # Output: kʌ× k_×a kʌ kʌā kʌr̥ k_hʌ bʌ̄× bʌ̄ bʌ̄ō bhʌ× bhʌ bhʌā kʌi kʌṿ_i kʌṿī

    # Rearranging Nukta
    Strng = re.sub('('+Schwa+')('+Nukta+')',r'\2\1',Strng)
    # Output: kʌ× k_×a kʌ kʌā kʌr̥ k_hʌ b̄ʌ× b̄ʌ b̄ʌō bhʌ× bhʌ bhʌā kʌi kʌṿ_i kʌṿī

    # Removing Schwa if followed by VowelSigns
    Strng = re.sub('('+Schwa+')(?='+VowelSignList+')','',Strng)
    # Output: k× k_×a kʌ kā kr̥ k_hʌ b̄× b̄ʌ b̄ō bh× bhʌ bhā ki kʌṿ_i kʌṿī

    # Replace Schwa by Vowel 'a'
    Strng = Strng.replace(Schwa,VowelA)
    # Output: k× k_×a ka kā kr̥ k_ha b̄× b̄a b̄ō bh× bha bhā ki kaṿ_i kaṿī

    # Remove DepV
    Strng = Strng.replace(DepV,'')
    # Output: k× k_×a ka kā kr̥ k_ha b̄× b̄a b̄ō bh× bha bhā ki ka_i kaī

    # Remove Virama
    Strng = Strng.replace(Virama,'')
    # Output: k k_a ka kā kr̥ k_ha b̄ b̄a b̄ō bh bha bhā ki ka_i kaī

    return Strng

def FixVedic(Strng, Target):
    # Alternate Vedic Forms
    Strng = Strng.replace('{\\m+}', '\\m+')
    Strng = Strng.replace('\\`', '\\_') ## Alternate form of Anudatta
    Strng = Strng.replace('\\\'\'', '\\"') ## Alternate form of Dirdha udatta

    # Fix Malformed Input //m+, //++

    Strng = Strng.replace('\\\\м', '\\м')
    Strng = Strng.replace('\\\\m', '\\m')
    Strng = Strng.replace('\\\\\'', '\\\'')
    Strng = Strng.replace('\\\\"', '\\"')
    Strng = Strng.replace('\\\\_', '\\_')

    vedicDiacRoman = ["IAST", "IASTPali", "ISO", "Titus", "ISOPali"]
    vedicnonDiacRoman = ["HK", "Itrans", "Velthuis", "SLP1", "WX"]

    if Target in vedicDiacRoman:
        Strng = VedicSvarasDiacrtics(Strng, Target)
    elif Target  == "IPA":
        Strng = Strng.replace('\\"','↑↑').replace("\\_", '↓').replace("\\\'",'↑')
        Strng = Strng.replace('\\m++', 'gͫ̄')
        Strng = Strng.replace('\\m+', 'gͫ')
    elif Target == "RomanReadable" or Target == "RomanColloquial":
        Strng = Strng.replace('\\"','').replace("\\_", '').replace("\\\'",'')
        Strng = Strng.replace('\\m++', 'ggum')
        Strng = Strng.replace('\\m+', 'gum')
    elif Target in vedicnonDiacRoman:
        pass
    elif Target == "RussianCyrillic":
        Strng = VedicSvarasCyrillic(Strng, Target)
    else:
        Strng = VedicSvarasOthers(Strng, Target)

    return Strng

# PostFile ? why not fix !?
def PostFixRomanOutput(Strng,Source,Target):
    Strng = Strng.replace("\u02BD","")

    Strng = FixVedic(Strng, Target)

    #print(Source, Target)

    # For Kashmiri
    if Target in ['IAST', 'ISO', 'ISOPali', 'Titus']:
        Strng = Strng.replace("uʼ", "ü").replace("ūʼ", "ǖ").replace('aʼ', 'ö').replace('āʼ', 'ȫ')

    if Source == 'Sinhala' and Target == 'IPA':
        Strng = SinhalaIPAFix(Strng)

    if Target == "IPA":
        Strng = FixIPA(Strng)

    if Target == 'Santali':
        Strng = FixSantali(Strng)

    if Target == "Avestan":
        Strng = FixAvestan(Strng)

    if Target == "SoraSompeng":
        Strng = FixSoraSompeng(Strng)

    if Target == "WarangCiti":
        Strng = FixWarangCiti(Strng)

    if Target == "Wancho":
        Strng = FixWancho(Strng)

    if Target == "Mro":
        Strng = FixMro(Strng)

    if Target == "RomanReadable":
        Strng = FixRomanReadable(Strng)
        if Source == 'Tamil':
            Strng = Strng.replace('t', 'th').replace("d", "dh").replace("h'","")

    if Target == "RomanColloquial":
        if Source == 'Tamil':
            Strng = Strng.replace('t', 'th').replace("d", "dh").replace("h'","")
        if Source == 'Oriya':
            Strng = Strng.replace("ksh", "x")
            Strng = re.sub("x(?=[aeiou])", "ksh", Strng)
            Strng = Strng.replace('jny', 'gy').replace("sh", "s").replace('r\'', 'd')
        if Source == 'Bengali':
            Strng = Strng.replace('m\'', "ng")

        Strng = FixRomanColloquial(Strng)


    if Target == "IAST" or Target == "IASTPali":
        Strng = Strng.replace("a_i", "aï")
        Strng = Strng.replace("a_u", "aü")

    if Target == "ISO" or Target == "ISOPali":
        Strng = Strng.replace("\\’", "\\\'")
        Strng = Strng.replace("\\’\u02BD", "\\\'")

        Strng = Strng.replace("a_i", "a:i")
        Strng = Strng.replace("a_u", "a:u")

    if Target == "Velthuis" or Target == "Itrans":
        Strng = Strng.replace("\\.a", "\\\'")

    if Target == "Aksharaa":
        Strng = Strng.replace("\\a;", "\\\'")

    if Target == "HanifiRohingya":
        Strng = FixHanifiRohingya(Strng)

    if Target == "Mongolian":
        Strng = FixMongolian(Strng)

    if Target == "Itrans":
        Strng = re.sub('([aAiIuUeo])(RR)(i|I)', r'\1'+'R_L' + r'\3', Strng)
        Strng = re.sub('([aAiIuUeo])(LL)(i|I)', r'\1'+'L_L'+ r'\3', Strng)

    if Source == "RomanSemitic":
        pass
        #Strng = Strng.replace('a̤', '\u0324')

    if Source in ['IAST','ISO'] and Target == 'Malayalam':
        Strng = Strng.replace('ṯ', 'ṟ')

    return Strng

def FixSemiticOutput(Strng,Source,Target):
    Strng = Strng.replace('\u02DE', '') ## dummy
    try:
        Strng = globals()["Fix"+Target.replace('-','_')](Strng, Source)
    except KeyError:
        pass
        #print("Fix"+Target+" doesn't exist")

    return Strng

# Fixing the Indic Ouput for the standard corrections
# Indic Fix are mandatory corrections to the immediate ouput.
def FixIndicOutput(Strng,Source,Target,ctx=None):
    vir = GM.CrunchList('ViramaMap', Target)[0]

    Strng = Strng.replace(vir + '_', vir)

    try:
        fn = globals()["Fix"+Target]
        # ctx passed only to functions that declare it (e.g. FixThai/
        # FixLaoPali, for transcription_mode) - everything else keeps its
        # existing (Strng) call unchanged. Mirrors GM.resolve()'s own
        # ctx-passing rule; can't use resolve() itself here since this
        # dispatch resolves through globals() (a dict), not a module
        # object, so there's no getattr() target to hand it.
        if ctx is not None and GM.accepts_ctx(fn):
            Strng = fn(Strng, ctx=ctx)
        else:
            Strng = fn(Strng)
    except KeyError:
        pass
        #print #"Fix"+Target+" doesn't exist"

    Strng = Strng.replace('\u02BD','')
    # Shifting Vowel Signs and Diacritics
    # க²ா ->  கா²
    Strng = ShiftDiacritics(Strng,Target,reverse=False)

    ## Make the Vedic Signs readable
    vedicScripts = ['Assamese', 'Bengali', 'Devanagari', 'Gujarati', 'Kannada', 'Malayalam', 'Oriya', 'Gurmukhi', 'Tamil', 'Telugu', 'TamilExtended', 'Grantha', 'Sharada']

    if Target not in vedicScripts:
        Strng = Strng.replace('॒','↓')
        Strng = Strng.replace('᳚','↑↑')
        Strng = Strng.replace('॑','↑')

    return Strng

def _FixHebrEncode(Strng, Source):
    vowelsigns = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew') + ['\u05BC']) + ')'
    vowelsigns2 = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew') + ['\u05BC']) + ')?'

    #print('here fixing')
    #print('reverse is ', str(reverse), 'vinodh')
    Strng = re.sub('(׳)' + vowelsigns + vowelsigns2, r'\3\2\1', Strng)
    Strng = re.sub('(וֹ)(׳)', r'\2\1', Strng)
    Strng = re.sub('(וּ)(׳)', r'\2\1', Strng)
    Strng = re.sub('(׳)(\u05b7)', r'\2\1', Strng)
    Strng = re.sub('(׳)(\u05b7)', r'\1', Strng)

    return Strng

def _FixHebrDecode(Strng, Source):
    vowelsigns = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew') + ['\u05BC']) + ')'
    vowelsigns2 = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew') + ['\u05BC']) + ')?'

    #print('here fixing')
    #print('reverse is ', str(reverse), 'vinodh')
    # swap garesh and short vowels
    vowels = ['ְ','ֱ','ֲ','ֳ','ִ','ֵ','ֶ','ַ','ָ','ֹ','ֺ','ֻ','ׇ','\u05BC']
    vowelsR = '(' + '|'.join(vowels + ['וֹ', 'וּ']) + ')'
    Strng = re.sub(vowelsR + "(׳)", r'\2\1', Strng)
    Strng = re.sub(vowelsR + "(׳)", r'\2\1', Strng)

    Strng = re.sub(vowelsR + "(׳)", r'\2\1', Strng)
    Strng = re.sub(vowelsR + "(׳)", r'\2\1', Strng)

    return Strng

def FixHebr(Strng, Source, reverse = False):
    return _FixHebrDecode(Strng, Source) if reverse else _FixHebrEncode(Strng, Source)

# Hebrew's own logic now lives in ScriptProcessing/Hebrew.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Hebrew import _FixHebrewEncode, _FixHebrewDecode, FixHebrew


# Mongolian's own logic now lives in ScriptProcessing/Mongolian.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Mongolian import _FixMongolianEncode, _FixMongolianDecode, FixMongolian

# HanifiRohingya's own Fix logic now lives in ScriptProcessing/HanifiRohingya.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixHanifiRohingya", ...) dispatch keeps working.
from .ScriptProcessing.HanifiRohingya import _hanifi_rohingya_lookups, _FixHanifiRohingyaEncode, _FixHanifiRohingyaDecode, FixHanifiRohingya

# MasaramGondi's own Fix logic now lives in ScriptProcessing/MasaramGondi.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixMasaramGondi", ...) dispatch keeps working.
from .ScriptProcessing.MasaramGondi import _FixMasaramGondiEncode, _FixMasaramGondiDecode, FixMasaramGondi


# GunjalaGondi's own Fix logic now lives in ScriptProcessing/GunjalaGondi.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixGunjalaGondi", ...) dispatch keeps working.
from .ScriptProcessing.GunjalaGondi import _FixGunjalaGondiEncode, _FixGunjalaGondiDecode, FixGunjalaGondi

# Soyombo's own logic now lives in ScriptProcessing/Soyombo.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Soyombo import _FixSoyomboEncode, _FixSoyomboDecode, FixSoyombo

# Kharoshthi's own Fix logic now lives in ScriptProcessing/Kharoshthi.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixKharoshthi", ...) dispatch keeps working.
from .ScriptProcessing.Kharoshthi import FixKharoshthi, KharoshthiNumerals, kharoshthiNumber

# Marchen's own logic now lives in ScriptProcessing/Marchen.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Marchen import _FixMarchenEncode, _FixMarchenDecode, FixMarchen

# Mro's own Fix logic now lives in ScriptProcessing/Mro.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixMro", ...) dispatch keeps working.
from .ScriptProcessing.Mro import _FixMroEncode, _FixMroDecode, FixMro

# Wancho's own Fix logic now lives in ScriptProcessing/Wancho.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixWancho", ...) dispatch keeps working.
from .ScriptProcessing.Wancho import _FixWanchoEncode, _FixWanchoDecode, FixWancho

def _FixSiddhamEncode(Strng):
    pass

    return Strng

def _FixSiddhamDecode(Strng):
    ## reverse the alternate forms
    Strng = Strng.replace('𑗜', '𑖲') # VS U
    Strng = Strng.replace('𑗝', '𑖳') # VS UU
    Strng = Strng.replace('𑗛', '𑖄') # VS U
    Strng = Strng.replace('𑗘', '𑖂') # VS I1
    Strng = Strng.replace('𑗙', '𑖂') # VS I2
    Strng = Strng.replace('𑗚', '𑖃') # VS II

    return Strng

def FixSiddham(Strng, reverse=False):
    return _FixSiddhamDecode(Strng) if reverse else _FixSiddhamEncode(Strng)

# Bhaiksuki's own logic now lives in ScriptProcessing/Bhaiksuki.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Bhaiksuki import _FixBhaiksukiEncode, _FixBhaiksukiDecode, FixBhaiksuki

# Khudawadi's own Fix logic now lives in ScriptProcessing/Khudawadi.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixKhudawadi", ...) dispatch keeps working.
from .ScriptProcessing.Khudawadi import _FixKhudawadiEncode, _FixKhudawadiDecode, FixKhudawadi

# Tamil's Fix logic now lives in ScriptProcessing/Tamil.py (consolidated
# there with its pre/post-options too - see that file's header comment for
# why the cross-module imports there are whole-module style, not
# `from .X import name`). Re-exported here so GM.resolve's getattr(CF,
# "FixTamil", ...) dispatch in Convert.py keeps working unchanged.
from .ScriptProcessing.Tamil import FixTamil, _FixTamilEncode, _FixTamilDecode

# Oriya's own logic now lives in ScriptProcessing/Oriya.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Oriya import _FixOriyaEncode, _FixOriyaDecode, FixOriya

# GurmukhiLoC's own Fix logic now lives in ScriptProcessing/GurmukhiLoC.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixGurmukhiLoC", ...) dispatch keeps working.
from .ScriptProcessing.GurmukhiLoC import _FixGurmukhiLoCEncode, _FixGurmukhiLoCDecode, FixGurmukhiLoC

# Correct Ru'', Lu'' -> R, lR
# Tippi/Bindu
# Gurmukhi's own logic now lives in ScriptProcessing/Gurmukhi.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Gurmukhi import _FixGurmukhiEncode, _FixGurmukhiDecode, FixGurmukhi

# Fix ru', ru'',lu',lu'' in Tamil & Gurmukhi
# रुʼ -> ऋ, रूʼ -> ॠ, लुʼ -> ऌ, लूʼ -> ॡ
def CorrectRuLu(Strng,Target,reverse=False):
    ra = GM.CrunchList('ConsonantMap', Target)[26]
    la = GM.CrunchList('ConsonantMap', Target)[27]
    uuu = GM.CrunchSymbols(GM.VowelSigns,Target)[4:6] #Vowel Signs u & U
    ap = '\u02BC'
    # Generate ru', rU', lu', lU'
    ruCons = [ra+x+ap for x in uuu ] + [la+x+ap for x in uuu]
    # Replace above with actual Vocalic Vowels
    for x,y in zip(ruCons,GM.CrunchSymbols(GM.Vowels,Target)[6:10]):
        if not reverse:
            Strng = Strng.replace(x,y)
        else:
            Strng = Strng.replace(y,x)

    return Strng

#Shift Diacritics after vowel signs
def ShiftDiacritics(Strng,Target,reverse=False):
    VS = '|'.join(GM.CrunchSymbols(GM.VowelSigns,Target))
    Diac = '|'.join(GM.Diacritics)

    if not reverse:
        Strng = re.sub('('+Diac+')'+'('+VS+')',r'\2\1',Strng)

        if Target == 'Tamil':
            Strng = Strng.replace( '³்', '்³',)

    else:
        if Target == 'Tamil':
            Strng = Strng.replace( '்³', '³்',)

        Strng = re.sub('('+VS+')'+'('+Diac+')',r'\2\1',Strng)

    return Strng


# TamilExtended's own logic now lives in ScriptProcessing/TamilExtended.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.TamilExtended import _FixTamilExtendedEncode, _FixTamilExtendedDecode, FixTamilExtended

# Move Vowel Signs
def _FixTamilGranthaEncode(Strng):
    ListC = '|'.join(GM.CrunchSymbols(GM.Consonants, 'TamilGrantha'))
    ListEAI = '|'.join(TamilGrantha.VowelSignMap[9:11]+TamilGrantha.SouthVowelSignMap[0:1])
    ListOAU = TamilGrantha.VowelSignMap[11:13]+TamilGrantha.SouthVowelSignMap[1:2]

    # k + VS e/E/ai -> Joiners + VS e/E/ai + k
    Strng = re.sub('('+ListC+')'+'('+ListEAI+')','\u200B\u200C\u200D\u200C'+r'\2\1',Strng)
    # k + VS o/O/au -> Joiners + VS e/E + k + VS AA/La
    Strng = re.sub('('+ListC+')'+'('+ListOAU[0]+')','\u200B\u200C\u200D\u200C'+TamilGrantha.VowelSignMap[9]+r'\1'+TamilGrantha.VowelSignMap[0],Strng)
    Strng = re.sub('('+ListC+')'+'('+ListOAU[2]+')','\u200B\u200C\u200D\u200C'+TamilGrantha.SouthVowelSignMap[0]+r'\1'+TamilGrantha.VowelSignMap[0],Strng)
    Strng = re.sub('('+ListC+')'+'('+ListOAU[1]+')','\u200B\u200C\u200D\u200C'+TamilGrantha.SouthVowelSignMap[0]+r'\1'+Tamil.SouthConsonantMap[0],Strng)

    ## Reversing நே்ˆদ
    Strng = re.sub('(\u200B\u200C\u200D\u200C.)'+'('+ListC+')'+'(்ˆ)',r'\2\3\1',Strng)


    return Strng

def _FixTamilGranthaDecode(Strng):
    ListC = '|'.join(GM.CrunchSymbols(GM.Consonants, 'TamilGrantha'))
    ListEAI = '|'.join(TamilGrantha.VowelSignMap[9:11]+TamilGrantha.SouthVowelSignMap[0:1])
    ListOAU = TamilGrantha.VowelSignMap[11:13]+TamilGrantha.SouthVowelSignMap[1:2]

    #print('I am here')
    # k + VS o/O/au <- Joiners + VS e/E + k + VS AA/La
    Strng = re.sub('\u200B'+TamilGrantha.VowelSignMap[9]+'('+ListC+')'+TamilGrantha.VowelSignMap[0],r'\1'+ListOAU[0],Strng)
    Strng = re.sub('\u200B'+TamilGrantha.SouthVowelSignMap[0]+'('+ListC+')'+TamilGrantha.VowelSignMap[0],r'\1'+ListOAU[2],Strng)
    Strng = re.sub('\u200B'+TamilGrantha.SouthVowelSignMap[0]+'('+ListC+')'+Tamil.SouthConsonantMap[0],r'\1'+ListOAU[1],Strng)
    # k + VS e/E/ai <- Joiners + VS e/E/ai + k
    Strng = re.sub('\u200B'+'('+ListEAI+')'+'('+ListC+')',r'\2\1',Strng)

    return Strng

def FixTamilGrantha(Strng, reverse=False):
    return _FixTamilGranthaDecode(Strng) if reverse else _FixTamilGranthaEncode(Strng)

# KhmerLoC's own Fix logic now lives in ScriptProcessing/KhmerLoC.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixKhmerLoC", ...) dispatch keeps working.
from .ScriptProcessing.KhmerLoC import FixKhmerLoC

# Khmer - Subjoining Consonants and Repha
# Khmer's own logic now lives in ScriptProcessing/Khmer.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Khmer import _FixKhmerEncode, _FixKhmerDecode, FixKhmer

# KhamtiShan's own logic now lives in ScriptProcessing/KhamtiShan.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.KhamtiShan import _FixKhamtiShanEncode, _FixKhamtiShanDecode, FixKhamtiShan

# TaiLaing's own Fix logic now lives in ScriptProcessing/TaiLaing.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixTaiLaing", ...) dispatch keeps working.
from .ScriptProcessing.TaiLaing import _FixTaiLaingEncode, _FixTaiLaingDecode, FixTaiLaing

# Shan's own logic now lives in ScriptProcessing/Shan.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Shan import _FixShanEncode, _FixShanDecode, FixShan

# Mon's own Fix logic now lives in ScriptProcessing/Mon.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixMon", ...) dispatch keeps working.
from .ScriptProcessing.Mon import _FixMonEncode, _FixMonDecode, FixMon

# Burmese - Tall A + Subjoning Consonants
# Burmese's own logic now lives in ScriptProcessing/Burmese.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Burmese import _FixBurmeseEncode, _FixBurmeseDecode, FixBurmese

# Add Repha (Bali,Java,Sundanese)
# a + r + ka -> a<repha>ka
# r +ya -> rya (no repha if syllable first)
def AddRepha(Strng,Script,Repha,reverse=False):
    vir = GM.CrunchSymbols(GM.VowelSigns,Script)[0]
    ra = GM.CrunchSymbols(GM.Consonants,Script)[26]

    ListC = '|'.join(GM.CrunchSymbols(GM.Consonants,Script))
    ListV = '|'.join(GM.CrunchSymbols(GM.Vowels,Script))
    ListVS = '|'.join(GM.CrunchSymbols(GM.VowelSignsNV,Script))

    if not reverse:
        # Introduce Repha: ka/ki/A + ra + vira -> ka/ki/A + Repha
        # Check all ListC + ListV + ListVS etc if '|' is introduced
        Strng = re.sub('('+ListC+'|'+ListV+'|'+ListVS+')'+'('+ra+vir+')',r'\1'+Repha,Strng)
        ## Not working
    else:
        # Replace Repha with ra+vir
        Strng = Strng.replace(Repha,ra+vir)

    return Strng

# Tagbanwa's own Fix logic now lives in ScriptProcessing/Tagbanwa.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixTagbanwa", ...) dispatch keeps working.
from .ScriptProcessing.Tagbanwa import _FixTagbanwaEncode, _FixTagbanwaDecode, FixTagbanwa

# Buhid's own Fix logic now lives in ScriptProcessing/Buhid.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixBuhid", ...) dispatch keeps working.
from .ScriptProcessing.Buhid import _FixBuhidEncode, _FixBuhidDecode, FixBuhid

# Buginese's own Fix logic now lives in ScriptProcessing/Buginese.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixBuginese", ...) dispatch keeps working.
from .ScriptProcessing.Buginese import _FixBugineseEncode, _FixBugineseDecode, FixBuginese


# Balinese Repha
# Balinese's own logic now lives in ScriptProcessing/Balinese.py -
# consolidated there (batch migration).
from .ScriptProcessing.Balinese import _FixBalineseEncode, _FixBalineseDecode, FixBalinese

# Javanese - Reppha & Subjoining ra & ya
# DivesAkuru's own logic now lives in ScriptProcessing/DivesAkuru.py -
# consolidated there (batch migration).
from .ScriptProcessing.DivesAkuru import _FixDivesAkuruEncode, _FixDivesAkuruDecode, FixDivesAkuru

# Javanese - Reppha & Subjoining ra & ya
# Kawi's own logic now lives in ScriptProcessing/Kawi.py -
# consolidated there (batch migration).
from .ScriptProcessing.Kawi import FixKawi, _FixKawiEncode, _FixKawiDecode

# Javanese - Reppha & Subjoining ra & ya
# Javanese's own logic now lives in ScriptProcessing/Javanese.py -
# consolidated there (batch migration).
from .ScriptProcessing.Javanese import _FixJavaneseEncode, _FixJavaneseDecode, FixJavanese


# Urdu's own Fix logic now lives in ScriptProcessing/Urdu.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixUrdu", ...) dispatch keeps working.
from .ScriptProcessing.Urdu import FixUrdu


# Shahmukhi's own Fix logic now lives in ScriptProcessing/Shahmukhi.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixShahmukhi", ...) dispatch keeps working.
from .ScriptProcessing.Shahmukhi import FixShahmukhi

# Urdu - Shadda, Final E
def _FixUrduShahmukhiEncode(Target, Strng):
    Strng = Strng.replace('\u02BD','')

    vir = GM.CrunchSymbols(GM.VowelSigns,Target)[0]

    ConUnAsp = [GM.CrunchList('ConsonantMap', Target)[x] for x in [0,2,5,7,10,12,15,17,20,22,4,9,14,19,24]+list(range(25,33))] # Add SemiVowels & Nukta Consonants
    ConUnAsp = ConUnAsp + GM.CrunchList('SouthConsonantMap',Target) + GM.CrunchList('NuktaConsonantMap',Target)

    ## Add word-final E, Short A sign

    ShortVowels = '|'.join(['\u0652','\u064E','\u0650','\u064F'])
    a = '\u064E'
    ya = '\u06CC'
    va  = '\u0648'
    yaBig = '\u06D2'
    Aa = Urdu.VowelSignMap[0]

    #Strng = Strng.replace(u'\u064E'+ya,ya)
    #Strng = Strng.replace(u'\u064E'+va,va)

    ## Fixing Hamza

    ListVS = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns,Target)) + ')'
    ListV = '(' + '|'.join(GM.CrunchSymbols(GM.Vowels,Target)) + ')'
    ListVSA = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns,Target)+[a]) + ')'

    ListC = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants,Target)) + ')'
    # Fix NunGhunna
    Strng = re.sub('(\u06BA\u02BD?)' + ListC, '\u0646\u0658' + r'\2', Strng)

    hamzaFull = "\u0621"
    hamzaChair = "\u0626"

    Strng = re.sub(ListVS + ListV, r'\1' + hamzaFull + r'\2', Strng)
    Strng = re.sub(ListV + ListV, r'\1' + hamzaFull + r'\2', Strng)
    Strng = re.sub('('+a+')' + ListV +'(?!' + ListVSA + ')'   , r'\1' + hamzaFull + r'\2', Strng)

    Strng = re.sub('('+a+')'+'('+ShortVowels+')',r'\2',Strng)
    Strng = re.sub('(?<!'+Aa+')'+'('+a+')'+'('+va+'|'+ya+')'+'(?!'+ ShortVowels +')',r'\2',Strng)
    ListC = '|'.join(GM.CrunchSymbols(GM.Consonants,Target)).replace(a,'')
    Ayoga = '|'.join(Urdu.AyogavahaMap[0] + Urdu.AyogavahaMap[1])

    Strng = Strng.replace(ya,yaBig)
    Strng = re.sub('('+yaBig+')'+'(?='+'|'.join(ConUnAsp)+ShortVowels+')',ya,Strng)
    Strng = re.sub('('+yaBig+')'+'('+ListC+')',ya+r'\2',Strng)
    Strng = re.sub('('+yaBig+')'+'('+Ayoga+')',ya+r'\2',Strng)

    Strng = Strng.replace('\u0650'+yaBig,'\u0650'+ya)

    #Strng = Strng.replace(a+Urdu.VowelSignMap[0],Urdu.VowelSignMap[0]) ## remove a sign from consonants

    ## ye ## yezu ## Fix this

    ## Adding Gemination of Consonant

    ConAsp   = [GM.CrunchList('ConsonantMap', Target)[x] for x in [1,3,6,8,11,13,16,18,21,23]]
    ConUnAsp_a =  [x.replace('\u064e','') for x in ConUnAsp]

    Strng = re.sub('('+'|'.join(ConUnAsp_a)+')'+'('+vir+')'+r'\1',r'\1'+GM.Gemination[Target],Strng)

    ## Move Shadda to the ha do=chasmee
    ## katthu -> کَتھُّ
    Strng = re.sub('(.)(ّ)(\u06BE)', r'\1\3\2', Strng)

    ## Fix

    Strng = Strng.replace('ےے', 'یے')
    Strng = Strng.replace('ےی', 'یی')
    Strng = Strng.replace('ےْ', 'یْ')

    #http://www.columbia.edu/~mk2580/urdu_section/handouts/hamza.pdf

    # Hamza on ya
    Strng = Strng.replace('ءاِی','\u0626\u0650\u06CC')
    Strng = Strng.replace('ءاے', 'ئے')

    Strng = Strng.replace('ءای', 'ئی')

    # Hamza on waw
    Strng = Strng.replace('ءاو','ؤ') #o
    Strng = Strng.replace('ءاُو', '\u0624\u064F') #long u

    Strng = Strng.replace('ءاُ', '\u0624\u064F') #short u

    # kau/ kaU

    Strng = re.sub('('+hamzaFull+')(اُو)', r'\1'+'\u0624\u064F', Strng)
    Strng = re.sub('('+hamzaFull+')(اُ)', r'\1'+'\u0624\u064F', Strng)

    Strng = re.sub('('+hamzaFull+')(او)', r'\1'+'\u0624', Strng)

    # Hamza on ya for short i
    Strng = Strng.replace('ءاِ', '\u0626\u0650')
    Strng = Strng.replace('ئِءآ', '\u0626\u0650\u0627')

    Strng = re.sub('('+hamzaFull+')(\u0627\u0650)', r'\1'+'\u0626\u0650', Strng)

    # for gae kae etc
    Strng = re.sub('('+hamzaFull+')(ا)(ے|ی)', r'\1'+'\u0626' + r'\3', Strng)

    ## Fix Double Hamza to Single Hamza

    Strng = Strng.replace('ئِئ', 'ئِ')
    Strng = Strng.replace('ئِؤ', 'ئِو')

    ## Fix Retroflex with combining characters
    Strng = Strng.replace('ࣇ', 'لؕ')

    if Target == 'Shahmukhi':
        #aspirated nasals and liquids
        Strng = re.sub('(ن|م|ی|ر|ل|و)(\u0652)(ہ)',r'\1'+'\u06BE', Strng)

    # Fix word-final ha





#    for i in range(len(ConAsp)):
#        Strng = re.sub('('+ConAsp[i]+')'+'('+vir+')'+'('+ConAsp[i]+')',r'\3'+GM.Gemination[Target],Strng)

    # Add Hamza

    pass

    ### Todo

    # Punctuation
    Strng = PersoArabicPuntuation(Strng, False)

#    Strng = Strng.replace(Aa+Aa,Aa+hamzaFull+Aa)
#    Strng = re.sub("("+ListVS+")"+"(?="+iii+")",r'\1'+hamzaChair,Strng)
#
#    Strng = Strng.replace(u"\u02BE","")

    #Strng = re.sub('('+ListC+')'+'(?!'+ListVS+')',r'\1'+a,Strng)

    return Strng

def _FixUrduShahmukhiDecode(Target, Strng):
    Strng = Strng.replace('\u02BD','')

    vir = GM.CrunchSymbols(GM.VowelSigns,Target)[0]

    ConUnAsp = [GM.CrunchList('ConsonantMap', Target)[x] for x in [0,2,5,7,10,12,15,17,20,22,4,9,14,19,24]+list(range(25,33))] # Add SemiVowels & Nukta Consonants
    ConUnAsp = ConUnAsp + GM.CrunchList('SouthConsonantMap',Target) + GM.CrunchList('NuktaConsonantMap',Target)

    ## Add word-final E, Short A sign

    ShortVowels = '|'.join(['\u0652','\u064E','\u0650','\u064F'])
    a = '\u064E'
    ya = '\u06CC'
    va  = '\u0648'
    yaBig = '\u06D2'
    Aa = Urdu.VowelSignMap[0]

    #Strng = Strng.replace(u'\u064E'+ya,ya)
    #Strng = Strng.replace(u'\u064E'+va,va)

    #print('I am being called')
    if True:
        #print(Strng)

        #Fix Nun Ghuunnai
        Strng = Strng.replace('\u0646\u0658', '\u06BA')

        ## replace chaschmee ha with regular ha when not surrounded preceeded by consonnants
        Strng = re.sub('(\s)\u06BE',r'\1'+'ہ', Strng)

        #decompose hamza with long e
        Strng = Strng.replace('ۓ', '_\u06d2')

        if Target == 'Shahmukhi':
            #aspirated nasals and liquids
            Strng = re.sub('(ن|م|ی|ر|ل|و)(\u06BE)',r'\1'+'\u0652ہ', Strng)

        ## Fix Retroflex with combining characters
        Strng = Strng.replace('لؕ', 'ࣇ')

        ListC = GM.CrunchSymbols(GM.Consonants,Target)

        ## Replacig Arabic with closest Indic counterparts

        Strng = Strng.replace('ص', 'س')
        Strng = Strng.replace('ث', 'س')

        Strng = Strng.replace('ح', 'ہ')
        Strng = Strng.replace('ۃ', 'ہ')

        Strng = Strng.replace('ذ', 'ز')
        Strng = Strng.replace('ض', 'ز')
        Strng = Strng.replace('ظ', 'ز')

        Strng = Strng.replace('ط', 'ت')

        Strng = Strng.replace('ژ', 'ز')

        Strng = Strng.replace('ع', 'اَ')

        Strng = Strng.replace('ً', 'نْ')

        Strng = Strng.replace('ئ', '_'+ya)

        Strng = Strng.replace('ؤ', '_'+va+a)

        Strng = Strng.replace('ء', '_')

        Strng = Strng.replace('یٰ', 'ا')

        Strng = Strng.replace('ك', 'ک')

        Strng = Strng.replace('ي', 'ی')

        #print(Strng)

        ## Gemination ##

        ## Move Shadda before the ha do=chasmee
        Strng = re.sub('(\u06BE)(ّ)', r'\2\1', Strng)

        Strng = re.sub('(' + ShortVowels + ')(ّ)', r'\2'+r'\1', Strng)
        Strng = re.sub('(.)(ّ)', r'\1'+'ْ'+r'\1', Strng)

        #print(Strng)
        #print(Target)
        if "\u02BB\u02BB" in Strng: ## Short Vowels not showm. INnsert /a/ to all consonats and approximate
            Strng = Strng.replace('ا', 'اَ')
            #retroflex la

            Strng = Strng.replace('لؕ', 'لَؕ')
            for c in ListC:
                Strng = Strng.replace(c.replace(a, ''), c)
                Strng = Strng.replace(c + 'اَ', c + 'ا')
                Strng = Strng.replace(c + 'ا' + 'و', c + 'ا' + '\u200B' + 'و')
                Strng = Strng.replace(c + 'ا' + 'ی', c + 'ا' + '\u200B' + 'ی')

            Strng = Strng.replace(a + 'ھ', 'ھ' + a)

            Strng = Strng.replace('ھ' + a + 'اَ' , 'ھ' + a + 'ا')

            ### Change this for dochashmee ha
            Strng = Strng.replace('ھ' + a + 'ا' + 'و', 'ھ' + a + 'ا' + '\u200B' + 'و')
            Strng = Strng.replace('ھ' + a + 'ا' + 'ی', 'ھ' + a + 'ا' + '\u200B' + 'ی')

            Strng = Strng.replace(a + a, a)

            Strng = Strng.replace('اَے', 'اے')
            Strng= Strng.replace(yaBig, ya)

            Strng = Strng.replace('\u02BB\u02BB', '')

        else:
            ShortVowelsR = '|'.join(['\u0652','\u0650','\u064F'])
            longVowels = '|'.join(['و', 'ا', ya])

            Strng= Strng.replace(yaBig, ya)

            ListCR = '|'.join(GM.CrunchSymbols(GM.Consonants,Target)).replace(a,'')

            Strng = re.sub('(' + ListCR + ')' + '('+ShortVowelsR+')',r'\1' + a + r'\2',Strng)
            Strng = re.sub('(' + ListCR + ')' + '('+longVowels+')'  + '(?!' + ShortVowels + ')',r'\1' + a + r'\2',Strng)

            #Hamzya ya va
            Strng = re.sub('(' + ListCR + ')' + '(_)', r'\1' + a + r'\2',Strng)


        VowelVS = '|'.join(GM.CrunchSymbols(GM.VowelSigns,Target))


    # print(Strng)

#    for i in range(len(ConAsp)):
#        Strng = re.sub('('+ConAsp[i]+')'+'('+vir+')'+'('+ConAsp[i]+')',r'\3'+GM.Gemination[Target],Strng)

    # Add Hamza

    pass

    ### Todo

    # Punctuation
    Strng = PersoArabicPuntuation(Strng, True)

#    Strng = Strng.replace(Aa+Aa,Aa+hamzaFull+Aa)
#    Strng = re.sub("("+ListVS+")"+"(?="+iii+")",r'\1'+hamzaChair,Strng)
#
#    Strng = Strng.replace(u"\u02BE","")

    #Strng = re.sub('('+ListC+')'+'(?!'+ListVS+')',r'\1'+a,Strng)

    return Strng

def FixUrduShahmukhi(Target, Strng,reverse=False):
    return _FixUrduShahmukhiDecode(Target, Strng) if reverse else _FixUrduShahmukhiEncode(Target, Strng)


def PersoArabicPuntuation(Strng, reverse=False):
    # Punctuation
    # print("Trying to reverse thigns")
    if (not reverse):
        for x,y in zip([',','?',';'],['،','؟','؛']):
            Strng = Strng.replace(x,y)
        Strng = Strng.replace(".", "۔")
    else :
        #print("here reversing things")
        for x,y in zip([',','?',';'],['،','؟','؛']):
            Strng = Strng.replace(y,x)
        Strng = Strng.replace("۔", ".")

    return Strng

### Anusvara to Nasal for Thanaa - Consider Add
# ThaanaVowelSign A
# Thaana's own Fix logic now lives in ScriptProcessing/Thaana.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixThaana", ...) dispatch keeps working.
from .ScriptProcessing.Thaana import _FixThaanaEncode, _FixThaanaDecode, FixThaana

# Saurashtra's own Fix logic now lives in ScriptProcessing/Saurashtra.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixSaurashtra", ...) dispatch keeps working.
from .ScriptProcessing.Saurashtra import _FixSaurashtraEncode, _FixSaurashtraDecode, FixSaurashtra

# TibetanLoC's own Fix logic now lives in ScriptProcessing/TibetanLoC.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixTibetanLoC", ...) dispatch keeps working.
from .ScriptProcessing.TibetanLoC import FixTibetanLoC

# Tibetan Subjoining Consnants
# Tibetan's own logic now lives in ScriptProcessing/Tibetan.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Tibetan import _FixTibetanEncode, _FixTibetanDecode, FixTibetan

# Thai, Lao follow visual ordering of Vowels signs ; <e> + k => <e>k
# Other Indic scripts follow logical order ; k + <e> => <e>k
# Swapping Vowel Signs for conversion
def ReverseVowelSigns(Strng,Script,reverse=False):
    EAIO = "|".join(sorted(GM.CrunchSymbols(GM.VowelSignsNV,Script)[9:12]+GM.CrunchSymbols(GM.VowelSignsNV,Script)[17:],key=len,reverse=True))
    cons = "|".join(GM.CrunchSymbols(GM.Consonants,Script))
    a = GM.CrunchSymbols(GM.Vowels,Script)[0].split()[0]
    consa = "|".join(GM.CrunchSymbols(GM.Consonants,Script) + [a])

    if Script == "Thai":
        EAIO += "|ใ"
        cons = "|".join(GM.CrunchSymbols(GM.Consonants,Script) + ['ฮ','บ', 'ฝ', 'ด', 'ฦ', 'ฤ'])

    if Script == "Lao":
        cons = "|".join(GM.CrunchSymbols(GM.Consonants,Script) + ['ດ','ບ','ຟ'] )

    a = GM.CrunchSymbols(GM.Vowels,Script)[0]

    if not reverse:
        Strng = re.sub("("+consa+")("+EAIO+")",r"\2\1",Strng)
    else:
        Strng = re.sub("("+EAIO+")"+"("+consa+")",r'\2\1',Strng)

    return Strng

# KhomThai's own Fix logic now lives in ScriptProcessing/KhomThai.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixKhomThai", ...) dispatch keeps working.
from .ScriptProcessing.KhomThai import _FixKhomThaiEncode, _FixKhomThaiDecode, FixKhomThai

def FixThai(Strng,reverse=False,ctx=None):
    Strng = ThaiReverseVowelSigns(Strng,reverse)
    Strng = ThaiDigraphConjuncts(Strng,reverse)

    transcription_mode = ctx.transcription_mode if ctx is not None else False
    if transcription_mode:
        Strng = PostProcess.ThaiLaoTranscription(Strng,"Thai", '\u0E30', '\u0E31', True)

        Strng = Strng.replace("หฺ์","ห์")

    return Strng

def ThaiReverseVowelSigns(Strng,reverse=False):
#    EAIO = "".join(Thai.VowelSignMap[9:12])
#    cons = "|".join(GM.CrunchSymbols(GM.Consonants, "Thai"))
#    a = Thai.VowelMap[0]
#    Strng = re.sub("("+cons+")(["+EAIO+"])(?!["+EAIO+"]"+a+")",r"\2\1",Strng)

    Strng = ReverseVowelSigns(Strng,"Thai",reverse)
    if not reverse:
        # VS AA + Anusvara -> VS AM (Ligature)
        # VS I + Anusvara -> VS IM (Ligature)
        Strng = Strng.replace("\u0E32\u0E4D","\u0E33").replace("\u0E34\u0E4D","\u0E36")
    else:
        # Reverse above
        Strng = Strng.replace("\u0E33","\u0E32\u0E4D").replace("\u0E36","\u0E34\u0E4D")

    return Strng

def _FixLaoPaliEncode(Strng, ctx):
    Strng = ReverseVowelSigns(Strng,"LaoPali",False)

    transcription_mode = ctx.transcription_mode if ctx is not None else False
    if transcription_mode:
        Strng = LaoPaliTranscribe(Strng, True)

        Strng = Strng.replace("ຫ຺໌","ຫ໌")

    Strng = Strng.replace("\u0EB2\u0ECD","\u0EB3")

    return Strng

def _FixLaoPaliDecode(Strng, ctx):
    Strng = ReverseVowelSigns(Strng,"LaoPali",True)

    transcription_mode = ctx.transcription_mode if ctx is not None else False
    if transcription_mode:
        Strng = LaoPaliTranscribe(Strng, True)

        Strng = Strng.replace("ຫ຺໌","ຫ໌")

    # VS AA + Anusvara <- VS AM (Ligature)
    Strng= Strng.replace("\u0EB3","\u0EB2\u0ECD")

    return Strng

def FixLaoPali(Strng,reverse=False,ctx=None):
    return _FixLaoPaliDecode(Strng, ctx) if reverse else _FixLaoPaliEncode(Strng, ctx)

# Makasar's own Fix logic now lives in ScriptProcessing/Makasar.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixMakasar", ...) dispatch keeps working.
from .ScriptProcessing.Makasar import _FixMakasarEncode, _FixMakasarDecode, FixMakasar

# Avestan's own Fix logic now lives in ScriptProcessing/Avestan.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixAvestan", ...) dispatch keeps working.
from .ScriptProcessing.Avestan import _FixAvestanEncode, _FixAvestanDecode, FixAvestan

# Lao's own logic now lives in ScriptProcessing/Lao.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Lao import _FixLaoEncode, _FixLaoDecode, FixLao, LaoTranscribe

# Re-arrange Vowels Signs /E/, /AI/, /O/ for digraph <dv>, <mh> etc
# e.g dve -> เทฺว instead of ทฺเว
def ThaiDigraphConjuncts(Strng,reverse=False):
    EAIO = "".join(Thai.VowelSignMap[9:12])
    cons = "|".join(GM.CrunchSymbols(GM.Consonants, "Thai"))
    yrlvh = "|".join(GM.CrunchSymbols(GM.Consonants, "Thai")[25:29] + GM.CrunchSymbols(GM.Consonants, "Thai")[32:33])
    sh = "|".join(Thai.ConsonantMap[31:33])
    vir = Thai.ViramaMap[0]

    #Replace \s with all punctuations
    if not reverse:
        # Comments
        Strng = re.sub("(?<=\s)("+cons+")"+"("+vir+")"+"(["+EAIO+"])"+"("+cons+")",r"\3\1\2\4",Strng)
        Strng = re.sub("("+cons+")"+"("+vir+")"+"(["+EAIO+"])"+"("+yrlvh+")",r"\3\1\2\4",Strng)
        Strng = re.sub("("+sh+")"+"("+vir+")"+"(["+EAIO+"])"+"("+cons+")",r"\3\1\2\4",Strng)
    else:
        ## Reverse the above.
        Strng = re.sub("(["+EAIO+"])"+"("+vir+")"+"("+cons+")",r"\2\3\1",Strng)

    return Strng

# OldPersian's own Fix logic now lives in ScriptProcessing/OldPersian.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixOldPersian", ...) dispatch keeps working.
from .ScriptProcessing.OldPersian import FixOldPersian, OldPersianSyllable, OldPersianNumeral

# Syllabization of Persian
# d<a> +i -> d<i> + i
# d<a> + u -> d<u> + u
# Convert numbers into Persinal Numeral System
# Sinhala's own logic now lives in ScriptProcessing/Sinhala.py -
# consolidated there (batch migration).
from .ScriptProcessing.Sinhala import _FixSinhalaEncode, _FixSinhalaDecode, FixSinhala

# Santali's own Fix logic now lives in ScriptProcessing/Santali.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixSantali", ...) dispatch keeps working.
from .ScriptProcessing.Santali import _FixSantaliEncode, _FixSantaliDecode, FixSantali

# SoraSompeng's own Fix logic now lives in ScriptProcessing/SoraSompeng.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixSoraSompeng", ...) dispatch keeps working.
from .ScriptProcessing.SoraSompeng import _FixSoraSompengEncode, _FixSoraSompengDecode, FixSoraSompeng


# FixRomanReadable and FixRomanColloquial share the same nasal-assimilation
# algorithm; Colloquial differs only in dropping the apostrophe marker that
# Readable keeps, and stripping underscores at the end.
def _FixRomanReadableColloquial(Strng, reverse, colloquial):
    if not reverse:
        Strng = Strng.replace('\\n', '\uE001')
        Strng = re.sub('([aiueo])nj([aeiou])', r'\1' + 'ny' + r'\2', Strng)
        Strng = re.sub('(\W)nj([aeiou])', r'\1' + 'ny' + r'\2', Strng)
        Strng = re.sub('^nj([aeiou])', 'ny' + r'\1', Strng)

        Strng = Strng.replace("njnj", "nny")

        Strng = Strng.replace("Mk", "ngk")
        Strng = Strng.replace("Mg", "ngg")
        Strng = Strng.replace("Mc", "njc")
        Strng = Strng.replace("Mj", "njj")
        Strng = Strng.replace("Md", "nd")
        Strng = Strng.replace("Mt", "nt")
        Strng = Strng.replace("Mb", "mb")
        Strng = Strng.replace("Mp", "mp")

        Strng = Strng.replace("M", 'm\u034F' if colloquial else 'm\u034F\'')

        Strng = Strng.replace("ngk", "nk")
        Strng = Strng.replace("ngg", "ng")
        Strng = Strng.replace("njc", "nc")
        Strng = Strng.replace("njj", "nj")

        Strng = Strng.replace("jnj", "jny")

        Strng = Strng.replace('\uE001', '\\n')

        if colloquial:
            Strng = Strng.replace('\'', '').replace("_", "")
    else:
        pass

    return Strng

# RomanReadable's own logic now lives in ScriptProcessing/RomanReadable.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.RomanReadable import FixRomanReadable

# RomanColloquial's own Fix logic now lives in ScriptProcessing/RomanColloquial.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixRomanColloquial", ...) dispatch keeps working.
from .ScriptProcessing.RomanColloquial import FixRomanColloquial


# WarangCiti's own logic now lives in ScriptProcessing/WarangCiti.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.WarangCiti import _FixWarangCitiEncode, _FixWarangCitiDecode, FixWarangCiti

# LimbuLoC's own Fix logic now lives in ScriptProcessing/LimbuLoC.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixLimbuLoC", ...) dispatch keeps working.
from .ScriptProcessing.LimbuLoC import _FixLimbuLoCEncode, _FixLimbuLoCDecode, FixLimbuLoC

#Subojined & Final
# Limbu's own logic now lives in ScriptProcessing/Limbu.py -
# consolidated there (batch migration).
from .ScriptProcessing.Limbu import _FixLimbuEncode, _FixLimbuDecode, FixLimbu


def _FixDevanagariEncode(Strng):
    Sindhi = ['ॻ','ॼ','ॾ','ॿ']
    SindhiApprox = ['ˍग','ˍज','ˍड','ˍब']
    Strng = Strng.replace('ʔ', 'ॽ')

    for x, y in zip(Sindhi, SindhiApprox):
        Strng = Strng.replace(y, x)

    Strng = Strng.replace('ज़़','ॹ')
    Strng = Strng.replace('श़','ॹ')
    Strng = Strng.replace('ऱ्', 'ऱ्‌') ## Prevent RRA from forming conjuncts

    ## Except for YA and HA
    Strng = Strng.replace('ऱ्‌य', 'ऱ्य')
    Strng = Strng.replace('ऱ्‌ह', 'ऱ्ह')

    # Kashmiri ux, uux

    #Strng = Strng.replace('उʼ', 'ॶ').replace('ऊʼ', 'ॷ').replace('ुʼ', 'ॖ').replace('ूʼ','ॗ')

    # Kashmir oe oe

    #Strng = Strng.replace('अʼ', 'ॳ').replace('आʼ', 'ॴ')

    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'Devanagari'))

    Strng = re.sub('(' + ListC + ')' + 'ʼ', r'\1' + '\u093A', Strng)
    Strng = Strng.replace('\u093Eʼ','\u093B')





    return Strng

def _FixDevanagariDecode(Strng):
    Sindhi = ['ॻ','ॼ','ॾ','ॿ']
    SindhiApprox = ['ˍग','ˍज','ˍड','ˍब']
    # remove schwa accent
    Strng = Strng.replace('\u0954', '')

    Strng = PostProcess.DevanagariPrishtamatra(Strng, reverse=True)
    Strng = Strng.replace('ॽ', 'ʔ')
    Strng = Strng.replace('ॹ', 'ज़़')

    for x, y in zip(Sindhi, SindhiApprox):
        Strng = Strng.replace(x, y)

    # Kashmiri ux, uux
    #Strng = Strng.replace('ॶ', 'उʼ').replace('ॷ', 'ऊʼ').replace('ॖ', 'ुʼ').replace('ॗ', 'ूʼ')

    # oe
    #Strng = Strng.replace('ॳ', 'अʼ').replace('ॴ', 'आʼ').replace('\u093B', '\u093Eʼ').replace('\u093A','ʼ')


    return Strng

def FixDevanagari(Strng, reverse=False):
    return _FixDevanagariDecode(Strng) if reverse else _FixDevanagariEncode(Strng)

# Kaithi's own logic now lives in ScriptProcessing/Kaithi.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Kaithi import _FixKaithiEncode, _FixKaithiDecode, FixKaithi

# Lao2's own Fix logic now lives in ScriptProcessing/Lao2.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixLao2", ...) dispatch keeps working.
from .ScriptProcessing.Lao2 import FixLao2

# Nandinagari's own logic now lives in ScriptProcessing/Nandinagari.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Nandinagari import _FixNandinagariEncode, _FixNandinagariDecode, FixNandinagari

#Subjoined, final and la-ligatures
# Fix aH -> a ;
# Lepcha's own Fix logic now lives in ScriptProcessing/Lepcha.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixLepcha", ...) dispatch keeps working.
from .ScriptProcessing.Lepcha import _FixLepchaEncode, _FixLepchaDecode, FixLepcha

# Repha & Subjoined
# Sundanese's own logic now lives in ScriptProcessing/Sundanese.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Sundanese import _FixSundaneseEncode, _FixSundaneseDecode, FixSundanese

# Repha & Subjoined
# Rejang's own Fix logic now lives in ScriptProcessing/Rejang.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixRejang", ...) dispatch keeps working.
from .ScriptProcessing.Rejang import _FixRejangEncode, _FixRejangDecode, FixRejang

# Chakmaa VS A and Subjoined
# Chakma's own logic now lives in ScriptProcessing/Chakma.py -
# consolidated there (batch migration).
from .ScriptProcessing.Chakma import _FixChakmaEncode, _FixChakmaDecode, FixChakma

# IAST's own logic now lives in ScriptProcessing/IAST.py -
# consolidated there (batch migration).
from .ScriptProcessing.IAST import _FixIASTEncode, _FixIASTDecode, FixIAST

# IPA's own Fix logic now lives in ScriptProcessing/IPA.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixIPA", ...) dispatch keeps working.
from .ScriptProcessing.IPA import _FixIPAEncode, _FixIPADecode, FixIPA

# Rearrange PhagsPa Letters ; Subjoined Letters ;
# PhagsPa's own logic now lives in ScriptProcessing/PhagsPa.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.PhagsPa import _FixPhagsPaEncode, _FixPhagsPaDecode, FixPhagsPa

# Meetei Mayek Final
# Think of a-k-ka vers a-ka+vir-ka, also ag to ak. (Virama extends to second letter... ag could be replaced by ak..
# since a+ga+vir woould orthographically wrong (it has no following consonant to extend to), considered replacing a+g+virama with a+k

# Latn's own logic now lives in ScriptProcessing/Latn.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Latn import _FixLatnEncode, _FixLatnDecode, FixLatn

# Arab's own logic now lives in ScriptProcessing/Arab.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Arab import _FixArabEncode, _FixArabDecode, FixArab

def _FixThaaEncode(Strng, Source):
    Strng = PersoArabicPuntuation(Strng, False)
    pass
    #Strng = Strng.replace('â', 'ʾ')

    return Strng

def _FixThaaDecode(Strng, Source):
    Strng = PersoArabicPuntuation(Strng, True)
    pass

    return Strng

def FixThaa(Strng, Source, reverse=False):
    return _FixThaaDecode(Strng, Source) if reverse else _FixThaaEncode(Strng, Source)

def FixArab_Ph(Strng, Source, reverse=False):
    return FixArab(Strng, Source, reverse)

# Arab-Fa's own logic now lives in ScriptProcessing/Arab_Fa.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Arab_Fa import FixArab_Fa

def _FixArab_UrEncode(Strng, Source):
    Strng = FixArab(Strng, Source, False)

    if Source != 'Type':
        ## introduce hamza
        pass

    return Strng

def _FixArab_UrDecode(Strng, Source):
    Strng = FixArab(Strng, Source, True)

    pass

    return Strng

def FixArab_Ur(Strng, Source, reverse=False):
    return _FixArab_UrDecode(Strng, Source) if reverse else _FixArab_UrEncode(Strng, Source)

# Ugar's own Fix logic now lives in ScriptProcessing/Ugar.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixUgar", ...) dispatch keeps working.
from .ScriptProcessing.Ugar import _FixUgarEncode, _FixUgarDecode, FixUgar

# Sogd's own logic now lives in ScriptProcessing/Sogd.py -
# consolidated there (batch migration).
from .ScriptProcessing.Sogd import _FixSogdEncode, _FixSogdDecode, FixSogd

def _FixMalayalamEncode(Strng):
    Strng = PostProcess.MalayalamChillu(Strng, False)

    Strng = PostProcess.RetainDandasIndic(Strng, 'Malayalam', True)
    Strng = PostProcess.RetainIndicNumerals(Strng, 'Malayalam', True)

    # fix n2ra
    #Strng = Strng.replace('ன்ற')

    Chillus=['\u0D7A','\u0D7B','\u0D7C','\u0D7D','\u0D7E', 'ഩ‍്']

    Anu = GM.CrunchSymbols(GM.CombiningSigns,'Malayalam')[1]


    return Strng

def _FixMalayalamDecode(Strng):
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
    return _FixMalayalamDecode(Strng) if reverse else _FixMalayalamEncode(Strng)

# Telugu's own logic now lives in ScriptProcessing/Telugu.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Telugu import _FixTeluguEncode, _FixTeluguDecode, FixTelugu

# MeeteiMayek's own Fix logic now lives in ScriptProcessing/MeeteiMayek.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixMeeteiMayek", ...) dispatch keeps working.
from .ScriptProcessing.MeeteiMayek import _FixMeeteiMayekEncode, _FixMeeteiMayekDecode, FixMeeteiMayek

## Reverse not working
## For other batak writings as well

## Consider replacement of Anusvara by Nasal for East Asian Sripts which don't ahve a Sanskrit writing Tradition

# BatakSima's own Fix logic now lives in ScriptProcessing/BatakSima.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixBatakSima", ...) dispatch keeps working.
from .ScriptProcessing.BatakSima import _FixBatakSimaEncode, _FixBatakSimaDecode, FixBatakSima

# Cham Final & Subjoined
# Cham's own Fix logic now lives in ScriptProcessing/Cham.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixCham", ...) dispatch keeps working.
from .ScriptProcessing.Cham import _FixChamEncode, _FixChamDecode, FixCham

# Subjoined Consonants in Tai Tham
# Mai Kang Lai - /ng/
# TaiTham's own Fix logic now lives in ScriptProcessing/TaiTham.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixTaiTham", ...) dispatch keeps working.
from .ScriptProcessing.TaiTham import _FixTaiThamEncode, _FixTaiThamDecode, FixTaiTham

# LaoTham's own Fix logic now lives in ScriptProcessing/LaoTham.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixLaoTham", ...) dispatch keeps working.
from .ScriptProcessing.LaoTham import FixLaoTham

# FixThamLoC/FixLueTham/FixKhuenTham share the same "Tall A" regex logic;
# they differ in the TaiTham consonant list used for the Tall A match
# (ThamLoC alone includes one extra consonant), and in one extra step
# each: ThamLoC does a marker cleanup (forward, only when the Khuen-text
# u02BE marker is present) plus a reverse-direction subconsonant fix;
# KhuenTham does an unconditional ra-haam/lue-karan swap in both
# directions; LueTham has neither extra step.
def _FixTaiThamFamily(Strng, reverse, tall_a_cons, marker_cleanup, ra_haam_swap):
    Strng = FixTaiTham(Strng, reverse)

    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'TaiTham'))
    if not reverse:
        E = "ᩮ"
        AA = 'ᩣ'
        TallACons = '|'.join(tall_a_cons) ## va da dha ga
        Strng = re.sub('('+TallACons+')(᩠)('+ListC +')'+'('+E+'?)'+AA,r'\1\2\3\4'+'ᩤ',Strng)
        Strng = re.sub('('+TallACons+')(᩠)('+ListC +')'+'(᩠)('+ListC +')'+'('+E+'?)'+AA,r'\1\2\3\4\5\6'+'ᩤ',Strng)

        if marker_cleanup and '\u02BE' in Strng:
            Strng = Strng.replace('᩺', '᩼').replace('\u02BE', '')
        elif ra_haam_swap:
            # ra-haam with lue-karan
            Strng = Strng.replace('᩺', '᩼')
    else:
        if marker_cleanup:
            #sub consonants
            Strng = Strng.replace('ᩜ', '\u1A7A''ᨾ')
            Strng = Strng.replace('ᩛ', '\u1A7A''ᨻ')
        elif ra_haam_swap:
            # replace lue-karan with ra-haam
            Strng = Strng.replace('᩼', '᩺')

    return Strng

# ThamLoC's own Fix logic now lives in ScriptProcessing/ThamLoC.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixThamLoC", ...) dispatch keeps working.
from .ScriptProcessing.ThamLoC import FixThamLoC

# LueTham's own Fix logic now lives in ScriptProcessing/LueTham.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixLueTham", ...) dispatch keeps working.
from .ScriptProcessing.LueTham import FixLueTham

# KhuenTham's own logic now lives in ScriptProcessing/KhuenTham.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.KhuenTham import FixKhuenTham

# Transcription for Pali Lao
def LaoPaliTranscribe(Strng,reverse=False, anusvaraChange = True):
    from . import PostProcess as pp
    shortA, conjA = '\u0EB0', '\u0EB1'

    if not reverse:
        Strng = pp.ThaiLaoTranscription(Strng,"LaoPali",shortA,conjA, anusvaraChange = anusvaraChange)
    else:
        Strng = pp.ThaiLaoTranscription(Strng,"LaoPali",shortA, conjA,reverse=True)

    return Strng

# Assamese and Bengali have the same mapping file duplicated
# Replace Bengali /ra/ with Assamese /ra/
# Bengali's own logic now lives in ScriptProcessing/Bengali.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Bengali import _FixBengaliEncode, _FixBengaliDecode, FixBengali

# Assamese's own Fix logic now lives in ScriptProcessing/Assamese.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixAssamese", ...) dispatch keeps working.
from .ScriptProcessing.Assamese import _FixAssameseEncode, _FixAssameseDecode, FixAssamese

# Sharada's own Fix logic now lives in ScriptProcessing/Sharada.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixSharada", ...) dispatch keeps working.
from .ScriptProcessing.Sharada import _FixSharadaEncode, _FixSharadaDecode, FixSharada

# Kannada's own logic now lives in ScriptProcessing/Kannada.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Kannada import _FixKannadaEncode, _FixKannadaDecode, FixKannada

# Grantha's own logic now lives in ScriptProcessing/Grantha.py -
# consolidated there (batch migration).
from .ScriptProcessing.Grantha import FixGrantha, _FixGranthaEncode, _FixGranthaDecode

# Mahajani's own Fix logic now lives in ScriptProcessing/Mahajani.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixMahajani", ...) dispatch keeps working.
from .ScriptProcessing.Mahajani import _FixMahajaniEncode, _FixMahajaniDecode, FixMahajani

# Ahom's own logic now lives in ScriptProcessing/Ahom.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Ahom import _FixAhomEncode, _FixAhomDecode, FixAhom

# Multani's own Fix logic now lives in ScriptProcessing/Multani.py -
# consolidated there (batch migration). Re-exported here so
# GM.resolve's getattr(CF, "FixMultani", ...) dispatch keeps working.
from .ScriptProcessing.Multani import _FixMultaniEncode, _FixMultaniDecode, FixMultani


# Gujarati's own logic now lives in ScriptProcessing/Gujarati.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Gujarati import _FixGujaratiEncode, _FixGujaratiDecode, FixGujarati

# ZanabazarSquare's own logic now lives in ScriptProcessing/ZanabazarSquare.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.ZanabazarSquare import _FixZanabazarSquareEncode, _FixZanabazarSquareDecode, FixZanabazarSquare

# Khojki's own logic now lives in ScriptProcessing/Khojki.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Khojki import _FixKhojkiEncode, _FixKhojkiDecode, FixKhojki

# Newa's own logic now lives in ScriptProcessing/Newa.py -
# consolidated there (batch migration). Re-exported here so GM.resolve(CF, 'FixX', ...)'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Newa import _FixNewaEncode, _FixNewaDecode, FixNewa

