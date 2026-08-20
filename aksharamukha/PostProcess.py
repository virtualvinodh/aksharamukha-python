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

# ============================================================
# Frontend-facing options - selectable in the real Aksharamukha
# frontend UI today (confirmed against aksharamukha-front's
# ScriptMixin.js, not inferred). A user can pick these directly.
# ============================================================


## Ahom ##

## Arabic ##

## Assamese ##

## Avestan ##

# Khojki's own logic now lives in ScriptProcessing/Khojki.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Khojki import KhojkiQa, KhojkiRetainSpace

# Ahom's own logic now lives in ScriptProcessing/Ahom.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Ahom import removePaliAhom

# Sinhala's own logic now lives in ScriptProcessing/Sinhala.py -
# consolidated there (batch migration).
from .ScriptProcessing.Sinhala import SinhalaPali_post as SinhalaPali, SinhalaConjuncts

# RomanLoC's own logic now lives in ScriptProcessing/RomanLoC.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.RomanLoC import LoCMarc8

def AnusvaraAsN(Strng):
    """Anusvara as n - m' -> n'."""
    Strng = Strng.replace('m\u034F', 'n')
    return Strng

#show Schwa
# Devanagari's own logic now lives in ScriptProcessing/Devanagari.py -
# consolidated there (batch migration).
from .ScriptProcessing.Devanagari import ShowSchwaHindi, devanagariuttara, devanagarinepali, devanagaribalbodh, devanagarijain, DevanagariAnusvara, jainomDevangari, DevanagariACandra, DevanagariPrishtamatra

# Kannada's own logic now lives in ScriptProcessing/Kannada.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Kannada import KannadaSpacingCandrabindu, KannadaNotRepha, KannadaNakaraPollu

# Telugu's own logic now lives in ScriptProcessing/Telugu.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Telugu import TeluguNakaraPollu, TeluguTamilZha, TeluguTamilRra, TeluguReph, TeluguArasunnaChandrabindu

#testcase todo
# Dogra's own logic now lives in ScriptProcessing/Dogra.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Dogra import olddogra, DograShaKha
from .ScriptProcessing.HebrewSBL import removetddash

#todo add to frontend
def inherentAO(Strng):
    """inherent /a/ as /o-circumflex/."""
    Strng = Strng.replace('a', 'ô')

    return Strng

# Bengali's own logic now lives in ScriptProcessing/Bengali.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Bengali import BengaliOldRA, khandatabatova, BengaliRaBa, BengaliIntervocalicDDA

#trigger - UI prompt to show "preserve source" must be enabled for this option
#testcase todo
def BengaliSwitchYaYYa(Strng):
    """ya -> yya-with-nukta & yya-with-nukta -> ya (swaps the plain and nuktaed Bengali ya letters)."""
    Strng = re.sub('(?<!\u09CD)য', '@#$', Strng)
    Strng = re.sub('য়', 'য', Strng)
    Strng = Strng.replace('@#$', 'য়')

    return Strng

#testcase todo
def AlephMaterLectionis(Strng, target='semitic'):
    """Aleph as mater lectionis - k+hamza -> k+a-macron (inserts long a after a consonant followed by hamza)."""
    cons = '(' + '|'.join(GM.SemiticConsonants) + ')'

    # opt 1
    Strng = re.sub(cons + '(ʾ)', r'\1' + 'ā', Strng)

    return Strng

#testcase todo
def syriacRoman(Strng):
    """Syriac convention - v gh-dotless kh f -> b-line g-line k-line p-macron."""
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
from .ScriptProcessing.Arab import arabicRemoveAdditionsPhonetic, ArabAtoAleph

#testcase todo
# Hebrew's own logic now lives in ScriptProcessing/Hebrew.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Hebrew import removeNikkud, HeberewQoph, HebewShortO

#testcase todo
def removeMajliyana(Strng):
    """Remove Majliyana - strips the underline diacritic marking Majliyana (palatalized) Syriac consonants."""
    Strng = Strng.replace('\u0330', '')

    return Strng

#testcase todo
def removeRukkaka(Strng):
    """Remove Rukkaka - strips the soft/spirantization (rukkakha) dot from Syriac letters."""
    Strng = Strng.replace('\u0741', '')

    return Strng

#testcase todo
def removeQussaya(Strng):
    """Remove Qussaya - strips the hard/occlusive (qushshaya) dot from Syriac letters."""
    Strng = Strng.replace('\u0742', '')

    return Strng

#testcase todo
def removeVowelsSyriac(Strng):
    """Remove Vowel Diacritics - strips all Syriac vowel point combining marks."""
    Strng = re.sub('[\u0732\u0735\u073C\u0738\u0739\u073F]', '', Strng)

    Strng = re.sub('[ّܰܶܺܽܳ]', '', Strng)

    return Strng

#testcase todo
def removeDiacriticsArabic(Strng):
    """Remove Harakat - ghandi-with-marks -> ghandi (strips sukun, fatha, kasra, damma diacritics)."""
    diacrtics = ["\u0652", "\u064E", "\u0650", "\u064F"]

    for diacritic in diacrtics:
        Strng = Strng.replace(diacritic, '')

    return Strng

#testcase todo
def removeSukunEnd(Strng):
    """Remove Sukun at end of words - hind-with-final-sukun -> hind (drops word-final sukun mark)."""
    Strng = re.sub('(\u0652)(\W|$)', r'\2', Strng)

    return Strng

#testcase todo
# Arab-Fa's own logic now lives in ScriptProcessing/Arab_Fa.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Arab_Fa import persianPaGaFaJa

#testcase todo
def removeSegmentSpacesBurmese(Strng):
    # segment text into syllables
    """Join syllables - le thai pyo' -> merged Burmese syllable string (removes spaces inserted between segmented syllables)."""
    import regex

    Strng = regex.sub('(\p{L}\p{M}*) (\p{L})', r'\1\2', Strng)
    Strng = regex.sub('(\p{L}\p{M}*) (\p{L})', r'\1\2', Strng)

    return Strng

def UseAlternateo1(Strng):
    """Long-o vowel sequence -> single alternate o vowel sign glyph."""
    Strng = Strng.replace('ᩮᩣ', 'ᩰ')

    return Strng

def UseAlternateo2(Strng):
    """Pali /o/ - alternate o vowel sign glyph -> the two-part long-o vowel sequence."""
    Strng = Strng.replace('ᩰ', 'ᩮᩣ')

    return Strng

