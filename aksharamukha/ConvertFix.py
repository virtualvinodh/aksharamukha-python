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
def FixIndicOutput(Strng,Source,Target,transcription_mode=False):
    vir = GM.CrunchList('ViramaMap', Target)[0]

    Strng = Strng.replace(vir + '_', vir)

    try:
        # transcription_mode only means anything to FixThai/FixLaoPali;
        # every other script's Fix* function takes no such argument.
        if Target in ('Thai', 'LaoPali'):
            Strng = globals()["Fix"+Target](Strng, transcription_mode=transcription_mode)
        else:
            Strng = globals()["Fix"+Target](Strng)
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

def _FixHebrewEncode(Strng):
    vowelsigns = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew')) + ')'
    consonants = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Hebrew')+['צּ','גּ']) + ')'

    vowelsignsA = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew') + ['ַ']) + ')'
    vowelsignsAD = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew') + ['ַ', 'ּ']) + ')'

    vowelsignsADShin = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew') + ['ַ', 'ּ', 'ׁ']) + ')'
    vowelsignsADShinG = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew') + ['ַ', 'ּ', 'ׁ', '׳']) + ')'


    finalCons = ['כ', 'מ', 'נ', 'פ', 'צ', 'פּ', 'כּ']
    finals = ['ך', 'ם', 'ן', 'ף', 'ץ', 'ףּ', 'ךּ']

    otherCons = 'ב,ח,ע,צ,ש,ת'.split(',')
    consonantsAll = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Hebrew') + finals  + otherCons + ['׳']) + ')'

    Strng = Strng.replace('\u02BD', '')
    Strng = Strng.replace('\u02BE', '')

    ## geminate cc/jj
    Strng = Strng.replace('ג׳ְג׳', 'גּ׳').replace('צ׳ְצ׳', 'צּ׳')

    # Fix Anusvara

    # mK, mG, mp, mC, md, mt
    Strng = re.sub('מְ' + '\u02BC' + '([גדזטכצקת])', 'נְ' + r'\1', Strng)
    Strng = re.sub('מְ' + '\u02BC', 'מְ', Strng)

    # insert a_sign
    Strng = re.sub(consonants + '(?!' + vowelsigns + ')', r'\1' + '\u05B7' + r'\2', Strng)

    # reverse dagesh patah
    Strng = Strng.replace('\u05b7\u05Bc', '\u05Bc\u05b7')

    # fix double a to single a
    Strng = Strng.replace('\u05b7\u05b7', '\u05B7')

    # Fix a appear with Dagesh and Shva.. k -> kaph + patau + dagesh + shva -> kaph + dagesh + shva
    Strng = Strng.replace('\u05b7\u05bc\u05B0', '\u05bc\u05B0')


    # fix order of vowel signs and vowels sign with ch/j
    Strng = re.sub('(׳)' + vowelsigns, r'\2\1', Strng)
    Strng = re.sub('(וֹ)(׳)', r'\2\1', Strng)
    Strng = re.sub('(וּ)(׳)', r'\2\1', Strng)
    Strng = re.sub('(׳)(\u05b7)', r'\2\1', Strng)
    Strng = re.sub('(׳)(\u05b7)', r'\1', Strng)

    # Fix Pateh appearing with vowel signs
    Strng = re.sub('(\u05b7)' + vowelsigns, r'\2', Strng)
    Strng = re.sub('(\u05b7)' + '(\u05BC)' + vowelsigns, r'\2\3', Strng)

    #Do gemination
    ## consonant doubling with Dagesh
    ## gemination with dagesh as well
    Strng = re.sub('([' + 'ושרקסנמליזטײ' + 'הגדת' + '])(ְ)' + r'\1', r'\1' + 'ּ', Strng)
    Strng = re.sub('(שׁ)(ְ)' + r'\1', r'\1' + 'ּ', Strng)
    ## for geminate ka use qa
    ## bba -> ba, ppa -> pa ; cannot use dagesh for gemination too ambigous
    Strng = Strng.replace('כְּכּ', 'קּ').replace('פְּפּ','פּ').replace('בְּבּ','בּ')

    # Fix Finals
    shortVowels = '(' + '|'.join(['\u05B7', '\u05B8', '\u05B4', '\u05BB', '\u05B5', '\u05B6', '\u05B9', '\u05B0']) + ')'

    vowelsAll = '(' + '|'.join(['\u05B7', '\u05B8', '\u05B4', '\u05BB', '\u05B5', '\u05B6', '\u05B9', '\u05B0', 'י', 'וֹ', 'וּ'] + ['׳']) + ')'

    for c, f in zip(finalCons, finals):
        Strng = re.sub(vowelsAll + '(' + c + ')' + shortVowels + '(׳?)' + '(?!' + consonantsAll + '|י|ו)', r'\1' + f +  r'\3' + r'\4', Strng)

    # remove final schwa
    Strng = re.sub('(?<!ה)(ְ)(׳?)' + '(?!' + consonantsAll + '|י|ו)', r'\2\3', Strng)

    # Fix Va + O
    Strng = Strng.replace('װ' + '\u05B9', '\u05D5\u05BA')

    Strng = Strng.replace('װ' , '\u05D5')
    Strng = Strng.replace('ײ' , 'י')

    Strng = Strng.replace('\u02BC', '')


    Strng = Strng.replace('௞', '')

    return Strng

def _FixHebrewDecode(Strng):
    vowelsigns = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew')) + ')'
    consonants = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Hebrew')+['צּ','גּ']) + ')'

    vowelsignsA = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew') + ['ַ']) + ')'
    vowelsignsAD = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew') + ['ַ', 'ּ']) + ')'

    vowelsignsADShin = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew') + ['ַ', 'ּ', 'ׁ']) + ')'
    vowelsignsADShinG = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew') + ['ַ', 'ּ', 'ׁ', '׳']) + ')'


    finalCons = ['כ', 'מ', 'נ', 'פ', 'צ', 'פּ', 'כּ']
    finals = ['ך', 'ם', 'ן', 'ף', 'ץ', 'ףּ', 'ךּ']

    otherCons = 'ב,ח,ע,צ,ש,ת'.split(',')
    consonantsAll = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Hebrew') + finals  + otherCons + ['׳']) + ')'

    vowels = ['ְ','ֱ','ֲ','ֳ','ִ','ֵ','ֶ','ַ','ָ','ֹ','ֺ','ֻ','ׇ']
    vowelsR = '(' + '|'.join(vowels + ['וֹ', 'וּ']) + ')'

    for f,c in zip(finals, finalCons):
        Strng = Strng.replace(f, c)

    # Swap the order of diacritics
    Strng = re.sub(vowelsR + '([ּׁׂ])', r'\2\1', Strng)

    ## gimme, teh and other consonants  with Dagesh just replace themselves
    #Strng = re.sub('([דתצ])(ּ)', r'\1', Strng)

    ## approx vowels

    # Short vowels with Schwa
    Strng = Strng.replace('אֲ', 'אַ')
    Strng = Strng.replace('עֲ', 'אַ')

    Strng = Strng.replace('\u05B1', '\u05B6').replace('\u05B3', '\u05B9').replace('\u05B2','\u05b7')

    # replace malei forms
    Strng = re.sub('(?<=[ֵֶַָֹ])([א])'+'(?!' + vowelsignsA + ')', '', Strng)
    Strng = re.sub('(?<=[ִֵֶַָֹֻ])([ה])'+'(?!' + vowelsignsAD + ')', '', Strng)

    Strng = re.sub('(?<=[ֵֶ])([י])'+'(?!' + vowelsR + vowelsigns + ')', '', Strng)

    # ha + dagesh to normal ha
    Strng = Strng.replace('הּ', 'ה')

    ## consonant doubling with Dagesh

    Strng = re.sub('([' + 'שרקסנמליזט' + '])(ּ)', r'\1' + 'ְ' + 'ְ' + r'\1', Strng) ## twice to mark it specifically
    Strng = re.sub('([דתצה])(ּ)', r'\1'+ 'ְ' + 'ְ' + r'\1', Strng)


    ## approx Cons
    Strng = Strng.replace('ת', 'ט').replace('ח', 'כ').replace('ע', 'א').replace('שׂ', 'ס')
    Strng = re.sub('ש(?![ׂׄ])', 'שׁ', Strng)

    Strng = Strng.replace('ׁׁ','ׁ')

    ## replace vet with double vav if not followed by dagesh
    Strng = re.sub('ב(?!ּ)', 'װ', Strng)

    # swap garesh and short vowels
    Strng = re.sub(vowelsR + "(׳)", r'\2\1', Strng)

    ## reverse dagesh of cca jja
    Strng = Strng.replace('גּ׳', 'ג׳ְג׳').replace('צּ׳', 'צ׳ְצ׳')

    # tsa when not followed by gatresh with t+sa (including vowel signs)
    Strng = re.sub('צ' + '(?!׳)', 'טְְס', Strng)

    ## reinsert uo2dbc of vau based vowels
    Strng = re.sub('(\s|^|\.|,|א)' + '(וֹ|וּ)', 'א' + r'\1\2' , Strng)
    Strng = re.sub('(וּ)' + vowelsignsA, 'װְװ' + r'\2', Strng)

    ## vav, yod to double vav/yod if followed by short vowels or long vowels
    Strng = re.sub('י' + '(?=' + vowelsigns + '|ַ)', 'ײ', Strng)
    Strng = re.sub('ו' + '(?=' + '[ְִֵֶַָׇֺֻ]' +  '|ַ)', 'װ', Strng)

    ## replace vay ad yod in other cases when no preceded or succeeded by the vowels
    Strng  = re.sub('(?<!ִ)(י)', 'ײ' , Strng)
    Strng = re.sub('(ו)(?![ֹֺּ])', 'װ', Strng)

    ## Intrdouce Schva nach

    # Replva holem for vav with holem
    Strng = Strng.replace('ֺ','ֹ')

    # remove stray alephs
    Strng = re.sub('[א](?!' + vowelsR + ')', '', Strng)

    ## remove schwa at the end of vwords
    Strng = re.sub(consonantsAll + "(?!" + vowelsignsADShinG + ')', r'\1' + 'ְ' + r'\2', Strng)

    ## Aleph + Svha = a
    Strng = Strng.replace('אְ','')

    ## Hard Svha nakh
    if '௞' in Strng:
        # added in preoptions
        Strng = Strng.replace('௞', '')
        Strng = Strng.replace('ְ' + 'ְ','ְ')
    else:
        ## Schva nach
        # https://judaism.stackexchange.com/questions/92599/what-are-the-rules-for-shva-na
        # http://www.shailamorah.com/kriah-roundtable/teaching-shva-rules
        Strng = re.sub('(\s|\.|,|^)' + consonantsAll + '(ְ)', r'\1\2' + 'ֶ', Strng)
        Strng = re.sub('(ּ)' + '(ְ)', r'\1' + 'ֶ' , Strng)
        Strng = re.sub(consonantsAll + '(' 'ְ' + 'ְ' + ')' + '(' + r'\1' + ')(' + 'ְ' + ')', r'\1\2\3' +  'ֶ', Strng)
        Strng = re.sub(consonantsAll + '(ְ)' + '(' + r'\1' + ')'+ '(?!(\s|\.|\n|,|$))', r'\1' + 'ֶ' + r'\3', Strng)
        Strng = re.sub(consonantsAll + '(ְ)' + consonantsAll + '(ְ)' + '(?!(\s|\.|\n|,|$))', r'\1\2' + r'\3' + 'ֶ' , Strng)

        Strng = Strng.replace('ְ' + 'ְ','ְ') #two schva to one
        Strng = Strng.replace('ֶ' + 'ְ','ְ') #two schva to one

    ## remove patesh
    Strng = re.sub('(?<![אע])\u05B7', '', Strng)

    Strng = Strng.replace('௞', '')

    return Strng

def FixHebrew(Strng, reverse = False):
    return _FixHebrewDecode(Strng) if reverse else _FixHebrewEncode(Strng)


def _FixMongolianEncode(Strng):
    vowels = '(' + '|'.join(GM.CrunchSymbols(GM.Vowels, 'Mongolian')) + ')'
    consonants = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Mongolian')) + ')'

    #Strng = re.sub(consonants + '?' + vowels + '([\u1880\u1881])?', r'\1\2\3 ', Strng)
    Strng = re.sub('(\u180B)' + consonants, r'\2', Strng)
    Strng = re.sub('(\u180B)' + vowels, r'\2', Strng)

    Strng = re.sub(consonants + consonants + consonants + vowels + '(\u1880)', r'\5\1\2\3\4', Strng)
    Strng = re.sub(consonants + consonants + vowels + '(\u1880)', r'\4\1\2\3', Strng)
    Strng = re.sub(consonants + '?' + vowels + '(\u1880)', r'\3\1\2', Strng)
    Strng = Strng.replace(' \u02BC', '\u200B')
    Strng = Strng.replace('\u02BC', '\u200B')


    return Strng

def _FixMongolianDecode(Strng):
    vowels = '(' + '|'.join(GM.CrunchSymbols(GM.Vowels, 'Mongolian')) + ')'
    consonants = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Mongolian')) + ')'

    ## add variation seelct one
    #print(Strng)
    Strng = re.sub('(ᠠ)(?!\u180B)', r'\1' + '\u180B', Strng)
    #print(Strng)

    return Strng

def FixMongolian(Strng, reverse=False):
    return _FixMongolianDecode(Strng) if reverse else _FixMongolianEncode(Strng)

def _hanifi_rohingya_lookups():
    consList = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'HanifiRohingya')+['\U00010D17', '\U00010D19']) + ')'
    vowList = '(' + '|'.join(GM.CrunchSymbols(GM.Vowels, 'HanifiRohingya')) + ')'

    vowListNotA = '(' + '|'.join(GM.CrunchSymbols(GM.Vowels, 'HanifiRohingya')[1:]) + ')'

    consListLookBehind = ''.join(map(lambda x: '(?<!' + x + ')', GM.CrunchSymbols(GM.Consonants, 'HanifiRohingya')))
    return consList, vowList, vowListNotA, consListLookBehind

def _FixHanifiRohingyaEncode(Strng):
    consList, vowList, vowListNotA, consListLookBehind = _hanifi_rohingya_lookups()

    Strng = re.sub(consListLookBehind + vowList, '\U00010D00' + r'\1', Strng ) # Add Vowel Carrier
    Strng = re.sub(consList + r'\1', r'\1' + '\U00010D27', Strng) # Add Gemination

    Strng = re.sub(vowListNotA + '𐴀𐴟', r'\1' + '\U00010D17', Strng) # koi, kui etc
    Strng = re.sub(vowListNotA + '𐴀𐴞', r'\1' + '\U00010D19', Strng) # kou etc. using the dipthong character

    Strng = Strng.replace('\U00010D24\\', '\U00010D25') #swap tone 2
    Strng = Strng.replace('\U00010D24/', '\U00010D26') #swap tone 3

    Strng = Strng.replace('_', '\U00010D22') # Map Sukun

    for x,y in zip([',','?',';'],['،','؟','؛']):
        Strng = Strng.replace(x,y)

    return Strng

def _FixHanifiRohingyaDecode(Strng):
    consList, vowList, vowListNotA, consListLookBehind = _hanifi_rohingya_lookups()

    tones = '([\U00010D24\U00010D25\U00010D26])'
    Strng = re.sub('(\U00010D00)' + tones + vowList, r'\1\3\2', Strng) # Swap Vowel-carrier + tone + vowelsign
    Strng = re.sub(consList + tones + vowList, r'\1\3\2', Strng) # swap cons + tone + vowel sign

    Strng = re.sub(vowListNotA.replace('\U00010D00', '') + '\U00010D17' , r'\1' + '𐴀𐴟', Strng) #swap tone 2
    Strng = re.sub(vowListNotA.replace('\U00010D00', '') +'\U00010D19', r'\1' + '𐴀𐴞' , Strng) #swap tone 3

    Strng = Strng.replace('\U00010D00', '') # remove vowel carrier
    Strng = re.sub('(.)' + '\U00010D27', r'\1\1' , Strng) # reverse gemination

    Strng = Strng.replace('\U00010D25', '\U00010D24\\') #swap tone 2
    Strng = Strng.replace('\U00010D26', '\U00010D24/') # swap tone 3

    Strng = re.sub(consList + '\U00010D17' , r'\1' + '\U00010D16\u02BE', Strng) # cons + dipth.y -> y + nukta

    Strng = re.sub(consList +'\U00010D19', r'\1' + '\U00010D18\u02BE', Strng) # cons + dipth.w -> v + nukta

    Strng = Strng.replace('\U00010D22', '_') #remove Sukun

    Strng = Strng.replace('𐴜', '𐴖') # v -> w; Archaic v is not used anyway

    for x,y in zip([',','?',';'],['،','؟','؛']):
        Strng = Strng.replace(y,x)

    return Strng

def FixHanifiRohingya(Strng, reverse=False):
    return _FixHanifiRohingyaDecode(Strng) if reverse else _FixHanifiRohingyaEncode(Strng)
