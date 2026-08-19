# -*- coding: utf-8 -*-

# LimbuLoC's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re

def _FixLimbuLoCEncode(Strng):

    from .. import ConvertFix as CF
    Strng = CF.FixLimbu(Strng, False)

    return Strng

def _FixLimbuLoCDecode(Strng):

    from .. import ConvertFix as CF
    Strng = CF.FixLimbu(Strng, True)
    Strng = Strng.replace('ʔ', '᤹')
    Strng = Strng.replace('꞉', '’')

    return Strng

def FixLimbuLoC(Strng, reverse=False):

    from .. import ConvertFix as CF
    return _FixLimbuLoCDecode(Strng) if reverse else _FixLimbuLoCEncode(Strng)
