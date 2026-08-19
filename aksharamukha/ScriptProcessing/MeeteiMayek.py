# -*- coding: utf-8 -*-

# MeeteiMayek's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from aksharamukha.ScriptMap.MainIndic import MeeteiMayek

# ---- Fix (encode/decode conversion logic) ----

def _FixMeeteiMayekEncode(Strng):
    """Converts eight specific consonant+virama sequences into their dedicated Meetei Mayek final-consonant Unicode characters."""
    vir = MeeteiMayek.ViramaMap[0]
    listC = [x+vir for x in [MeeteiMayek.ConsonantMap[x] for x in [0,27,24,20,19,15,4,25]]]
    finalC = ['\uABDB','\uABDC','\uABDD','\uABDE','\uABDF','\uABE0','\uABE1','\uABE2']

    for x,y in zip(listC,finalC):
        Strng = re.sub(x,y,Strng)

    return Strng

def _FixMeeteiMayekDecode(Strng):
    """Expands the dedicated Meetei Mayek final-consonant characters back into their consonant+virama component sequences."""
    vir = MeeteiMayek.ViramaMap[0]
    listC = [x+vir for x in [MeeteiMayek.ConsonantMap[x] for x in [0,27,24,20,19,15,4,25]]]
    finalC = ['\uABDB','\uABDC','\uABDD','\uABDE','\uABDF','\uABE0','\uABE1','\uABE2']

    for x,y in zip(listC,finalC):
        Strng = Strng.replace(y, x)

    return Strng

def FixMeeteiMayek(Strng,reverse=False):
    """Dispatches to the Meetei Mayek encode or decode fix routine depending on the reverse flag."""
    return _FixMeeteiMayekDecode(Strng) if reverse else _FixMeeteiMayekEncode(Strng)
