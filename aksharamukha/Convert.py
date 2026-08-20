# -*- coding: utf-8 -*-

from . import GeneralMap as GM, PreProcess as PrP, ConvertFix as CF
from . import PostProcess as PP
from . import ScriptRegistry as SR
import aksharamukha.FallBack as FB
import string
import re
from functools import cmp_to_key
import json
from . import gimeltra

### Mapping : https://viss.wordpress.com/2015/05/17/how-to-transcribe-pa%E1%B8%B7i-in-lanna-and-burmese/ ###
### Assmae kva -> becomes kba ## Check Assamese Wikipedia
### ITRANS features like comments implement
### Check Aksharamukha Todo list... and cross check and implement that
### Add HK-Itrans Option of Vishvas Vasuki
### Remove Diacritics
### Add space before punctiations and then remove it

# Sort Functions

def TamilSort(x,y):
    if('\u0B83' in x[0] and len(x[0]) != 1):
        return -1
    elif(x[0] < y[0]):
        return 1
    else:
        return 0

def lenSort(x,y):
    if(len(x[0]) > len(y[0])):
        return -1
    else:
        return 0

def convertInter(Strng,Source):
    ScriptAll = GM.Vowels+GM.Consonants+GM.CombiningSigns+GM.Numerals+GM.Signs+GM.Aytham
    SourceScript = GM.CrunchSymbols(ScriptAll,Source)
    TargetScript = GM.CrunchSymbols(ScriptAll,GM.Inter)
    ScriptMapAll = sorted(zip(SourceScript,TargetScript),key=cmp_to_key(lenSort))

    for x,y in ScriptMapAll:
        Strng = Strng.replace(x,y)

    #print(Strng)

    return Strng

def _build_char_pairs(Source, Target, source_transform=None, target_transform=None):
    # Shared by every convertScript branch that maps characters
    # group-by-group via GM.ScriptAll, sorted longest-first so multi-
    # character sequences replace before any of their own prefixes/
    # suffixes. source_transform/target_transform, if given, receive
    # (charList, crunched_list) and return a replacement list - used for
    # the DepV/Schwa disambiguation markers some branches need on one
    # side or the other (e.g. Latin->Indic prefixes DepV onto VowelSigns
    # on the Source side; Indic->Latin suffixes Schwa onto Consonants and
    # prefixes DepV onto Vowels on the Target side). Branches with no
    # such need (e.g. Indic->Indic) just omit the transform.
    charPairs = []
    for charList in GM.ScriptAll:
        SourceScript = GM.CrunchSymbols(GM.retCharList(charList), Source)
        TargetScript = GM.CrunchSymbols(GM.retCharList(charList), Target)
        if source_transform:
            SourceScript = source_transform(charList, SourceScript)
        if target_transform:
            TargetScript = target_transform(charList, TargetScript)
        ScriptMap = list(zip(SourceScript, TargetScript))
        ScriptMap.sort(reverse=True)
        charPairs += ScriptMap
    return sorted(charPairs, key=cmp_to_key(lenSort))

def _om_boundary_class(Source):
    # The punctuation/whitespace boundary class used to detect a standalone
    # Om symbol before swapping it for the Target script's own Om - shared
    # verbatim by the two branches that build it (Latin->Indic, Indic->
    # Indic). What each branch then DOES with it differs for real reasons
    # (single vs double regex pass, a len(sOm)==1 guard, or no regex pass
    # at all for Indic->Latin) - only this construction is genuinely
    # identical, so only this part is shared.
    return '(' + '|'.join(["\u005C"+x for x in list(string.punctuation)]+ ['\s']
    + [x.replace('.', '\.') for x in GM.CrunchSymbols(GM.Signs,Source)[1:3]]) + ')'

