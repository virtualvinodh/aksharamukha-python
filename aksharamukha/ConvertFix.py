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
    """Comparator for sorting candidate strings by descending length of their first element."""
    if(len(x[0]) > len(y[0])):
        return -1
    else:
        return 0

def OriyaIPAFixPre(Strng):
    """Rewrites Oriya anusvara/visarga to nasal-consonant/h sequences before generic IPA conversion."""
    Strng = Strng.replace('ଂ', 'ଙ୍')
    Strng = Strng.replace('ଃ', 'ହ୍')

    return Strng

def SinhalaIPAFix(Strng):
    """Realizes schwa as open ʌ (rather than ə) after 1-3 leading consonants in Sinhala IPA output."""
    consonants = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'IPA')) + ')'

    Strng = re.sub('^' + consonants + '(ə)', r'\1ʌ', Strng)
    Strng = re.sub('(\s)' + consonants + '(ə)', r'\1\2ʌ', Strng)

    Strng = re.sub('^' + consonants + consonants +'(ə)', r'\1ʌ', Strng)
    Strng = re.sub('(\s)' + consonants + consonants +'(ə)', r'\1\2ʌ', Strng)

    Strng = re.sub('^' + consonants + consonants + consonants +'(ə)', r'\1ʌ', Strng)
    Strng = re.sub('(\s)' + consonants + consonants + consonants +'(ə)', r'\1\2ʌ', Strng)


    return Strng

def OriyaIPAFix(Strng):
    """Applies Oriya-specific phonetic realizations to IPA output: schwa->ɔ, affricate/retroflex simplification, vowel-length collapsing."""
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
    """Converts Latin-encoded Vedic svara/anunasika escape sequences (\\m+, \\`, etc.) into Indic Vedic accent marks, reordering svara after the ayogavaha."""
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
    """Reverses Indic Vedic accent marks and anunasika ligatures back into their Latin escape-sequence notation."""
    Strng = Strng.replace('᳚', '\\"')
    Strng = Strng.replace('॑', '\\\'')
    Strng = Strng.replace('॒', '\\_')
    Strng = Strng.replace('ꣳ', '\\m+')
    Strng = Strng.replace('ꣴ', '\\m++')

    return Strng

def VedicSvarasOthers(Strng, Target):
    """Renders Vedic svara escape sequences as arrow symbols and anunasika ligatures for scripts without dedicated accent diacritics."""
    Strng = Strng.replace('\\"','↑↑').replace("\\_", '↓').replace("\\\'",'↑')
    anu = GM.CrunchList('AyogavahaMap', Target)[1]
    Strng = Strng.replace('\\m++', 'ꣴ')
    Strng = Strng.replace('\\m+', 'ꣳ')

    Ayogavaha = GM.CrunchList('AyogavahaMap', Target)

    return Strng

def VedicSvarasDiacrtics(Strng, Target):
    """Converts Vedic svara escape sequences into Unicode combining diacritics for diacritic-based Roman targets (IAST/ISO/Titus)."""
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
    """Converts Vedic svara escape sequences into combining diacritics/ligatures for RussianCyrillic output."""
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

