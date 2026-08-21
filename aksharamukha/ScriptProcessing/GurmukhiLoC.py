# -*- coding: utf-8 -*-

# GurmukhiLoC's Fix logic and LoC (Library of Congress) romanization
# logic. See ScriptProcessing/HOW_TO_ADD_LOC.md for the naming
# convention this follows and how to add a new script. Gurmukhi is one
# of the scripts with a genuinely different LoC character mapping
# (bindi<->tippi, etc.), hence the separate 'GurmukhiLoC' pivot.
# GurmukhiLoCToRomanLoc_post has no RomanLocTo-direction counterpart -
# not every script needs all four functions.
#
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.MainIndic import Gurmukhi

# ---- Fix (encode/decode conversion logic) ----

# internal
def _FixGurmukhiLoCEncode(Strng):

    """Corrects ru/lu vowel signs, collapses a doubled ava sign into parenthesized ā, inserts the gemination sign, retains Indic numerals, and expands addak+Vedic-svara sequences for LoC Gurmukhi encoding."""
    from .. import ConvertFix as CF

    from .. import PostProcess
    Strng = CF.CorrectRuLu(Strng,"Gurmukhi",False)

    ava = Gurmukhi.SignMap[0]
    avaA = '\u0028\u0A06\u0029'

    # Tippi/Bindu conversion options are optional. Look into PostProcess

    Strng = Strng.replace(ava+ava,avaA)
    Strng = PostProcess.InsertGeminationSign(Strng, 'Gurmukhi')
    Strng = PostProcess.RetainIndicNumerals(Strng, 'Gurmukhi', True)

    Vedicomp = '([' + ''.join(GM.VedicSvarasList) + '])'

    Strng = re.sub(Vedicomp + '\u0A71' + '(.)', r'\1' + r'\2' + Gurmukhi.ViramaMap[0] + r'\2' , Strng)


    return Strng

# internal
def _FixGurmukhiLoCDecode(Strng):

    """Reverses ru/lu correction, restores the doubled ava sign from parenthesized ā, retains Indic numerals, and reverses the gemination sign for LoC Gurmukhi decoding."""
    from .. import ConvertFix as CF

    from .. import PostProcess
    Strng = CF.CorrectRuLu(Strng,"Gurmukhi",True)

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

# internal
def FixGurmukhiLoC(Strng,reverse=False):

    """Dispatches to the Gurmukhi LoC encode or decode fix routine based on the reverse flag."""

    return _FixGurmukhiLoCDecode(Strng) if reverse else _FixGurmukhiLoCEncode(Strng)

# ---- Post-processing options ----

# internal
def GurmukhiLoCToRomanLoc_post(Strng):
    """Converts nasalized m before homorganic stops into the corresponding nasal consonant (velar/palatal/retroflex/dental/labial) for Gurmukhi LoC romanization."""
    Strng = re.sub('(m̆|ṃ)(k|g)', 'ṅ' + r'\2', Strng)
    Strng = re.sub('(m̆|ṃ)(c|j)', 'ñ' + r'\2', Strng)
    Strng = re.sub('(m̆|ṃ)(ṭ|ḍ)', 'ṇ' + r'\2', Strng)
    Strng = re.sub('(m̆|ṃ)(t|d)', 'n' + r'\2', Strng)
    Strng = re.sub('(m̆|ṃ)(p|b)', 'm' + r'\2', Strng)

    return Strng
