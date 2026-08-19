# -*- coding: utf-8 -*-

# Mon's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re

def _FixMonEncode(Strng):

    from .. import ConvertFix as CF
    pairs = [('င', 'ၚ'),('ဉ', 'ည'), ('ဈ', 'ၛ')]

    for x, y in pairs:
        Strng = Strng.replace(y, x)

    Strng = CF.FixBurmese(Strng, False)

    Strng = Strng.replace('ည', '\uE001') #

    for x, y in pairs:
        Strng = Strng.replace(x, y)

    Strng = Strng.replace('\uE001', 'ည\u1039ည')

    medials_cons_mon = ['\u1039န', '\u1039မ', '\u1039လ']
    medials_mon = ['ၞ', 'ၟ', 'ၠ']

    for x, y in zip(medials_cons_mon, medials_mon):
        Strng = Strng.replace(x, y)

    Strng = Strng.replace('ၠြ', 'ြၠ')

    # Contigous Mon Medials
    for i, med1 in enumerate(medials_mon):
        for j, med2 in enumerate(medials_mon):
            Strng = Strng.replace(med1 + med2, medials_cons_mon[i] + medials_cons_mon[j])

    # Contiguous Medials + ya, ra and va
    for i, med in enumerate(medials_mon):
        Strng = Strng.replace(med + 'ျ', medials_cons_mon[i] + 'ျ')

        Strng = Strng.replace('ရ်' + med,  'ရ်' + medials_cons_mon[i])
        Strng = Strng.replace('ၚ်' + med,  'ၚ်' + medials_cons_mon[i])


    # RA + Medial

    return Strng

def _FixMonDecode(Strng):

    from .. import ConvertFix as CF
    pairs = [('င', 'ၚ'),('ဉ', 'ည'), ('ဈ', 'ၛ')]

    for x, y in pairs:
        Strng = Strng.replace(y, x)

    Strng = CF.FixBurmese(Strng, True)

    Strng = Strng.replace('ည', '\uE001') #

    for x, y in pairs:
        Strng = Strng.replace(x, y)

    Strng = Strng.replace('\uE001', 'ည\u1039ည')

    medials_cons_mon = ['\u1039န', '\u1039မ', '\u1039လ']
    medials_mon = ['ၞ', 'ၟ', 'ၠ']

    Strng = Strng.replace('်ရၠ', 'ၠ်ရ')

    for x, y in zip(medials_cons_mon, medials_mon):
        Strng = Strng.replace(y, x)

    Strng = Strng.replace('\u1039', '်')

    return Strng

def FixMon(Strng, reverse=False):

    from .. import ConvertFix as CF
    return _FixMonDecode(Strng) if reverse else _FixMonEncode(Strng)