def FixRomanOutput(Strng,Target):

    # Input:Devanagari & Output:ISO
    # Input: क् क्अ क का कृ क्ह ब़् ब़ ब़ो भ् भ भा कि कइ कई
    # Output: kʌ× kʌ×a kʌ kʌā kʌr̥ kʌ×hʌ bʌ̄× bʌ̄ bʌ̄ō bhʌ× bhʌ bhʌā kʌi kʌṿi kʌṿī

    """Shapes generic Roman-script output shared across all Latin romanization targets: schwa/virama joiner insertion, nukta reordering, and related spacing fixes."""
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
    """Dispatches Vedic accent-marker normalization to the right target-specific handler (diacritic/IPA/RomanReadable/Cyrillic/plain) based on Target."""
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
    """Top-level post-fix dispatcher for all Roman targets: applies FixVedic then per-target/per-source special cases (Kashmiri vowels, IPA, Santali, Avestan, SoraSompeng, WarangCiti, Wancho, Mro, RomanReadable/Colloquial Tamil/Oriya/Bengali tweaks, IAST/ISO diaeresis)."""
    from . import Options
    Strng = Strng.replace("\u02BD","")

    Strng = FixVedic(Strng, Target)

    #print(Source, Target)

    # For Kashmiri
    if Target in ['IAST', 'ISO', 'ISOPali', 'Titus']:
        Strng = Strng.replace("uʼ", "ü").replace("ūʼ", "ǖ").replace('aʼ', 'ö').replace('āʼ', 'ȫ')

    if Source == 'Sinhala' and Target == 'IPA':
        Strng = SinhalaIPAFix(Strng)

    if Target == "IPA":
        Strng = Options.call_fix('FixIPA', Strng)

    if Target == 'Santali':
        Strng = Options.call_fix('FixSantali', Strng)

    if Target == "Avestan":
        Strng = Options.call_fix('FixAvestan', Strng)

    if Target == "SoraSompeng":
        Strng = Options.call_fix('FixSoraSompeng', Strng)

    if Target == "WarangCiti":
        Strng = Options.call_fix('FixWarangCiti', Strng)

    if Target == "Wancho":
        Strng = Options.call_fix('FixWancho', Strng)

    if Target == "Mro":
        Strng = Options.call_fix('FixMro', Strng)

    if Target == "RomanReadable":
        Strng = Options.call_fix('FixRomanReadable', Strng)
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

        Strng = Options.call_fix('FixRomanColloquial', Strng)


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
        Strng = Options.call_fix('FixHanifiRohingya', Strng)

    if Target == "Mongolian":
        Strng = Options.call_fix('FixMongolian', Strng)

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
    """Dispatches to the target Semitic script's own Fix<Target> function by name, looked up via Options.FIX_FUNCS."""
    from . import Options
    Strng = Strng.replace('\u02DE', '') ## dummy
    Strng = Options.call_fix("Fix"+Target.replace('-','_'), Strng, Source, optional=True)

    return Strng

# Fixing the Indic Ouput for the standard corrections
# Indic Fix are mandatory corrections to the immediate ouput.
def FixIndicOutput(Strng,Source,Target,ctx=None):
    """Top-level post-fix dispatcher for Indic targets: calls Fix<Target>, shifts diacritics past vowel signs, and renders Vedic accent marks as arrows for non-Vedic-native scripts."""
    from . import Options
    vir = GM.CrunchList('ViramaMap', Target)[0]

    Strng = Strng.replace(vir + '_', vir)

    # ctx passed only to functions that declare it (e.g. FixThai/
    # FixLaoPali, for transcription_mode) - everything else keeps its
    # existing (Strng) call unchanged. Options.call_fix already checks
    # this internally (same _accepts_ctx() check GM.resolve() uses).
    Strng = Options.call_fix("Fix"+Target, Strng, optional=True, ctx=ctx)

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


# Correct Ru'', Lu'' -> R, lR
# Tippi/Bindu

# Fix ru', ru'',lu',lu'' in Tamil & Gurmukhi
# रुʼ -> ऋ, रूʼ -> ॠ, लुʼ -> ऌ, लूʼ -> ॡ
def CorrectRuLu(Strng,Target,reverse=False):
    """Converts ra/la + u/U vowel sign + apostrophe sequences into the vocalic r̥/r̥̄/l̥/l̥̄ letters, or reverses that."""
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
    """Reorders a following combining diacritic to sit before the vowel sign it modifies, or reverses that ordering."""
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


# Move Vowel Signs


# Khmer - Subjoining Consonants and Repha


# Burmese - Tall A + Subjoning Consonants

# Add Repha (Bali,Java,Sundanese)
# a + r + ka -> a<repha>ka
# r +ya -> rya (no repha if syllable first)
def AddRepha(Strng,Script,Repha,reverse=False):
    """Contracts a consonant/vowel followed by ra+virama into the Repha glyph, or expands Repha back to ra+virama."""
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


# Balinese Repha

# Javanese - Reppha & Subjoining ra & ya

# Javanese - Reppha & Subjoining ra & ya