#testcase todo
#testcase todo
def estrangelasyriac(Strng):

    """No-op placeholder (reserved for Estrangela Syriac font-variant handling)."""
    return Strng

#testcase todo
def easternsyriac(Strng):

    """No-op placeholder (reserved for Eastern Syriac font-variant handling)."""
    return Strng

#testcase todo
def westernsyriac(Strng):

    """No-op placeholder (reserved for Western Syriac font-variant handling)."""
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
    """Use tilde for nasalization - kaM ka~ kaMka ka~ka -> ka-tilde ka-tilde kanka kaka (converts anusvara/nasal marks to a combining tilde)."""
    Strng = AnusvaratoNasalASTISO(Strng)
    Strng = re.sub('(m̐|ṃ|ṁ)', '\u0303', Strng)

    return Strng

#todo feature
def verticalKana(Strng):

    """Vertical text (no-op placeholder; vertical layout is not yet implemented here)."""
    return Strng

#todo feature
def verticalSiddham(Strng):

    """No-op placeholder (reserved for vertical Siddham text layout)."""
    return Strng

#todo testcase
def vtobJapanese(txt):

    """/v/ -> /b/ - vino -> bino (merges v-row kana into b-row for nativized Japanese output)."""
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
def gainGimel(Strng):
    """Marked ayin (dagesh-like dot) -> Hebrew gimel (renders Semitic ghayin as Hebrew ga)."""
    return Strng.replace('עׄ','ג')

#todo testcase
# Hebr-Ar's own logic now lives in ScriptProcessing/Hebr_Ar.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Hebr_Ar import gainGimel, tavTwodot, tavThreedot
def urduRemoveInherent(Strng):
    """Remove all inherent /a/ - hndvstan -> not hanadavasatana (strips non-word-initial short a vowels for Urdu rendering)."""
    Strng = re.sub('\Ba', '', Strng)

    return Strng
from .ScriptProcessing.Gurmukhi import GurmukhiYakaash

#misnomer
def mDotAboveToBelow(Strng):
    """m-dot-below -> m-dot-above."""
    Strng = Strng.replace('ṃ', 'ṁ')

    return Strng

#todo : ISOPali postoptions empty todo

# ISO's own logic now lives in ScriptProcessing/ISO.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.ISO import noLongEO

# TamilExtended's own logic now lives in ScriptProcessing/TamilExtended.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.TamilExtended import TamilStyleUUCore, TamilStyleUUOther, TamilExtendedNNA, TamilExtendedAnusvara

# Tamil's post-options (and its default-bundle TamilNaToNNa/
# TamilpredictDentaNa) now live in ScriptProcessing/Tamil.py, consolidated
# there with its Fix logic and pre-options too. Re-exported here so
# Options.py's getmembers(PostProcess, isfunction) discovery still finds
# them, and so PostOptions.py's default bundle for Tamil keeps resolving.
from .ScriptProcessing.Tamil import ContextualLLa, FinalNNa, TamilAddFirstVarga, TamilDisableSHA, TamilGranthaVisarga, TamilOmDisable, TamilRemoveApostrophe, TamilRemoveNumbers, TamilSubScript, oldtamilortho

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
    """Converts double and single full-stop dots into Devanagari danda punctuation (.. -> double danda, . -> danda)."""
    Strng = Strng.replace('..', '॥')
    Strng = Strng.replace('.', '।')

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
from .ScriptProcessing.Tibetan import TibetanSyllabize, TibetanSanskritPalatals, tibetandbumed, TibetanNada, TibetanTsheg

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

# IAST's own logic now lives in ScriptProcessing/IAST.py -
# consolidated there (batch migration).
from .ScriptProcessing.IAST import RomanLoCSLaDotLaUnderscore_post as RomanLoCSLaDotLaUnderscore

# DevanagariLoC's own logic now lives in ScriptProcessing/DevanagariLoC.py -
# consolidated there (LoC redesign; renamed from RomanLoCDevanagari.py).
from .ScriptProcessing.DevanagariLoC import HindiMarathiRomanLoCFix_post as HindiMarathiRomanLoCFix

# DivesAkuru's own logic now lives in ScriptProcessing/DivesAkuru.py -
# consolidated there (batch migration).
from .ScriptProcessing.DivesAkuru import DivesAkuruAlternateIndVowels_post as DivesAkuruAlternateIndVowels, DivesAkuruHomoOrganNasal, UseAlternateYA

# Kawi's own logic now lives in ScriptProcessing/Kawi.py -
# consolidated there (batch migration).
from .ScriptProcessing.Kawi import KawiAltAiAU, KawiArchaicJNA, KawiDecomposedVowel, KawiMoveRepha_post as KawiMoveRepha

# Javanese's own logic now lives in ScriptProcessing/Javanese.py -
# consolidated there (batch migration).
from .ScriptProcessing.Javanese import JavaneseArchaicJNA, JavaneseAvowels, JavaneseMoveRepha_post as JavaneseMoveRepha

# JavaneseLoC's own logic now lives in ScriptProcessing/JavaneseLoC.py -
# consolidated there (LoC redesign; renamed from RomanLoCJavanese.py).
from .ScriptProcessing.JavaneseLoC import JavaneseSimplified

# BalineseLoC's own logic now lives in ScriptProcessing/BalineseLoC.py -
# consolidated there (LoC redesign; renamed from RomanLoCBalinese.py).
from .ScriptProcessing.BalineseLoC import BalineseSimplified

# Balinese's own logic now lives in ScriptProcessing/Balinese.py -
# consolidated there (batch migration).
from .ScriptProcessing.Balinese import BalineseArchaicJNA, BalineseAvowels, BalineseMoveRepha_post as BalineseMoveRepha

def MalayalamTTNTA(Strng):
    """Doubled ra (tta) & n+ra (nta) -> t-line doubled & n+t-line."""
    Strng = Strng.replace('ṟṟ', 'ṯṯ')
    Strng = Strng.replace('nṟ', 'nṯ')
    return Strng

def AnusvaratoNasalASTISO(Strng):
    #Strng = Strng.replace('ṁ', 'ṃ')

    """Anusvara to nasal - gam-ga -> gan-ga (converts anusvara before homorganic consonants into the matching nasal consonant)."""
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
    """No-op placeholder (reserved for Tai Kuen script-specific post-processing)."""
    return Strng

def TaiThamLao(Strng):
    """No-op placeholder (reserved for Tai Tham Lao-variant post-processing)."""
    return Strng

