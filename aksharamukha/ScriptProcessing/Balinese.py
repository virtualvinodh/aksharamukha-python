# -*- coding: utf-8 -*-

# Balinese's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
#
# BalineseMoveRepha's own source is textually IDENTICAL between
# PreProcess.py and PostProcess.py, but each calls a bare, unqualified
# BalineseJavaneseMoveRepha(...) - and THAT helper genuinely differs
# between the two modules (confirmed: near-inverse regex passes). Same
# identical wrapper text would silently resolve to different behavior
# depending on which shared helper ends up in scope, so this still needs
# the _pre/_post suffix treatment despite looking like a non-collision at
# a glance. AddRepha and BalineseJavaneseMoveRepha stay shared (also used
# by ScriptProcessing/Javanese.py), called via CF./PP./PostProcess. as
# before.

import re

def _FixBalineseEncode(Strng):
    from .. import ConvertFix as CF
    Repha = '\u1B03'

    Strng = CF.AddRepha(Strng,"Balinese",Repha,False)

    pass

    return Strng

def _FixBalineseDecode(Strng):
    from .. import ConvertFix as CF
    Repha = '\u1B03'

    Strng = CF.AddRepha(Strng,"Balinese",Repha,True)

    # reversing archaic jna
    Strng = Strng.replace('ᭌ', 'ᬚ᭄ᬜ')
    # Fix a-based vowels
    vowelsA = ['ᬅᬶ', 'ᬅᬷ', 'ᬅᬸ', 'ᬅᬹ', 'ᬅᬺ', 'ᬅᬻ', 'ᬅ᭄ᬮᭂ', 'ᬅ᭄ᬮᭃ', 'ᬅᬾ', 'ᬅᬿ', 'ᬅᭀ', 'ᬅᭁ']
    vowels = ['ᬇ', 'ᬈ', 'ᬉ', 'ᬊ', 'ᬋ', 'ᬌ', 'ᬍ', 'ᬎ', 'ᬏ', 'ᬐ', 'ᬑ', 'ᬒ']

    for v, vA in zip(vowels, vowelsA):
        Strng = Strng.replace(vA, v)

    return Strng

def FixBalinese(Strng,reverse=False):
    return _FixBalineseDecode(Strng) if reverse else _FixBalineseEncode(Strng)

def BalineseMoveRepha_pre(Strng):
    from .. import PreProcess as PP
    return PP.BalineseJavaneseMoveRepha(Strng, 'Balinese', 'ᬃ')

def BalineseArchaicJNA(Strng):
    Strng = Strng.replace('ᬚ᭄ᬜ', 'ᭌ')
    return Strng

def BalineseAvowels(Strng):
    vowelsA = ['ᬅᬶ', 'ᬅᬷ', 'ᬅᬸ', 'ᬅᬹ', 'ᬅᬺ', 'ᬅᬻ', 'ᬅ᭄ᬮᭂ', 'ᬅ᭄ᬮᭃ', 'ᬅᬾ', 'ᬅᬿ', 'ᬅᭀ', 'ᬅᭁ']
    vowels = ['ᬇ', 'ᬈ', 'ᬉ', 'ᬊ', 'ᬋ', 'ᬌ', 'ᬍ', 'ᬎ', 'ᬏ', 'ᬐ', 'ᬑ', 'ᬒ']

    for v, vA in zip(vowels, vowelsA):
        Strng = Strng.replace(v, vA)

    return Strng

def BalineseMoveRepha_post(Strng):
    from .. import PostProcess
    return PostProcess.BalineseJavaneseMoveRepha(Strng, 'Balinese', 'ᬃ')