def _FixMasaramGondiEncode(Strng):
    consList = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'MasaramGondi')) + ')'

    Strng = Strng.replace('𑴌𑵅𑴪','\U00011D2E') # KSSA
    Strng = Strng.replace('𑴓𑵅𑴕','\U00011D2F') # JNYA
    Strng = Strng.replace('𑴛𑵅𑴦','\U00011D30') # TRA

    Strng = re.sub(consList + '\U00011D45\U00011D26', r'\1' + '\U00011D47', Strng) # kra
    Strng = re.sub('\U00011D26\U00011D45' + consList, '\U00011D46' + r'\1', Strng) # rka

    ## remove final virama when not followed by a consonant
    Strng = re.sub('\U00011D45(?!' + consList + ')' , '\U00011D44', Strng)

    return Strng

def _FixMasaramGondiDecode(Strng):
    consList = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'MasaramGondi')) + ')'

    Strng = Strng.replace('\U00011D2E', '𑴌𑵅𑴪') # KSSA
    Strng = Strng.replace('\U00011D2F', '𑴓𑵅𑴕') # JNYA
    Strng = Strng.replace('\U00011D30', '𑴛𑵅𑴦') # TRA

    Strng = Strng.replace('\U00011D47', '\U00011D45\U00011D26',) # kra
    Strng = Strng.replace('\U00011D46', '\U00011D26\U00011D45') # rka

    Strng = Strng.replace('\U00011D44','\U00011D45')

    return Strng

def FixMasaramGondi(Strng, reverse=False):
    return _FixMasaramGondiDecode(Strng) if reverse else _FixMasaramGondiEncode(Strng)


def _FixGunjalaGondiEncode(Strng):
    consList = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'GunjalaGondi')) + ')'

    Strng = re.sub('(\U00011D7A\u02BE)([\U00011D7B\U00011D7C\U00011D80\U00011D81])', '\U00011D95' + r'\1', Strng)
    Strng = re.sub('(\U00011D7A\u02BF)([\U00011D7D\U00011D7E\U00011D82\U00011D83])', '\U00011D95' + r'\1', Strng)

    Strng = Strng.replace('\u02BE', '')
    Strng = Strng.replace('\u02BF', '')

    ## remove final virama when not followed by a consonant
    Strng = re.sub('\U00011D97(?!' + consList + ')' , '', Strng)

    return Strng

def _FixGunjalaGondiDecode(Strng):
    consList = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'GunjalaGondi')) + ')'

    pass

    return Strng

def FixGunjalaGondi(Strng, reverse=False):
    return _FixGunjalaGondiDecode(Strng) if reverse else _FixGunjalaGondiEncode(Strng)

def _FixSoyomboEncode(Strng):
    finVir = ['\U00011A5E\U00011A99','\U00011A5C\U00011A99','\U00011A60\U00011A99','\U00011A6D\U00011A99','\U00011A6F\U00011A99','\U00011A72\U00011A99','\U00011A74\U00011A99','\U00011A7C\U00011A99','\U00011A7D\U00011A99','\U00011A7F\U00011A99','\U00011A81\U00011A99']
    fin = ['\U00011A8A','\U00011A8B','\U00011A8C','\U00011A8D','\U00011A8E','\U00011A8F','\U00011A90','\U00011A91','\U00011A92','\U00011A93','\U00011A94']
    consList = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Soyombo')) + ')'

    Strng = Strng.replace('𑩜𑪙𑪀', '\U00011A83')  #KSSA
    Strng = re.sub('\U00011A7F\U00011A99' + '(?=' + consList + ')' , '\U00011A88', Strng) # Fix shka

    ## Gemination ##
    Strng = re.sub('(?<!𑪙)(.)𑪙' + r'\1', r'\1' + '\U00011A98', Strng)
    # final consonats
    if '\u02BE' in Strng:
        for x, y in zip (finVir, fin):
            Strng = re.sub(x + '(?!' + consList + ')' , y, Strng)

        Strng = re.sub('𑪈(?!' + consList + ')' , '\U00011A93', Strng)

        Strng = Strng.replace('\u02BE', '')

    ## remove final virama when not followed by a consonant
    Strng = re.sub('\U00011A99(?!' + consList + ')' , '', Strng)

    return Strng

def _FixSoyomboDecode(Strng):
    finVir = ['\U00011A5E\U00011A99','\U00011A5C\U00011A99','\U00011A60\U00011A99','\U00011A6D\U00011A99','\U00011A6F\U00011A99','\U00011A72\U00011A99','\U00011A74\U00011A99','\U00011A7C\U00011A99','\U00011A7D\U00011A99','\U00011A7F\U00011A99','\U00011A81\U00011A99']
    fin = ['\U00011A8A','\U00011A8B','\U00011A8C','\U00011A8D','\U00011A8E','\U00011A8F','\U00011A90','\U00011A91','\U00011A92','\U00011A93','\U00011A94']
    consList = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Soyombo')) + ')'

    Strng = Strng.replace('\U00011A9A', ' ') ## Reverse Tsheg
    Strng = Strng.replace('\U00011A83', '𑩜𑪙𑪀')  #KSSA

    ## Gemination ##
    Strng = re.sub('(.)\U00011A98', r'\1' + '\U00011A99' + r'\1', Strng)

    viraCon = ['\U00011A7C\U00011A99', '\U00011A7D\U00011A99', '\U00011A81\U00011A99', '\U00011A7F\U00011A99']
    initial = ['\U00011A86', '\U00011A87', '\U00011A89', '\U00011A88']

    for x, y in zip(viraCon, initial):
        Strng = Strng.replace(y, x)

    tsaSeries = ['𑩵','𑩶','𑩷']
    caSeries = ['𑩡','𑩢','𑩣']

    for x, y in zip(tsaSeries,caSeries):
        Strng = Strng.replace(y, x)

    ## initial ##

    for x, y in zip(finVir, fin):
        Strng = Strng.replace(y, x)

    return Strng

def FixSoyombo(Strng, reverse=False):
    return _FixSoyomboDecode(Strng) if reverse else _FixSoyomboEncode(Strng)

def FixKharoshthi(Strng, reverse=False):
    Strng = KharoshthiNumerals(Strng, reverse)

    return Strng

def _FixMarchenEncode(Strng):
    subjoinCons = '𑱲 𑱳 𑱴 𑱵 𑱶 𑱷 𑱸 𑱹 𑱺 𑱻 𑱼 𑱽 𑱾 𑱿 𑲀 𑲁 𑲂 𑲃 𑲄 𑲅 𑲆 𑲇 𑲉 𑲊 𑲋 𑲌 𑲍 𑲎'.split(' ')
    subjoined = '𑲒 𑲓 𑲔 𑲕 𑲖 𑲗 𑲘 𑲙 𑲚 𑲛 𑲜 𑲝 𑲞 𑲟 𑲠 𑲡 𑲢 𑲣 𑲤 𑲥 𑲦 𑲧 𑲩 𑲪 𑲫 𑲬 𑲭 𑲮'.split(' ')

    for x, y in zip(subjoinCons, subjoined):
        Strng = Strng.replace('ʾ' + x, y)

    Strng = Strng.replace('ʾ', '')
    Strng = Strng.replace('\u02BF', '')


    return Strng

def _FixMarchenDecode(Strng):
    subjoinCons = '𑱲 𑱳 𑱴 𑱵 𑱶 𑱷 𑱸 𑱹 𑱺 𑱻 𑱼 𑱽 𑱾 𑱿 𑲀 𑲁 𑲂 𑲃 𑲄 𑲅 𑲆 𑲇 𑲉 𑲊 𑲋 𑲌 𑲍 𑲎'.split(' ')
    subjoined = '𑲒 𑲓 𑲔 𑲕 𑲖 𑲗 𑲘 𑲙 𑲚 𑲛 𑲜 𑲝 𑲞 𑲟 𑲠 𑲡 𑲢 𑲣 𑲤 𑲥 𑲦 𑲧 𑲩 𑲪 𑲫 𑲬 𑲭 𑲮'.split(' ')

    tsaSeries = ['\U00011C82', '\U00011C83', '\U00011C84']
    jaSereis =  ['\U00011C76', '\U00011C77', '\U00011C78']

    for x, y in zip(tsaSeries, jaSereis):
        Strng = Strng.replace(y, x)

    for x, y in zip(subjoinCons, subjoined):
        Strng = Strng.replace(y, 'ʾ' + x)

    return Strng

def FixMarchen(Strng, reverse=False):
    return _FixMarchenDecode(Strng) if reverse else _FixMarchenEncode(Strng)

def _FixMroEncode(Strng):
    extracons = ['\U00016A4E', '\U00016A59', '\U00016A5A', '\U00016A5B', '\U00016A5C', '\U00016A5E']
    consnormaldig = ['𖩃𖩢', '𖩌𖩢', '𖩍𖩢', '𖩍𖩣', '𖩉𖩢', '𖩀𖩢']
    consnormal = ['𖩃', '𖩌', '𖩍', '𖩍', '𖩉', '𖩀']

    for x, y in zip(consnormaldig, extracons):
        Strng = Strng.replace(x, y)

    return Strng

def _FixMroDecode(Strng):
    extracons = ['\U00016A4E', '\U00016A59', '\U00016A5A', '\U00016A5B', '\U00016A5C', '\U00016A5E']
    consnormaldig = ['𖩃𖩢', '𖩌𖩢', '𖩍𖩢', '𖩍𖩣', '𖩉𖩢', '𖩀𖩢']
    consnormal = ['𖩃', '𖩌', '𖩍', '𖩍', '𖩉', '𖩀']

    for x, y in zip(extracons, consnormal):
        Strng = Strng.replace(x, y)

    return Strng

def FixMro(Strng, reverse=False):
    return _FixMroDecode(Strng) if reverse else _FixMroEncode(Strng)

def _FixWanchoEncode(Strng):
    tonemarks = ['\U0001E2EC', '\U0001E2ED', '\U0001E2EE', '\U0001E2EF']
    tonewri = ['\\_', '\\-', '\\!', '\\;']

    nasalization = ['\U0001E2E6', '\U0001E2E7', '\U0001E2E8', '\U0001E2EA'] # o, e, aa , u ; nasalization
    nasvowels = ['\U0001E2D5', '\U0001E2DB', '\U0001E2C0', '\U0001E2DE']

    Anusvaras = ['\U0001E2E2', '\U0001E2E3', '\U0001E2E4', '\U0001E2E5'] # o, aa, a, i
    AnusvaraVowels = ['\U0001E2D5', '\U0001E2C0', '\U0001E2C1', '\U0001E2DC']

    for x, y in zip(tonemarks, tonewri):
        Strng = Strng.replace(y, x)

    for x, y in zip(nasvowels, nasalization):
        Strng = Strng.replace(x + 'ʿ', y)

    Strng = Strng.replace('ʿ', '𞋉')

    for x, y in zip(AnusvaraVowels, Anusvaras):
        Strng = Strng.replace(x + 'ʾ', y)

    Strng = Strng.replace('ʾ', '𞋝')

    Strng = Strng.replace('𞋋𞋗', '\U0001E2E1')
    Strng = Strng.replace('𞋋𞋎', '\U0001E2E0')

    Strng = Strng.replace('𞋓Ø', '\U0001E2D2') ## WA
    Strng = Strng.replace('Ø', '')



    return Strng

def _FixWanchoDecode(Strng):
    tonemarks = ['\U0001E2EC', '\U0001E2ED', '\U0001E2EE', '\U0001E2EF']
    tonewri = ['\\_', '\\-', '\\!', '\\;']

    nasalization = ['\U0001E2E6', '\U0001E2E7', '\U0001E2E8', '\U0001E2EA'] # o, e, aa , u ; nasalization
    nasvowels = ['\U0001E2D5', '\U0001E2DB', '\U0001E2C0', '\U0001E2DE']

    Anusvaras = ['\U0001E2E2', '\U0001E2E3', '\U0001E2E4', '\U0001E2E5'] # o, aa, a, i
    AnusvaraVowels = ['\U0001E2D5', '\U0001E2C0', '\U0001E2C1', '\U0001E2DC']

    for x, y in zip(tonemarks, tonewri):
        Strng = Strng.replace(x, y)

    for x, y in zip(nasvowels, nasalization):
        Strng = Strng.replace(y, x + 'ʿ')

    for x, y in zip(AnusvaraVowels, Anusvaras):
        Strng = Strng.replace(y, x + 'ʾ')

    Strng = Strng.replace('\U0001E2E1', '𞋋𞋗')
    Strng = Strng.replace('\U0001E2E0', '𞋋𞋎')

    Strng = Strng.replace('\U0001E2D2', '𞋓Ø') ## WA


    return Strng

def FixWancho(Strng, reverse=False):
    return _FixWanchoDecode(Strng) if reverse else _FixWanchoEncode(Strng)

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

def _FixBhaiksukiEncode(Strng):
    Strng = Strng.replace(' ', '𑱃')

    return Strng

def _FixBhaiksukiDecode(Strng):
    Strng = Strng.replace('𑱃', ' ')

    return Strng

def FixBhaiksuki(Strng, reverse=False):
    return _FixBhaiksukiDecode(Strng) if reverse else _FixBhaiksukiEncode(Strng)

def _FixKhudawadiEncode(Strng):
    sindhi = ['𑊽', '𑋃', '𑋉', '𑋕']
    sindhiapprox = ['ˍ𑊼', 'ˍ𑋂', 'ˍ𑋈', 'ˍ𑋔']

    for x, y in zip(sindhi, sindhiapprox):
        Strng = Strng.replace(y,x)

    return Strng

def _FixKhudawadiDecode(Strng):
    sindhi = ['𑊽', '𑋃', '𑋉', '𑋕']
    sindhiapprox = ['ˍ𑊼', 'ˍ𑋂', 'ˍ𑋈', 'ˍ𑋔']

    for x, y in zip(sindhi, sindhiapprox):
        Strng = Strng.replace(x,y)

    return Strng

def FixKhudawadi(Strng, reverse=False):
    return _FixKhudawadiDecode(Strng) if reverse else _FixKhudawadiEncode(Strng)

# Correct Ru2, Lu2 -> R, lR
def _FixTamilEncode(Strng):
    Strng = CorrectRuLu(Strng,"Tamil",False)

    ava = Tamil.SignMap[0]
    avaA = '\u0028\u0B86\u0029'

    VedicSign = ['॑', '॒', '᳚']
    TamilDiacritic = ['ʼ', 'ˮ', '꞉']#, '²', '³', '⁴', '₂', '₃', '₄']

    Strng = Strng.replace(ava+ava,avaA)
    Strng = PostProcess.RetainDandasIndic(Strng, 'Tamil', True)
    Strng = PostProcess.RetainIndicNumerals(Strng, 'Tamil', True)

    for x in TamilDiacritic:
        for y in VedicSign:
            Strng = Strng.replace(x + y, y + x)

    return Strng

def _FixTamilDecode(Strng):
    Strng = CorrectRuLu(Strng,"Tamil",True)

    ava = Tamil.SignMap[0]
    avaA = '\u0028\u0B86\u0029'

    VedicSign = ['॑', '॒', '᳚']
    TamilDiacritic = ['ʼ', 'ˮ', '꞉']#, '²', '³', '⁴', '₂', '₃', '₄']

    Strng = PostProcess.RetainDandasIndic(Strng, 'Tamil')
    Strng = PostProcess.RetainIndicNumerals(Strng, 'Tamil')
    Strng = Strng.replace(avaA,ava+ava)
    Strng = Strng.replace('ஷ²', 'ஶ')

    Strng = Strng.replace('𑌃', '꞉')

    for x in TamilDiacritic:
        for y in VedicSign:
            Strng = Strng.replace(y + x, x + y)

    return Strng

def FixTamil(Strng,reverse=False):
    return _FixTamilDecode(Strng) if reverse else _FixTamilEncode(Strng)

def _FixOriyaEncode(Strng):
    pass

    return Strng

def _FixOriyaDecode(Strng):
    Strng = Strng.replace('ଵ','ୱ')

    return Strng

def FixOriya(Strng, reverse=False):
    return _FixOriyaDecode(Strng) if reverse else _FixOriyaEncode(Strng)

def _FixGurmukhiLoCEncode(Strng):
    Strng = CorrectRuLu(Strng,"Gurmukhi",False)

    ava = Gurmukhi.SignMap[0]
    avaA = '\u0028\u0A06\u0029'

    # Tippi/Bindu conversion options are optional. Look into PostProcess

    Strng = Strng.replace(ava+ava,avaA)
    Strng = PostProcess.InsertGeminationSign(Strng, 'Gurmukhi')
    Strng = PostProcess.RetainIndicNumerals(Strng, 'Gurmukhi', True)

    Vedicomp = '([' + ''.join(GM.VedicSvarasList) + '])'

    Strng = re.sub(Vedicomp + '\u0A71' + '(.)', r'\1' + r'\2' + Gurmukhi.ViramaMap[0] + r'\2' , Strng)


    return Strng

def _FixGurmukhiLoCDecode(Strng):
    Strng = CorrectRuLu(Strng,"Gurmukhi",True)

    ava = Gurmukhi.SignMap[0]
    avaA = '\u0028\u0A06\u0029'

    # Tippi/Bindu conversion options are optional. Look into PostProcess

    Strng = PostProcess.RetainIndicNumerals(Strng, 'Gurmukhi')
    Strng = Strng.replace(avaA,ava+ava)
    Strng = PostProcess.ReverseGeminationSign(Strng, 'Gurmukhi')
    #Strng = Strng.replace('ੰਨ','ਨ੍ਨ')
    #Strng = Strng.replace('ੰਮ','ਮ੍ਮ')
    # Replace Tippi by Bindu
    #Strng = PostProcess.GurmukhiYakaash(Strng, True)

    return Strng

