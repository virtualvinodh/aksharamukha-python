# -*- coding: utf-8 -*-

# LaoPali's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
#
# LaoPhonetic/LaoTranscription each independently define the SAME option
# name in both PreProcess.py and PostProcess.py as different functions -
# suffixed _pre/_post here. LaoPhonetic_post's own body bare-calls
# LaoTranscription(Strng), which must resolve to the POST-side sibling
# specifically (same trap as Balinese/Javanese's MoveRepha) - renamed
# that call site to LaoTranscription_post explicitly.
#
# LaoPaliTranscribe (a ConvertFix.py private helper) is exclusively used
# by LaoPali's own Fix functions and LaoSajjhayawithA - absorbed here,
# de-qualified to a bare call where it used to be CF.LaoPaliTranscribe.
# It itself had a pre-existing local `from . import PostProcess as pp`
# written for its old depth inside ConvertFix.py - fixed to `from ..`
# for its new depth here (same bug class as Lao.py's LaoTranscribe).
#
# ReverseVowelSigns/ThaiLaoTranscription/ThaiSajjhayaOrthography all stay
# shared (also used by Thai and/or Lao), called via CF./PostProcess. as
# before.

import re

# ---- Fix (encode/decode conversion logic) ----

# internal
def _FixLaoPaliEncode(Strng, ctx):
    """Encodes Lao Pali text: reverses vowel sign order, optionally applies phonetic transcription, and ligates AA+anusvara into the AM vowel sign."""
    from .. import ConvertFix as CF
    Strng = CF.ReverseVowelSigns(Strng,"LaoPali",False)

    transcription_mode = ctx.transcription_mode if ctx is not None else False
    if transcription_mode:
        Strng = LaoPaliTranscribe(Strng, True)

        Strng = Strng.replace("ຫ຺໌","ຫ໌")

    Strng = Strng.replace("\u0EB2\u0ECD","\u0EB3")

    return Strng

# internal
def _FixLaoPaliDecode(Strng, ctx):
    """Decodes Lao Pali text: restores vowel sign order, optionally applies phonetic transcription, and expands the AM vowel sign back into AA+anusvara."""
    from .. import ConvertFix as CF
    Strng = CF.ReverseVowelSigns(Strng,"LaoPali",True)

    transcription_mode = ctx.transcription_mode if ctx is not None else False
    if transcription_mode:
        Strng = LaoPaliTranscribe(Strng, True)

        Strng = Strng.replace("ຫ຺໌","ຫ໌")

    # VS AA + Anusvara <- VS AM (Ligature)
    Strng= Strng.replace("\u0EB3","\u0EB2\u0ECD")

    return Strng

# internal
def FixLaoPali(Strng,reverse=False,ctx=None):
    """Dispatches to the Lao Pali encode or decode fix routine depending on conversion direction."""
    return _FixLaoPaliDecode(Strng, ctx) if reverse else _FixLaoPaliEncode(Strng, ctx)

# internal
def LaoPaliTranscribe(Strng,reverse=False, anusvaraChange = True):
    """Converts between orthographic and colloquial Lao phonetic transcription using the short-a and conjunct short-a signs."""
    from .. import PostProcess as pp
    shortA, conjA = '\u0EB0', '\u0EB1'

    if not reverse:
        Strng = pp.ThaiLaoTranscription(Strng,"LaoPali",shortA,conjA, anusvaraChange = anusvaraChange)
    else:
        Strng = pp.ThaiLaoTranscription(Strng,"LaoPali",shortA, conjA,reverse=True)

    return Strng

# ---- Pre-processing options ----

# frontend
def LaoTranscription_pre(Strng):

    """Placeholder pre-processing step for Lao transcription mode; currently a no-op."""
    return Strng

# frontend
def LaoPhonetic_pre(Strng):
    """Applies Lao phonetic normalization before conversion: ດ→ທ, ບ→ພ, drops the nikkhahit off ງໍ, and strips a combining mark."""
    Strng = Strng.replace('ດ', 'ທ')
    Strng = Strng.replace('ບ', 'ພ')
    Strng = Strng.replace('ງໍ', 'ງ')

    Strng = Strng.replace('\u035C', '')

    return Strng

