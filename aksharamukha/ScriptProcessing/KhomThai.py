# -*- coding: utf-8 -*-

# KhomThai's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re

def _FixKhomThaiEncode(Strng):

    from .. import ConvertFix as CF
    Strng = Strng.replace('โ','เา')
    Strng = CF.ThaiReverseVowelSigns(Strng,False)
    Strng = re.sub('(.\u0E3A)(.\u0E3A)(ใ)', r'\3\1\2', Strng) # reversed
    Strng = re.sub('(.\u0E3A)(ใ)', r'\2\1', Strng) # reversed

    Strng = re.sub('((.\u0E3A)+)(เ)', r'\3\1', Strng) # reversed
    Strng = re.sub('(.\u0E3A)?(.)(ฺร)', r'\3\1\2', Strng) # reversed
    Strng = Strng.replace('เอา', 'โอ')

    Strng = Strng.replace("เอำ", 'เาอํ')
    Strng = Strng.replace('เาอํ', 'โอํ')

    return Strng

def _FixKhomThaiDecode(Strng):

    from .. import ConvertFix as CF
    Strng = re.sub('(ใ)(.\u0E3A)(.\u0E3A)', r'\2\3\1', Strng)
    Strng = re.sub('(ใ)(.\u0E3A)', r'\2\1', Strng)

    Strng = re.sub('(ฺร)(.\u0E3A)?(.)', r'\2\3\1', Strng)
    Strng = re.sub('(เ)((.\u0E3A)+)', r'\2\1', Strng)
    Strng = CF.ThaiReverseVowelSigns(Strng,True)
    Strng = Strng.replace('เา', 'โ')

    return Strng

def FixKhomThai(Strng, reverse=False):

    from .. import ConvertFix as CF
    return _FixKhomThaiDecode(Strng) if reverse else _FixKhomThaiEncode(Strng)
