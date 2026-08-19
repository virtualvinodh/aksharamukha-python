# -*- coding: utf-8 -*-

# MeeteiMayek's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from aksharamukha.ScriptMap.MainIndic import MeeteiMayek

def _FixMeeteiMayekEncode(Strng):
    vir = MeeteiMayek.ViramaMap[0]
    listC = [x+vir for x in [MeeteiMayek.ConsonantMap[x] for x in [0,27,24,20,19,15,4,25]]]
    finalC = ['\uABDB','\uABDC','\uABDD','\uABDE','\uABDF','\uABE0','\uABE1','\uABE2']

    for x,y in zip(listC,finalC):
        Strng = re.sub(x,y,Strng)

    return Strng

def _FixMeeteiMayekDecode(Strng):
    vir = MeeteiMayek.ViramaMap[0]
    listC = [x+vir for x in [MeeteiMayek.ConsonantMap[x] for x in [0,27,24,20,19,15,4,25]]]
    finalC = ['\uABDB','\uABDC','\uABDD','\uABDE','\uABDF','\uABE0','\uABE1','\uABE2']

    for x,y in zip(listC,finalC):
        Strng = Strng.replace(y, x)

    return Strng

def FixMeeteiMayek(Strng,reverse=False):
    return _FixMeeteiMayekDecode(Strng) if reverse else _FixMeeteiMayekEncode(Strng)