# Newa's own logic now lives in ScriptProcessing/Newa.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Newa import nepaldevafont, NewaMurmurConsonants, NewaSpecialTa, NewaDisableRepha

# Chakma's own logic now lives in ScriptProcessing/Chakma.py -
# consolidated there (batch migration).
from .ScriptProcessing.Chakma import ChakmaPali_post as ChakmaPali, ChakmaEnableAllConjuncts, ChakmaVowelsIndependent

# LaoPali's own logic now lives in ScriptProcessing/LaoPali.py -
# consolidated there (batch migration).
from .ScriptProcessing.LaoPali import LaoTranscription_post as LaoTranscription, LaoPhonetic_post as LaoPhonetic, LaoSajjhaya, LaoSajjhayawithA

# Siddham's own logic now lives in ScriptProcessing/Siddham.py -
# consolidated there (batch migration).
from .ScriptProcessing.Siddham import UseAlternateI1, UseAlternateI2, UseAlternateII, UseAlternateU, UseAlternateVSU, UseAlternateVSUU, siddhammukta

# Lao's own logic now lives in ScriptProcessing/Lao.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Lao import LaoNative

# Sundanese's own logic now lives in ScriptProcessing/Sundanese.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Sundanese import SundaneseHistoricConjuncts

# Limbu's own logic now lives in ScriptProcessing/Limbu.py -
# consolidated there (batch migration).
from .ScriptProcessing.Limbu import LimbuSpellingSaI_post as LimbuSpellingSaI

# Malayalam's own logic now lives in ScriptProcessing/Malayalam.py -
# consolidated there (batch migration).
from .ScriptProcessing.Malayalam import tradOrtho, dotReph, archaicAIAU, MalayalamPrakrit_post as MalayalamPrakrit, historicChillu, MalayalamLineVirama, MalayalamCircVirama, RephaDoubleMalayalam

def siddhamap(Strng):
    """No-op placeholder (reserved for Siddham-specific post-processing)."""
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
    """Restores medieval/pre-reform Tamil orthography for the e/o vowel signs (splits modern e/o/ee/oo forms into their older two-part equivalents)."""
    OldEO = ['எ்', 'ெ்', 'ஒ்', 'ெ்ா', 'எ', 'ெ', 'ஒ', 'ொ']
    NewEO = ['எ', 'ெ', 'ஒ', 'ொ', 'ஏ', 'ே', 'ஓ', 'ோ']

    for x,y in zip(NewEO, OldEO):
        Strng = Strng.replace(x,y)

    return Strng

# DevanagariLimbu's own logic now lives in ScriptProcessing/DevanagariLimbu.py -
# consolidated there (batch migration).
from .ScriptProcessing.DevanagariLimbu import LimbuDevanagariConvention_post as LimbuDevanagariConvention

# Nandinagari's own logic now lives in ScriptProcessing/Nandinagari.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Nandinagari import NandinagariPrishtamatra

# Oriya's own logic now lives in ScriptProcessing/Oriya.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Oriya import OriyaVaAlt, OriyaYYA

def BengaliYYA(Strng):
    """ya everywhere - yayati yajna -> nukta-ya-yati nukta-yajna (replaces every plain ya with nuktaed yya in Bengali)."""
    return YYAEverywhere(Strng, 'Bengali')

def RetainTeluguDanda(Strng):
    """Converts roman full stops to Telugu danda punctuation."""
    return RetainDandasIndic(Strng, 'Telugu')

def RetainTeluguNumerals(Strng):
    """Converts Western Arabic digits to Telugu numerals."""
    return RetainIndicNumerals(Strng, 'Telugu')

def RetainTamilDanda(Strng):
    """Converts roman full stops to Tamil danda punctuation."""
    return RetainDandasIndic(Strng, 'Tamil')

def RetainTamilNumerals(Strng):
    """Converts Western Arabic digits to Tamil numerals."""
    return RetainIndicNumerals(Strng, 'Tamil')

def RetainKannadaDanda(Strng):
    """Converts roman full stops to Kannada danda punctuation."""
    return RetainDandasIndic(Strng, 'Kannada')

def RetainKannadaNumerals(Strng):
    """Converts Western Arabic digits to Kannada numerals."""
    return RetainIndicNumerals(Strng, 'Kannada')

def RetainMalayalamDanda(Strng):
    """Converts roman full stops to Malayalam danda punctuation."""
    return RetainDandasIndic(Strng, 'Malayalam')

def RetainMalayalamNumerals(Strng):
    """Converts Western Arabic digits to Malayalam numerals."""
    return RetainIndicNumerals(Strng, 'Malayalam')

def RetainGujaratiDanda(Strng):
    """Converts roman full stops to Gujarati danda punctuation."""
    return RetainDandasIndic(Strng, 'Gujarati')

def RetainGurmukhiNumerals(Strng):
    """Converts Western Arabic digits to Gurmukhi numerals."""
    return RetainIndicNumerals(Strng, 'Gurmukhi')

def IASTPali(Strng):
    """Converts the IAST underlined-l (l with line below) used for retroflex l to the standard Pali l-underdot."""
    Strng = Strng.replace('l̤', 'ḷ')

    return Strng

def ThamTallADisable(Strng):
    """Disable explicit Tall -a - collapses the tall-a vowel sign to the regular a vowel sign, letting the font choose the visual form."""
    Strng = Strng.replace('\u1A64', '\u1A63')

    return Strng

def ThamTallAOthers(Strng):
    """Tall -a with ca/ba/ra/bha - applies the Tai Tham tall-a vowel sign after these four consonants via FixTallA."""
    TallACons = '|'.join(['ᨧ', 'ᨻ', 'ᩁ', 'ᨽ']) ## ca ba ra bha

    Strng = FixTallA(Strng, TallACons)

    return Strng

#start here

def ThamShiftMaiKangLai(Strng):
    """Shift Mai Kang Lai - repositions the Tai Tham mai kang lai sign to follow the vowel/diacritic it modifies instead of preceding it."""
    Strng = re.sub('(\u1A58)(.)', r'\2\1', Strng)
    ListV = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns,'TaiTham') + ['ᩤ']) + ')'

    Strng = re.sub('(\u1A58)([\u1A55\u1A56])', r'\2\1', Strng)
    Strng = re.sub('(\u1A58)(\u1A60.)', r'\2\1', Strng)
    Strng = re.sub('(\u1A58)' + ListV, r'\2\1', Strng)
    Strng = re.sub('(\u1A58)' + ListV, r'\2\1', Strng)

    #Strng = Strng.replace('\u1A63\u1A58', '\u1A58\u1A63')

    return Strng

