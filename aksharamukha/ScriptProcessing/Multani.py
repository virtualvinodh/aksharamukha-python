# -*- coding: utf-8 -*-

# Multani's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def _FixMultaniEncode(Strng):
    Strng = Strng.replace('\u02BE','').replace('\u02BF','')
    Strng = Strng.replace('ˍ\U0001128C', '\U0001128D').replace('ˍ\U00011282','\U00011293') ## Plosives


    return Strng

def _FixMultaniDecode(Strng):
    Strng = Strng.replace('\U0001128D','ˍ\U0001128C').replace('\U00011293','ˍ\U00011292') ## Plsosives

    return Strng

def FixMultani(Strng, reverse=False):
    return _FixMultaniDecode(Strng) if reverse else _FixMultaniEncode(Strng)
