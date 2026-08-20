# -*- coding: utf-8 -*-

# Lao's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# ConvertFix/PreProcess/PostProcess are imported LOCALLY inside each
# function that needs them (not at module level) - required to avoid a
# load-order-dependent circular import, since these three modules
# re-export names from here. See ScriptProcessing/Tamil.py.

import re

# ---- Fix (encode/decode conversion logic) ----

# internal
def _FixLaoEncode(Strng):

    """Applies Lao encoding fixes: maps aspirate consonants marked with a pseudo-nukta to their unaspirated forms, reverses vowel-sign order, transcribes tone/vowel spelling, and merges AA+Anusvara into the AM ligature."""
    from .. import ConvertFix as CF

    Strng = Strng.replace("ທ\uEB0A", "ດ")
    Strng = Strng.replace("ປ\uEB0A", 'ບ')
    Strng = Strng.replace("ພ\uEB0A",'ຟ')

    Strng = re.sub("(?<!ດ)(?<!ບ)(?<!ຟ)\uEB0A", "", Strng)

    Strng = CF.ReverseVowelSigns(Strng,"Lao",False)
    Strng = LaoTranscribe(Strng,False)

    Strng = Strng.replace("\u0EB2\u0ECD","\u0EB3")

    # Remove the Pseduo Nukta
    Strng = Strng.replace("\uEB0A", "")


    return Strng

# internal
def _FixLaoDecode(Strng):

    """Reverses Lao encoding fixes: restores aspirate consonants from their unaspirated pseudo-nukta forms, restores vowel-sign order, reverses transcription, and splits the AM ligature back to AA+Anusvara."""
    from .. import ConvertFix as CF
    Strng = Strng.replace("ດ", "ທ\uEB0A")
    Strng = Strng.replace('ບ', "ປ\uEB0A")
    Strng = Strng.replace('ຟ', "ພ\uEB0A")
    Strng = Strng.replace('ັ','ະ')


    Strng = CF.ReverseVowelSigns(Strng,"Lao",True)
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

# internal
def FixLao(Strng,reverse=False):

    """Dispatches to the Lao encode or decode fix routine depending on the reverse flag."""
    return _FixLaoDecode(Strng) if reverse else _FixLaoEncode(Strng)

# internal
def LaoTranscribe(Strng,reverse=False):

    """Applies or reverses Lao short-a/conjunct-a transcription rules via the shared Thai/Lao transcription routine."""
    from .. import PostProcess as pp

    shortA, conjA = '\u0EB0', '\u0EB1'

    if not reverse:
        Strng = pp.ThaiLaoTranscription(Strng,"Lao",shortA,conjA)
    else:
        Strng = pp.ThaiLaoTranscription(Strng,"Lao",shortA, conjA,reverse=True)

    return Strng

# ---- Post-processing options ----

# frontend
def LaoNative(Strng):

    """Nativizes Lao spelling by simplifying doubled aspirate/sibilant consonant clusters: ພຸທທັງ ຄັຈຈາມິ ສັພພັງ → ພຸດທັງ ຄັຈສາມິ ສັບພັງ."""

    Strng = re.sub('ຕ([ເແໂໄ]?)ຕ', 'ດ' + r'\1' + 'ຕ', Strng)
    Strng = re.sub('ຕ([ເແໂໄ]?)ຖ', 'ດ' + r'\1' + 'ຖ', Strng)
    Strng = re.sub('ທ([ເແໂໄ]?)ທ', 'ດ' + r'\1' + 'ທ', Strng)
    Strng = re.sub('ສ([ເແໂໄ]?)ສ', 'ດ' + r'\1' + 'ສ', Strng)

    Strng = re.sub('ປ([ເແໂໄ]?)ປ', 'ບ' + r'\1' + 'ປ', Strng)
    Strng = re.sub('ພ([ເແໂໄ]?)ພ', 'ບ' + r'\1' + 'ພ', Strng)

    return Strng
