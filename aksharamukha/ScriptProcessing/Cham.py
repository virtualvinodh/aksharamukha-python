# -*- coding: utf-8 -*-

# Cham's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.EastIndic import Cham

# ---- Fix (encode/decode conversion logic) ----

def _FixChamEncode(Strng):
    """Forms Cham subjoined consonant ligatures (ya/ra/la/va), converts consonants to word-final forms before virama, and builds final-h (ꩍ) forms."""
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
    """Reverses Cham subjoined consonant ligatures and final-h forms when decoding; the non-final-to-final consonant merge is not reversible."""
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
    """Dispatches to the Cham encode or decode fix-up routine based on the reverse flag."""
    return _FixChamDecode(Strng) if reverse else _FixChamEncode(Strng)
