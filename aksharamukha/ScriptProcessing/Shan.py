# -*- coding: utf-8 -*-

# Shan's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def _FixShanEncode(Strng):
    Strng = Strng.replace('်ရ', 'ြ')
    Strng = Strng.replace('်ယ', 'ျ')
    Strng = Strng.replace('်ဝ', '\u1082')
    #Strng = Strng.replace('်ႁ', 'ှ')

    ## Maintain the order of the medials
    Strng = re.sub('(ှ)' + '([ျြွ])', r'\2\1', Strng)
    Strng = Strng.replace("\u103C\u103B", "\u103B\u103C")
    Strng = Strng.replace("\u103D\u103B", "\u103B\u103D")
    Strng = Strng.replace("ွ\u103C", "\u103Cွ")

    ## Fix Shya
    Strng = re.sub('သျ\u02BD?ျ', 'သျ်ယ', Strng)


    return Strng

def _FixShanDecode(Strng):
    ## Reverse the order of the medials
    Strng = re.sub('([ျြွ])' + '(ှ)', r'\2\1', Strng)
    Strng = Strng.replace("\u103B\u103C", "\u103C\u103B")
    Strng = Strng.replace("\u103B\u103D", "\u103D\u103B")
    Strng = Strng.replace("\u103Cွ", "ွ\u103C")

    Strng = Strng.replace('ြ', '်ရ')
    Strng = Strng.replace('ျ', '်ယ')
    Strng = Strng.replace('ွ', '်ဝ')
    Strng = Strng.replace('\u1082', '်ဝ')
    Strng = Strng.replace('ှ', '်ႁ')

    #for old shan in case it appears
    Strng = Strng.replace('\u1039', '\u103A')

    return Strng

def FixShan(Strng, reverse=False):
    return _FixShanDecode(Strng) if reverse else _FixShanEncode(Strng)

def segmentShanSyllables(Strng):
    # segment text into syllables

    # https://github.com/ye-kyaw-thu/myWord/blob/main/syl_segment.py
    myConsonant = r"ၵၶၷꧠငၸꧡꩡꧢၺꩦꩧꩨꩩꧣတထၻꩪၼပၽၿꧤမယရလဝသႁꩮၹၾႀဢ"
    otherChar = r"႞႟႐-႙၊။!-/:-@[-`{-~\s"
    ssSymbol = r'္'
    aThat = r'်'

    BreakPattern = re.compile(r"((?<!" + ssSymbol + r")["+ myConsonant + r"](?![" + aThat + ssSymbol + r"])" + r"|["  + otherChar + r"])", re.UNICODE)
    Strng = Strng.replace("့်", "့်")
    Strng = BreakPattern.sub(' ' + r"\1", Strng)

    return Strng