def UrduRemoveShortVowels(Strng):
    """Remove short vowels - hindustan-with-marks -> hindustan (strips sukun, fatha, kasra, damma, and the Urdu small-v diacritics)."""
    ShortVowels = ['\u0652','\u064E','\u0650','\u064F', '\u0658']

    for vow in ShortVowels:
        Strng = Strng.replace(vow,"")

    return Strng

def swapEe(Strng):
    """E/O for long, e/o for short - swaps the case convention of the e and o vowel placeholders so uppercase marks the long vowel."""
    Strng = Strng.replace('E', 'X@X@')
    Strng = Strng.replace('e', 'E')
    Strng = Strng.replace('X@X@', 'e')

    Strng = Strng.replace('O', 'X@X@')
    Strng = Strng.replace('o', 'O')
    Strng = Strng.replace('X@X@', 'o')

    return Strng

def capitalizeSentence(Strng):
    """Capitalizes the first letter of each sentence (after start of string, ./?/!, newline, or quote-opened line) and after an '@' marker."""
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

# ============================================================
# Internal-only options - not exposed in the frontend UI, but
# genuinely used: called directly by other backend code (Convert.py,
# ConvertFix.py, PostOptions.py/PreOptions.py's default-option
# tables, transliterate.py's LoC/semiticISO dynamic dispatch, or
# another option function), or proven working by a real test
# fixture even though nothing currently calls it. Still reachable
# via the generic pre_options=[name]/post_options=[name] API even
# when nothing internal calls it, since every function here is
# registered by Options.py's reflection regardless of section.
# ============================================================


### Rewrite all ListC, ListV as sorted(List,key=len,reverse=True).
### Consider Adding Options to ignore Nukta etc for Gujarati bengali by default

## order the functions by script ##

def _convertCleanup(Strng):
    """Strips internal marker/placeholder characters before the text
    is used further - including as input to another convertScript()
    call, since a single transliterate.process() call can chain
    several of them (Itrans's ## split, the Japanese pivot, the
    src==tgtOld self-conversion case). That's why this runs inside
    convertScript() itself rather than once at the end like
    _finalCleanup below - it has to run after every individual
    conversion step, not just the last one.

    U+F001/U+05CC/U+05CD are markers from the Semitic/Syriac
    romanization pivot (see PreProcess.insertViramaSyriac,
    PreProcess.AlephMaterLectionis, and the nativizing-Semitic-to-
    Indic flag set in transliterate.py's _resolve_semitic_indic_
    naming). Doubled okina and U+02C2 turned out to still be live too
    (confirmed the hard way - removing them broke Burmese/Shan
    RomanLoC and a Saurashtra test) despite no literal source
    occurrence of either being grep-able - they arise from adjacent
    single-character insertions combining at runtime, or survive as
    literal input, not from a hardcoded multi-char marker."""
    Strng = Strng.replace("\uF001", "").replace("\u05CC", "").replace("ʻʻ", "").replace('\u05CD', '').replace('\u02C2', '')

    return Strng

def _applyPunctuationNumeralOptions(Strng, tgt, postoptions):
    """Applies numeral-style and full-stop postoptions the caller
    explicitly requested (romanNumerals/indicNumerals/romanFullStop) -
    this is user-requested output formatting, not cleanup (see
    _finalCleanup below for the unconditional cleanup step)."""
    ## Fix Dandas & Numerals
    if 'romanNumerals' in postoptions:
        Strng = RetainIndicNumerals(Strng,tgt,reverse=True)
    if 'indicNumerals' in postoptions:
        Strng = RetainIndicNumerals(Strng,tgt,reverse=False)
    if 'romanFullStop' in postoptions:
        Strng = RetainDandasIndic(Strng, tgt, reverse=True)

    return Strng

def _finalCleanup(Strng, tgt):
    """Restores the placeholder characters PreProcess.
    RetainDevangariDanda/RetainPipeDanda substituted in during pre-
    processing to shield danda/period characters from the table-
    driven conversion logic - the reverse half of that shield, run
    once at the very end of the whole pipeline (unlike
    _convertCleanup above, which runs after every individual
    conversion step)."""
    Strng = Strng.replace('\u034F', '') ## remove token characters for specialized processing

    #Devanagari Dandas
    if not SR.get(tgt).is_transliteration:
        Strng = Strng.replace( '│', '।',).replace('┃', '॥')
    else:
        Strng = Strng.replace( '│', '|',).replace('┃', '||')
    #Pipe scripts as source
    Strng = Strng.replace( "●", ".",)

    return Strng
from .ScriptProcessing.Khojki import KhojkiRRI
from .ScriptProcessing.Ahom import AhomClosed
from .ScriptProcessing.Sinhala import SinhalaDefaultConjuncts, SinhalaChandrbinduAnusvara
from .ScriptProcessing.Telugu import TeluguRemoveNukta, TeluguRemoveAeAo

#testcase todo
# HebrewSBL's own logic now lives in ScriptProcessing/HebrewSBL.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.HebrewSBL import HebrewToHebrewSBLPost as HebrewSBLTarget, HebrewSBLToHebrewPost as HebrewSBLSource

# ISO259/ISO233/PersianDMG's Target/Source logic (part of
# GeneralMap.semiticISO's pseudo-script romanization pivot) now lives
# in ScriptProcessing/ISO259.py, ScriptProcessing/ISO233.py,
# ScriptProcessing/PersianDMG.py - consolidated there (batch migration
# - see ScriptProcessing/Tamil.py for the full rationale/pattern this
# follows). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.ISO259 import HebrewToISO259Post as ISO259Target, ISO259ToHebrewPost as ISO259Source
from .ScriptProcessing.ISO233 import ArabToISO233Post as ISO233Target, ISO233ToArabPost as ISO233Source
from .ScriptProcessing.PersianDMG import ArabFaToPersianDMGPost as PersianDMGTarget, PersianDMGToArabFaPost as PersianDMGSource
from .ScriptProcessing.Bengali import BengaliConjunctVB

#testcase todo
def arabizeLatn(Strng, target='semitic'):
    """Converts generic Roman Semitic transliteration into Arabic-specific conventions, resolving hamza after consonants into a/a-macron/a-circumflex and normalizing glottal-stop marks."""
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

