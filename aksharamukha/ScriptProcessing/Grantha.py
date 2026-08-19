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
    """Dispatches to the Grantha encode or decode fix-up routine based on the reverse flag."""
    return _FixGranthaDecode(Strng) if reverse else _FixGranthaEncode(Strng)

def _FixGranthaEncode(Strng):
    """Maps accent and anusvara-variant marks to Grantha-specific Unicode codepoints and inserts a ZWNJ after visarga-virama when encoding."""
    Strng = Strng.replace('॑', '᳴')
    Strng = Strng.replace('᳚', '॑')
    Strng = Strng.replace('ꣳ', '𑍞')
    Strng = Strng.replace('ꣴ', '𑍟')
    Strng = Strng.replace('𑌼𑍍', '𑌼𑍍\u200C')

    return Strng

def _FixGranthaDecode(Strng):
    """Reverses the Grantha-specific accent, anusvara, and ZWNJ mappings applied during encoding when decoding back to the internal representation."""
    Strng = Strng.replace('𑌼𑍍\u200C', '𑌼𑍍')
    Strng = Strng.replace('॑', '᳚')
    Strng = Strng.replace('᳴', '॑')
    Strng = Strng.replace('𑍞', 'ꣳ')
    Strng = Strng.replace('𑍟', 'ꣴ')

    return Strng

def GranthaOldau(Strng):
    """Uses the old Grantha AU vowel sign, e.g. 𑌕𑍗 → 𑌕𑍌."""
    Strng = Strng.replace('𑍗', '𑍌')

    return Strng

def GranthaPrakrit(Strng):
    """Applies Prakrit orthography for Grantha, converting anusvara to the anusvara-above form except word-initially, e.g. 𑌬𑍁𑌦𑍍𑌧𑌂 → 𑌬𑍁𑌂𑌧𑌀."""
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

    """Other Grantha final forms option, currently a no-op passthrough, e.g. 𑌦𑌿𑌕𑍍 → 𑌦𑌿𑌕𑍍."""
    return Strng

def granthaserif(Strng):
    """Noto Serif Grantha rendering option, currently a no-op passthrough, e.g. 𑌬𑍁𑌦𑍍𑌧𑌂 → 𑌬𑍁𑌦𑍍𑌧𑌂."""
    return Strng

def egrantamil(Strng):
    """E-Grantamil encoding option, currently a no-op passthrough."""
    return Strng
