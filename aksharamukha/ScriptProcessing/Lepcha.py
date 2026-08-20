# -*- coding: utf-8 -*-

# Lepcha's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.MainIndic import Lepcha

# ---- Fix (encode/decode conversion logic) ----

# internal
def _FixLepchaEncode(Strng):
    """Forms Lepcha subjoined consonant clusters, converts consonants to their word-final forms, and reorders the rang vowel sign around final consonants."""
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

# internal
def _FixLepchaDecode(Strng):
    """Reverses Lepcha subjoined consonant clusters and rang vowel-sign reordering; word-final consonant merging is not reversible."""
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

# internal
def FixLepcha(Strng,reverse=False):
    """Dispatches to the Lepcha encode or decode fix-up routine based on the reverse flag."""
    return _FixLepchaDecode(Strng) if reverse else _FixLepchaEncode(Strng)
