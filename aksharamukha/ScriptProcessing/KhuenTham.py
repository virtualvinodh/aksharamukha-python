# -*- coding: utf-8 -*-

# KhuenTham's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# ConvertFix/PreProcess/PostProcess are imported LOCALLY inside each
# function that needs them (not at module level) - required to avoid a
# load-order-dependent circular import, since these three modules
# re-export names from here. See ScriptProcessing/Tamil.py.

import re

def FixKhuenTham(Strng, reverse=False):

    from .. import ConvertFix as CF
    return CF._FixTaiThamFamily(Strng, reverse, ['ᩅ', 'ᨴ', 'ᨵ', 'ᨣ'], marker_cleanup=False, ra_haam_swap=True)

def KhuenRaHaamKaren(Strng):

    from .. import ConvertFix as CF
    # replace ra ham with r+ra-haam ->
    Strng = Strng.replace('᩺', 'ᩁ\u1A60')

    # replace lue-karan with ra-haam
    Strng = Strng.replace('᩼', '᩺')

    return Strng
