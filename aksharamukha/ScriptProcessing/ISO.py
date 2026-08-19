# -*- coding: utf-8 -*-

# ISO's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# ConvertFix/PreProcess/PostProcess are imported LOCALLY inside each
# function that needs them (not at module level) - required to avoid a
# load-order-dependent circular import, since these three modules
# re-export names from here. See ScriptProcessing/Tamil.py.

import re

def longEOISO(Strng):

    from .. import PreProcess as PP
    Strng = Strng.replace('e', 'ē').replace('o', 'ō')

    return Strng

def joinVowelConsISO(Strng):

    from .. import PreProcess as PP
    return PP.joinVowelCons(Strng, 'ISO')

def noLongEO(Strng):

    from .. import PreProcess as PP
    Strng = Strng.replace('ē', 'e').replace('ō', 'o')

    return Strng
