# -*- coding: utf-8 -*-

# IPA's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

# ---- Fix (encode/decode conversion logic) ----

# internal
def _FixIPAEncode(Strng):
    """Reorders tilde before the length mark, appends a short echo vowel after visarga-derived h, and fixes a schwa ligature when encoding to IPA."""
    colon_tilde = "\u02D0\u0303"
    tilde_colon = "\u0303\u02D0"

    # ɑː̃ -> ɑ̃ː
    Strng = Strng.replace(colon_tilde,tilde_colon)
    # Add Visarga echo - kuH/kUH -> kuhŭ/kuːhŭ
    Strng = re.sub("(.)(\u02D0?)(\u0068)",r'\1\2\3\1'+'\u0306',Strng)
    Strng = Strng.replace('ə̸ə̸', 'ɑ̷ː')

    return Strng

# internal
def _FixIPADecode(Strng):
    """Reverses IPA encoding fixes: restores tilde/length-mark order and removes the visarga echo vowel."""
    colon_tilde = "\u02D0\u0303"
    tilde_colon = "\u0303\u02D0"

    Strng = Strng.replace('ɑ̷ː', 'ə̸ə̸')
    # ɑː̃ <- ɑ̃ː
    Strng = Strng.replace(tilde_colon,colon_tilde)
    # Reverse Visarga echo - kuH/kUH <- kuhŭ/kuːhŭ
    Strng = re.sub("(.)(\u02D0?)(\u0068)"+r"\1"+"\u0306",r"\1\2\3",Strng)

    return Strng

# internal
def FixIPA(Strng, reverse=False):
    """Dispatches to the IPA encode or decode fix routine depending on conversion direction."""
    return _FixIPADecode(Strng) if reverse else _FixIPAEncode(Strng)
