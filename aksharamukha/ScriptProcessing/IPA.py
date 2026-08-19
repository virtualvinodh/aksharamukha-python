# -*- coding: utf-8 -*-

# IPA's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def _FixIPAEncode(Strng):
    colon_tilde = "\u02D0\u0303"
    tilde_colon = "\u0303\u02D0"

    # ɑː̃ -> ɑ̃ː
    Strng = Strng.replace(colon_tilde,tilde_colon)
    # Add Visarga echo - kuH/kUH -> kuhŭ/kuːhŭ
    Strng = re.sub("(.)(\u02D0?)(\u0068)",r'\1\2\3\1'+'\u0306',Strng)
    Strng = Strng.replace('ə̸ə̸', 'ɑ̷ː')

    return Strng

def _FixIPADecode(Strng):
    colon_tilde = "\u02D0\u0303"
    tilde_colon = "\u0303\u02D0"

    Strng = Strng.replace('ɑ̷ː', 'ə̸ə̸')
    # ɑː̃ <- ɑ̃ː
    Strng = Strng.replace(tilde_colon,colon_tilde)
    # Reverse Visarga echo - kuH/kUH <- kuhŭ/kuːhŭ
    Strng = re.sub("(.)(\u02D0?)(\u0068)"+r"\1"+"\u0306",r"\1\2\3",Strng)

    return Strng

def FixIPA(Strng, reverse=False):
    return _FixIPADecode(Strng) if reverse else _FixIPAEncode(Strng)