# frontend
def LaoSajhayaOrthography(Strng):
    """Renders Pali Sajjhāya orthography in Lao script by converting virama/tone marks to the subjoining sign - e.g. ພຸທ໌ຘ."""
    Strng = Strng.replace('ັງ', 'ັງ຺')

    Strng = re.sub('([ເໂໄ])(.๎)([ຍຣລວຨຩສຫຬ])', r'\2\1\3', Strng)

    Strng = Strng.replace('໌', '຺')
    Strng = Strng.replace('๎', '຺')
    Strng = Strng.replace('ັ', '')

    return Strng

# frontend
def LaoSajhayaOrthographywithA(Strng):
    """Renders nativized Lao Sajjhāya orthography by stripping the short-a sign before applying Sajjhāya formatting - e.g. ພຸທ໌ຘະ."""
    Strng = Strng.replace('ະ', '')
    Strng = LaoSajhayaOrthography(Strng)

    return Strng

# ---- Post-processing options ----

# frontend
def LaoTranscription_post(Strng):
    """Post-processing step that applies Lao Pali transcription and removes the short-a sign before a final virama-like mark."""
    Strng = LaoPaliTranscribe(Strng)

    Strng = Strng.replace('ະ໌', '໌')

    return Strng

# frontend
def LaoPhonetic_post(Strng):
    """Post-processes Lao phonetic text: reorders subjoined y/r/l/v/h consonants, reapplies transcription, and restores native consonant letters (ທ→ດ, ພ→ບ)."""
    Strng = re.sub('(\u0EBA)([ໂເໄ]?)([ຍຣລວຫ])', '\u035C'+ r'\2\3', Strng)
    Strng = re.sub('([ຍຣລວຫ])' + '\u035C' + '([ໂເໄ]?)' + r'\1', r'\1' + '\u0EBA' + r'\2\1', Strng)

    Strng = Strng.replace('ຫ\u0EBA', 'ຫ\u035C')

    Strng = re.sub('([ຍຣລວຫ])' + '\u035C' + r'\1', r'\1' + '\u0EBA' + r'\1', Strng)

    Strng = LaoTranscription_post(Strng)

    Strng = Strng.replace('\u0EB0\u035C', '\u035C')

    Strng = Strng.replace('ງ', 'ງໍ')

    #Strng = Strng.replace('ຄ', 'ກ')
    #Strng = Strng.replace('ຊ', 'ຈ')
    Strng = Strng.replace('ທ', 'ດ')
    Strng = Strng.replace('ພ', 'ບ')

    return Strng

# frontend
def LaoSajjhaya(Strng):
    """Converts Lao text to Pali Sajjhāya orthography and reorders vowel-consonant-tone clusters - ພຸທ຺ຘ → ພຸທ໌ຘ."""
    from .. import PostProcess
    Strng = PostProcess.ThaiSajjhayaOrthography(Strng, Script = "LaoPali")

    Strng = re.sub('([ເໂໄ])(.)(\u0ECE)', r'\2\3\1', Strng)

    return Strng

# frontend
def LaoSajjhayawithA(Strng):
    """Converts Lao text to nativized Sajjhāya orthography with the inherent vowel restored - ພຸທ຺ຘໍ → ພຸທ໌ຘັງ."""
    Strng = LaoSajjhaya(Strng)

    # The below logic is for Thai yamakkan. Use Thai Yamakkan not to break it
    Strng = Strng.replace('\u0ECE', '\u0E4E')

    Strng = Strng.replace('ັງ', 'ັງ຺')
    Strng = LaoPaliTranscribe(Strng, anusvaraChange = True)

    Strng = Strng.replace('ະໍ', 'ໍ')
    Strng = Strng.replace('ະັ', 'ັ')
    Strng = Strng.replace('ະ๎', '๎')

    Strng = Strng.replace('ະ໌', '໌')
    Strng = Strng.replace('ະົ', 'ົ')

    Strng = re.sub('([ເໂໄ])(.๎)([ຍຣລວຨຩສຫຬ])ະ', r'\1\2\3', Strng)

    Strng = Strng.replace('າໍ', 'ຳ')

    # Use Lao Yamakkan again
    Strng = Strng.replace('\u0E4E', '\u0ECE')

    return Strng