#testcase todo
def urduizeLatn(Strng, target='semitic'):
    """Converts generic Roman Semitic transliteration into Urdu-specific conventions, resolving hamza into a/a-circumflex and normalizing glottal-stop marks to hamza."""
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
    """Converts generic Roman Semitic transliteration into Syriac-specific conventions by expanding word-initial long a/e vowels back into hamza plus short vowel."""
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
    """Converts generic Roman Semitic transliteration into Hebrew-specific conventions by inserting aleph before word-initial vowels."""
    if target != 'indic':
        Strng = LatnInitialVowels(Strng, 'ʾ')

    return Strng
from .ScriptProcessing.Arab import ArabRemoveAdditions

#testcase todo
#testcase todo
def removeSemiticLetters(Strng):
    """Neutralizes emphatic/interdental Semitic consonant letters to plain Latin approximations (t-dot->t, h-dot->h, d-dot/d-line/z-dot->z, w->v, ayin->hamza, s-dot->s)."""
    Strng = Strng.replace('ṭ', 't').replace('ḥ', 'h').replace('ḍ', 'z').replace('ḏ', 'z').replace('ẓ', 'z')\
        .replace('w', 'v').replace('ʿ', 'ʾ').replace('ṣ', 's')

    return Strng
from .ScriptProcessing.Hebrew import HebrewVetVav, HebrewnonFinalShort

#testcase todo
def LatnInitialVowels(Strng, initLetter=''):
    """Replaces word-initial long-vowel forms (a-circumflex, i-macron-circumflex, etc.) with a leading marker letter plus the corresponding plain vowel; helper for the *izeLatn functions."""
    initVow = 'â ā̂ î ī̂ û ū̂ ê ē̂ âŷ ô ō̂ âŵ'.split(' ')
    nonInitVow = 'a ā i ī u ū e ē aŷ o ō aŵ'.split(' ')

    for x, y in zip(initVow, nonInitVow):
        Strng = Strng.replace(x, initLetter+y)

    Strng = Strng.replace('\u0302', '')

    Strng = re.sub('\u033d', '', Strng)
    #Strng = 'Vinodh'
    return Strng

#testcase todo
# BurmeseLoC's own LoC logic now lives in ScriptProcessing/BurmeseLoC.py -
# consolidated there (LoC redesign).
from .ScriptProcessing.BurmeseLoC import BurmeseToRomanLocPost, RomanLocToBurmesePost

#ThamLoC
# ThamLoC's own LoC logic now lives in ScriptProcessing/ThamLoC.py -
# consolidated there (LoC redesign).
from .ScriptProcessing.ThamLoC import ThamLoCToRomanLocPost, RomanLocToThamLoCPost

# khmer
# KhmerLoC's own LoC logic now lives in ScriptProcessing/KhmerLoC.py -
# consolidated there (LoC redesign).
from .ScriptProcessing.KhmerLoC import KhmerLoCToRomanLocPost, RomanLocToKhmerLoCPost

# shan
# ShanLoC's own LoC logic now lives in ScriptProcessing/ShanLoC.py -
# consolidated there (LoC redesign).
from .ScriptProcessing.ShanLoC import ShanLoCToRomanLocPost, RomanLocToShanLoCPost

#testcase todo
### Add new consonants here when added to gimeltra_data
#testcase todo
def insertARomanSemitic(Strng):
    """Inserts an inherent /a/ after Semitic consonants (and gemination marks) that are not already followed by an explicit vowel."""
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
    """Fixes Roman Semitic gemination notation (consonant+virama+same consonant -> gemination sign for Arabic-target output) and reorders emphatic-consonant nukta-equivalent markers around their vowel."""
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

#todo testcase
#todo testcase
#todo testcase
def tokushuon(txt):
   """Applies Japanese tokushuon (special loanword kana) spelling conventions, e.g. si->suxi, zi->zuxi, yi->ixi, fy->fux, nye->nixe, and context-sensitive hu/hye expansions."""
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
    """Pivots Japanese text through Telugu/ISO/Inter intermediate scripts en route to a RomanKana representation."""
    from . import Convert
    txt = Convert.convertScript(txt, src, "Telugu")

    txt = txt.replace('ˆ', '')
    txt = Convert.convertScript(txt.lower(), "ISO", "Inter")

    txt = Convert.convertScript(txt, "Telugu", "RomanKana")

    return txt

def _japanese_visarga_nasalization_punctuation(txt):
    # Visarga
    """Expands visarga into vowel-echoed h, assimilates nasal consonants before homorganic stops, and converts ASCII punctuation to Japanese full-width punctuation."""
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
    """Applies empirical consonant-cluster fixes for naturalized Japanese romanization (tr/dr->tor/dor, tya/dya/sya palatalization spellings, di/du/ti/tu epenthetic vowels, ye/vye handling)."""
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
    """Branches Japanese post-processing on the nativize flag: resolves r/k gemination marks and applies tokushuon when not nativized, or simplifies yi/ye/wu/wo/she spellings when nativized."""
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
    """Encodes intermediate romanized Japanese text into Hiragana or Katakana via kana2roman, handling consonant/vowel gemination and choonpu (long-vowel) marks."""
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
    """Runs the full Japanese post-processing pipeline (pivot to RomanKana, punctuation/nasalization fixes, consonant fixes, nativize branch, kana encoding) to produce Hiragana/Katakana output."""
    from . import Convert

    txt = _japanese_pivot_to_romankana(src, txt)
    txt = _japanese_visarga_nasalization_punctuation(txt)
    txt = _japanese_empirical_consonant_fixes(txt, postoptions)
    txt = _japanese_nativize_branch_fix(txt, nativize)
    txt = _japanese_encode_to_kana(txt, tgt, nativize)

    txt = Convert.convertScript(txt, "Inter", "ISO")

    return txt

#todo testcase
# Gurmukhi's own logic now lives in ScriptProcessing/Gurmukhi.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.Gurmukhi import GurmukhiCandrabindu, GurmukhiTippiBindu, GurmukhiTippiGemination

#misnomer
# MalayalamLoC's own LoC logic now lives in ScriptProcessing/MalayalamLoC.py -
# consolidated there (LoC redesign).
from .ScriptProcessing.MalayalamLoC import MalayalamToRomanLocPost
from .ScriptProcessing.TamilExtended import TamilpredictDentaNaExtended
from .ScriptProcessing.Tamil import TamilNaToNNa, TamilpredictDentaNa

def Dot2Pipes(Strng):
    """Converts double and single full-stop dots into ASCII pipe punctuation (.. -> ||, . -> |)."""
    Strng = Strng.replace('..', '||')
    Strng = Strng.replace('.', '|')

    return Strng
