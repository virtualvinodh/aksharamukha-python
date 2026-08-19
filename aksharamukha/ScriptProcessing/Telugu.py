# -*- coding: utf-8 -*-

# Telugu's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# ConvertFix/PreProcess/PostProcess are imported LOCALLY inside each
# function that needs them (not at module level) - required to avoid a
# load-order-dependent circular import, since these three modules
# re-export names from here. See ScriptProcessing/Tamil.py.

import re
from .. import GeneralMap as GM

def _FixTeluguEncode(Strng):

    """Retains Indic dandas and numerals when encoding into Telugu script."""
    from .. import PostProcess
    Strng = PostProcess.RetainDandasIndic(Strng, 'Telugu', True)
    Strng = PostProcess.RetainIndicNumerals(Strng, 'Telugu', True)

    return Strng

def _FixTeluguDecode(Strng):

    """Restores Indic dandas and numerals and normalizes candrabindu to arasunna when decoding out of Telugu script."""
    from .. import PostProcess
    Strng = PostProcess.RetainIndicNumerals(Strng, 'Telugu')
    Strng = PostProcess.RetainDandasIndic(Strng, 'Telugu')
    Strng = Strng.replace('ఁ', 'ఀ')

    return Strng

def FixTelugu(Strng, reverse=False):

    """Dispatches to the Telugu encode or decode fix-up routine based on the reverse flag."""
    from .. import PostProcess
    return _FixTeluguDecode(Strng) if reverse else _FixTeluguEncode(Strng)

def TeluguRemoveNukta(Strng):

    """Removes the nukta combining mark from Telugu text."""
    from .. import PostProcess
    Strng = Strng.replace('\u0C3C', '')

    return Strng

def TeluguRemoveAeAo(Strng):

    """Removes the candra-sign-plus-ZWSP sequence used to mark short e/o vowels in Telugu."""
    from .. import PostProcess
    Strng = Strng.replace('\u0952\u200B', '')

    return Strng

def TeluguNakaraPollu(Strng):

    """Converts word-final na-virama to the special Telugu nakaara pollu character, e.g. భగవన్ → భగవౝ."""
    from .. import PostProcess
    ListC = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, 'Telugu')) + ")"

    Strng = re.sub('(?<!\u0C4D)న్(?!' + ListC + ')', '\u0C5D', Strng)

    return Strng

def TeluguTamilZha(Strng):

    """Tamil-style zha rendering option for Telugu, currently a no-op passthrough, e.g. ఆఴ్వార్ → ఆఴ్వార్."""
    from .. import PostProcess

    return Strng

def TeluguTamilRra(Strng):

    """Renders Tamil-style rra/tra/ndra conjuncts using the Telugu ౘ character, e.g. ఆఱ్ఱు → ఆౘ్ౘు."""
    from .. import PostProcess
    Strng = Strng.replace('ఱ్ఱ', 'ౘ్ౘ')
    Strng = Strng.replace('ట్ర', 'ౘ్ౘ')
    Strng = Strng.replace('ండ్ర','న్ఱ')

    return Strng

def TeluguReph(Strng):

    """Inserts a ZWNJ after ra-virama before a consonant to render it as a Telugu repha (valapala gilaka), e.g. ధర్మ → ధర్‍మ."""
    from .. import PostProcess
    consonants = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Telugu')) + ')'
    Strng = re.sub('ర్' + consonants, 'ర్‍' + r'\1', Strng)
    Strng = Strng.replace('\u0C4Dర్‍', '\u0C4Dర్')

    return Strng

def TeluguArasunnaChandrabindu(Strng):

    """Treats the Telugu arasunna character as chandrabindu, e.g. హూఀ → హూఁ."""
    from .. import PostProcess
    Strng = Strng.replace('ఀ', 'ఁ')

    return Strng
