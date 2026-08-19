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

def _FixLaoPaliEncode(Strng, ctx):
    from .. import ConvertFix as CF
    Strng = CF.ReverseVowelSigns(Strng,"LaoPali",False)

    transcription_mode = ctx.transcription_mode if ctx is not None else False
    if transcription_mode:
        Strng = LaoPaliTranscribe(Strng, True)

        Strng = Strng.replace("ຫ຺໌","ຫ໌")

    Strng = Strng.replace("\u0EB2\u0ECD","\u0EB3")

    return Strng

def _FixLaoPaliDecode(Strng, ctx):
    from .. import ConvertFix as CF
    Strng = CF.ReverseVowelSigns(Strng,"LaoPali",True)

    transcription_mode = ctx.transcription_mode if ctx is not None else False
    if transcription_mode:
        Strng = LaoPaliTranscribe(Strng, True)

        Strng = Strng.replace("ຫ຺໌","ຫ໌")

    # VS AA + Anusvara <- VS AM (Ligature)
    Strng= Strng.replace("\u0EB3","\u0EB2\u0ECD")

    return Strng

def FixLaoPali(Strng,reverse=False,ctx=None):
    return _FixLaoPaliDecode(Strng, ctx) if reverse else _FixLaoPaliEncode(Strng, ctx)

def LaoPaliTranscribe(Strng,reverse=False, anusvaraChange = True):
    from .. import PostProcess as pp
    shortA, conjA = '\u0EB0', '\u0EB1'

    if not reverse:
        Strng = pp.ThaiLaoTranscription(Strng,"LaoPali",shortA,conjA, anusvaraChange = anusvaraChange)
    else:
        Strng = pp.ThaiLaoTranscription(Strng,"LaoPali",shortA, conjA,reverse=True)

    return Strng

def LaoTranscription_pre(Strng):

    return Strng

def LaoPhonetic_pre(Strng):
    Strng = Strng.replace('ດ', 'ທ')
    Strng = Strng.replace('ບ', 'ພ')
    Strng = Strng.replace('ງໍ', 'ງ')

    Strng = Strng.replace('\u035C', '')

    return Strng

def LaoSajhayaOrthography(Strng):
    Strng = Strng.replace('ັງ', 'ັງ຺')

    Strng = re.sub('([ເໂໄ])(.๎)([ຍຣລວຨຩສຫຬ])', r'\2\1\3', Strng)

    Strng = Strng.replace('໌', '຺')
    Strng = Strng.replace('๎', '຺')
    Strng = Strng.replace('ັ', '')

    return Strng

def LaoSajhayaOrthographywithA(Strng):
    Strng = Strng.replace('ະ', '')
    Strng = LaoSajhayaOrthography(Strng)

    return Strng

def LaoTranscription_post(Strng):
    Strng = LaoPaliTranscribe(Strng)

    Strng = Strng.replace('ະ໌', '໌')

    return Strng

def LaoPhonetic_post(Strng):
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

def LaoSajjhaya(Strng):
    from .. import PostProcess
    Strng = PostProcess.ThaiSajjhayaOrthography(Strng, Script = "LaoPali")

    Strng = re.sub('([ເໂໄ])(.)(\u0ECE)', r'\2\3\1', Strng)

    return Strng

def LaoSajjhayawithA(Strng):
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