from .ScriptProcessing.Tibetan import TibetanRemoveVirama, TibetanRemoveBa

# reverse these in preprocess
def RomanLoCVaWa(Strng):
    """Replaces v with w, per LoC romanization convention for scripts where va is rendered as w."""
    Strng = Strng.replace('v', 'w')
    return Strng

def RomanLoCSasha(Strng):
    """Replaces s-dot-below (sa) with sh, per LoC romanization convention."""
    Strng = Strng.replace('ṣ', 'sh')
    return Strng

def RomanLoCLaUnderscoreDoubleDot(Strng):
    """Replaces l-line-below with l-double-underdot, per LoC romanization convention."""
    Strng = Strng.replace('ḻ', 'l̤')

    return Strng
from .ScriptProcessing.DevanagariLoC import DevanagariToRomanLocPost

# TibetanLoC's own LoC logic now lives in ScriptProcessing/TibetanLoC.py -
# consolidated there (LoC redesign).
from .ScriptProcessing.TibetanLoC import TibetanLoCToRomanLocPost
from .ScriptProcessing.JavaneseLoC import JavaneseToRomanLocPost
from .ScriptProcessing.BalineseLoC import BalineseToRomanLocPost

def BalineseJavaneseMoveRepha(Strng, tgt, reph):
    """Repositions the Balinese/Javanese repha (pre-base r) sign to follow the consonant cluster (and any anusvara-type sign) it modifies."""
    repha = '(' + reph + ')'

    cons = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, tgt)) + ')'
    vows = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSignsNV, tgt)) + ')'
    vir = GM.CrunchSymbols(GM.virama, tgt)[0]

    Strng = re.sub(repha+'('+cons+')'+'('+ vir + cons +')*'+'(' + vows + ')?', r'\2\4\6\1', Strng)

    candAnu = '[' + ''.join(GM.CrunchSymbols(GM.CombiningSigns, tgt)[:2]) + ']'
    Strng = re.sub(repha+'(' + candAnu + ')', r'\2\1', Strng)

    return Strng

# GurmukhiLoC's own LoC logic now lives in ScriptProcessing/GurmukhiLoC.py -
# consolidated there (LoC redesign).
from .ScriptProcessing.GurmukhiLoC import GurmukhiLoCToRomanLocPost

# Sinhala's own LoC logic now lives in ScriptProcessing/Sinhala.py -
# consolidated there (LoC redesign).
from .ScriptProcessing.Sinhala import SinhalaSannakaNasalization
from .ScriptProcessing.Chakma import ChakmaGemination

# WarangCiti's own logic now lives in ScriptProcessing/WarangCiti.py -
# consolidated there (batch migration). Re-exported here so Options.py's PostProcess getmembers()'s
# reflection-based dispatch keeps finding these names.
from .ScriptProcessing.WarangCiti import WarangCitiModernOrthogaphy

def MultaniAbjad(Strng):
    """Simplifies Multani abjad-style orthography by dropping vowels between consonants in CVC/consonant-cluster contexts, matching its abjad (consonant-only) spelling convention."""
    ListAll = "(" + "|".join(GM.CrunchSymbols(GM.Characters, 'Multani') + ["𑊓", "𑊍"]) + ")"
    ListC = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, 'Multani') + ["𑊓", "𑊍"]) + ")"
    ListV = "(" + "|".join(GM.CrunchSymbols(GM.Vowels, 'Multani') + ["𑊓", "𑊍"]) + ")"

    Strng = re.sub(ListC + ListV + ListC, r'\1\3', Strng)
    Strng = re.sub('('+ ListC + '{2,})' + ListV, r'\1', Strng)
    Strng = re.sub(ListV + ListC + ListV, r'\1\2', Strng)

    return Strng
from .ScriptProcessing.Sundanese import SundaneseRemoveHistoric
from .ScriptProcessing.Limbu import LimburemoveHistorical

def ModiRemoveLong(Strng):
    """Converts long vowel signs and independent vowels in Modi script (i, u, r-vocalic and their vowel-sign forms) to their short equivalents."""
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

def ThaanaRemoveHistorical(Strng):
    """Replaces the historical Thaana letter naa (retroflex n) with the modern noonu letter."""
    return Strng.replace('ޱ','ނ')
from .ScriptProcessing.Oriya import OriyaVa

def MalayalamremoveHistorical(Strng):
    """Replaces the historical Malayalam na letter with the modern na, and the virama-joined na-chillu sequence with the standalone chillu-n."""
    Strng = Strng.replace('\u0D29','\u0D28')
    Strng = Strng.replace('ന‍്', 'ൻ')

    return Strng

    ## Insert Gemination Sign

def MeeteiMayekremoveHistorical(Strng):
    """Replaces historical/obsolete Meetei Mayek letters and the diaeresis-marked cheitap ee/oo sequences with their modern equivalents."""
    removePairs = [('ꫢ', 'ꯆ'), ('ꫣ', 'ꯅ'), ('ꫤ','ꯇ'), ('ꫥ','ꯊ'), ('ꫦ','ꯗ'), ('ꫧ','ꯙ'), ('ꫨ','ꯅ'),
                   ('ꫩ','ꯁ'), ('ꫪ','ꯁ'), ('\uAAF5','ꯍ꯭'), ('ꯑꫫ','ꯏ'), ('ꯑꫬ','ꯎ'), ('ꫫ','ꯤ'), ('ꫬ','ꯨ')]

    for x,y in removePairs:
        Strng = Strng.replace(x,y)

    return Strng

# കൽന് കത്ല് ക്ഷേത്ര് കൻല് - Check this

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

def RemoveSchwa(Strng,Target):

    """Inserts an explicit virama after script consonants that are not already followed by a vowel sign, suppressing the inherent /a/ (schwa) reading."""
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

    """Replaces consonant+virama+identical-consonant (and consonant+virama+its aspirated counterpart) sequences with a dedicated gemination sign."""
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

    """Expands a dedicated gemination sign back into consonant+virama+consonant (or its aspirated counterpart), inverse of InsertGeminationSign."""
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

    """Forms the Bengali khanda ta (cluster-final ta, U+09CE) from ta+virama when not followed by a joining consonant, or reverses khanda ta back to ta+virama when reverse=True."""
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

    """Converts a homorganic nasal consonant followed by virama and a same-varga consonant into anusvara plus that consonant."""
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
    """Converts anusvara followed by a homorganic consonant into the corresponding nasal consonant plus virama (inverse of NasalToAnusvara)."""
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

