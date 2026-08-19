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

    from .. import PostProcess
    Strng = PostProcess.RetainDandasIndic(Strng, 'Telugu', True)
    Strng = PostProcess.RetainIndicNumerals(Strng, 'Telugu', True)

    return Strng

def _FixTeluguDecode(Strng):

    from .. import PostProcess
    Strng = PostProcess.RetainIndicNumerals(Strng, 'Telugu')
    Strng = PostProcess.RetainDandasIndic(Strng, 'Telugu')
    Strng = Strng.replace('ఁ', 'ఀ')

    return Strng

def FixTelugu(Strng, reverse=False):

    from .. import PostProcess
    return _FixTeluguDecode(Strng) if reverse else _FixTeluguEncode(Strng)

def TeluguRemoveNukta(Strng):

    from .. import PostProcess
    Strng = Strng.replace('\u0C3C', '')

    return Strng

def TeluguRemoveAeAo(Strng):

    from .. import PostProcess
    Strng = Strng.replace('\u0952\u200B', '')

    return Strng

def TeluguNakaraPollu(Strng):

    from .. import PostProcess
    ListC = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, 'Telugu')) + ")"

    Strng = re.sub('(?<!\u0C4D)న్(?!' + ListC + ')', '\u0C5D', Strng)

    return Strng

def TeluguTamilZha(Strng):

    from .. import PostProcess

    return Strng

def TeluguTamilRra(Strng):

    from .. import PostProcess
    Strng = Strng.replace('ఱ్ఱ', 'ౘ్ౘ')
    Strng = Strng.replace('ట్ర', 'ౘ్ౘ')
    Strng = Strng.replace('ండ్ర','న్ఱ')

    return Strng

def TeluguReph(Strng):

    from .. import PostProcess
    consonants = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Telugu')) + ')'
    Strng = re.sub('ర్' + consonants, 'ర్‍' + r'\1', Strng)
    Strng = Strng.replace('\u0C4Dర్‍', '\u0C4Dర్')

    return Strng

def TeluguArasunnaChandrabindu(Strng):

    from .. import PostProcess
    Strng = Strng.replace('ఀ', 'ఁ')

    return Strng