def FixGurmukhiLoC(Strng,reverse=False):
    return _FixGurmukhiLoCDecode(Strng) if reverse else _FixGurmukhiLoCEncode(Strng)

# Correct Ru'', Lu'' -> R, lR
# Tippi/Bindu
def _FixGurmukhiEncode(Strng):
    Strng = CorrectRuLu(Strng,"Gurmukhi",False)

    ava = Gurmukhi.SignMap[0]
    avaA = '\u0028\u0A06\u0029'

    # Tippi/Bindu conversion options are optional. Look into PostProcess

    Strng = Strng.replace(ava+ava,avaA)
    Strng = PostProcess.InsertGeminationSign(Strng, 'Gurmukhi')
    Strng = PostProcess.RetainIndicNumerals(Strng, 'Gurmukhi', True)

    Vedicomp = '([' + ''.join(GM.VedicSvarasList) + '])'

    Strng = re.sub(Vedicomp + '\u0A71' + '(.)', r'\1' + r'\2' + Gurmukhi.ViramaMap[0] + r'\2' , Strng)


    return Strng

def _FixGurmukhiDecode(Strng):
    Strng = CorrectRuLu(Strng,"Gurmukhi",True)

    ava = Gurmukhi.SignMap[0]
    avaA = '\u0028\u0A06\u0029'

    # Tippi/Bindu conversion options are optional. Look into PostProcess

    Strng = PostProcess.RetainIndicNumerals(Strng, 'Gurmukhi')
    Strng = Strng.replace(avaA,ava+ava)
    Strng = PostProcess.ReverseGeminationSign(Strng, 'Gurmukhi')
    Strng = Strng.replace('ੰਨ','ਨ੍ਨ')
    Strng = Strng.replace('ੰਮ','ਮ੍ਮ')
    # Replace Tippi by Bindu
    Strng = Strng.replace('\u0A70','\u0A02')
    Strng = PostProcess.GurmukhiYakaash(Strng, True)

    return Strng

def FixGurmukhi(Strng,reverse=False):
    return _FixGurmukhiDecode(Strng) if reverse else _FixGurmukhiEncode(Strng)

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


def _FixTamilExtendedEncode(Strng):
    Strng = Strng.replace('ക്‌ഷ', 'ക്ഷ')
    Strng = Strng.replace('ശ്‌ര', 'ശ്‍ര')
    Strng = Strng.replace('ൗ', 'ൌ')

    for svara in GM.VedicSvarasList:
        Strng = Strng.replace('\u200C' + svara, svara + '\u200C')

    return Strng

def _FixTamilExtendedDecode(Strng):
    for svara in GM.VedicSvarasList:
        Strng = Strng.replace(svara + '\u200C', '\u200C' + svara)

    Strng = Strng.replace('\u0D4D', '\u0D4D\u200C')

    return Strng

def FixTamilExtended(Strng, reverse=False):
    return _FixTamilExtendedDecode(Strng) if reverse else _FixTamilExtendedEncode(Strng)

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

def FixKhmerLoC(Strng,reverse=False):
    return FixKhmer(Strng, reverse, target="KhmerLoC")

# Khmer - Subjoining Consonants and Repha
def _FixKhmerEncode(Strng, target):
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,target))
    ListV ='|'.join(GM.CrunchSymbols(GM.VowelSigns,target))
    ListA ='|'.join(GM.CrunchSymbols(GM.CombiningSigns,target))

    ra = Khmer.ConsonantMap[26]
    vir = Khmer.ViramaMap[0]

    Strng = re.sub(vir+'('+ListC+')','\u17D2'+r'\1',Strng)
    # Introduce Repha : ra + sub Virama + Cons -> Cons + Repha
    Strng = re.sub('(?<!\u17D2)('+ra+')'+'\u17D2'+'('+ListC+')',r'\2'+'\u17CC',Strng)
    # i + Anusara -> i-Anusvara ligature
    Strng = Strng.replace('\u17B7\u17C6','\u17B9')


    return Strng

def _FixKhmerDecode(Strng, target):
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,target))
    ListV ='|'.join(GM.CrunchSymbols(GM.VowelSigns,target))
    ListA ='|'.join(GM.CrunchSymbols(GM.CombiningSigns,target))

    ra = Khmer.ConsonantMap[26]
    vir = Khmer.ViramaMap[0]

    # Replace Subjoining Virama with Explicit Virama
    Strng = Strng.replace('\u17D2',vir)
    Strng = re.sub(vir+'(?=[\u17AB\u17AC\u17AD\u17AE])','\u17D2',Strng)
    # Remove Repha : ra + sub Virama + Cons <- Cons + Repha
    Strng = re.sub('('+ListC+')'+'\u17CC',ra+vir+r'\1',Strng)
    # i + Anusara -> i-Anusvara ligature
    Strng = Strng.replace('\u17B9','\u17B7\u17C6')

    return Strng

def FixKhmer(Strng,reverse=False, target="Khmer"):
    return _FixKhmerDecode(Strng, target) if reverse else _FixKhmerEncode(Strng, target)

def _FixKhamtiShanEncode(Strng):
    Strng = Strng.replace('်ရ', 'ြ')
    Strng = Strng.replace('်ယ', 'ျ')
    Strng = Strng.replace('်ဝ', 'ွ')

    ## Maintain the order of the medials
    Strng = Strng.replace("\u103C\u103B", "\u103B\u103C")
    Strng = Strng.replace("\u103D\u103B", "\u103B\u103D")
    Strng = Strng.replace("ႂ\u103C", "\u103Cွ")

    return Strng

def _FixKhamtiShanDecode(Strng):
    Strng = Strng.replace('ꩳ', 'ရ')
    Strng = Strng.replace("\u103B\u103C", "\u103C\u103B")
    Strng = Strng.replace("\u103B\u103D", "\u103D\u103B")
    Strng = Strng.replace("\u103Cႂ", "ႂ\u103C")

    Strng = Strng.replace('ြ', '်ꩳ')
    Strng = Strng.replace('ꩳ', 'ရ')
    Strng = Strng.replace('ျ', '်ယ')
    Strng = Strng.replace('ွ', '်ဝ')

    return Strng

def FixKhamtiShan(Strng, reverse=False):
    return _FixKhamtiShanDecode(Strng) if reverse else _FixKhamtiShanEncode(Strng)

def _FixTaiLaingEncode(Strng):
    Strng = Strng.replace('်ꩺ', 'ြ')
    Strng = Strng.replace('်ယ', 'ျ')
    Strng = Strng.replace('်ဝ', 'ႂ')

    ## Maintain the order of the medials
    Strng = Strng.replace("\u103C\u103B", "\u103B\u103C")
    Strng = Strng.replace("\u103D\u103B", "\u103B\u103D")
    Strng = Strng.replace("ႂ\u103C", "\u103Cႂ")

    Strng = Strng.replace('ႂျ','်၀ျ')


    return Strng

def _FixTaiLaingDecode(Strng):
    Strng = Strng.replace("\u103B\u103C", "\u103C\u103B")
    Strng = Strng.replace("\u103B\u103D", "\u103D\u103B")
    Strng = Strng.replace("\u103Cႂ", "ႂ\u103C")

    Strng = Strng.replace('ြ', '်ꩺ')
    Strng = Strng.replace('ျ', '်ယ')
    Strng = Strng.replace('ႂ', '်ဝ')

    return Strng

def FixTaiLaing(Strng, reverse=False):
    return _FixTaiLaingDecode(Strng) if reverse else _FixTaiLaingEncode(Strng)

def _FixShanEncode(Strng):
    Strng = Strng.replace('်ရ', 'ြ')
    Strng = Strng.replace('်ယ', 'ျ')
    Strng = Strng.replace('်ဝ', '\u1082')
    #Strng = Strng.replace('်ႁ', 'ှ')

    ## Maintain the order of the medials
    Strng = re.sub('(ှ)' + '([ျြွ])', r'\2\1', Strng)
    Strng = Strng.replace("\u103C\u103B", "\u103B\u103C")
    Strng = Strng.replace("\u103D\u103B", "\u103B\u103D")
    Strng = Strng.replace("ွ\u103C", "\u103Cွ")

    ## Fix Shya
    Strng = re.sub('သျ\u02BD?ျ', 'သျ်ယ', Strng)


    return Strng

def _FixShanDecode(Strng):
    ## Reverse the order of the medials
    Strng = re.sub('([ျြွ])' + '(ှ)', r'\2\1', Strng)
    Strng = Strng.replace("\u103B\u103C", "\u103C\u103B")
    Strng = Strng.replace("\u103B\u103D", "\u103D\u103B")
    Strng = Strng.replace("\u103Cွ", "ွ\u103C")

    Strng = Strng.replace('ြ', '်ရ')
    Strng = Strng.replace('ျ', '်ယ')
    Strng = Strng.replace('ွ', '်ဝ')
    Strng = Strng.replace('\u1082', '်ဝ')
    Strng = Strng.replace('ှ', '်ႁ')

    #for old shan in case it appears
    Strng = Strng.replace('\u1039', '\u103A')

    return Strng

def FixShan(Strng, reverse=False):
    return _FixShanDecode(Strng) if reverse else _FixShanEncode(Strng)

def _FixMonEncode(Strng):
    pairs = [('င', 'ၚ'),('ဉ', 'ည'), ('ဈ', 'ၛ')]

    for x, y in pairs:
        Strng = Strng.replace(y, x)

    Strng = FixBurmese(Strng, False)

    Strng = Strng.replace('ည', '\uE001') #

    for x, y in pairs:
        Strng = Strng.replace(x, y)

    Strng = Strng.replace('\uE001', 'ည\u1039ည')

    medials_cons_mon = ['\u1039န', '\u1039မ', '\u1039လ']
    medials_mon = ['ၞ', 'ၟ', 'ၠ']

    for x, y in zip(medials_cons_mon, medials_mon):
        Strng = Strng.replace(x, y)

    Strng = Strng.replace('ၠြ', 'ြၠ')

    # Contigous Mon Medials
    for i, med1 in enumerate(medials_mon):
        for j, med2 in enumerate(medials_mon):
            Strng = Strng.replace(med1 + med2, medials_cons_mon[i] + medials_cons_mon[j])

    # Contiguous Medials + ya, ra and va
    for i, med in enumerate(medials_mon):
        Strng = Strng.replace(med + 'ျ', medials_cons_mon[i] + 'ျ')

        Strng = Strng.replace('ရ်' + med,  'ရ်' + medials_cons_mon[i])
        Strng = Strng.replace('ၚ်' + med,  'ၚ်' + medials_cons_mon[i])


    # RA + Medial

    return Strng

def _FixMonDecode(Strng):
    pairs = [('င', 'ၚ'),('ဉ', 'ည'), ('ဈ', 'ၛ')]

    for x, y in pairs:
        Strng = Strng.replace(y, x)

    Strng = FixBurmese(Strng, True)

    Strng = Strng.replace('ည', '\uE001') #

    for x, y in pairs:
        Strng = Strng.replace(x, y)

    Strng = Strng.replace('\uE001', 'ည\u1039ည')

    medials_cons_mon = ['\u1039န', '\u1039မ', '\u1039လ']
    medials_mon = ['ၞ', 'ၟ', 'ၠ']

    Strng = Strng.replace('်ရၠ', 'ၠ်ရ')

    for x, y in zip(medials_cons_mon, medials_mon):
        Strng = Strng.replace(y, x)

    Strng = Strng.replace('\u1039', '်')

    return Strng

def FixMon(Strng, reverse=False):
    return _FixMonDecode(Strng) if reverse else _FixMonEncode(Strng)

# Burmese - Tall A + Subjoning Consonants
def _FixBurmeseEncode(Strng):
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
    return _FixBurmeseDecode(Strng) if reverse else _FixBurmeseEncode(Strng)

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

def _FixTagbanwaEncode(Strng):
    Strng = PostProcess.InsertGeminationSign(Strng, 'Tagbanwa')

    return Strng

def _FixTagbanwaDecode(Strng):
    pass

    return Strng

def FixTagbanwa(Strng, reverse=False):
    return _FixTagbanwaDecode(Strng) if reverse else _FixTagbanwaEncode(Strng)

def _FixBuhidEncode(Strng):
    Strng = PostProcess.InsertGeminationSign(Strng, 'Buhid')

    return Strng

def _FixBuhidDecode(Strng):
    pass

    return Strng

def FixBuhid(Strng, reverse=False):
    return _FixBuhidDecode(Strng) if reverse else _FixBuhidEncode(Strng)

def _FixBugineseEncode(Strng):
    Strng = Strng.replace("ᨂ\u02BEᨀ","ᨃ")
    Strng = Strng.replace("ᨆ\u02BEᨄ","ᨇ")
    Strng = Strng.replace("ᨊ\u02BEᨑ","ᨋ")
    Strng = Strng.replace("ᨎ\u02BEᨌ","ᨏ")

    Strng = PostProcess.InsertGeminationSign(Strng, 'Buginese')

    Strng = Strng.replace('\u02BE', '')

    return Strng

def _FixBugineseDecode(Strng):
    Strng = Strng.replace("ᨃ", "ᨂ\u02BEᨀ")
    Strng = Strng.replace("ᨇ", "ᨆ\u02BEᨄ")
    Strng = Strng.replace("ᨋ", "ᨊ\u02BEᨑ")
    Strng = Strng.replace("ᨏ", "ᨎ\u02BEᨌ")

    return Strng

def FixBuginese(Strng, reverse=False):
    return _FixBugineseDecode(Strng) if reverse else _FixBugineseEncode(Strng)


# Balinese Repha
def _FixBalineseEncode(Strng):
    Repha = '\u1B03'

    Strng = AddRepha(Strng,"Balinese",Repha,False)

    pass

    return Strng

def _FixBalineseDecode(Strng):
    Repha = '\u1B03'

    Strng = AddRepha(Strng,"Balinese",Repha,True)

    # reversing archaic jna
    Strng = Strng.replace('ᭌ', 'ᬚ᭄ᬜ')
    # Fix a-based vowels
    vowelsA = ['ᬅᬶ', 'ᬅᬷ', 'ᬅᬸ', 'ᬅᬹ', 'ᬅᬺ', 'ᬅᬻ', 'ᬅ᭄ᬮᭂ', 'ᬅ᭄ᬮᭃ', 'ᬅᬾ', 'ᬅᬿ', 'ᬅᭀ', 'ᬅᭁ']
    vowels = ['ᬇ', 'ᬈ', 'ᬉ', 'ᬊ', 'ᬋ', 'ᬌ', 'ᬍ', 'ᬎ', 'ᬏ', 'ᬐ', 'ᬑ', 'ᬒ']

    for v, vA in zip(vowels, vowelsA):
        Strng = Strng.replace(vA, v)

    return Strng

def FixBalinese(Strng,reverse=False):
    return _FixBalineseDecode(Strng) if reverse else _FixBalineseEncode(Strng)

# Javanese - Reppha & Subjoining ra & ya
def _FixDivesAkuruEncode(Strng):
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

def _FixDivesAkuruDecode(Strng):
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

def FixDivesAkuru(Strng, reverse=False):
    return _FixDivesAkuruDecode(Strng) if reverse else _FixDivesAkuruEncode(Strng)

# Javanese - Reppha & Subjoining ra & ya
def _FixKawiEncode(Strng):
    target = 'Kawi'

    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,target))
    ListV ='|'.join(GM.CrunchSymbols(GM.VowelSigns,target))
    ListA ='|'.join(GM.CrunchSymbols(GM.CombiningSigns,target))

    ra = Kawi.ConsonantMap[26]
    vir = Kawi.ViramaMap[0]
    aVS = '\U00011F34'
    aVSAlt = '\U00011F35'
    E = '\U00011F3E'
    AA = '\U00011F34'

    Strng = re.sub(vir+'('+ListC+')','\U00011F42'+r'\1',Strng)
    # Introduce Repha : ra + sub Virama + Cons -> Cons + Repha
    Strng = re.sub('(?<!\U00011F42)'+ra+'\U00011F42'+'('+ListC+')','\U00011F02'+r'\1',Strng)
    #special AA
    TallACons = '|'.join(['\U00011F26', '\U00011F16', '\U00011F1C'])

    Strng = re.sub('(?<!\U00011F42)('+TallACons+')'+'('+E+'?)'+AA,r'\1\2'+'\U00011F35',Strng)

     ## buddho --> Tall A
    Strng = re.sub('('+TallACons+')(\U00011F42)('+ListC +')'+'('+E+'?)'+AA,r'\1\2\3\4'+'\U00011F35',Strng)
    Strng = re.sub('('+TallACons+')(\U00011F42)('+ListC +')'+'(\U00011F42)('+ListC +')'+'('+E+'?)'+AA,r'\1\2\3\4\5\6'+'\U00011F35',Strng)

    ## post-base consonant signs do not need disambiguating AA
    postBaseCons = '|'.join(['\U00011F1A', '\U00011F26', '\U00011F27', '\U00011F2B', '\U00011F31'])
    Strng = re.sub('(\U00011F42)('+postBaseCons+')'+'(\U00011F35)', r'\1\2' + AA, Strng)



    return Strng