## Check Namna, ramya -> Malayalam; fix
def MToAnusvara(Strng,Target):

    """Converts a word/syllable-final labial nasal consonant (ma+virama) not followed by another consonant into anusvara."""
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

def YYAEverywhere(Strng, Target):
    """Replaces every occurrence of the plain ya consonant with the nukta-marked yya (antahstha ya) in the given target script."""
    Ya = GM.CrunchList('ConsonantMap', Target)[25]
    YYa = GM.CrunchList('NuktaConsonantMap',Target)[7]

    Strng = Strng.replace(Ya, YYa)

    return Strng

def YaToYYa(Strng,Target):
    """Converts ya into the nukta-marked yya (antahstha ya) after a preceding letter, for scripts (Assamese, Bengali, Oriya, Chakma) that distinguish the two."""
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

    """Replaces va with ba, for target scripts where the va and ba consonants have historically merged."""
    va = GM.CrunchSymbols(GM.Consonants, Target)[28]
    ba = GM.CrunchSymbols(GM.Consonants, Target)[22]

    if Target == 'Bengali':
        #Strng = Strng.replace('ৎৱ', 'ত্ব')
        pass

    Strng = Strng.replace(va,ba)

    return Strng

def tbadiff(Strng,Target):

    """Restores the khanda-ta+ba sequence to ta+virama+ba, distinguishing it from the regular khanda-ta merger."""
    Strng = Strng.replace('ৎব', 'ত্ব')

    return Strng

def RetainDandasIndic(Strng, Target, reverse=False):
    """Converts roman '.'/'..'  full stops to native single/double danda punctuation, or reverses danda back to '.'/'..' when reverse=True."""
    Dandas = GM.CrunchList('SignMap', Target)[1:3]

    if not reverse:
        Strng = Strng.replace('..', Dandas[1])
        Strng = Strng.replace('.', Dandas[0])
    else:
        Strng = Strng.replace(Dandas[0], '.')
        Strng = Strng.replace(Dandas[1], '..')

    return Strng

def RetainIndicNumerals(Strng,Target, reverse=False):
    """Converts Western Arabic digits to the target script's native numerals, or reverses native numerals back to Arabic digits when reverse=True."""
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
    """Converts the target script's native numerals to Western Arabic digits, or reverses Arabic digits back to native numerals when reverse=True."""
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
    """No-op placeholder (reserved for the indicNumerals post-option; numeral conversion is handled by RetainIndicNumerals)."""
    return Strng

def romanFullStop(Strng):
    """No-op placeholder (reserved for the romanFullStop post-option; danda conversion is handled by RetainDandasIndic)."""
    return Strng

def indicDandas(Strng):
    """No-op placeholder (reserved for the indicDandas post-option)."""
    return Strng

def romanNumerals(Strng):
    """No-op placeholder (reserved for the romanNumerals post-option; numeral conversion is handled by RetainRomanNumerals)."""
    return Strng

def RemoveDiacritics(Strng):
    """Strips a generic set of removable diacritic marks (GM.DiacriticsRemovable) from the string."""
    for x in GM.DiacriticsRemovable:
        Strng = Strng.replace(x,'')

    return Strng

def RemoveDiacriticsTamil(Strng):
    """Strips Tamil-specific removable diacritic marks (GM.DiacriticsRemovableTamil) from the string."""
    for x in GM.DiacriticsRemovableTamil:
        Strng = Strng.replace(x,'')

    return Strng

def SaurashtraHaru(Strng):

    """Replaces specific Saurashtra consonant+virama+ha clusters with the dedicated haru (below-base h) sign."""
    ListC = '|'.join([Saurashtra.ConsonantMap[x] for x in [19,24,26,27]])
    vir = Saurashtra.ViramaMap[0]
    ha = Saurashtra.ConsonantMap[32]

    Strng = re.sub('('+ListC+')'+vir+ha,r'\1'+'\uA8B4',Strng)

    return Strng

def ThaiLaoTranscription(Strng,Script,shortA,shortAconj,reverse=False, anusvaraChange=True):
    ## For Native lao: aMDa give an'da as intermediate (N doesn't exist in Native Lao )
    ## Hence issues with nasal conversion

    """Bidirectionally converts between segmented Thai/Lao/LaoPali script forms and unsegmented encoded text: inserts/removes the inherent short-a vowel and its conjunct form, handles anusvara-to-nasal conversion, reorders pre-posed vowels around consonant+virama clusters, and fixes r/l vowel-swap and special consonant-cluster spellings (e.g. prahlada, sarva)."""
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

# not used
def FixTallA(Strng, TallACons):
    """Introduces the Tai Tham tall-a vowel sign after specified base or subjoined consonants (including through consonant clusters), and reverses it for consonants with protruding subjoined forms."""
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

    """Applies Avestan orthographic conventions: inserts nasalization before consonant clusters, softens word-final a before n/m, marks retroflex n before velars/dentals, selects consonant allophones before ii/uu vowels, and picks the ta variant by following context."""
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
def PhagsPaRearrange(Strng,Target):
    """Inserts virama before word-final 'Phags-pa consonants (marked by trailing spaces), then converts remaining spaces and Mongolian-style punctuation into 'Phags-pa segment markers."""
    vir = GM.CrunchList('ViramaMap', Target)[0]
    ListC = '|'.join(GM.CrunchSymbols(GM.Consonants,Target))
    ListV = '|'.join(GM.CrunchSymbols(GM.Vowels,Target))
    ListVS = '|'.join(GM.CrunchSymbols(GM.VowelSignsNV,Target))

    Strng = re.sub("(?<!( |"+vir+"))"+"("+ListC+")"+"(?= )",r'\2'+vir,Strng)
    #print Strng

    Strng = Strng.replace(" ","").replace("᠂"," ").replace("᠃"," ")
    return Strng

# New LoC (Library of Congress) romanization post-options - see
# ScriptProcessing/HOW_TO_ADD_LOC.md for the naming convention.
from .ScriptProcessing.TeluguLoC import TeluguToRomanLocPost, RomanLocToTeluguPost
from .ScriptProcessing.KannadaLoC import KannadaToRomanLocPost
from .ScriptProcessing.SinhalaLoC import SinhalaToRomanLocPost
from .ScriptProcessing.OriyaLoC import OriyaToRomanLocPost
from .ScriptProcessing.AssameseLoC import AssameseToRomanLocPost, RomanLocToAssamesePost
from .ScriptProcessing.BengaliLoC import BengaliToRomanLocPost, RomanLocToBengaliPost
from .ScriptProcessing.GujaratiLoC import GujaratiToRomanLocPost

