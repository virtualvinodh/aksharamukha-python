# -*- coding: utf-8 -*-

# Marchen's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def _FixMarchenEncode(Strng):
    subjoinCons = '𑱲 𑱳 𑱴 𑱵 𑱶 𑱷 𑱸 𑱹 𑱺 𑱻 𑱼 𑱽 𑱾 𑱿 𑲀 𑲁 𑲂 𑲃 𑲄 𑲅 𑲆 𑲇 𑲉 𑲊 𑲋 𑲌 𑲍 𑲎'.split(' ')
    subjoined = '𑲒 𑲓 𑲔 𑲕 𑲖 𑲗 𑲘 𑲙 𑲚 𑲛 𑲜 𑲝 𑲞 𑲟 𑲠 𑲡 𑲢 𑲣 𑲤 𑲥 𑲦 𑲧 𑲩 𑲪 𑲫 𑲬 𑲭 𑲮'.split(' ')

    for x, y in zip(subjoinCons, subjoined):
        Strng = Strng.replace('ʾ' + x, y)

    Strng = Strng.replace('ʾ', '')
    Strng = Strng.replace('\u02BF', '')


    return Strng

def _FixMarchenDecode(Strng):
    subjoinCons = '𑱲 𑱳 𑱴 𑱵 𑱶 𑱷 𑱸 𑱹 𑱺 𑱻 𑱼 𑱽 𑱾 𑱿 𑲀 𑲁 𑲂 𑲃 𑲄 𑲅 𑲆 𑲇 𑲉 𑲊 𑲋 𑲌 𑲍 𑲎'.split(' ')
    subjoined = '𑲒 𑲓 𑲔 𑲕 𑲖 𑲗 𑲘 𑲙 𑲚 𑲛 𑲜 𑲝 𑲞 𑲟 𑲠 𑲡 𑲢 𑲣 𑲤 𑲥 𑲦 𑲧 𑲩 𑲪 𑲫 𑲬 𑲭 𑲮'.split(' ')

    tsaSeries = ['\U00011C82', '\U00011C83', '\U00011C84']
    jaSereis =  ['\U00011C76', '\U00011C77', '\U00011C78']

    for x, y in zip(tsaSeries, jaSereis):
        Strng = Strng.replace(y, x)

    for x, y in zip(subjoinCons, subjoined):
        Strng = Strng.replace(y, 'ʾ' + x)

    return Strng

def FixMarchen(Strng, reverse=False):
    return _FixMarchenDecode(Strng) if reverse else _FixMarchenEncode(Strng)

def MarchenSanskritPalatals(Strng):
    tsaSeries = ['\U00011C82', '\U00011C83', '\U00011C84']
    jaSereis =  ['\U00011C76', '\U00011C77', '\U00011C78']

    for x, y in zip(tsaSeries, jaSereis):
        Strng = Strng.replace(x, y)

    return Strng
