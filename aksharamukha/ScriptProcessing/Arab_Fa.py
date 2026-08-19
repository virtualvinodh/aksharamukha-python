# -*- coding: utf-8 -*-

# Arab-Fa's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# ConvertFix/PreProcess/PostProcess are imported LOCALLY inside each
# function that needs them (not at module level) - required to avoid a
# load-order-dependent circular import, since these three modules
# re-export names from here. See ScriptProcessing/Tamil.py.

import re

def FixArab_Fa(Strng, Source, reverse=False):

    from .. import ConvertFix as CF
    Strng = CF.FixArab(Strng, Source, reverse)

    return Strng

def persianPaGaFaJa(Strng):

    from .. import ConvertFix as CF
    Strng = Strng.replace('پ', 'ف').replace('گ', 'ج')

    return Strng
