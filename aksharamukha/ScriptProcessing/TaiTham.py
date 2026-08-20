# -*- coding: utf-8 -*-

# TaiTham's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.EastIndic import TaiTham

# ---- Fix (encode/decode conversion logic) ----

# internal
def _FixTaiThamEncode(Strng):

    """Applies Tai Tham-specific subjoining of ra/la, the mai kang lai and great-sa ligatures, tall-A vowel forms, and conjunct reordering when encoding."""
    from .. import PostProcess
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

# internal
def _FixTaiThamDecode(Strng):

    """Reverses Tai Tham subjoining, ligature, and tall-A vowel fixes back to standard consonant-plus-virama sequences when decoding."""
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

# internal
def FixTaiTham(Strng,reverse=False):

    """Dispatches to the Tai Tham encode or decode fix-up routine based on the reverse flag."""
    return _FixTaiThamDecode(Strng) if reverse else _FixTaiThamEncode(Strng)

# ---- Post-processing options ----

# unreferenced
def TaiThamHighNga(Strng):
    """Replaces the low-register Tai Tham nga consonant with its high-register variant."""
    Strng = Strng.replace('\u1A58','\u1A59')

    return Strng

# unreferenced
def TaiThamMoveNnga(Strng):
    """Repositions the Tai Tham high-register nga sign to follow the character it attaches to."""
    Strng = re.sub('(.)(\u1A58)',r'\2\1',Strng) # Probably its u1A59

    return Strng

# unreferenced
def TaiThamO(Strng):
    """Merges the Tai Tham e-vowel-sign + aa-vowel-sign sequence into the single dedicated o vowel sign."""
    Strng = Strng.replace("\u1A6E\u1A63","\u1A70")

    return Strng

