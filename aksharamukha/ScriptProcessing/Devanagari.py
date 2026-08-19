# -*- coding: utf-8 -*-

# Devanagari's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
#
# _FixDevanagariDecode's call to DevanagariPrishtamatra and
# ShowSchwaHindi's call to RemoveSchwaHindi both de-qualify to bare calls
# now that their targets are co-located here too.
#
# DevanagariAnusvara's call to NasalToAnusvara stays qualified -
# NasalToAnusvara is a genuinely shared/generic helper that remains in
# PostProcess.py.

import re
from .. import GeneralMap as GM

def _FixDevanagariDecode(Strng):
    """Strips the schwa accent, reverses Prishthamatra vowel-sign spelling, and decodes ॽ, ॹ, and Sindhi implosive letters to their approximate spellings."""
    Sindhi = ['ॻ','ॼ','ॾ','ॿ']
    SindhiApprox = ['ˍग','ˍज','ˍड','ˍब']
    # remove schwa accent
    Strng = Strng.replace('\u0954', '')

    Strng = DevanagariPrishtamatra(Strng, reverse=True)
    Strng = Strng.replace('ॽ', 'ʔ')
    Strng = Strng.replace('ॹ', 'ज़़')

    for x, y in zip(Sindhi, SindhiApprox):
        Strng = Strng.replace(x, y)

    # Kashmiri ux, uux
    #Strng = Strng.replace('ॶ', 'उʼ').replace('ॷ', 'ऊʼ').replace('ॖ', 'ुʼ').replace('ॗ', 'ूʼ')

    # oe
    #Strng = Strng.replace('ॳ', 'अʼ').replace('ॴ', 'आʼ').replace('\u093B', '\u093Eʼ').replace('\u093A','ʼ')


    return Strng

def _FixDevanagariEncode(Strng):
    """Maps ʔ and Sindhi implosive letters to Devanagari equivalents, blocks RRA from forming conjuncts (except before ya/ha), and encodes apostrophe-marked Kashmiri oe/ooe vowels."""
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

def FixDevanagari(Strng, reverse=False):
    """Dispatches to the Devanagari encode or decode fix routine depending on conversion direction."""
    return _FixDevanagariDecode(Strng) if reverse else _FixDevanagariEncode(Strng)

def AnuChandraEqDeva(Strng):

    """Treats anusvara and chandrabindu as equivalent by converting chandrabindu to anusvara in Devanagari."""
    return AnuChandraEq(Strng, 'Devanagari')

def AnuChandraEq(Strng, script):
    """Converts the chandrabindu to the anusvara for the given script, treating the two as equivalent."""
    Chandrabindu = GM.CrunchList('AyogavahaMap', script)[0]
    Anusvara = GM.CrunchList('AyogavahaMap', script)[1]

    Strng = Strng.replace(Chandrabindu, Anusvara)

    return Strng

def RemoveSchwaHindi(Strng, showschwa=False):
    """Applies Hindi schwa-deletion rules, dropping the inherent vowel from word-medial and word-final consonants (राम → rām, सबसे → sabse)."""
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

def ShowSchwaHindi(Strng):
    """Marks deleted Hindi schwas with a visible accent instead of silently removing them (rāma → राम॔, viracita → विर॔॔चित॔)."""
    Strng = RemoveSchwaHindi(Strng, True)
    return Strng

def devanagariuttara(Strng):

    """Selects the Uttara Devanagari letterform style (rendering-style marker; does not alter the text)."""
    return Strng

def devanagarinepali(Strng):

    """Selects the Nepali Devanagari letterform style (rendering-style marker; does not alter the text)."""
    return Strng

def devanagaribalbodh(Strng):

    """Selects the Balbodh Devanagari letterform style (rendering-style marker; does not alter the text)."""
    return Strng

def devanagarijain(Strng):

    """Selects the Jain Devanagari letterform style (rendering-style marker; does not alter the text)."""
    return Strng

def DevanagariAnusvara(Strng):
    """Converts nasal consonants to anusvara for nasalization (पञ्चगङ्गा → पंचगंगा)."""
    from .. import PostProcess

    return PostProcess.NasalToAnusvara(Strng, 'Devanagari')

def jainomDevangari(Strng):
    """Replaces the standard OM sign with the Jain OM character (ॐ → ꣽ)."""
    Strng = Strng.replace('ॐ', 'ꣽ')

    return Strng

def DevanagariACandra(Strng):
    """Replaces the candra E vowel letter with the short A-candra letter (ऍ → ॲ)."""
    Strng = Strng.replace('ऍ', 'ॲ')

    return Strng

def DevanagariPrishtamatra(Strng, reverse = False):
    """Converts between standard and Prishthamatra (right-side matra) vowel-sign orthography (के कै को कौ ↔ कॎ कॎे कॎा कॎो)."""
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
