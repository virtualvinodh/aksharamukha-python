# -*- coding: utf-8 -*-

# TamilExtended's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# ConvertFix/PreProcess/PostProcess are imported LOCALLY inside each
# function that needs them (not at module level) - required to avoid a
# load-order-dependent circular import, since these three modules
# re-export names from here. See ScriptProcessing/Tamil.py.

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.MainIndic import Tamil
from aksharamukha.ScriptMap.MainIndic import TamilExtended

# ---- Fix (encode/decode conversion logic) ----

def _FixTamilExtendedEncode(Strng):

    """Normalizes the ksha and shra conjuncts, uses the older-style AU vowel sign, and repositions zero-width joiners relative to Vedic svara marks when encoding Tamil-Grantha extended text."""
    from .. import PostProcess
    Strng = Strng.replace('ക്‌ഷ', 'ക്ഷ')
    Strng = Strng.replace('ശ്‌ര', 'ശ്‍ര')
    Strng = Strng.replace('ൗ', 'ൌ')

    for svara in GM.VedicSvarasList:
        Strng = Strng.replace('\u200C' + svara, svara + '\u200C')

    return Strng

def _FixTamilExtendedDecode(Strng):

    """Repositions zero-width joiners relative to Vedic svara marks and inserts a ZWNJ after every virama when decoding Tamil-Grantha extended text."""
    from .. import PostProcess
    for svara in GM.VedicSvarasList:
        Strng = Strng.replace(svara + '\u200C', '\u200C' + svara)

    Strng = Strng.replace('\u0D4D', '\u0D4D\u200C')

    return Strng

def FixTamilExtended(Strng, reverse=False):

    """Dispatches to the Tamil-Grantha extended encode or decode fix routine depending on conversion direction."""
    return _FixTamilExtendedDecode(Strng) if reverse else _FixTamilExtendedEncode(Strng)

# ---- Post-processing options ----

def TamilStyleUUCore(Strng):

    """Applies the core-Grantha style for u/ū vowel signs by inserting a ZWJ after certain consonants (ഗുബൂഫുഭൂ → ഗ‍ുബ‍ൂഫ‍ുഭ‍ൂ)."""
    from .. import PostProcess
    Strng = re.sub('([ഖഗഘഛഝഠഡഢഥദധഫബഭ])' + '([ുൂ])', r'\1' + '\u200D' + r'\2', Strng)

    return Strng

def TamilStyleUUOther(Strng):

    """Applies the Tamilized-Grantha style for u/ū vowel signs on sibilants, ha, and the shra conjunct by inserting a ZWJ (ജൂസുഷുഹൂ → ജ‍ൂസ‍ുഷ‍ുഹ‍ൂ)."""
    from .. import PostProcess
    Strng = re.sub('([ജശഷസഹ])' + '([ുൂ])', r'\1' + '\u200D' + r'\2', Strng)
    Strng = re.sub('(ശ്ര)' + '([ുൂ])', r'\1' + '\u200D' + r'\2', Strng)
    Strng = re.sub('(ശ്‍ര)' + '([ുൂ])', r'\1' + '\u200D' + r'\2', Strng)


    return Strng

