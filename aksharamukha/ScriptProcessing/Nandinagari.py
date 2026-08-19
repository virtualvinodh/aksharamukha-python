# -*- coding: utf-8 -*-

# Nandinagari's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# ConvertFix/PreProcess/PostProcess are imported LOCALLY inside each
# function that needs them (not at module level) - required to avoid a
# load-order-dependent circular import, since these three modules
# re-export names from here. See ScriptProcessing/Tamil.py.

import re

def _FixNandinagariEncode(Strng):

    from .. import PostProcess
    pass

    return Strng

def _FixNandinagariDecode(Strng):

    from .. import PostProcess
    Strng = PostProcess.NandinagariPrishtamatra(Strng, reverse=True)

    return Strng

def FixNandinagari(Strng, reverse=False):

    from .. import PostProcess
    return _FixNandinagariDecode(Strng) if reverse else _FixNandinagariEncode(Strng)

def NandinagariPrishtamatra(Strng, reverse = False):

    from .. import PostProcess
    if not reverse:
        Strng = Strng.replace('𑧚','𑧤')
        Strng = Strng.replace('𑧛','𑧤𑧚')
        Strng = Strng.replace('𑧜','𑧤𑧑')
        Strng = Strng.replace('𑧝','𑧤𑧜')
    else:
        Strng = Strng.replace('𑧤𑧚', '𑧛')
        Strng = Strng.replace('𑧤𑧑', '𑧜')
        Strng = Strng.replace('𑧤𑧜', '𑧝')
        Strng = Strng.replace('𑧤', '𑧚')


    return Strng