# Conversion Module
def convertScript(Strng,Source,Target,ctx=None):
    if SR.get(Source).is_latin and SR.get(Target).is_indic:
        Strng = _convert_latin_to_indic(Strng, Source, Target, ctx)
    elif SR.get(Source).is_latin and SR.get(Target).is_latin:
        Strng = _convert_latin_to_latin(Strng, Source, Target, ctx)
    elif SR.get(Source).is_indic and SR.get(Target).is_indic:
        Strng = _convert_indic_to_indic(Strng, Source, Target, ctx)
    elif SR.get(Source).is_indic and SR.get(Target).is_latin:
        Strng = _convert_indic_to_latin(Strng, Source, Target, ctx)
    elif SR.get(Source).is_semitic and SR.get(Target).is_semitic:
        Strng = _convert_semitic_to_semitic(Strng, Source, Target, ctx)
    elif (SR.get(Source).is_indic or SR.get(Source).is_latin) and SR.get(Target).is_semitic:
        Strng = _convert_to_semitic(Strng, Source, Target, ctx)
    elif SR.get(Source).is_semitic and (SR.get(Target).is_indic or SR.get(Target).is_latin):
        Strng = _convert_semitic_to_other(Strng, Source, Target, ctx)

    #print(Strng)

    Strng = PP._convertCleanup(Strng)

    return Strng

def _convert_latin_to_indic(Strng, Source, Target, ctx):
    DepV = '\u1E7F'
    Strng = GM.resolve(CF,"Fix"+Source.replace('-','_'),Strng,reverse=True,optional=True,ctx=ctx)

   #short u
    if Source in ['IAST', 'ISO', 'ISOPali', 'Titus']:
        Strng = Strng.replace('ŭ', 'u\u00D7') # special explicit Virama

    ## Joiners {} : ZWNJ : () : ZWJ
    Strng = Strng.replace("{}", "\u200C")
    Strng = Strng.replace("()", "\u200D")

    Strng = CF.VedicSvarasLatinIndic(Strng, Source)

    punc = _om_boundary_class(Source)

    sOm, tOm = GM.CrunchList('OmMap', Source)[0],GM.CrunchList('OmMap', Target)[0]

    Strng = re.sub(punc + sOm + punc, r'\1' + tOm + r'\2', Strng)
    Strng = re.sub('^' + sOm + punc, tOm + r'\1', Strng)
    Strng = re.sub(punc + sOm + '$', r'\1' + tOm, Strng)
    Strng = re.sub('^' + sOm + '$', tOm, Strng)

    punc = '(\s)'

    Strng = re.sub(punc + sOm + punc, r'\1' + tOm + r'\2', Strng)
    Strng = re.sub('^' + sOm + punc, tOm + r'\1', Strng)
    Strng = re.sub(punc + sOm + '$', r'\1' + tOm, Strng)
    Strng = re.sub('^' + sOm + '$', tOm, Strng)


    Strng = convertInter(Strng,Source)
    Source = GM.Inter
    Strng = PrP.RomanPreFix(Strng,Source)

    #print(Strng)
    ## HK l_R l_RR

    Strng = Strng.replace("ṿ×_","ṿ")
    Strng = Strng.replace("ṿ×_","ṿ")

    ha = GM.CrunchSymbols(GM.Consonants,Source)[32]

    # Add DepVSign to all VowelSigns on the Source side, to differentiate
    # from Independent Vowels.
    def _source_add_depv(charList, crunched):
        if charList == 'VowelSigns':
            return [DepV+x for x in crunched]
        return crunched

    charPairs = _build_char_pairs(Source, Target, source_transform=_source_add_depv)

    # Perform replacement sequentially for each character group
    for x,y in charPairs:
        #print(x, '-->', y)
        Strng = Strng.replace(x,y)
        #print(Strng)

    ## a_i => a<dev>i<dev> ; a_u = a<dev>u<dev>
    Strng=Strng.replace('_' + GM.CrunchSymbols(GM.Vowels,Target)[2],  GM.CrunchSymbols(GM.Vowels,Target)[2])
    Strng=Strng.replace('_' + GM.CrunchSymbols(GM.Vowels,Target)[4],  GM.CrunchSymbols(GM.Vowels,Target)[4])

    ## Joiners Vir + ZWJ
    vir = GM.CrunchList('ViramaMap', Target)[0]
    Strng = Strng.replace(vir + "[]", "\u200D" + vir)

    if Source in ['Inter']:
        Strng = Strng.replace('\u00D7', vir) # special explicit Virama

    #print Strng

    #print(Strng)

    # Apply Fixes on the Output based on the Script
    Strng = CF.FixIndicOutput(Strng, Source, Target, ctx=ctx)

    #print(Strng)

    return Strng