def _FixKawiDecode(Strng):
    target = 'Kawi'

    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,target))
    ListV ='|'.join(GM.CrunchSymbols(GM.VowelSigns,target))
    ListA ='|'.join(GM.CrunchSymbols(GM.CombiningSigns,target))

    ra = Kawi.ConsonantMap[26]
    vir = Kawi.ViramaMap[0]
    aVS = '\U00011F34'
    aVSAlt = '\U00011F35'
    E = '\U00011F3E'
    AA = '\U00011F34'

    # Replace Subjoining Virama with Explicit Virama
    Strng = Strng.replace('\U00011F42',vir)
    # Replace Repha
    Strng = Strng.replace('\U00011F02', ra + vir)
    # reverse AltA
    Strng = Strng.replace(aVSAlt, aVS)
    # reverse JNA
    Strng = Strng.replace('\U00011F33', '𑼙𑽂𑼛')
    # decompose ind.vowels
    Strng = Strng.replace('\U00011F04\U00011F34', '\U00011F05').replace('\U00011F06\U00011F34', '\U00011F07').replace('\U00011F08\U00011F34', '\U00011F09')
    # reverse Alt ai, alt au
    Strng = Strng.replace('\U00011F3E\U00011F3E', '\U00011F3F')

    return Strng

def FixKawi(Strng, reverse=False):
    return _FixKawiDecode(Strng) if reverse else _FixKawiEncode(Strng)

# Javanese - Reppha & Subjoining ra & ya
def _FixJavaneseEncode(Strng):
    Repha = '\uA982'
    vir = Javanese.ViramaMap[0]
    ra, ya = Javanese.ConsonantMap[26], Javanese.ConsonantMap[25]
    SubRa, SubYa = '\uA9BF','\uA9BE'

    Strng = AddRepha(Strng,"Javanese",Repha,False)

    # Introduce subjoining Ra & Ya
    Strng = Strng.replace(vir+ra,SubRa).replace(vir+ya,SubYa)


    return Strng

def _FixJavaneseDecode(Strng):
    Repha = '\uA982'
    vir = Javanese.ViramaMap[0]
    ra, ya = Javanese.ConsonantMap[26], Javanese.ConsonantMap[25]
    SubRa, SubYa = '\uA9BF','\uA9BE'

    Strng = AddRepha(Strng,"Javanese",Repha,True)

    #Fix Archaic Jna
    Strng = Strng.replace('ꦘ', 'ꦗ꧀ꦚ')
    # Fix ra agang
    Strng = Strng.replace('ꦬ', ra)
    # Replace Subjoining forms with cons+vir
    Strng = Strng.replace(SubRa,vir+ra).replace(SubYa,vir+ya)
    # reversing archaic jna
    Strng = Strng.replace('ᭌ', 'ᬚ᭄ᬜ')
    # reverse a-based vowels
    vowelsA = ['ꦄꦶ', 'ꦄꦷ', 'ꦄꦸ', 'ꦄꦹ', 'ꦄꦽ', 'ꦄ꧀ꦉꦴ', 'ꦄ꧀ꦭꦼ', 'ꦄ꧀ꦭꦼꦴ', 'ꦄꦺ', 'ꦄꦻ', 'ꦄꦺꦴ', 'ꦄꦻꦴ']
    vowels = ['ꦆ', 'ꦇ', 'ꦈ', 'ꦈꦴ', 'ꦉ', 'ꦉꦴ', 'ꦊ', 'ꦋ', 'ꦌ', 'ꦍ', 'ꦎ', 'ꦎꦴ']

    for v, vA in zip(vowels, vowelsA):
        Strng = Strng.replace(vA, v)


    return Strng

def FixJavanese(Strng,reverse=False):
    return _FixJavaneseDecode(Strng) if reverse else _FixJavaneseEncode(Strng)


def FixUrdu(Strng, reverse=False):
    return FixUrduShahmukhi("Urdu", Strng, reverse)


def FixShahmukhi(Strng, reverse=False):
    return FixUrduShahmukhi('Shahmukhi', Strng, reverse)

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
def _FixThaanaEncode(Strng):
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'Thaana'))
    VowelVS = '|'.join(GM.CrunchSymbols(GM.VowelSigns,'Thaana'))
    aBase = '\u0787'

    # Replace VS-A + Vowel Sign -> Vowel Sign :
    Strng = PostProcess.InsertGeminationSign(Strng, 'Thaana')
    Strng = re.sub("(\u07A6)"+"(?=("+VowelVS+"))","",Strng)
    Strng = Strng.replace("\u02BE","")

    for x,y in zip([',','?',';'],['،','؟','؛']):
        Strng = Strng.replace(x,y)

    Strng = Strng.replace('ʔ', 'އް')


    return Strng

def _FixThaanaDecode(Strng):
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'Thaana'))
    VowelVS = '|'.join(GM.CrunchSymbols(GM.VowelSigns,'Thaana'))
    aBase = '\u0787'

    # Add VS-A to all VowelSigns
    # Approximate
    Strng = Strng.replace('ޢ','އ')
    Strng = Strng.replace('ޡ','ތ')
    Strng = Strng.replace('ޥ','ވ') # waav to va
    Strng = Strng.replace('ޠ','ތ') # To to ta
    Strng = Strng.replace('ޟ','ސ')
    Strng = Strng.replace('ޞ','ސ')
    Strng = Strng.replace('ޜ','ށ')
    Strng = Strng.replace('ޛ','ދ')
    Strng = Strng.replace('ޘ','ތ')
    Strng = Strng.replace('ޛ','ދ')
    Strng = Strng.replace('ޙ', 'ހ')

    Strng = re.sub('(' + ListC.replace('ަ','') + ')' + '(?!' + VowelVS + '|ަ' + ')', r'\1' + 'ް', Strng)

    Strng = re.sub('(?<!'+aBase+')(?<!'+'\u02BD\u02BD\u02BD'+')('+VowelVS+')',"\u07A6"+r'\1',Strng)
    Strng = PostProcess.ReverseGeminationSign(Strng, 'Thaana')

    Strng = Strng.replace('އް','ʔ')

    for x,y in zip([',','?',';'],['،','؟','؛']):
        Strng = Strng.replace(y,x)

    return Strng

def FixThaana(Strng, reverse=False):
    return _FixThaanaDecode(Strng) if reverse else _FixThaanaEncode(Strng)

def _FixSaurashtraEncode(Strng):
    Strng = Strng.replace('ꢒ꣄ꢰ', 'ꢒ꣄‍ꢰ') # Ksha

    return Strng

def _FixSaurashtraDecode(Strng):
    Strng = Strng.replace('ꢴ','꣄ꢲ')

    return Strng

def FixSaurashtra(Strng, reverse=False):
    return _FixSaurashtraDecode(Strng) if reverse else _FixSaurashtraEncode(Strng)

def FixTibetanLoC(Strng,reverse=False):
    return FixTibetan(Strng,reverse, swapNative=False)

# Tibetan Subjoining Consnants
def _FixTibetanEncode(Strng, swapNative):
    ListC = [Tibetan.ViramaMap[0]+chr(x) for x in range(0x0F40,0x0F68)] # Consonants
    ListSubC = [chr(x+80) for x in range(0x0F40,0x0F68)] # Subjoined Consonants

    SubC = ["ཝྭ","ཡྱ","རྱ","རྭ", "ྺྭ"]
    SubMinC = ["ཝྺ","ཡྻ","ཪྻ","ཪྺ", "ྺྺ"]

    #introduce virama for Jihva/Upadh
    Strng = re.sub('([ྈྉ])', r'\1' + '\u0f84',  Strng)

    for x,y in zip(ListC,ListSubC):
        Strng = Strng.replace(x,y)

    for x,y in zip(SubC,SubMinC):
        Strng = Strng.replace(x,y)

    Strng = Strng.replace(' ', '\u0F0B')

    Strng = Strng.replace("ཛྷ༹", "ཞ")

    Strng = Strng.replace("(", "༺")
    Strng = Strng.replace(")", "༻")

    Strng = Strng.replace("{", "༼")
    Strng = Strng.replace("}", "༽")



    return Strng

def _FixTibetanDecode(Strng, swapNative):
    ListC = [Tibetan.ViramaMap[0]+chr(x) for x in range(0x0F40,0x0F68)] # Consonants
    ListSubC = [chr(x+80) for x in range(0x0F40,0x0F68)] # Subjoined Consonants

    SubC = ["ཝྭ","ཡྱ","རྱ","རྭ", "ྺྭ"]
    SubMinC = ["ཝྺ","ཡྻ","ཪྻ","ཪྺ", "ྺྺ"]



    AspirateDecom= ["གྷ", "ཌྷ", "དྷ", "བྷ", "ཛྷ", "ྒྷ", "ྜྷ", "ྡྷ", "ྦྷ", "ྫྷ"]
    AspirateAtomic = ["གྷ", "ཌྷ", "དྷ", "བྷ", "ཛྷ", "ྒྷ", "ྜྷ", "ྡྷ", "ྦྷ", "ྫྷ"]

    for x, y in zip(AspirateDecom, AspirateAtomic):
        Strng = Strng.replace(x, y)

    for x,y in zip(SubC,SubMinC):
        Strng = Strng.replace(y,x)

    for x,y in zip(ListC,ListSubC):
        Strng = Strng.replace(y,x)

    for x,y in zip(['྄རྀ','྄རཱྀ','྄ལྀ',"྄ལཱྀ"],['ྲྀ','ྲཱྀ', 'ླྀ','ླཱྀ']):
        Strng = Strng.replace(x,y)

    Strng = Strng.replace('་', ' ')
    Strng = Strng.replace("༔", "།")
    Strng = Strng.replace("༈", "།")

    Strng = Strng.replace("༺", "(")
    Strng = Strng.replace("༻", ")")

    Strng = Strng.replace("༼", "{")
    Strng = Strng.replace("༽", "}")

    #remove virama from Jihva/Upadh
    Strng = re.sub('([ྈྉ])(\u0f84)', r'\1',  Strng)

    if swapNative:
        Strng = Strng.replace('ཇྷ', 'ཛྷ') ## JHA -> DZHA
        Strng = Strng.replace("ཇ", "ཛ")
        Strng = Strng.replace('ཅ', 'ཙ')
        Strng = Strng.replace('ཆ', 'ཚ')
        Strng = Strng.replace("ཞ", "ཛྷ༹")
        Strng = Strng.replace("འ", "ཨ")

    return Strng

def FixTibetan(Strng,reverse=False, swapNative = True):
    return _FixTibetanDecode(Strng, swapNative) if reverse else _FixTibetanEncode(Strng, swapNative)

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

def _FixKhomThaiEncode(Strng):
    Strng = Strng.replace('โ','เา')
    Strng = ThaiReverseVowelSigns(Strng,False)
    Strng = re.sub('(.\u0E3A)(.\u0E3A)(ใ)', r'\3\1\2', Strng) # reversed
    Strng = re.sub('(.\u0E3A)(ใ)', r'\2\1', Strng) # reversed

    Strng = re.sub('((.\u0E3A)+)(เ)', r'\3\1', Strng) # reversed
    Strng = re.sub('(.\u0E3A)?(.)(ฺร)', r'\3\1\2', Strng) # reversed
    Strng = Strng.replace('เอา', 'โอ')

    Strng = Strng.replace("เอำ", 'เาอํ')
    Strng = Strng.replace('เาอํ', 'โอํ')

    return Strng

def _FixKhomThaiDecode(Strng):
    Strng = re.sub('(ใ)(.\u0E3A)(.\u0E3A)', r'\2\3\1', Strng)
    Strng = re.sub('(ใ)(.\u0E3A)', r'\2\1', Strng)

    Strng = re.sub('(ฺร)(.\u0E3A)?(.)', r'\2\3\1', Strng)
    Strng = re.sub('(เ)((.\u0E3A)+)', r'\2\1', Strng)
    Strng = ThaiReverseVowelSigns(Strng,True)
    Strng = Strng.replace('เา', 'โ')

    return Strng

def FixKhomThai(Strng, reverse=False):
    return _FixKhomThaiDecode(Strng) if reverse else _FixKhomThaiEncode(Strng)

def FixThai(Strng,reverse=False,transcription_mode=False):
    Strng = ThaiReverseVowelSigns(Strng,reverse)
    Strng = ThaiDigraphConjuncts(Strng,reverse)

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

def _FixLaoPaliEncode(Strng, transcription_mode):
    Strng = ReverseVowelSigns(Strng,"LaoPali",False)

    if transcription_mode:
        Strng = LaoPaliTranscribe(Strng, True)

        Strng = Strng.replace("ຫ຺໌","ຫ໌")

    Strng = Strng.replace("\u0EB2\u0ECD","\u0EB3")

    return Strng

def _FixLaoPaliDecode(Strng, transcription_mode):
    Strng = ReverseVowelSigns(Strng,"LaoPali",True)

    if transcription_mode:
        Strng = LaoPaliTranscribe(Strng, True)

        Strng = Strng.replace("ຫ຺໌","ຫ໌")

    # VS AA + Anusvara <- VS AM (Ligature)
    Strng= Strng.replace("\u0EB3","\u0EB2\u0ECD")

    return Strng

def FixLaoPali(Strng,reverse=False,transcription_mode=False):
    return _FixLaoPaliDecode(Strng, transcription_mode) if reverse else _FixLaoPaliEncode(Strng, transcription_mode)

def _FixMakasarEncode(Strng):
    ListC = "|".join(Makasar.ConsonantMap)
    #ListV = "|".join(Makasar.VowelSignMap)
    #print(ListV)
    ListV = "|".join(['\U00011EF3', '\U00011EF4', '\U00011EF5', '\U00011EF6'])
    Anka = '\U00011EF2'
    #print(Makasar.VowelSignMap)

    Strng = PostProcess.InsertGeminationSign(Strng, 'Makasar')
    Strng = Strng.replace('\u02BE', '').replace('\u02BD', '')
    Strng = re.sub('(' + ListC + ')' + '(' + ListV + ')?' + r'\1', r'\1' + r'\2' + Anka, Strng)

    return Strng

def _FixMakasarDecode(Strng):
    ListC = "|".join(Makasar.ConsonantMap)
    #ListV = "|".join(Makasar.VowelSignMap)
    #print(ListV)
    ListV = "|".join(['\U00011EF3', '\U00011EF4', '\U00011EF5', '\U00011EF6'])
    Anka = '\U00011EF2'
    #print(Makasar.VowelSignMap)

    Strng = re.sub('(' + ListC + ')' + '(' + ListV + ')?' + Anka, r'\1' + r'\2' + r'\1', Strng)

    return Strng

def FixMakasar(Strng, reverse=False):
    return _FixMakasarDecode(Strng) if reverse else _FixMakasarEncode(Strng)

def _FixAvestanEncode(Strng):
    extraCons = ["\U00010B33","\U00010B32","\U00010B1D","\U00010B12", '𐬣', '𐬝']
    ListC = "|".join(GM.CrunchSymbols(GM.Consonants, "Avestan")+extraCons)
    ListV = "|".join(GM.CrunchSymbols(GM.Vowels,"Avestan"))

    ya = Avestan.ConsonantMap[25]
    va = Avestan.ConsonantMap[28]
    ii = Avestan.VowelMap[2] * 2
    uu = Avestan.VowelMap[4] * 2

    Strng = Strng.replace('𐬀𐬩', '𐬄') ## aM
    Strng = Strng.replace('𐬁𐬩', '𐬅') ## AM

    Strng = re.sub("(("+ListV+")"+"|"+"("+ListC+"))"+"("+ya+")",r'\1'+ii,Strng)
    Strng = re.sub("(("+ListV+")"+"|"+"("+ListC+"))"+"("+va+")",r'\1'+uu,Strng)

    Strng = Strng.replace(Avestan.ConsonantMap[15]  + '\u02BF', '\U00010B1D') ## TTE
    Strng = Strng.replace(va + '\u02BF', '\U00010B21') # BHA

    Strng = Strng.replace('𐬰\u02BF', '𐬲').replace('𐬱\u02BF', '𐬲') ## ZHA
    Strng = Strng.replace('𐬢\u02BF','𐬤') ## NGVA
    Strng = Strng.replace('𐬁_𐬋', '𐬃') ## AO

    Strng = Strng.replace('\u02BF', '')




    return Strng

def _FixAvestanDecode(Strng):
    extraCons = ["\U00010B33","\U00010B32","\U00010B1D","\U00010B12", '𐬣', '𐬝']
    ListC = "|".join(GM.CrunchSymbols(GM.Consonants, "Avestan")+extraCons)
    ListV = "|".join(GM.CrunchSymbols(GM.Vowels,"Avestan"))

    ya = Avestan.ConsonantMap[25]
    va = Avestan.ConsonantMap[28]
    ii = Avestan.VowelMap[2] * 2
    uu = Avestan.VowelMap[4] * 2

    Strng = Strng.replace('𐬄', '𐬀𐬩')
    Strng = Strng.replace('𐬅', '𐬁𐬩')

    Strng = Strng.replace(ii, ya).replace(uu, va)

    #print('I am here')

    Strng = Strng.replace('\U00010B1D', Avestan.ConsonantMap[15]  + '\u02BF')
    Strng = Strng.replace('𐬣', Avestan.ConsonantMap[4])

    Strng = Strng.replace('\U00010B12', Avestan.ConsonantMap[1])
    Strng = Strng.replace('\U00010B33', Avestan.ConsonantMap[29])
    Strng = Strng.replace('𐬡', va + '\u02BF')

    Strng = Strng.replace('𐬲', '𐬰\u02BF') ## ZHA
    Strng = Strng.replace('𐬤', '𐬢\u02BF') ## NGVA
    Strng = Strng.replace('𐬃', '𐬁_𐬋') ## AO

    ## 𐬲𐬤𐬃  approximate this

    ### Replave JHA + Nukta as ZHA in Devanagari & Gujarati

    return Strng