def TamilpredictDentaNaExtended(Strng):

    """Corrects ambiguous nna/dental-na spellings back to dental na for a hardcoded list of known Sanskrit-derived words in Tamil-Grantha extended text."""
    from .. import PostProcess
    listDentalNa = '''ഩഖ
ഩഗര
ഩകുല
ഩഗ്‌ഩ
ഩക്ഷത്‌ര
ഩടരാജ
ഩടീ
ഩദീ
ഩന്‌ദഩ
ഩപുംസക
ഩഭ**
ഩമ**
ഩമശ്‌
ഩമസ്‌
ഩമാമ
ഩമാമി
ഩമാമോ
ഩമുചി
ഩമോ
ഩമോനമ
ഩമോനമോ
ഩമോസ്‌തു
ഩമോസ്‌തുതേ
ഩമഃ
ഩയഩ
ഩര**
ഩരക
ഩര്‌തക
ഩര്‌തഩ
ഩര്‌മദ
ഩല**
ഩലിഩ
ഩവ**
ഩവീഩ
ഩവ്‌യ
ഩശ്‌**
ഩഷ്‌ട
ഩാരായണ
ഩാഗ
ഩാടക
ഩാഡീ
ഩാട്‌യ
ഩാഡ്‌യ
ഩാഥ
ഩാദ
ഩാരത
ഩാഩാ***
ഩാഩ്‌യ**
ഩാഩൃത
ഩാഭ
ഩാമ
ഩായക
ഩായികാ
ഩാരദ
ഩാരസിംഹ
ഩാരി
ഩാരീ
ഩാവ***
ഩാശ
ഩാസിക
ഩിഗമ
ഩികട
ഩികര
ഩികാമ
ഩികായ
ഩിഖില
ഩികുഞ്‌ജ
ഩിഘൂഩ
ഩികേത
ഩിഗ്‌രഹ
ഩിഗൃഹ
ഩികൃന്‌ത
ഩിഗ്‌രന്‌ത
ഩിക്ഷിപ
ഩിക്ഷേപ
ഩിഘ്‌ഩ
ഩിജ
ഩിദര്‌ശ
ഩിതമ്‌ബ
ഩിതര
ഩിദാഘ
ഩിദാഩ
ഩിതാന്‌ത
ഩിധാഩ
ഩിധായ
ഩിധ
ഩിധേഹി
ഩിദ്‌ര
ഩിത്‌യ
ഩിന്‌ദാ
ഩിബദ്‌ധ
ഩിബധ്‌
ഩിബന്‌ധഩ
ഩിപട
ഩിപതിത
ഩിപത്‌യ
ഩിപപാത
ഩിപാതിത
ഩിപാത്‌യ
ഩിപുണ
ഩിബോധ
ഩിഭൃത
ഩിമഗ്‌ഩ
ഩിമിത്‌ത
ഩിമിഷ
ഩിയത
ഩിയന്‌ത
ഩിയന്‌ത്‌ര
ഩിയമ
ഩിയുക്‌ത
ഩിയുജ്‌യ
ഩിയോ
ഩിര
ഩിര്‌
ഩിലയ
ഩിവര്‌
ഩിവസ
ഩിവാര
ഩിവാസ
ഩിവിഷ്‌ട
ഩിവേദ
ഩിവേശ
ഩിവൃ
ഩിശ
ഩിശ്‌
ഩിഷ
ഩിഷ്‌
ഩിസ
ഩിസ്‌
ഩിഹിത
ഩിഃശ
ഩിഃഷ
ഩിഃസ
ഩീച
ഩീതി
ഩീര
ഩീല
ഩൂതഩ
ഩൂപുര
ഩേത്‌ര
ഩേയ**
ഩൈമിത്‌ത
ഩൈമിഷ
ഩൈരാശ്‌യ
ഩൈരൃത
ഩൈവേദ്‌യ
ഩൈഷ്‌
ഩ്‌യായ
ഩ്‌യാസ
ഩ്‌യൂഩ
ഩൃ'''.split('\n')

    vir = Tamil.ViramaMap[0]

    for wordNna in listDentalNa:
        wordNa = re.sub('^ഩ', 'ന', wordNna)
        if '²' in wordNna[-1] or '³' in wordNna[-1] or '⁴' in wordNna[-1]:
            number = wordNna[-1]

            wordNnaN = wordNna[:-1]
            wordNaN = wordNa[:-1]
            for vow in GM.CrunchSymbols(GM.VowelSigns, 'Tamil'):
                Strng = Strng.replace(wordNnaN + vow + number, wordNaN + vow + number)

        Strng = Strng.replace(wordNna, wordNa)

        for wordNna in ['ഩാമ','ഩര']:
            wordNa = re.sub('^ഩ', 'ന', wordNna)
            Strng = Strng.replace(wordNa + vir, wordNna + vir)

        Strng = Strng.replace('ഩ്‌ന', 'ന്‌ന')

    return Strng

def TamilExtendedNNA(Strng):

    """Contextually converts dental na to nna per Tamil spelling rules, then fixes known exceptions via the hardcoded word list (ഗജാനനന്‌ → ഗജാഩഩഩ്‌)."""
    from .. import PostProcess
    na = TamilExtended.ConsonantMap[19]
    nna = TamilExtended.SouthConsonantMap[3]
    vir = TamilExtended.ViramaMap[0]
    ta = TamilExtended.ConsonantMap[15]

    ListV = '|'.join(GM.CrunchSymbols(GM.Vowels+GM.VowelSigns+GM.Consonants,'TamilExtended')+[TamilExtended.SignMap[0]])

    Strng = re.sub('('+ListV+')'+ GM.VedicSvaras + '('+na+')' + '(?!' + vir + ')',r'\1\2'+nna,Strng)
    Strng = re.sub('('+ListV+')'+ GM.VedicSvaras + '('+na+')' + '(?!' + vir + ')',r'\1\2'+nna,Strng)

    Strng = re.sub('(ന്‌)(?![തഥദധ])', 'ഩ്‌', Strng)

    Strng = re.sub('(\s)ഩ്', r'\1' + 'ന്‌', Strng)
    Strng = re.sub('^ഩ്', r'' + 'ന്‌', Strng)

    Strng = TamilpredictDentaNaExtended(Strng)

    return Strng

def TamilExtendedAnusvara(Strng):

    """Converts anusvara to homorganic nasal consonants and word-final anusvara to a plain म് to avoid anusvara spelling (സംഘം → സങ്‌ഘമ്)."""
    from .. import PostProcess
    Strng = PostProcess.AnusvaraToNasal(Strng, 'TamilExtended')
    Strng = Strng.replace('\u0D02', 'മ്‌')

    return Strng
