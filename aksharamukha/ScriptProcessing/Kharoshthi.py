# -*- coding: utf-8 -*-

# Kharoshthi's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

# ---- Fix (encode/decode conversion logic) ----

def FixKharoshthi(Strng, reverse=False):
    """Converts decimal numerals in the text to or from Kharoshthi numeral notation."""
    Strng = KharoshthiNumerals(Strng, reverse)

    return Strng

def KharoshthiNumerals(Strng, reverse=False):
    """Finds decimal numbers in the text and converts them to Kharoshthi additive numerals, or reverses Kharoshthi digits back to decimal."""
    Numbers = sorted(map(int,re.findall("\d+", Strng)),reverse=True)

    if not reverse:
        for num in Numbers:
             Strng = Strng.replace(str(num),kharoshthiNumber(num))
    else:
        one = '𐩀'
        two = '𐩁'
        three = '𐩂'
        four = '𐩃'
        ten = '𐩄'
        twenty = '𐩅'
        hundred = '𐩆'
        thousand = '𐩇'

        Strng = Strng.replace(one, '1#')
        Strng = Strng.replace(two, '2#')
        Strng = Strng.replace(three, '3#')
        Strng = Strng.replace(four, '4#')
        Strng = Strng.replace(ten, '10#')
        Strng = Strng.replace(twenty, '20#')
        Strng = Strng.replace(hundred, '100#')
        Strng = Strng.replace(thousand, '1000#')


    return Strng

def kharoshthiNumber(Strng):
    """Converts a single integer into its Kharoshthi additive numeral representation using thousand/hundred/twenty/ten/unit signs."""
    one = '𐩀'
    two = '𐩁'
    three = '𐩂'
    four = '𐩃'
    ten = '𐩄'
    twenty = '𐩅'
    hundred = '𐩆'
    thousand = '𐩇'

    num = int(Strng)
    kharnum = ''
    thou = int(num/1000)
    if thou > 0:
        if thou > 1:
            kharnum += kharoshthiNumber(thou)
        kharnum += thousand
    hund = int((num - (thou*1000))/100)
    if hund > 0:
        if hund > 1:
            kharnum += kharoshthiNumber(hund)
        kharnum += hundred
    twen = int((num - (thou*1000) - (hund * 100))/20)
    if twen > 0:
        kharnum += twenty * twen
    tenn = int((num - (thou*1000) - (hund * 100) - (twen*20))/10)
    if tenn > 0:
        if tenn > 1:
            kharnum += kharoshthiNumber(tenn)
        kharnum += ten
    ones = int((num - (thou*1000) - (hund * 100) - (twen*20) - (tenn * 10)))
    if ones > 0:
        if ones == 1:
            kharnum += one
        elif ones == 2:
            kharnum += two
        elif ones == 3:
            kharnum += three
        elif ones == 4:
            kharnum += four
        elif ones == 5:
            kharnum += four + one
        elif ones == 6:
            kharnum += four + two
        elif ones == 7:
            kharnum += four + three
        elif ones == 8:
            kharnum += four + four
        elif ones == 9:
            kharnum += four + four + one

    return kharnum