def FixAvestan(Strng, reverse=False):
    return _FixAvestanDecode(Strng) if reverse else _FixAvestanEncode(Strng)

def _FixLaoEncode(Strng):

    Strng = Strng.replace("ທ\uEB0A", "ດ")
    Strng = Strng.replace("ປ\uEB0A", 'ບ')
    Strng = Strng.replace("ພ\uEB0A",'ຟ')

    Strng = re.sub("(?<!ດ)(?<!ບ)(?<!ຟ)\uEB0A", "", Strng)

    Strng = ReverseVowelSigns(Strng,"Lao",False)
    Strng = LaoTranscribe(Strng,False)

    Strng = Strng.replace("\u0EB2\u0ECD","\u0EB3")

    # Remove the Pseduo Nukta
    Strng = Strng.replace("\uEB0A", "")


    return Strng

def _FixLaoDecode(Strng):
    Strng = Strng.replace("ດ", "ທ\uEB0A")
    Strng = Strng.replace('ບ', "ປ\uEB0A")
    Strng = Strng.replace('ຟ', "ພ\uEB0A")
    Strng = Strng.replace('ັ','ະ')


    Strng = ReverseVowelSigns(Strng,"Lao",True)
    Strng = LaoTranscribe(Strng,True)

    # VS AA + Anusvara <- VS AM (Ligature)
    Strng= Strng.replace("\u0EB3","\u0EB2\u0ECD")

    # Swap Nukta
    Strng = Strng.replace("\u0EBA\uEB0A","\uEB0A\u0EBA")

    ## Fix NHukt and vowe a short a

    Strng = Strng.replace('຺ະ', '')
    #Strng = Strng.replace('຺', '')

    Strng = Strng.replace('ອ\u0EBAົ','ອົ')

    return Strng

def FixLao(Strng,reverse=False):
    return _FixLaoDecode(Strng) if reverse else _FixLaoEncode(Strng)

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

def FixOldPersian(Strng,reverse=False):
    Strng = OldPersianSyllable(Strng,reverse)
    Strng = OldPersianNumeral(Strng,reverse)

    return Strng

# Syllabization of Persian
# d<a> +i -> d<i> + i
# d<a> + u -> d<u> + u
def OldPersianSyllable(Strng,reverse=True):
    ICons = [x+'\U000103A1' for x in ['\U000103AD','\U000103B6','\U000103A9','\U000103BA','\U000103AB','\U000103B4','\U000103BC']]
    ICons_ = [x+'_\U000103A1' for x in ['\U000103AD','\U000103B6','\U000103A9','\U000103BA','\U000103AB','\U000103B4','\U000103BC']]
    ISyll = [x+'\U000103A1' for x in ['\U000103AE','\U000103B7','\U000103AA','\U000103BB','\U000103AB','\U000103B4','\U000103BC']]

    UCons = [x+'\U000103A2' for x in ['\U000103AD','\U000103B6','\U000103A3','\U000103A5','\U000103AB','\U000103B4','\U000103BC']]
    UCons_ = [x+'_\U000103A2' for x in ['\U000103AD','\U000103B6','\U000103A3','\U000103A5','\U000103AB','\U000103B4','\U000103BC']]
    USyll = [x+'\U000103A2' for x in ['\U000103AF','\U000103B8','\U000103A4','\U000103A6','\U000103AC','\U000103B5','\U000103BD']]

    ACons = [x+'<\U000103A0' for x in ['\U000103AD','\U000103B6','\U000103A3','\U000103A5','\U000103A9','\U000103BA','𐎼','𐎴','𐎫']]
    ASyll = ['\U000103AD','\U000103B6','\U000103A3','\U000103A5','\U000103A9','\U000103BA','𐎼','𐎴','𐎫']

    SylAlpha = '([𐎧𐎨𐏂𐎰𐎱𐎳𐎲𐎹𐎾𐎿𐏀𐏁𐏃])'

    ListC = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'OldPersian')) + ')'

    if not reverse:
        #print(Strng)
        Strng = Strng.replace(" ","\U000103D0").replace("_","").replace("<","")
        for x,y in zip(ICons+UCons+ACons,ISyll+USyll+ASyll):
            Strng = Strng.replace(x,y)
        #print(Strng)
    else:
        Strng = re.sub('𐎻(?!\U000103A1)', '𐎻\U000103A1', Strng)

        for x,y in zip(ICons_+UCons_,ISyll+USyll):
            Strng = Strng.replace(y,x)

        Strng = re.sub(SylAlpha + '(𐎠𐎡)', r'\1<\2', Strng)
        Strng = re.sub(SylAlpha + '(𐎠𐎢)', r'\1<\2', Strng)

        Strng = re.sub(ListC + '\U000103A0', r'\1' + '_\U000103A0', Strng)
        Strng = re.sub(SylAlpha + '([\U000103A1\U000103A2])', r'\1_\2', Strng)

        Strng = re.sub('([' + "".join(ASyll) + '])' + '([\U000103A1\U000103A2])', r'\1' + '<' + '\U000103A0' + r'\2' , Strng)

        Strng = Strng.replace('𐏐',' ')



    if not reverse:
        # Replace Space with Word Sperator
        # Remove _ - (why :-/ )
        pass
        #Strng = Strng.replace(" ","\U000103D0").replace("_","").replace("<","")
    else:
        pass
        #Strng = re.sub('([\U000103AD\U000103B6\U000103A3\U000103A5\U000103A9\U000103BA])_\U000103A0(?![𐎡𐎢])',r"\1",Strng)


    ## Fix dai Vs tai

    return Strng

# Convert numbers into Persinal Numeral System
def OldPersianNumeral(Strng,reverse=False):
    One = '\U000103D1'
    Two = '\U000103D2'
    Ten = '\U000103D3'
    Twenty = '\U000103D4'
    Hundred = '\U000103D5'

    Numbers = sorted(map(int,re.findall("\d+", Strng)),reverse=True)

    if not reverse:
        for num in Numbers:
            hN = int(num / 100)
            tW = int((num - (hN*100)) / 20)
            tN = int((num - (hN*100) - (tW*20)) /10)
            t2 = int((num - (hN*100) - (tW*20) - (tN*10)) /2)
            n1 = int(num - (hN*100) - (tW*20) - (tN*10) - (t2*2))

            perNum = (Hundred*hN) + (Twenty*tW) + (Ten*tN) + (Two*t2) + (One*n1)

            Strng = Strng.replace(str(num),perNum)
    else:
        Strng = Strng.replace(One, '1#')
        Strng = Strng.replace(Two, '2#')
        Strng = Strng.replace(Ten, '10#')
        Strng = Strng.replace(Twenty, '20#')
        Strng = Strng.replace(Hundred, '100#')

    return Strng

def KharoshthiNumerals(Strng, reverse=False):
    Numbers = sorted(map(int,re.findall("\d+", Strng)),reverse=True)

    if not reverse:
        for num in Numbers:
             Strng = Strng.replace(str(num),kharoshthiNumber(num))
    else:
        one = '𐩀'
        two = '𐩁'
        three = '𐩂'
        four = '𐩃'
        ten = '𐩄'
        twenty = '𐩅'
        hundred = '𐩆'
        thousand = '𐩇'

        Strng = Strng.replace(one, '1#')
        Strng = Strng.replace(two, '2#')
        Strng = Strng.replace(three, '3#')
        Strng = Strng.replace(four, '4#')
        Strng = Strng.replace(ten, '10#')
        Strng = Strng.replace(twenty, '20#')
        Strng = Strng.replace(hundred, '100#')
        Strng = Strng.replace(thousand, '1000#')


    return Strng

def kharoshthiNumber(Strng):
    one = '𐩀'
    two = '𐩁'
    three = '𐩂'
    four = '𐩃'
    ten = '𐩄'
    twenty = '𐩅'
    hundred = '𐩆'
    thousand = '𐩇'

    num = int(Strng)
    kharnum = ''
    thou = int(num/1000)
    if thou > 0:
        if thou > 1:
            kharnum += kharoshthiNumber(thou)
        kharnum += thousand
    hund = int((num - (thou*1000))/100)
    if hund > 0:
        if hund > 1:
            kharnum += kharoshthiNumber(hund)
        kharnum += hundred
    twen = int((num - (thou*1000) - (hund * 100))/20)
    if twen > 0:
        kharnum += twenty * twen
    tenn = int((num - (thou*1000) - (hund * 100) - (twen*20))/10)
    if tenn > 0:
        if tenn > 1:
            kharnum += kharoshthiNumber(tenn)
        kharnum += ten
    ones = int((num - (thou*1000) - (hund * 100) - (twen*20) - (tenn * 10)))
    if ones > 0:
        if ones == 1:
            kharnum += one
        elif ones == 2:
            kharnum += two
        elif ones == 3:
            kharnum += three
        elif ones == 4:
            kharnum += four
        elif ones == 5:
            kharnum += four + one
        elif ones == 6:
            kharnum += four + two
        elif ones == 7:
            kharnum += four + three
        elif ones == 8:
            kharnum += four + four
        elif ones == 9:
            kharnum += four + four + one

    return kharnum

def _FixSinhalaEncode(Strng):
    Strng = PostProcess.SinhalaDefaultConjuncts(Strng)

    Strng = PostProcess.RetainIndicNumerals(Strng, 'Sinhala', True)
    #Sinhala JNA
    Strng = Strng.replace("\u0DA2\u0DCA\u0DA4","\u0DA5")
    #sinhala
    Strng = Strng.replace("(අ)(අ)","(ආ)")


    return Strng

def _FixSinhalaDecode(Strng):
    Strng = PostProcess.SinhalaDefaultConjuncts(Strng)

    #sinhala numerals
    Strng = PostProcess.RetainIndicNumerals(Strng, 'Sinhala')
    Strng = Strng.replace("\u0DA5","\u0DA2\u0DCA\u0DA4")
    ## Remove joiners
    Strng = Strng.replace("‍","")
    Strng = Strng.replace("(ආ)","(අ)(අ)")


    return Strng

def FixSinhala(Strng, reverse=False):
    return _FixSinhalaDecode(Strng) if reverse else _FixSinhalaEncode(Strng)

def _FixSantaliEncode(Strng):
    Strng = Strng.replace('ᱹᱸ', 'ᱺ')
    Strng = Strng.replace('ᱻᱸ', 'ᱸᱻ')

    return Strng

def _FixSantaliDecode(Strng):
    Strng = Strng.replace('ᱺ', 'ᱹᱸ')
    Strng = Strng.replace('ᱽ','’')
    Strng = Strng.replace('ᱸᱻ', 'ᱻᱸ')

    return Strng

def FixSantali(Strng, reverse=False):
    return _FixSantaliDecode(Strng) if reverse else _FixSantaliEncode(Strng)

def _FixSoraSompengEncode(Strng):
    ListC = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, 'SoraSompeng')) + ')'

    Strng = re.sub(ListC + '(ə)', r'\1', Strng)
    Strng = Strng.replace('ə', '\U000110E6\U000110E8')

    return Strng

def _FixSoraSompengDecode(Strng):
    ListC = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, 'SoraSompeng')) + ')'

    ListV = "(" + "|".join(GM.CrunchSymbols(GM.Vowels, 'SoraSompeng')) + ')'
    Strng = re.sub(ListC + '(?!' + ListV + ')', r'\1' + 'ə', Strng)

    Strng = Strng.replace('𑃔ə𑃨', '𑃔𑃨ə')

    Strng = Strng.replace('𑃦𑃨', 'ə')
    Strng = Strng.replace('ə𑃨', '𑃨')

    return Strng

def FixSoraSompeng(Strng, reverse=False):
    return _FixSoraSompengDecode(Strng) if reverse else _FixSoraSompengEncode(Strng)


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

def FixRomanReadable(Strng, reverse = False):
    return _FixRomanReadableColloquial(Strng, reverse, colloquial=False)

def FixRomanColloquial(Strng, reverse = False):
    return _FixRomanReadableColloquial(Strng, reverse, colloquial=True)


def _FixWarangCitiEncode(Strng):
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
    return _FixWarangCitiDecode(Strng) if reverse else _FixWarangCitiEncode(Strng)

def _FixLimbuLoCEncode(Strng):
    Strng = FixLimbu(Strng, False)

    return Strng

def _FixLimbuLoCDecode(Strng):
    Strng = FixLimbu(Strng, True)
    Strng = Strng.replace('ʔ', '᤹')
    Strng = Strng.replace('꞉', '’')

    return Strng

def FixLimbuLoC(Strng, reverse=False):
    return _FixLimbuLoCDecode(Strng) if reverse else _FixLimbuLoCEncode(Strng)

#Subojined & Final
def _FixLimbuEncode(Strng):
    vir = Limbu.ViramaMap[0]

    SCons = [vir+x for x in [Limbu.ConsonantMap[x] for x in [25,26,28]]]  # /ya/, /ra/, /va/
    SubCons = ['\u1929','\u192A','\u192B']

    for x,y in zip(SCons,SubCons):
        # Replace Subjoined Consonants
        Strng = Strng.replace(x,y)

    signAll = '|'.join(GM.CrunchSymbols(GM.Consonants+GM.Vowels+GM.VowelSignsNV, "Limbu"))

    FCons = [x+vir for x in [Limbu.ConsonantMap[x] for x in[0,4,15,19,20,24,26,27]]]
    FinalCons = ['\u1930','\u1931','\u1933','\u1934','\u1935','\u1936','\u1937','\u1938']

    ### ZWNJ with finalcons + ya/ra/la/va (perhaps do this for other scripts)ˍ
    #Strng = Strng.replace("\u1922\u193A", "\u193A\u1922")
    Strng = Strng.replace('꞉', '᤺')

    for x,y in zip(FCons,FinalCons):
        # Replace Final pure consonants
        Strng = re.sub('('+signAll+')'+ '(\u193A?)' + '('+x+')',r'\1\2'+y,Strng)

    Strng = Strng.replace('ʔ','᤹')
    Strng = Strng.replace('!','᥄')
    Strng = Strng.replace('?','᥅')
    ## Add proper support for Limbu e,o to Devanagari
    ## Limbu Question mark and exclamation mark?
    ## LImbu to devanagari conventions
    ## Limbu Danda

    return Strng

def _FixLimbuDecode(Strng):
    vir = Limbu.ViramaMap[0]

    SCons = [vir+x for x in [Limbu.ConsonantMap[x] for x in [25,26,28]]]  # /ya/, /ra/, /va/
    SubCons = ['\u1929','\u192A','\u192B']

    for x,y in zip(SCons,SubCons):
        # Reverse above
        Strng = Strng.replace(y,x)

    signAll = '|'.join(GM.CrunchSymbols(GM.Consonants+GM.Vowels+GM.VowelSignsNV, "Limbu"))

    FCons = [x+vir for x in [Limbu.ConsonantMap[x] for x in[0,4,15,19,20,24,26,27]]]
    FinalCons = ['\u1930','\u1931','\u1933','\u1934','\u1935','\u1936','\u1937','\u1938']

    ### ZWNJ with finalcons + ya/ra/la/va (perhaps do this for other scripts)ˍ
    #Strng = Strng.replace("\u193A\u1922", "\u1922\u193A")
    Strng = re.sub('(' + '|'.join(FinalCons) + ')' + '(?=[ᤕᤖᤘ])', r'\1' + '\u200C', Strng)
    Strng = re.sub('([ᤀᤁᤂᤃᤄᤅᤆᤇᤈᤉᤊᤋᤌᤍᤎᤏᤐᤑᤒᤓᤔᤕᤖᤗᤘᤚᤛᤜᤠᤣᤥᤧᤨᤩᤪᤫ])᤺', r'\1' + '꞉', Strng)
    ## Modifying letter colon ## Fix this only with aH ᤆᤠ᤺ᤣ

    for x,y in zip(FCons,FinalCons):
        # Reverse above
        Strng = Strng.replace(y,x)

    Strng = Strng.replace('᤹', 'ʔ')
    Strng = Strng.replace('᥄', '!')
    Strng = Strng.replace('᥅', '?')
    ## Add proper support for Limbu e,o to Devanagari
    ## Limbu Question mark and exclamation mark?
    ## LImbu to devanagari conventions
    ## Limbu Danda

    return Strng

def FixLimbu(Strng,reverse=False):
    return _FixLimbuDecode(Strng) if reverse else _FixLimbuEncode(Strng)


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

def _FixKaithiEncode(Strng):
    Strng = Strng.replace(' ', '⸱')

    return Strng

def _FixKaithiDecode(Strng):
    Strng = Strng.replace("⸱",' ')
    # Strng = re.sub('', '', Strng)

    return Strng

