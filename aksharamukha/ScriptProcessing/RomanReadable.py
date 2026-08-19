# -*- coding: utf-8 -*-

# RomanReadable's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# ConvertFix/PreProcess/PostProcess are imported LOCALLY inside each
# function that needs them (not at module level) - required to avoid a
# load-order-dependent circular import, since these three modules
# re-export names from here. See ScriptProcessing/Tamil.py.

import re

def FixRomanReadable(Strng, reverse = False):

    from .. import ConvertFix as CF
    return CF._FixRomanReadableColloquial(Strng, reverse, colloquial=False)

def RomanReadableLongEO(Strng):

    from .. import ConvertFix as CF

    Strng = Strng.replace('o', 'oa')
    Strng = Strng.replace('oa\'', 'o')

    Strng = Strng.replace('e', 'ae')
    Strng = Strng.replace('ae\'', 'e')

    Strng = Strng.replace('aeae', 'ee')
    Strng = Strng.replace('oaoa', 'oo')

    return Strng