# ============================================================
# Unreferenced - no call site found anywhere in the codebase (not
# the frontend, not internal backend code, not a test fixture) by
# a full reference scan across every .py file plus the frontend's
# ScriptMixin.js. NOT a delete list: this session already proved a
# clean static search can miss a genuinely live dependency (see
# PostProcess._convertCleanup's doubled-okina/U+02C2 history) - it
# means nothing was found, not that nothing uses it. Verify with a
# real remove-and-test pass (full corpus regen + test suite) before
# treating anything here as safe to delete.
# ============================================================


#testcase todo
def syriacVowelsBelow(Strng):

    """No-op placeholder (reserved for lowering Syriac vowel diacritics below the line)."""
    return Strng

#testcase todo
def syriacWesternOToU(Strng):

    """No-op placeholder (reserved for Western Syriac o-to-u vowel shift)."""
    return Strng

#testcase todo
def removeDiacriticsPersian(Strng):

    """No-op placeholder (reserved for stripping Persian diacritics)."""
    return Strng

#testcase todo
def removeDiacriticsSyriac(Strng):

    """No-op placeholder (reserved for stripping Syriac diacritics)."""
    return Strng

#testcase todo
def useKtivMale(Strng):

    """No-op placeholder (reserved for switching Hebrew to ktiv male full spelling)."""
    return Strng

#testcase todo
def PhoneticMapping(Strng):

    """No-op placeholder (reserved for phonetic remapping)."""
    return Strng

#testcase todo
def ArabicGimelGaGha(Strng):
    """Replaces Arabic jim with ghayn (renders Hebrew/Semitic 'ga' sound as Arabic 'gha')."""
    Strng = Strng.replace('ج', 'غ')

    return Strng

#testcase todo
def ArabicGimelPaBa(Strng):
    """Replaces Arabic fa with ba (renders Hebrew/Semitic 'pa' sound as Arabic 'ba')."""
    Strng = Strng.replace('ف', 'ب')

    return Strng

#todo feature
def siddhamBija(Strng):

    """No-op placeholder (reserved for Siddham bija/seed-syllable rendering)."""
    return Strng

#todo testcase
def arabPaFa(Strng):

    """Replaces Arabic pe with fa (renders Persian/Urdu 'pa' sound as Arabic 'fa')."""
    return Strng.replace('پ','ف')

#todo testcase
def arabChaSa(Strng):

    """Replaces Arabic che with sin (renders Persian/Urdu 'cha' sound as Arabic 'sa')."""
    return Strng.replace('چ', 'س')

#todo testcase
def HiraganaaunotDipthong(Strng):

    """No-op placeholder (reserved for preventing au from being read as a Hiragana diphthong)."""
    return Strng

#not used
def IASTISONasalTilde(Strng):

    """No-op placeholder (reserved for IAST/ISO nasalization tilde handling)."""
    return Strng

#todo testcase
#todo testcase
#todo testcase
def HebrewKatevMalei(Strng):
    """Replaces Hebrew qamats and patach vowel points with aleph, producing ktiv male (full/plene) spelling."""
    Strng = Strng.replace('ָ', 'א') # long aa
    Strng = Strng.replace('ַ', 'א') # short a

    return Strng

# RomanLoC's own LoC logic now lives in ScriptProcessing/RomanLoC.py -
# consolidated there (LoC redesign).
from .ScriptProcessing.RomanLoC import RomanLoCChandrabindu_post as RomanLoCChandrabindu, KhandaTaRomanLoC_post as KhandaTaRomanLoC

def MalayalamNTA(Strng):
    """Converts the n+ra sequence into n+t-line (Malayalam nta orthographic convention)."""
    Strng = Strng.replace('nṟ', 'nṯ')
    return Strng

def AmbigousTamilOrthography(Strng):

    """No-op placeholder (reserved for resolving ambiguous Tamil orthography)."""
    return Strng

def TamilSHADisable(Strng):
    """Replaces Tamil sha (Grantha letter) with sa followed by a superscript '2' marker, disabling the dedicated sha glyph."""
    return Strng.replace("ஶ", "ஸ²")

def UrduAlternateUU(Strng):
    """Intended to replace a short-u+wow sequence with wow+hamza-below as an alternate Urdu spelling; the search string is a literal backslash-escaped text, not an actual Unicode sequence, so this currently has no effect."""
    Strng = Strng.replace("\\u064F\\u0648","\u0648\u0657")

    return Strng

# not used
def TaiThamO(Strng):
    """Merges the Tai Tham e-vowel-sign + aa-vowel-sign sequence into the single dedicated o vowel sign."""
    Strng = Strng.replace("\u1A6E\u1A63","\u1A70")

    return Strng

# not used
def TaiThamHighNga(Strng):
    """Replaces the low-register Tai Tham nga consonant with its high-register variant."""
    Strng = Strng.replace('\u1A58','\u1A59')

    return Strng

# not used
def TaiThamMoveNnga(Strng):
    """Repositions the Tai Tham high-register nga sign to follow the character it attaches to."""
    Strng = re.sub('(.)(\u1A58)',r'\2\1',Strng) # Probably its u1A59

    return Strng

def LatinPipes(Strng):
    ###

    """No-op placeholder (reserved for converting pipe punctuation in Latin-script output)."""
    return Strng

# not used
def DevanagariAVowels(Strng):
    """Decomposes old-style independent Devanagari vowel letters into the inherent-a consonant carrier plus the corresponding dependent vowel sign."""
    oldVowels = Devanagari.VowelMap[2:12]+Devanagari.SouthVowelMap[:1]
    a = Devanagari.VowelMap[0]
    newAVowels = [a+x for x in Devanagari.VowelSignMap[1:11]+Devanagari.SouthVowelSignMap[:1]]

    for x,y in zip(oldVowels,newAVowels):
        Strng = Strng.replace(x,y)

    return Strng

# not used
def AnusvaraToNasalIPA(Strng):

    """Converts the IPA nasalization diacritic before stops into the corresponding homorganic nasal consonant (velar/palatal/dental/retroflex), including after a length mark."""
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

    """Removes the multiplication-sign (x) marker character from IPA output."""
    Strng = Strng.replace('×','')

    return Strng

# not used
def ChakmaAVowels(Strng):

    """No-op placeholder (reserved for Chakma inherent-vowel handling)."""
    return Strng