def FixKaithi(Strng, reverse=False):
    return _FixKaithiDecode(Strng) if reverse else _FixKaithiEncode(Strng)

def FixLao2(Strng, reverse = False):
    return FixLao(Strng, reverse)

def _FixNandinagariEncode(Strng):
    pass

    return Strng

def _FixNandinagariDecode(Strng):
    Strng = PostProcess.NandinagariPrishtamatra(Strng, reverse=True)

    return Strng

def FixNandinagari(Strng, reverse=False):
    return _FixNandinagariDecode(Strng) if reverse else _FixNandinagariEncode(Strng)

#Subjoined, final and la-ligatures
# Fix aH -> a ;
def _FixLepchaEncode(Strng):
    vir = Lepcha.ViramaMap[0]
    la = Lepcha.ConsonantMap[27]

    conLa = [x+vir+la for x in [Lepcha.ConsonantMap[c] for c in [0,2,20,22,24,32]]+[Lepcha.NuktaConsonantMap[6]]]
    conL = ['\u1C01','\u1C04','\u1C0F','\u1C14','\u1C16','\u1C1E','\u1C12']

    for x,y in zip(conLa,conL):
        # Replace k + vira + la -> kla
        Strng = Strng.replace(x,y)

    yr = [vir+x for x in Lepcha.ConsonantMap[25:27]]
    yrSub = ['\u1C24','\u1C25']

    for x,y in zip(yr,yrSub):
        # sbjoined ya and ra
        Strng = Strng.replace(x,y)

    ## Word Final Consonants

    ## Consider adding -u instead of mass replacement [for Cham too] !

    listNF = [Lepcha.ConsonantMap[x] for x in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,17,18,21,22,23,29,30,31]]
    listF = [(Lepcha.ConsonantMap[:33]+Lepcha.AyogavahaMap)[x] for x in [0,0,0,34,0,0,0,0,19,15,15,15,15,19,15,15,15,20,20,20,15,15,15]]

    listNF += Lepcha.ConsonantMap[25:26]+Lepcha.ConsonantMap[28:29]
    listF += Lepcha.VowelMap[2:3] + Lepcha.VowelMap[4:5]

    # Remove Nukta if it appears with Virama
    # ka + Q + Viramam -> ka + virama
    Strng = Strng.replace(Lepcha.NuktaMap[0]+vir,vir)
    Strng = Strng.replace(Lepcha.ConsonantMap[32]+vir,'') # Remove <h> ; sihma -> sima
    consAll = "(" + "|".join(Lepcha.ConsonantMap + Lepcha.VowelMap + Lepcha.VowelSignMap) + ")"
    for x,y in zip(listNF,listF):
        Strng = re.sub(consAll+"(" + x+vir + ")",r'\1'+y+vir,Strng)



    conFinal = [x+vir for x in [Lepcha.ConsonantMap[c] for c in [0,15,19,20,24,26,27]]]
    conF = ['\u1C2D','\u1C33','\u1C30','\u1C31','\u1C2E','\u1C32','\u1C2F',]
    finConsList = ''.join(conF)

    signAll = '|'.join(GM.CrunchSymbols(GM.Consonants+GM.Vowels+GM.VowelSignsNV, "Lepcha"))

    for x,y in zip(conFinal,conF):
        # Replace final consonants
        Strng = re.sub('('+signAll+')'+'('+x+')',r'\1'+y,Strng)

    # Remove Virama - Lepcha doesn't have virama ?

    signVow = '|'.join(GM.CrunchSymbols(GM.VowelSignsNV,"Lepcha"))

    Strng = Strng.replace(vir,'') ## Removing faux Virama
    # Using Sign Kang with Vowel Signs
    # Inherent Consonant uses 1C34
    # kiM -> ki + 1C35 ; kaM -> ka + 1C34
    Strng = re.sub("("+signVow+')'+'('+Lepcha.AyogavahaMap[1]+')',r'\1'+'\u1C35',Strng)
    Strng = Strng.replace("ᰧᰶᰵ", "ᰧᰵᰶ") ## Fiximg IM issues kIM swap the Ran and M to display it better
    # swap rang + final con - unicode ordering to get the correct rendering
    # kIP -> ᰀᰧᰱᰶ
    Strng = re.sub('(ᰶ)' + '([' + finConsList + '])', r'\2\1', Strng)

    return Strng

def _FixLepchaDecode(Strng):
    vir = Lepcha.ViramaMap[0]
    la = Lepcha.ConsonantMap[27]

    conLa = [x+vir+la for x in [Lepcha.ConsonantMap[c] for c in [0,2,20,22,24,32]]+[Lepcha.NuktaConsonantMap[6]]]
    conL = ['\u1C01','\u1C04','\u1C0F','\u1C14','\u1C16','\u1C1E','\u1C12']

    for x,y in zip(conLa,conL):
        # Reverse above
        Strng = Strng.replace(y,x)

    yr = [vir+x for x in Lepcha.ConsonantMap[25:27]]
    yrSub = ['\u1C24','\u1C25']

    for x,y in zip(yr,yrSub):
        # reverse above
        Strng = Strng.replace(y,x)

    ## Word Final Consonants

    ## Consider adding -u instead of mass replacement [for Cham too] !

    listNF = [Lepcha.ConsonantMap[x] for x in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,17,18,21,22,23,29,30,31]]
    listF = [(Lepcha.ConsonantMap[:33]+Lepcha.AyogavahaMap)[x] for x in [0,0,0,34,0,0,0,0,19,15,15,15,15,19,15,15,15,20,20,20,15,15,15]]

    listNF += Lepcha.ConsonantMap[25:26]+Lepcha.ConsonantMap[28:29]
    listF += Lepcha.VowelMap[2:3] + Lepcha.VowelMap[4:5]

    pass # Irreversible

    conFinal = [x+vir for x in [Lepcha.ConsonantMap[c] for c in [0,15,19,20,24,26,27]]]
    conF = ['\u1C2D','\u1C33','\u1C30','\u1C31','\u1C2E','\u1C32','\u1C2F',]
    finConsList = ''.join(conF)

    signAll = '|'.join(GM.CrunchSymbols(GM.Consonants+GM.Vowels+GM.VowelSignsNV, "Lepcha"))

    for x,y in zip(conFinal,conF):
        # KIp ᰀᰧᰱᰶ -> rang, final consonant
        Strng = re.sub('([' + finConsList + '])' + '(ᰶ)', r'\2\1', Strng)
        Strng = Strng.replace(y,x)

    # Remove Virama - Lepcha doesn't have virama ?

    signVow = '|'.join(GM.CrunchSymbols(GM.VowelSignsNV,"Lepcha"))

    Strng = Strng.replace('\u1C35',Lepcha.AyogavahaMap[1])
    Strng = Strng.replace("\u1C34\u1C36","\u1C36\u1C34") ## Fiximg IM issues kIM swap the Ran and M to display it better

    return Strng

def FixLepcha(Strng,reverse=False):
    return _FixLepchaDecode(Strng) if reverse else _FixLepchaEncode(Strng)

# Repha & Subjoined
def _FixSundaneseEncode(Strng):
    vir = Sundanese.ViramaMap[0]

    r = Sundanese.ConsonantMap[26] + vir
    ListC = '|'.join(GM.CrunchSymbols(GM.Consonants + GM.Vowels + GM.VowelSignsNV,'Sundanese'))
    #print(ListC)


    # Sundanese Repha
    Strng = re.sub('(' + ListC + ')' + r, r'\1' + '\u1B81', Strng)

    yrl = [vir+x for x in Sundanese.ConsonantMap[25:28]]
    yrlSub = ['\u1BA1','\u1BA2','\u1BA3']

    for x,y in zip(yrl,yrlSub):
        # Subjoined consonants
        Strng = Strng.replace(x,y)

    return Strng

def _FixSundaneseDecode(Strng):
    vir = Sundanese.ViramaMap[0]

    r = Sundanese.ConsonantMap[26] + vir
    ListC = '|'.join(GM.CrunchSymbols(GM.Consonants + GM.Vowels + GM.VowelSignsNV,'Sundanese'))
    #print(ListC)


    # Reverse above
    Strng = Strng.replace('\u1B81',r)
    Strng = PostProcess.SundaneseHistoricConjuncts(Strng, True)

    yrl = [vir+x for x in Sundanese.ConsonantMap[25:28]]
    yrlSub = ['\u1BA1','\u1BA2','\u1BA3']

    for x,y in zip(yrl,yrlSub):
        # Reverse above
        Strng = Strng.replace(y,x)

    return Strng

def FixSundanese(Strng,reverse=False):
    return _FixSundaneseDecode(Strng) if reverse else _FixSundaneseEncode(Strng)

# Repha & Subjoined
def _FixRejangEncode(Strng):
    vir = Rejang.ViramaMap[0]

    r = Rejang.ConsonantMap[26] + vir
    n = Rejang.ConsonantMap[19] + vir
    ListC = '|'.join(GM.CrunchSymbols(GM.Consonants + GM.Vowels + GM.VowelSignsNV,'Rejang'))

    Strng = re.sub('(' + ListC + ')' + r, r'\1' + '\uA951', Strng)
    Strng = re.sub('(' + ListC + ')' + n, r'\1' + '\uA950', Strng)

    return Strng

def _FixRejangDecode(Strng):
    vir = Rejang.ViramaMap[0]

    r = Rejang.ConsonantMap[26] + vir
    n = Rejang.ConsonantMap[19] + vir
    ListC = '|'.join(GM.CrunchSymbols(GM.Consonants + GM.Vowels + GM.VowelSignsNV,'Rejang'))

    # Reverse above
    Strng = Strng.replace('\uA951',r)
    Strng = Strng.replace('\uA950',n)

    return Strng

def FixRejang(Strng, reverse=False):
    return _FixRejangDecode(Strng) if reverse else _FixRejangEncode(Strng)

# Chakmaa VS A and Subjoined
def _FixChakmaEncode(Strng):
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

    Strng = PostProcess.ChakmaGemination(Strng)

    ###  O/Sub-va lookign similar; check

    return Strng

def _FixChakmaDecode(Strng):
    listC = '('+"|".join(sorted(GM.CrunchSymbols(GM.Consonants,"Chakma")+Chakma.VowelMap[:1],key=len,reverse=True))+')'
    listV = '('+"|".join(sorted(GM.CrunchSymbols(GM.VowelSigns,"Chakma")+Chakma.ViramaMap+['\U00011133'],key=len,reverse=True))+')'

    Strng = Strng.replace("\u02BD","")

    Strng = PostProcess.ChakmaGemination(Strng, reverse = True)

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
    return _FixChakmaDecode(Strng) if reverse else _FixChakmaEncode(Strng)

def _FixIASTEncode(Strng):

    return Strng

def _FixIASTDecode(Strng):
    Strng = Strng.replace("ṁ",IAST.AyogavahaMap[1])
    # ^ Some IAST publications use /ṁ/ instead of /m dot below/

    return Strng

def FixIAST(Strng,reverse=False):
    return _FixIASTDecode(Strng) if reverse else _FixIASTEncode(Strng)

def _FixIPAEncode(Strng):
    colon_tilde = "\u02D0\u0303"
    tilde_colon = "\u0303\u02D0"

    # ɑː̃ -> ɑ̃ː
    Strng = Strng.replace(colon_tilde,tilde_colon)
    # Add Visarga echo - kuH/kUH -> kuhŭ/kuːhŭ
    Strng = re.sub("(.)(\u02D0?)(\u0068)",r'\1\2\3\1'+'\u0306',Strng)
    Strng = Strng.replace('ə̸ə̸', 'ɑ̷ː')

    return Strng

def _FixIPADecode(Strng):
    colon_tilde = "\u02D0\u0303"
    tilde_colon = "\u0303\u02D0"

    Strng = Strng.replace('ɑ̷ː', 'ə̸ə̸')
    # ɑː̃ <- ɑ̃ː
    Strng = Strng.replace(tilde_colon,colon_tilde)
    # Reverse Visarga echo - kuH/kUH <- kuhŭ/kuːhŭ
    Strng = re.sub("(.)(\u02D0?)(\u0068)"+r"\1"+"\u0306",r"\1\2\3",Strng)

    return Strng

def FixIPA(Strng, reverse=False):
    return _FixIPADecode(Strng) if reverse else _FixIPAEncode(Strng)

# Rearrange PhagsPa Letters ; Subjoined Letters ;
def _FixPhagsPaEncode(Strng):
    candraBindu = PhagsPa.AyogavahaMap[0]
    ListC = "|".join(sorted(PhagsPa.ConsonantMap,key=len,reverse=True)) #Do this for all
    ListV = "|".join(sorted(PhagsPa.VowelMap,key=len,reverse=True))
    ListVS = "|".join(sorted(PhagsPa.VowelSignMap,key=len,reverse=True))

    vir  = PhagsPa.ViramaMap[0]
    Virrvy = [vir+x for x in [PhagsPa.ConsonantMap[c] for c in [25,26,28]]]
    Subrvy = ['\uA868','\uA871','\uA867']

    SubrvyE = ['ꡱꡨ'] + Subrvy


    # Removing Indep. Vowel Sign
    #ListV = ListV.replace("\u1E7F","")
    #Strng = Strng.replace("\u1E7F","")

    for x,y in zip(Virrvy,Subrvy):
        Strng = Strng.replace(x,y)

    Strng = re.sub("("+ListV+")"+"("+candraBindu+")",r'\2\1',Strng)

    # Move Chandrabindu - bhrUM
    Strng = re.sub("("+ListC+")"+"(("+"|".join(SubrvyE)+")?)"+"(("+ListVS+")?)"+"("+candraBindu+")",r'\6\1\2\4',Strng)
    # Move Sigh Candrabindu

    # Move Vowel Sign AA for subjoining vowels ## Not moving
   #  Strng = re.sub("(["+"".join(Subrvy[1])+"])"+"("+PhagsPa.VowelSignMap[0]+")",r'\2\1',Strng)


    ## Fix rka - superfixed ra ; rka used only for Specific Tibetan context.
    Strng = Strng.replace(" ", "᠂")
    Strng = Strng.replace("\u02BD","")

    ## separate syllables

    #Strng = re.sub("(?<!ꡖ)" + "(" + "(" + ListV +")" + ")" + "(?!" + ListCVir + ")", r'\1' + ' ', Strng)
    #Strng = re.sub("(" + "(" + ListC +")" + "(" + "|".join(Subrvy) + ")?" + "(" + ListVS + ")" + ")" + "(?!" + ListCVir + ")", r'\1' + ' ', Strng)
    #Strng = Strng.replace("")
    #Strng = re.sub("(" + "(" + ListC +")" + "(" + "|".join(Subrvy) + ")?" + "(?!" + ListCVir + ")" + ")", r'\1' + ' ', Strng)

    ## sakv sakr not changing properly
    Strng = re.sub("(("+candraBindu+")?"+"("+ListC+")"+"(("+"|".join(SubrvyE)+")?)"+"(("+ListVS+")?))" +
        "(("+candraBindu+")?"+"("+ListC+")"+"(("+"|".join(SubrvyE)+")?)"+"(("+ListVS+")?))" + "(?!" + vir + ")", r'\1 \8', Strng)
    Strng = re.sub("(("+candraBindu+")?"+"("+ListC+")"+"(("+"|".join(SubrvyE)+")?)"+"(("+ListVS+")?))" +
        "(("+candraBindu+")?"+"("+ListC+")"+"(("+"|".join(SubrvyE)+")?)"+"(("+ListVS+")?))" + "(?!" + vir + ")", r'\1 \8', Strng)

    Strng = re.sub("(("+candraBindu+")?"+"("+ListV+"))" +
        "(("+candraBindu+")?"+"("+ListC+")"+"(("+"|".join(SubrvyE)+")?)"+"(("+ListVS+")?))" + "(?!" + vir + ")", r'\1 \4', Strng)
    Strng = re.sub("(("+candraBindu+")?"+"("+ListV+"))" +
        "(("+candraBindu+")?"+"("+ListC+")"+"(("+"|".join(SubrvyE)+")?)"+"(("+ListVS+")?))" + "(?!" + vir + ")", r'\1 \4', Strng)

    Strng = re.sub("(("+candraBindu+")?"+"("+ListC+")"+"(("+"|".join(SubrvyE)+")?)"+"(("+ListVS+")?))" +
        "(("+candraBindu+")?"+"("+ListV+"))" + "(?!" + vir + ")", r'\1 \8', Strng)
    Strng = re.sub("(("+candraBindu+")?"+"("+ListC+")"+"(("+"|".join(SubrvyE)+")?)"+"(("+ListVS+")?))" +
        "(("+candraBindu+")?"+"("+ListV+"))" + "(?!" + vir + ")", r'\1 \8', Strng)

    Strng = re.sub("(("+candraBindu+")?"+"("+ListV+"))" + "(?!" + vir + ")" +
        "(("+candraBindu+")?"+"("+ListV+"))" + "(?!" + vir + ")", r'\1 \4', Strng)
    Strng = re.sub("(("+candraBindu+")?"+"("+ListV+"))" + "(?!" + vir + ")" +
        "(("+candraBindu+")?"+"("+ListV+"))" + "(?!" + vir + ")", r'\1 \4', Strng)

    Strng = Strng.replace("\n","\n")

    #Strng = "(" + "(" + ListC +")" + "(" + "|".join(Subrvy) + ")?" + "(" + ListVS + ")" + ")" + "(?!" + ListCVir + ")"

    Strng = '\u12BA᠂' + Strng

    ListCE = ListC + "|" + "|".join(SubrvyE)

    ## Probably add more punctuations
    Strng = re.sub('(?:(?<!\n)(?<!᠂)(?<![,\.\"\?\&\(\)]))' + "(?<!" + vir + ")" + '(' + ListC + ')' + vir + "((" + candraBindu +")?" + "("+ListC+"))",r"\1 \2", Strng) #\u02BF Virama
    Strng = re.sub('(?<!᠂)' + '(' + ListC + ')' + vir + "((" + candraBindu +")?" + "("+ListV+"))",r" \1", Strng) #\u02BF Virama

    Strng = Strng.replace(vir,"") #\u02BF Virama
    Strng = Strng.replace("\u1E7F","")
    Strng = Strng.replace("\u1E7E","")
    Strng = Strng.replace("\u12BA᠂","")

    Strng = Strng.replace("᠂", " ᠂ ")


    #print Strng



    return Strng

