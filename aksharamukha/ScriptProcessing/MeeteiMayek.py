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

# ---- Post-processing options ----

def MeeteiMayekremoveHistorical(Strng):
    """Replaces historical/obsolete Meetei Mayek letters and the diaeresis-marked cheitap ee/oo sequences with their modern equivalents."""
    removePairs = [('ꫢ', 'ꯆ'), ('ꫣ', 'ꯅ'), ('ꫤ','ꯇ'), ('ꫥ','ꯊ'), ('ꫦ','ꯗ'), ('ꫧ','ꯙ'), ('ꫨ','ꯅ'),
                   ('ꫩ','ꯁ'), ('ꫪ','ꯁ'), ('\uAAF5','ꯍ꯭'), ('ꯑꫫ','ꯏ'), ('ꯑꫬ','ꯎ'), ('ꫫ','ꯤ'), ('ꫬ','ꯨ')]

    for x,y in removePairs:
        Strng = Strng.replace(x,y)

    return Strng

