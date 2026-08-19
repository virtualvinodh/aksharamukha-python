# -*- coding: utf-8 -*-

# Gujarati's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# ConvertFix/PreProcess/PostProcess are imported LOCALLY inside each
# function that needs them (not at module level) - required to avoid a
# load-order-dependent circular import, since these three modules
# re-export names from here. See ScriptProcessing/Tamil.py.

import re

def _FixGujaratiEncode(Strng):

    from .. import PreProcess as PP

    from .. import PostProcess
    Strng = PostProcess.RetainDandasIndic(Strng, 'Gujarati', True)
    Strng = Strng.replace('જ઼઼', 'ૹ').replace('શ઼', 'ૹ')

    return Strng

def _FixGujaratiDecode(Strng):

    from .. import PreProcess as PP

    from .. import PostProcess
    Strng = PostProcess.RetainDandasIndic(Strng, 'Gujarati')
    Strng = Strng.replace('ૹ', 'જ઼઼').replace('ૹ', 'શ઼')

    return Strng

def FixGujarati(Strng, reverse=False):

    from .. import PreProcess as PP

    from .. import PostProcess
    return _FixGujaratiDecode(Strng) if reverse else _FixGujaratiEncode(Strng)

def SchwaFinalGujarati(Strng):

    from .. import PreProcess as PP

    from .. import PostProcess

    Strng = PP.RemoveFinal(Strng, 'Gujarati')

    return Strng