def _FixPhagsPaDecode(Strng):
    candraBindu = PhagsPa.AyogavahaMap[0]
    ListC = "|".join(sorted(PhagsPa.ConsonantMap,key=len,reverse=True)) #Do this for all
    ListV = "|".join(sorted(PhagsPa.VowelMap,key=len,reverse=True))
    ListVS = "|".join(sorted(PhagsPa.VowelSignMap,key=len,reverse=True))

    vir  = PhagsPa.ViramaMap[0]
    Virrvy = [vir+x for x in [PhagsPa.ConsonantMap[c] for c in [25,26,28]]]
    Subrvy = ['\uA868','\uA871','\uA867']

    SubrvyE = ['ꡱꡨ'] + Subrvy


    ListV = ListV.replace("\u1E7F","")

    Strng = Strng.replace('ꡖꡘꡟ','ꡱꡖꡟ')

    Aspirate = [('\uA842\uA85C','\u1E7E\uA842\u1E7E\uA85C\u1E7E'), ('\uA852\uA85C','\u1E7E\uA852\u1E7E\uA85C\u1E7E'), ('\uA86B\uA85C','\u1E7E\uA86B\u1E7E\uA85C\u1E7E'),
        ('\uA84A\uA85C','\u1E7E\uA84A\u1E7E\uA85C\u1E7E'),('\uA84E\uA85C','\u1E7E\uA84E\u1E7E\uA85C\u1E7E')]

    for x,y in Aspirate:
        Strng = Strng.replace(x,y)

    Strng = re.sub("("+PhagsPa.VowelSignMap[0]+")"+"(["+"".join(Subrvy[1])+"])",r'\2\1',Strng)
    Strng = re.sub("("+candraBindu+')'+"("+ListC+')'+"(("+"|".join(SubrvyE)+")?)"+"(("+ListVS+')?)',r'\2\3\5\1',Strng)
    Strng = re.sub("("+candraBindu+')'+'('+ListV+')',r'\2\1',Strng)

    for x,y in zip(Virrvy,Subrvy):
        Strng = Strng.replace(y,x)

    # Fixing  + Indepdendent vowels.
    Strng = re.sub("("+ListV+")","\u1E7F"r"\1",Strng)
    Strng = re.sub("("+ListC+"|ꡖ)"+"("+"\u1E7F"+")",r'\1',Strng)

    ## Fix rka - superfixed ra ; rka used only for Specific Tibetan context.
    Strng = Strng.replace("ꡆ","ꡒ")

    for x,y in zip(Virrvy,Subrvy):
        Strng = Strng.replace(x,y)

    #print(Strng)

    ## Fix splavya
    Strng = re.sub("((" + ListC + ")" + "(("+"|".join(SubrvyE)+")?)" + "(?!" + ListVS + "))"
        + "((("+ListC+")"+"(("+"|".join(SubrvyE)+")?)"+"(("+ListVS+"))" + "("+candraBindu+")?))"  , r"\1" + vir + r"\6", Strng)


    Strng = re.sub("((("+ListC+")"+"(("+"|".join(SubrvyE)+")?)"+"(("+ListVS+")?)" + "("+candraBindu+")?)"
        + "((" + ListC + ")" + "(("+"|".join(SubrvyE)+")?)" + "(?!" + ListVS + ")))" , r"\1" + vir, Strng)

    Strng = re.sub("((("+ListV+")" + "("+candraBindu+")?)"
        + "((" + ListC + ")" + "(("+"|".join(SubrvyE)+")?)" + "(?!" + ListVS + ")))" , r"\1" + vir, Strng)

    for x,y in zip(Virrvy,Subrvy):
        Strng = Strng.replace(y,x)

    Strng = Strng.replace(" ", "")
    Strng = Strng.replace("᠂"," ")
    Strng = Strng.replace("᠃"," ")

    Strng = Strng.replace(vir + vir, vir)

    # ꡳꡊꡞꡚ ꡩꡖ ꡗ ---> diMSTAya
    # Fix Aspirated add the extra character
    # Fix saphA -> sphA ; sata -> sat ; suda -> sud
    # Add options to retain space
    #Strng = Strng.replace("(" + ListC + ")")


    return Strng

def FixPhagsPa(Strng,reverse=False):
    return _FixPhagsPaDecode(Strng) if reverse else _FixPhagsPaEncode(Strng)

# Meetei Mayek Final
# Think of a-k-ka vers a-ka+vir-ka, also ag to ak. (Virama extends to second letter... ag could be replaced by ak..
# since a+ga+vir woould orthographically wrong (it has no following consonant to extend to), considered replacing a+g+virama with a+k

def _FixLatnEncode(Strng, Source):
    vir = ''

    #print('here at last ')

    Strng = re.sub('([aiuāīū' + vir + '])(꞉)', r'\2\1', Strng)
    Strng = re.sub('(꞉)(\u033D)', r'\2\1', Strng)

    Strng = Strng.replace('aʰ', 'ʰ') ## Remove extraneous h
    #Strng = PostProcess.LatnInitialVowels(Strng)

    return Strng

def _FixLatnDecode(Strng, Source):
    vir = ''

    #print('here at last ')

    #print(Strng)
    Strng = re.sub('([aiuāīū' + vir + '])(꞉)', r'\2\1', Strng)
    Strng = re.sub('(\u033D)(꞉)', r'\2\1', Strng)
    #print(Strng)

    return Strng

def FixLatn(Strng, Source, reverse=False):
    return _FixLatnDecode(Strng, Source) if reverse else _FixLatnEncode(Strng, Source)

def _FixArabEncode(Strng, Source):
    Strng = PersoArabicPuntuation(Strng, False)
    pass
    #Strng = Strng.replace('â', 'ʾ')

    return Strng

def _FixArabDecode(Strng, Source):
    Strng = PersoArabicPuntuation(Strng, True)
    Strng = Strng.replace('آ', 'آ').replace('ـ', '')
    ## reverse shadda kasra
    Strng = Strng.replace('\u064E\u0651', '\u0651\u064E')

    return Strng

def FixArab(Strng, Source, reverse=False):
    return _FixArabDecode(Strng, Source) if reverse else _FixArabEncode(Strng, Source)

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

def FixArab_Fa(Strng, Source, reverse=False):
    Strng = FixArab(Strng, Source, reverse)

    return Strng

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

def _FixUgarEncode(Strng, Source):
    Strng = Strng.replace("𐎒²","𐎝")
    Strng = Strng.replace(' ', '𐎟')

    return Strng

def _FixUgarDecode(Strng, Source):
    Strng = Strng.replace('𐎟', '')

    return Strng

def FixUgar(Strng, Source, reverse=False):
    return _FixUgarDecode(Strng, Source) if reverse else _FixUgarEncode(Strng, Source)

def _FixSogdEncode(Strng, Source):
    Strng = Strng.replace("𐼹²","𐽄")

    return Strng

def _FixSogdDecode(Strng, Source):
    pass

    return Strng

def FixSogd(Strng, Source, reverse=False):
    return _FixSogdDecode(Strng, Source) if reverse else _FixSogdEncode(Strng, Source)

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

def _FixTeluguEncode(Strng):
    Strng = PostProcess.RetainDandasIndic(Strng, 'Telugu', True)
    Strng = PostProcess.RetainIndicNumerals(Strng, 'Telugu', True)

    return Strng

def _FixTeluguDecode(Strng):
    Strng = PostProcess.RetainIndicNumerals(Strng, 'Telugu')
    Strng = PostProcess.RetainDandasIndic(Strng, 'Telugu')
    Strng = Strng.replace('ఁ', 'ఀ')

    return Strng

def FixTelugu(Strng, reverse=False):
    return _FixTeluguDecode(Strng) if reverse else _FixTeluguEncode(Strng)

def _FixMeeteiMayekEncode(Strng):
    vir = MeeteiMayek.ViramaMap[0]
    listC = [x+vir for x in [MeeteiMayek.ConsonantMap[x] for x in [0,27,24,20,19,15,4,25]]]
    finalC = ['\uABDB','\uABDC','\uABDD','\uABDE','\uABDF','\uABE0','\uABE1','\uABE2']

    for x,y in zip(listC,finalC):
        Strng = re.sub(x,y,Strng)

    return Strng

def _FixMeeteiMayekDecode(Strng):
    vir = MeeteiMayek.ViramaMap[0]
    listC = [x+vir for x in [MeeteiMayek.ConsonantMap[x] for x in [0,27,24,20,19,15,4,25]]]
    finalC = ['\uABDB','\uABDC','\uABDD','\uABDE','\uABDF','\uABE0','\uABE1','\uABE2']

    for x,y in zip(listC,finalC):
        Strng = Strng.replace(y, x)

    return Strng

def FixMeeteiMayek(Strng,reverse=False):
    return _FixMeeteiMayekDecode(Strng) if reverse else _FixMeeteiMayekEncode(Strng)

## Reverse not working
## For other batak writings as well

## Consider replacement of Anusvara by Nasal for East Asian Sripts which don't ahve a Sanskrit writing Tradition

def _FixBatakSimaEncode(Strng):
    Strng = Strng.replace('ᯙᯮ', 'ᯙᯯ')

    return Strng

def _FixBatakSimaDecode(Strng):
    Strng = Strng.replace('ᯙᯯ', 'ᯙᯮ')

    return Strng

def FixBatakSima(Strng, reverse=False):
    return _FixBatakSimaDecode(Strng) if reverse else _FixBatakSimaEncode(Strng)

# Cham Final & Subjoined
def _FixChamEncode(Strng):
    Strng = Strng.replace("\u02BD","")

    ## Check Differences between Vietnamese Cham & Cambodian Cham

    ListCAll = '('+'|'.join(GM.CrunchSymbols(GM.Consonants,'Cham')) + ')'
    ListVow = '('+'|'.join(GM.CrunchSymbols(GM.Vowels,'Cham')) + ')'
    ListVowS = '('+'|'.join(GM.CrunchSymbols(GM.VowelSignsNV,'Cham')) + ')'

    ## http://www.youtube.com/watch?v=z2_8GMqbO6M - Prenasalized Consonants
    vir = Cham.ViramaMap[0]
    nja = Cham.ConsonantMap[9] + vir + Cham.ConsonantMap[7]

#    if not reverse:
#        Strng = Strng.replace(nja,u'\uAA12')
#    else:
#        Strng = Strng.replace(u'\uAA12',nja)

    ## Replace Mue with ma, nue with na ???  - Should it be done ???

    ## Subjoined Consonants

    listC = [vir+x for x in Cham.ConsonantMap[25:29]]
    SubC = ['\uAA33','\uAA34','\uAA35','\uAA36'] # Subjoined - /ya/, /ra/, /la/, /va/
    for x,y in zip(listC,SubC):
        # Subjoined consonants
        Strng = Strng.replace(x,y)

    # Replace Consonants without Final forms to Consonts with Final Forms
    # vagh -> vag, prajJa -> pracJA etc

    listNF = [Cham.ConsonantMap[x] for x in [1,3,6,7,8,9,16,17,18,21,22,23,31,29]]  # Non Final
    listF = [Cham.ConsonantMap[x] for x in [0,2,5,5,5,19,15,15,15,20,20,20,30,30]]  # Final

    for x,y in zip(listNF,listF):
        Strng = Strng.replace(x+vir,y+vir)

    ## Fix Hma Hla - Word Initial
    ## hma  ꩍꨠ -> Becomes ःम

    ## Consonnant h

    listC = [x+vir for x in [Cham.ConsonantMap[x] for x in [0,2,4,5,15,19,20,25,26,27,30,24]]]
    finalC = ['\uAA40','\uAA41','\uAA42','\uAA44','\uAA45','\uAA46','\uAA47','\uAA48','\uAA49','\uAA4A','\uAA4B','\uAA4C']

    for x,y in zip(listC,finalC):
        # final consonants
        Strng = Strng.replace(x,y)
        Strng = re.sub('(' + ListCAll + '|' +  ListVow + '|' +  ListVowS + ')' + 'ꨨ' + vir, r'\1'+'ꩍ', Strng)


    # Remove faux Virama:
    va = Cham.ConsonantMap[28]
    Strng = Strng.replace(va+vir,va)
    #Strng = Strng.replace('ʾ', '')

    return Strng

def _FixChamDecode(Strng):
    Strng = Strng.replace("\u02BD","")

    ## Check Differences between Vietnamese Cham & Cambodian Cham

    ListCAll = '('+'|'.join(GM.CrunchSymbols(GM.Consonants,'Cham')) + ')'
    ListVow = '('+'|'.join(GM.CrunchSymbols(GM.Vowels,'Cham')) + ')'
    ListVowS = '('+'|'.join(GM.CrunchSymbols(GM.VowelSignsNV,'Cham')) + ')'

    ## http://www.youtube.com/watch?v=z2_8GMqbO6M - Prenasalized Consonants
    vir = Cham.ViramaMap[0]
    nja = Cham.ConsonantMap[9] + vir + Cham.ConsonantMap[7]

#    if not reverse:
#        Strng = Strng.replace(nja,u'\uAA12')
#    else:
#        Strng = Strng.replace(u'\uAA12',nja)

    ## Replace Mue with ma, nue with na ???  - Should it be done ???

    ## Subjoined Consonants

    listC = [vir+x for x in Cham.ConsonantMap[25:29]]
    SubC = ['\uAA33','\uAA34','\uAA35','\uAA36'] # Subjoined - /ya/, /ra/, /la/, /va/
    for x,y in zip(listC,SubC):
        # Reverse above
        Strng = Strng.replace(y,x)

    # Replace Consonants without Final forms to Consonts with Final Forms
    # vagh -> vag, prajJa -> pracJA etc

    listNF = [Cham.ConsonantMap[x] for x in [1,3,6,7,8,9,16,17,18,21,22,23,31,29]]  # Non Final
    listF = [Cham.ConsonantMap[x] for x in [0,2,5,5,5,19,15,15,15,20,20,20,30,30]]  # Final

    for x,y in zip(listNF,listF):
        pass # Irreversible

    ## Fix Hma Hla - Word Initial
    ## hma  ꩍꨠ -> Becomes ःम

    ## Consonnant h

    listC = [x+vir for x in [Cham.ConsonantMap[x] for x in [0,2,4,5,15,19,20,25,26,27,30,24]]]
    finalC = ['\uAA40','\uAA41','\uAA42','\uAA44','\uAA45','\uAA46','\uAA47','\uAA48','\uAA49','\uAA4A','\uAA4B','\uAA4C']

    for x,y in zip(listC,finalC):
        # final consonants
        Strng = Strng.replace('ꩍ','ꨨ' + vir)
        if y not in Cham.AyogavahaMap:
            Strng = Strng.replace(y,x)

    # Remove faux Virama:
    va = Cham.ConsonantMap[28]
    pass # Irreversible

    return Strng

def FixCham(Strng,reverse=False):
    return _FixChamDecode(Strng) if reverse else _FixChamEncode(Strng)

# Subjoined Consonants in Tai Tham
# Mai Kang Lai - /ng/
def _FixTaiThamEncode(Strng):
    vir = TaiTham.ViramaMap[0]
    Cons = [vir+x for x in [TaiTham.ConsonantMap[x] for x in [26,27]]] # /ra/ and /la/
    Sub =['\u1A55','\u1A56'] # Subjoined Forms of /ra/ and /la/

    # Ra/La + vira -> Subjoined
    for x,y in zip(Cons,Sub):
        Strng = Strng.replace(x,y)

    # Strng = Strng.replace("\u1A63\u1A74","\u1A74\u1A63") # kAM -> kMA (Like Thai ำ )
    # Check above in Pali texts
    #Strng = Strng.replace('ᩰ', 'ᩮᩣ')
    pass

    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'TaiTham'))
    ng = TaiTham.ConsonantMap[4]+vir

    # Mai Kang Lai
    Strng = re.sub('('+ng+')'+'('+ListC+')','\u1A58'+r'\2',Strng)
    # Subjoining Virama
    Strng = re.sub(vir+'('+ListC+')','\u1A60'+r'\1',Strng)
    # Great Sa
    Strng = Strng.replace('ᩈ᩠ᩈ','ᩔ')

    # Fix Tall A
    TallACons = '|'.join(['ᩅ', 'ᨴ', 'ᨵ', 'ᨣ']) ## va da dha ga

    Strng = PostProcess.FixTallA(Strng, TallACons)

    Strng = Strng.replace('\u1A55\u1A60\u1A3F', '\u1A60\u1A3F\u1A55') # Fix krya

    Strng = Strng.replace('\u1A60\u1A47', vir + '\u1A47') ## Fonts don't support SSA conjunct



    return Strng