def _convert_latin_to_latin(Strng, Source, Target, ctx):
    Strng = GM.resolve(CF,"Fix"+Source.replace('-','_'),Strng,reverse=True,optional=True,ctx=ctx)

    ScriptAll = GM.Vowels+GM.Consonants+GM.CombiningSigns+GM.Numerals+GM.Signs+GM.Aytham

    Strng = convertInter(Strng,Source)

    SourceScript = GM.CrunchSymbols(ScriptAll,GM.Inter)
    TargetScript = GM.CrunchSymbols(ScriptAll, Target)
    ScriptMapAll = list(zip(SourceScript,TargetScript))

    for x,y in ScriptMapAll:
        Strng = Strng.replace(x,y)

    Strng = CF.PostFixRomanOutput(Strng,Source,Target)

    return Strng

def _convert_indic_to_indic(Strng, Source, Target, ctx):
    Strng = PrP.RemoveJoiners(Strng)

    Strng = CF.ShiftDiacritics(Strng,Source,reverse=True)
    Strng = GM.resolve(CF,"Fix"+Source.replace('-','_'),Strng,reverse=True,optional=True,ctx=ctx)

    punc = _om_boundary_class(Source)

    sOm, tOm = GM.CrunchList('OmMap', Source)[0],GM.CrunchList('OmMap', Target)[0]

    if len(sOm) != 1:
        Strng = re.sub(punc + sOm + punc, r'\1' + tOm + r'\2', Strng)
        Strng = re.sub('^' + sOm + punc, tOm + r'\1', Strng)
        Strng = re.sub(punc + sOm + '$', r'\1' + tOm, Strng)
        Strng = re.sub('^' + sOm + '$', tOm, Strng)

    if len(sOm) == 1:
        Strng = Strng.replace(sOm, tOm)

    charPairs = _build_char_pairs(Source, Target)

    #print(Strng)

    # Perform replacement sequentially for each character group
    for x,y in charPairs:
        # print(x,y)
        Strng = Strng.replace(x,y)
        # print(Strng)

    # print(Strng)

    #Strng = Strng.replace(GM.CrunchList('OmMap', Source)[0],GM.CrunchList('OmMap', Target)[0])
    # Apply Fixes on the Output based on the Script

    Strng = CF.FixIndicOutput(Strng, Source, Target, ctx=ctx)

    return Strng

def _convert_indic_to_latin(Strng, Source, Target, ctx):
    Schwa = '\uF000'
    DepV = '\u1E7F'
    #print(Strng)
    Strng = PrP.RemoveJoiners(Strng)
    Strng = CF.ShiftDiacritics(Strng, Source, reverse=True)
    #print(Strng)
    Strng = GM.resolve(CF,"Fix"+Source.replace('-','_'),Strng,reverse=True,optional=True,ctx=ctx)
    #print(Strng)
    sOm, tOm = GM.CrunchList('OmMap', Source)[0],GM.CrunchList('OmMap', Target)[0]

    Strng = Strng.replace(sOm, tOm)

    def _target_add_schwa_depv(charList, crunched):
        if charList == 'Consonants':
            # Add Schwa to all Roman consonants. Basically, the Roman script is "Indianized"
            return [x+Schwa for x in crunched]
        elif charList == 'Vowels':
            # Add DepVSign to all Independent vowel to differentiate from vowel sign.
            return [DepV+x for x in crunched]
        return crunched

    charPairs = _build_char_pairs(Source, Target, target_transform=_target_add_schwa_depv)

    # special case just for roman semitic
    if Source == 'RomanSemitic':
        unasp = ['k', 'g', 'c', 'j', 't', 'd', 'p', 'b', 'ɽ', 'ʈ', 'ɖ', 'r']
        charPairsH = [(x, y) for x, y in charPairs if 'ʰ' in x]
        charPairsNotH = [(x, y) for x, y in charPairs if 'ʰ' not in x]
        charPairs = charPairsNotH + charPairsH
        for x, y in charPairs:
            if x in unasp:
                Strng = re.sub(x + '(?!(ʰ|\u0324))', y, Strng)
            else:
                Strng = Strng.replace(x,y)
    # for all other transformations
    else:
        # Perform replacement sequentially for each character group
        #print(Strng)
        for x,y in charPairs:
            Strng = Strng.replace(x,y)


    # Remove all intermediate characters and fix Output
    Strng = CF.FixRomanOutput(Strng,Target)

    Strng = CF.VedicSvarsIndicLatin(Strng)

    Strng = CF.PostFixRomanOutput(Strng,Source,Target)

    # Convert Syllabic lR -> l_R Important !!!

    return Strng

