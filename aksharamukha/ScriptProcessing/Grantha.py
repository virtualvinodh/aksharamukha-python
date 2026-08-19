# -*- coding: utf-8 -*-

# Grantha's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
#
# egrantamil is independently defined in both PreProcess.py and
# PostProcess.py, but both are truly identical no-op stubs (`return
# Strng` - no calls at all), unlike this session's other pre/post
# collisions. No bare-call-resolution risk (see Balinese.py/Javanese.py
# for where that risk IS real), so defined once here and re-exported
# unsuffixed to both modules.
#
# InsertGeminationSign/ReverseGeminationSign stay shared (also used by
# Malayalam and Gurmukhi), called via PostProcess. as before.

import re
import functools

def FixGrantha(Strng, reverse=False):
    return _FixGranthaDecode(Strng) if reverse else _FixGranthaEncode(Strng)

def _FixGranthaEncode(Strng):
    Strng = Strng.replace('॑', '᳴')
    Strng = Strng.replace('᳚', '॑')
    Strng = Strng.replace('ꣳ', '𑍞')
    Strng = Strng.replace('ꣴ', '𑍟')
    Strng = Strng.replace('𑌼𑍍', '𑌼𑍍\u200C')

    return Strng

def _FixGranthaDecode(Strng):
    Strng = Strng.replace('𑌼𑍍\u200C', '𑌼𑍍')
    Strng = Strng.replace('॑', '᳚')
    Strng = Strng.replace('᳴', '॑')
    Strng = Strng.replace('𑍞', 'ꣳ')
    Strng = Strng.replace('𑍟', 'ꣴ')

    return Strng

def GranthaOldau(Strng):
    Strng = Strng.replace('𑍗', '𑍌')

    return Strng

def GranthaPrakrit(Strng):
    from .. import PostProcess
    ## Replace Anusvara with Anusvara above
    Strng = Strng.replace("𑌂", "𑌀")
    Strng = PostProcess.InsertGeminationSign(Strng, 'Grantha')

    ## not at the beginning of words
    pat = r'\s𑌂.'
    Strng = functools.reduce(lambda s, m: s.replace(m, PostProcess.ReverseGeminationSign(m, 'Grantha')), re.findall(pat, Strng), Strng)

    pat = r'𑍍𑌂.'
    Strng = functools.reduce(lambda s, m: s.replace(m, PostProcess.ReverseGeminationSign(m, 'Grantha')), re.findall(pat, Strng), Strng)

    return Strng

def granthafinal(Strng):

    return Strng

def granthaserif(Strng):
    return Strng

def egrantamil(Strng):
    return Strng