def _FixTaiThamDecode(Strng):
    vir = TaiTham.ViramaMap[0]
    Cons = [vir+x for x in [TaiTham.ConsonantMap[x] for x in [26,27]]] # /ra/ and /la/
    Sub =['\u1A55','\u1A56'] # Subjoined Forms of /ra/ and /la/

    # Ra/La + vira -> Subjoined
    for x,y in zip(Cons,Sub):
        Strng = Strng.replace(y,x)

    #Strng = Strng.replace("\u1A74\u1A63","\u1A63\u1A74") # kAM <- kMA
    pass

    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'TaiTham'))
    ng = TaiTham.ConsonantMap[4]+vir

    AA = 'ᩣ'
    Strng = Strng.replace('ᩔ', 'ᩈ᩠ᩈ') ## Reverse great sa
    Strng = re.sub('('+ListC+')'+'\u1A58',r'\1' + ng,Strng) # Reverse: Kai mang Lai -> ng + virama
    Strng = Strng.replace('\u1A60',vir) # Regular Virama for Transliteration
    Strng = Strng.replace("ᩤ", AA) # Reverse Tall A

    Strng = Strng.replace('\u1A60\u1A3F\u1A55', '\u1A55\u1A60\u1A3F') # Rever krya


    return Strng

def FixTaiTham(Strng,reverse=False):
    return _FixTaiThamDecode(Strng) if reverse else _FixTaiThamEncode(Strng)

def FixLaoTham(Strng, reverse=False):
    Strng = FixTaiTham(Strng, reverse)

    return Strng

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

def FixThamLoC(Strng, reverse=False):
    return _FixTaiThamFamily(Strng, reverse, ['ᩅ', 'ᨴ', 'ᨵ', 'ᨣ', 'ᨷ'], marker_cleanup=True, ra_haam_swap=False)

def FixLueTham(Strng, reverse=False):
    return _FixTaiThamFamily(Strng, reverse, ['ᩅ', 'ᨴ', 'ᨵ', 'ᨣ'], marker_cleanup=False, ra_haam_swap=False)

def FixKhuenTham(Strng, reverse=False):
    return _FixTaiThamFamily(Strng, reverse, ['ᩅ', 'ᨴ', 'ᨵ', 'ᨣ'], marker_cleanup=False, ra_haam_swap=True)
def LaoTranscribe(Strng,reverse=False):
    from . import PostProcess as pp

    shortA, conjA = '\u0EB0', '\u0EB1'

    if not reverse:
        Strng = pp.ThaiLaoTranscription(Strng,"Lao",shortA,conjA)
    else:
        Strng = pp.ThaiLaoTranscription(Strng,"Lao",shortA, conjA,reverse=True)

    return Strng

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
def _FixBengaliEncode(Strng):
    Virama = ''.join(GM.CrunchSymbols(['ViramaMap'], 'Bengali'))
    ba = 'ব'

    Strng = re.sub('(?<![রবম])' + Virama + ba,  Virama + '\u200C' + ba, Strng)
    #print(Strng)
    ## Fix স্ভ়ারা  -> স্বারা ; subjoined ba is by default pronounced as /va/ in Bengali
    Strng = re.sub('(?<![রবমভ়])' + '(\u09CD\u09AD\u09BC)', '\u09CD\u09AC', Strng)
    #print(Strng)

    Strng = PostProcess.KhandaTa(Strng, 'Bengali', False)
    #print(Strng)

    return Strng

def _FixBengaliDecode(Strng):
    Virama = ''.join(GM.CrunchSymbols(['ViramaMap'], 'Bengali'))
    ba = 'ব'

    pass

    Strng = PostProcess.KhandaTa(Strng, 'Bengali', True)
    #print(Strng)

    return Strng

def FixBengali(Strng, reverse=False):
    return _FixBengaliDecode(Strng) if reverse else _FixBengaliEncode(Strng)

def _FixAssameseEncode(Strng):
    Ra = "\u09B0"
    AssRa = "\u09F0"

    Strng = PostProcess.KhandaTa(Strng, 'Assamese', False)

    Strng = Strng.replace(Ra,AssRa)

    return Strng

def _FixAssameseDecode(Strng):
    Ra = "\u09B0"
    AssRa = "\u09F0"

    Strng = PostProcess.KhandaTa(Strng, 'Assamese', True)

    Strng = Strng.replace(AssRa,Ra)

    return Strng

def FixAssamese(Strng,reverse=False):
    return _FixAssameseDecode(Strng) if reverse else _FixAssameseEncode(Strng)

def _FixSharadaEncode(Strng):
    Strng = PostProcess.KhandaTa(Strng, 'Assamese', False)

    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'Sharada'))
    Nukta = '|'.join(GM.CrunchSymbols(GM.CombiningSigns,'Sharada')[-1])
    Virama = ''.join(GM.CrunchSymbols(['ViramaMap'], 'Sharada'))

    Strng = Strng.replace( Nukta + Virama, Nukta + Virama + '\u200C')
    Strng = re.sub('(' + Virama + ')' + '(' + ListC + ')' + '(' + Nukta + ')', r'\1' + '\u200C' + r'\2\3', Strng)

    '''Strng = Strng.replace('𑆇ʼ','\U00011183\U000111CB\U000111B6').replace('𑆈ʼ','\U00011183\U000111CB\U000111B7')\
        .replace('𑆶ʼ','\U000111CB\U000111B6').replace('𑆷ʼ','\U000111CB\U000111B7')

    Strng = Strng.replace('\U00011184ʼ', '𑆃𑇋𑆳')
    Strng = re.sub('(?<!\U000111BE)\U000111B3ʼ', '\U000111CB\U000111B3', Strng)

    Strng = Strng.replace('𑆃ʼ', '𑆃𑇋', )
    Strng = re.sub('(' + ListC + ')'+ 'ʼ', r'\1' + '\U000111CB', Strng)'''






    return Strng

def _FixSharadaDecode(Strng):
    Strng = PostProcess.KhandaTa(Strng, 'Assamese', True)

    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'Sharada'))
    Nukta = '|'.join(GM.CrunchSymbols(GM.CombiningSigns,'Sharada')[-1])
    Virama = ''.join(GM.CrunchSymbols(['ViramaMap'], 'Sharada'))

    pass
    # u^ u^^ to vriaama
    # Fix Devanagari as well u^ u^^ to devanagri vowels

    # half-u and half-long-u
    #Strng = Strng.replace('\U00011183\U000111CB\U000111B6', '𑆇ʼ').replace('\U00011183\U000111CB\U000111B7', '𑆈ʼ').\
    #    replace('\U000111CB\U000111B6', '𑆶ʼ').replace('\U000111CB\U000111B7', '𑆷ʼ')

    #Strng = Strng.replace('𑆃𑇋𑆳', '\U00011184ʼ')
    #Strng = re.sub('(?<!\U000111BE)\U000111CB\U000111B3', '\U000111B3ʼ', Strng)

    #Strng = Strng.replace('𑆃𑇋', '𑆃ʼ')
    #Strng = re.sub('(' + ListC + ')'+ '\U000111CB', r'\1' +  'ʼ', Strng)

    return Strng

def FixSharada(Strng,reverse=False):
    return _FixSharadaDecode(Strng) if reverse else _FixSharadaEncode(Strng)

def _FixKannadaEncode(Strng):
    Strng = PostProcess.RetainDandasIndic(Strng, 'Kannada', True)
    #Strng = PostProcess.RetainIndicNumerals(Strng, 'Kannada', True)

    Strng = re.sub('(\u0CCD)([^\u0CAB\u0C9C])(\u0CBC)', r'\1' + '\u200C' + r'\2\3', Strng)

    return Strng

def _FixKannadaDecode(Strng):
    Strng = PostProcess.RetainDandasIndic(Strng, 'Kannada')

    return Strng

def FixKannada(Strng, reverse=False):
    return _FixKannadaDecode(Strng) if reverse else _FixKannadaEncode(Strng)

def _FixGranthaEncode(Strng):
    Strng = Strng.replace('॑', '᳴')
    Strng = Strng.replace('᳚', '॑')
    Strng = Strng.replace('ꣳ', '𑍞')
    Strng = Strng.replace('ꣴ', '𑍟')
    Strng = Strng.replace('𑌼𑍍', '𑌼𑍍\u200C')

    return Strng

def _FixGranthaDecode(Strng):
    Strng = Strng.replace('𑌼𑍍\u200C', '𑌼𑍍')
    Strng = Strng.replace('॑', '᳚')
    Strng = Strng.replace('᳴', '॑')
    Strng = Strng.replace('𑍞', 'ꣳ')
    Strng = Strng.replace('𑍟', 'ꣴ')

    return Strng

def FixGrantha(Strng, reverse=False):
    return _FixGranthaDecode(Strng) if reverse else _FixGranthaEncode(Strng)

def _FixMahajaniEncode(Strng):
    Strng = Strng.replace('𑅰𑅳ʾ𑅭ʿ𑅑', '\U00011176')
    Strng = Strng.replace('\u02BE','').replace('\u02BF','')

    return Strng

def _FixMahajaniDecode(Strng):
    Strng = Strng.replace('\U00011176', '𑅰𑅳ʾ𑅭ʿ𑅑')

    return Strng

def FixMahajani(Strng, reverse=False):
    return _FixMahajaniDecode(Strng) if reverse else _FixMahajaniEncode(Strng)

def _FixAhomEncode(Strng):
    ListVS = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSignsNV, 'Ahom')) + ')'
    Anu = '('+ GM.CrunchList('AyogavahaMap', 'Ahom')[1] + ')'

    Strng = Strng.replace('\U0001172B\U0001170D', '\U0001171E')
    Strng = Strng.replace('\U0001172B\U0001170E', '\U0001171D')

    Strng = re.sub(ListVS + Anu, r'\2\1', Strng)
    Strng = re.sub(Anu + '(𑜦)', r'\2\1', Strng)


    return Strng

def _FixAhomDecode(Strng):
    ListVS = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSignsNV, 'Ahom')) + ')'
    Anu = '('+ GM.CrunchList('AyogavahaMap', 'Ahom')[1] + ')'

    Strng = Strng.replace('\U0001171E', '\U0001172B\U0001170D')
    Strng = Strng.replace('\U0001171D', '\U0001172B\U0001170E')

    vir = Ahom.ViramaMap[0]
    anu = Ahom.AyogavahaMap[1]

    #reverse closed syllable e
    Strng = re.sub(anu + '\U00011727' + '(?!\U00011728)', '\U00011726\U00011727\U0001172A', Strng)
    Strng = re.sub('(\U00011726)(.)('+vir+')', '\U00011726\U00011727'+r'\2\3', Strng)

    #rever closed syllable o
    Strng = re.sub('(\U00011728)(.)('+vir+')', '\U00011726\U00011721'+r'\2\3', Strng)

    Strng = Strng.replace(anu + '\U00011728', '\U00011726\U00011721\U0001172A')

    Strng = re.sub(Anu + ListVS, r'\2\1', Strng)

    return Strng

def FixAhom(Strng, reverse=False):
    return _FixAhomDecode(Strng) if reverse else _FixAhomEncode(Strng)

def _FixMultaniEncode(Strng):
    Strng = Strng.replace('\u02BE','').replace('\u02BF','')
    Strng = Strng.replace('ˍ\U0001128C', '\U0001128D').replace('ˍ\U00011282','\U00011293') ## Plosives


    return Strng

def _FixMultaniDecode(Strng):
    Strng = Strng.replace('\U0001128D','ˍ\U0001128C').replace('\U00011293','ˍ\U00011292') ## Plsosives

    return Strng

def FixMultani(Strng, reverse=False):
    return _FixMultaniDecode(Strng) if reverse else _FixMultaniEncode(Strng)


def _FixGujaratiEncode(Strng):
    Strng = PostProcess.RetainDandasIndic(Strng, 'Gujarati', True)
    Strng = Strng.replace('જ઼઼', 'ૹ').replace('શ઼', 'ૹ')

    return Strng

def _FixGujaratiDecode(Strng):
    Strng = PostProcess.RetainDandasIndic(Strng, 'Gujarati')
    Strng = Strng.replace('ૹ', 'જ઼઼').replace('ૹ', 'શ઼')

    return Strng

def FixGujarati(Strng, reverse=False):
    return _FixGujaratiDecode(Strng) if reverse else _FixGujaratiEncode(Strng)

def _FixZanabazarSquareEncode(Strng):
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'ZanabazarSquare'))
    yrlv = ZanabazarSquare.ConsonantMap[25:29]
    yrlv_sub = ['\U00011A3B', '\U00011A3C', '\U00011A3D', '\U00011A3E']

    vir = ZanabazarSquare.ViramaMap[0]

    Strng = re.sub(vir+'('+ListC+')','\U00011A47'+r'\1',Strng)
    # KSSA
    Strng = Strng.replace('𑨋𑩇𑨯','𑨲')

    return Strng

def _FixZanabazarSquareDecode(Strng):
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'ZanabazarSquare'))
    yrlv = ZanabazarSquare.ConsonantMap[25:29]
    yrlv_sub = ['\U00011A3B', '\U00011A3C', '\U00011A3D', '\U00011A3E']

    vir = ZanabazarSquare.ViramaMap[0]

    Strng = Strng.replace('\U00011A41', ' ')

    tsaSeries = ['𑨣', '𑨤', '𑨥']
    caSeries = ['𑨐','𑨑','𑨒']

    for x, y in zip(tsaSeries,caSeries):
        Strng = Strng.replace(y, x)

    # subjoining contextual y/r/l/v
    for x, y in zip(yrlv, yrlv_sub):
        Strng = Strng.replace(y, '\U00011A47' + x)

    # Repha
    Strng = Strng.replace('\U00011A3A', yrlv[1] + '\U00011A47')

    # KSSA
    Strng = Strng.replace('𑨲', '𑨋𑩇𑨯')

    # Alternate ai/au
    Strng = Strng.replace('\U00011A07', '\U00011A04\U00011A0A')
    Strng = Strng.replace('\U00011A08', '\U00011A06\U00011A0A')

    # Mongolian final -> Virama
    Strng = Strng.replace('\U00011A33', vir)

    # Subojin to Normal vir
    Strng = Strng.replace('\U00011A47', vir)

    return Strng

def FixZanabazarSquare(Strng, reverse=False):
    return _FixZanabazarSquareDecode(Strng) if reverse else _FixZanabazarSquareEncode(Strng)

def _FixKhojkiEncode(Strng):
    sindhi = ['\U0001120B', '\U00011211', '\U0001121C', '\U00011222']
    sindhiapprox = ['ˍ\U0001120A', 'ˍ\U00011210', 'ˍ\U00011216', 'ˍ\U00011221']

    for x, y in zip(sindhi, sindhiapprox):
        Strng = Strng.replace(y, x)
    Strng = PostProcess.InsertGeminationSign(Strng, 'Khojki')
    # Move Shadda after consonant
    Strng = re.sub('(\U00011237)(.)', r'\2\1', Strng)
    # Reverse : Shadda + Nukta
    Strng = Strng.replace('𑈷𑈶', '𑈶𑈷')
    #Strng = re.sub('(' + GM.Germination['Khojki'] + ')', r'\2', Strng)
    # WordSeparatror
    Strng = Strng.replace(' ', '\U0001123A')

    return Strng

def _FixKhojkiDecode(Strng):
    sindhi = ['\U0001120B', '\U00011211', '\U0001121C', '\U00011222']
    sindhiapprox = ['ˍ\U0001120A', 'ˍ\U00011210', 'ˍ\U00011216', 'ˍ\U00011221']

    # Reverse Word Separator
    Strng = Strng.replace('\U0001123A', ' ')

    for x, y in zip(sindhi, sindhiapprox):
        Strng = Strng.replace(x, y)
    # Reverse : Nukta + Shadda
    Strng = Strng.replace('𑈶𑈷', '𑈷𑈶')
    # Move Shadda before consonant
    Strng = re.sub('(.)(\U00011237)', r'\2\1', Strng)
    Strng = PostProcess.ReverseGeminationSign(Strng, 'Khojki')

    return Strng

def FixKhojki(Strng, reverse=False):
    return _FixKhojkiDecode(Strng) if reverse else _FixKhojkiEncode(Strng)

def _FixNewaEncode(Strng):
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'Newa'))
    ra = Newa.ConsonantMap[26]
    vir = Newa.ViramaMap[0]
    ## The default behavior of Repha has been proposed to change
    # Strng = re.sub(ra + vir + '(' + ListC + ')', ra + vir + '\u200D' + r'\1', Strng)

    return Strng
def _FixNewaDecode(Strng):
    pass

    return Strng
def FixNewa(Strng, reverse=False):
    return _FixNewaDecode(Strng) if reverse else _FixNewaEncode(Strng)
