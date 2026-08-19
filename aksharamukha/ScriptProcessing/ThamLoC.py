# -*- coding: utf-8 -*-

# ThamLoC's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py. FixThamLoC delegates to
# the shared ConvertFix._FixTaiThamFamily; the pre/post options below
# are genuinely ThamLoC's own.
#
# ThamLoCRomanLoCTarget/ThamLoCRomanLoCSource each independently define
# the SAME option name in both PreProcess.py and PostProcess.py as
# genuinely different functions - suffixed _pre/_post here, same
# convention used everywhere else in ScriptProcessing/.
#
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import. See ScriptProcessing/Tamil.py.


import re
from .. import GeneralMap as GM


# ---- Fix (encode/decode conversion logic) ----

def FixThamLoC(Strng, reverse=False):

    """Core Tai Tham (LoC variant) encode/decode logic: delegate to the shared Tai Tham family fixer with marker cleanup enabled and ra-haam swapping disabled."""
    from .. import ConvertFix as CF
    return CF._FixTaiThamFamily(Strng, reverse, ['ᩅ', 'ᨴ', 'ᨵ', 'ᨣ', 'ᨷ'], marker_cleanup=True, ra_haam_swap=False)

# ---- Pre-processing options ----

def ThamLoCRomanLoCTarget_pre(Strng):
    """Apply Tai Tham LoC target-side vowel fixes for o/eo/aiy/koi/au sequences, the lue-karan sign, and vowel-killer marking."""
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'ThamLoC'))

    #Fix o
    Strng = Strng.replace('ᩮᩣ', 'ᩰ')

    #eo
    Strng = re.sub('ᩴ᩠ᨿ', '\u1A74\u1A7Fᨿ', Strng)

    #aiy
    Strng = re.sub('ᩱ᩠ᨿ', 'ᩱ\u1A7Fᨿ', Strng)

    #koi
    Strng = re.sub('᩠ᩅᩭ', '\u1A7Fᩅᩭ', Strng)

    #au
    Strng = re.sub('\u1A60\u1A45\u1A6B', '\u1A7F\u1A45\u1A6B', Strng)

    #close e/au
    Strng = re.sub('(᩠)(ᨿ|ᩅ)(?=(' + ListC + '))', '\u1A7F'+r'\2', Strng)

    # replace lue-karan with ra-haam
    Strng = Strng.replace('᩼', '᩺')

    #Mark Vowel Killer
    Strng = Strng.replace('᩺', '᩺''ʻ')

    return Strng

def ThamLoCRomanLoCSource_pre(Strng):
    """Insert a modifier-letter apostrophe before consonants following bare vowels, and expand ʻ to a+vowel-killer, for Tai Tham LoC source text."""
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'ThamLoCRomanLoC'))
    ListV ='|'.join(GM.CrunchSymbols(GM.Vowels,'ThamLoCRomanLoC'))

    #a
    Strng = re.sub('(a|ǫḥ|ǫ|œ|ò)(?=(' + ListC + '))', r'\1''\u02BD', Strng)

    Strng = Strng.replace('ʻ', 'a''᩺')

    return Strng

# ---- Post-processing options ----

def ThamLoCRomanLoCTarget_post(Strng):
    """No-op placeholder (reserved for Tai Tham LoC romanization target-side processing)."""
    return Strng

def ThamLoCRomanLoCSource_post(Strng):
    #cryptogammic dot to Sakot
    """Converts Tai Tham LoC romanization back to native encoding: maps cryptogrammic dot to sakot, fixes the aiy vowel+consonant sequence."""
    Strng = Strng.replace('\u1A7F', '᩠')

    #fixing aiy
    Strng = Strng.replace('\u1A71\u1A3F\u1A7A', '\u1A71᩠ᨿ')

    return Strng
