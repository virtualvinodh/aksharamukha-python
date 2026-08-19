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

    """Retains Indic dandas and merges nukta-marked ja/sha into the dedicated Gujarati letter ૹ when encoding."""
    from .. import PreProcess as PP

    from .. import PostProcess
    Strng = PostProcess.RetainDandasIndic(Strng, 'Gujarati', True)
    Strng = Strng.replace('જ઼઼', 'ૹ').replace('શ઼', 'ૹ')

    return Strng

def _FixGujaratiDecode(Strng):

    """Retains Indic dandas and expands the Gujarati letter ૹ back into nukta-marked ja/sha when decoding."""
    from .. import PreProcess as PP

    from .. import PostProcess
    Strng = PostProcess.RetainDandasIndic(Strng, 'Gujarati')
    Strng = Strng.replace('ૹ', 'જ઼઼').replace('ૹ', 'શ઼')

    return Strng

def FixGujarati(Strng, reverse=False):

    """Dispatches to the Gujarati encode or decode fix routine depending on conversion direction."""
    from .. import PreProcess as PP

    from .. import PostProcess
    return _FixGujaratiDecode(Strng) if reverse else _FixGujaratiEncode(Strng)

def SchwaFinalGujarati(Strng):

    """Deletes the inherent schwa only at the end of a word - राम → rām."""
    from .. import PreProcess as PP

    from .. import PostProcess

    Strng = PP.RemoveFinal(Strng, 'Gujarati')

    return Strng