def _convert_semitic_to_semitic(Strng, Source, Target, ctx):
    Strng = GM.resolve(CF,"Fix"+Source.replace('-','_'),Strng,Source,reverse=True,optional=True,ctx=ctx)

    tr = gimeltra.Transliterator()

    if Source == 'Ugar':
        Strng = Strng.replace('𐎟', ' ') # reverse ugaritic word separator

    #print(Strng)
    Strng = tr.tr(Strng, sc=Source, to_sc=Target)
    #print(Strng)

    # Apply Fixes on the Output based on the Script
    Strng = CF.FixSemiticOutput(Strng, Source, Target)

    return Strng

def _convert_to_semitic(Strng, Source, Target, ctx):
    tr = gimeltra.Transliterator()

    # deliberately no ctx=ctx - this is a separate sub-conversion
    # hop (through the RomanSemitic pivot), not a continuation of
    # this one; matches how recursive transliterate.convert() calls
    # get a fresh context too, not the parent's.
    Strng = convertScript(Strng, Source, "RomanSemitic")

    # print("The string is", Strng)

    #print(Strng)

    Strng = Strng.replace('QQ', '').replace('mQ', '') ## avoiding Q, mQ for Urdu to Semitic : Check why

    # remove gemination for every script except......
    ## Add all scripts with gemination sign here or vowel killer here
    ## Syriac doesn't show gemination hence not added below
    if 'Arab' not in Target and 'Hebr' not in Target and 'Latn' not in Target:
        Strng = re.sub('(.)' + '\u033D' + r'\1', r'\1', Strng)

    Strng = PP.FixSemiticRoman(Strng, Target)

    # for vocalized scripts
    # insert explicit 'a'
    # RomanSemitic is mapped as an Indic script : So no explicit a is added
    # hence /a/ is added explicitly
    if 'Arab' in Target or Target in ['Hebr', 'Syre', 'Syrj', 'Syrn', 'Thaa']:
        Strng = PP.insertARomanSemitic(Strng)

    # remove Virama
    # Strng = Strng.replace('×', '')

    Strng = tr.tr(Strng, sc='Latn', to_sc=Target)

    # Apply Fixes on the Output based on the Script
    Strng = CF.FixSemiticOutput(Strng, Source, Target)

    return Strng

def _convert_semitic_to_other(Strng, Source, Target, ctx):
    Strng = GM.resolve(CF,"Fix"+Source.replace('-','_'),Strng,Source,reverse=True,optional=True,ctx=ctx)

    tr = gimeltra.Transliterator()

    Strng = tr.tr(Strng, sc=Source, to_sc='Latn')
    #print(Strng)
    Strng = CF.FixSemiticOutput(Strng, Source, Target) ## generic fixes
    #print(Strng)
    Strng = PrP.FixSemiticRoman(Strng, Source) ## Specific fixes
    #print(Strng)

    # deliberately no ctx=ctx - this is a separate sub-conversion
    # hop (through the RomanSemitic pivot), not a continuation of
    # this one; matches how recursive transliterate.convert() calls
    # get a fresh context too, not the parent's.
    Strng = convertScript(Strng, 'RomanSemitic', Target)

    if Source == 'Ugar':
        Strng = Strng.replace('𐎟', ' ') # reverse ugaritic word separator

    return Strng