# Javanese - Reppha & Subjoining ra & ya


# Urdu - Shadda, Final E
def _FixUrduShahmukhiEncode(Target, Strng):
    """Encodes Urdu/Shahmukhi-specific orthography: hamza insertion between vowels, nun-ghunna marking, short-vowel/virama cleanup."""
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
    """Decodes Urdu/Shahmukhi text back toward the internal representation: normalizes Arabic-borrowed letters to their closest Indic-Perso-Arabic counterparts, chaschmee-ha and retroflex handling."""
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
    """Dispatches to the Urdu/Shahmukhi encode or decode function depending on the reverse flag."""
    return _FixUrduShahmukhiDecode(Target, Strng) if reverse else _FixUrduShahmukhiEncode(Target, Strng)


def PersoArabicPuntuation(Strng, reverse=False):
    # Punctuation
    # print("Trying to reverse thigns")
    """Swaps ASCII punctuation (, ? ; .) for their Perso-Arabic forms (، ؟ ؛ ۔), or reverses that."""
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


# Tibetan Subjoining Consnants

# Thai, Lao follow visual ordering of Vowels signs ; <e> + k => <e>k
# Other Indic scripts follow logical order ; k + <e> => <e>k
# Swapping Vowel Signs for conversion
def ReverseVowelSigns(Strng,Script,reverse=False):
    """Reorders leading vowel signs to/from consonant-first internal order, generically across scripts (with extra consonant sets for Thai/Lao)."""
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


# Re-arrange Vowels Signs /E/, /AI/, /O/ for digraph <dv>, <mh> etc
# e.g dve -> เทฺว instead of ทฺเว

# Syllabization of Persian
# d<a> +i -> d<i> + i
# d<a> + u -> d<u> + u
# Convert numbers into Persinal Numeral System


# FixRomanReadable and FixRomanColloquial share the same nasal-assimilation
# algorithm; Colloquial differs only in dropping the apostrophe marker that
# Readable keeps, and stripping underscores at the end.
def _FixRomanReadableColloquial(Strng, reverse, colloquial):
    """Applies nasal-assimilation spelling rules (anusvara realized as ng/ny/m by context) for the RomanReadable/RomanColloquial romanization schemes."""
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


#Subojined & Final


#Subjoined, final and la-ligatures
# Fix aH -> a ;

# Repha & Subjoined

# Repha & Subjoined

# Chakmaa VS A and Subjoined


# Rearrange PhagsPa Letters ; Subjoined Letters ;

# Meetei Mayek Final
# Think of a-k-ka vers a-ka+vir-ka, also ag to ak. (Virama extends to second letter... ag could be replaced by ak..
# since a+ga+vir woould orthographically wrong (it has no following consonant to extend to), considered replacing a+g+virama with a+k


## Reverse not working
## For other batak writings as well

## Consider replacement of Anusvara by Nasal for East Asian Sripts which don't ahve a Sanskrit writing Tradition


# Cham Final & Subjoined

# Subjoined Consonants in Tai Tham
# Mai Kang Lai - /ng/


# FixThamLoC/FixLueTham/FixKhuenTham share the same "Tall A" regex logic;
# they differ in the TaiTham consonant list used for the Tall A match
# (ThamLoC alone includes one extra consonant), and in one extra step
# each: ThamLoC does a marker cleanup (forward, only when the Khuen-text
# u02BE marker is present) plus a reverse-direction subconsonant fix;
# KhuenTham does an unconditional ra-haam/lue-karan swap in both
# directions; LueTham has neither extra step.
def _FixTaiThamFamily(Strng, reverse, tall_a_cons, marker_cleanup, ra_haam_swap):
    """Shared Tai Tham-family orthography logic (tall-A vowel placement, ra-haam/lue-karan marker handling), parametrized per dialect (ThamLoC/LueTham/etc)."""
    from . import Options
    Strng = Options.call_fix('FixTaiTham', Strng, reverse)

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


# Transcription for Pali Lao
# Assamese and Bengali have the same mapping file duplicated
# Replace Bengali /ra/ with Assamese /ra/


