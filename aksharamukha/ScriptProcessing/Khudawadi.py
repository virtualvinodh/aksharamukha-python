# -*- coding: utf-8 -*-

# Khudawadi's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def _FixKhudawadiEncode(Strng):
    sindhi = ['𑊽', '𑋃', '𑋉', '𑋕']
    sindhiapprox = ['ˍ𑊼', 'ˍ𑋂', 'ˍ𑋈', 'ˍ𑋔']

    for x, y in zip(sindhi, sindhiapprox):
        Strng = Strng.replace(y,x)

    return Strng

def _FixKhudawadiDecode(Strng):
    sindhi = ['𑊽', '𑋃', '𑋉', '𑋕']
    sindhiapprox = ['ˍ𑊼', 'ˍ𑋂', 'ˍ𑋈', 'ˍ𑋔']

    for x, y in zip(sindhi, sindhiapprox):
        Strng = Strng.replace(x,y)

    return Strng

def FixKhudawadi(Strng, reverse=False):
    return _FixKhudawadiDecode(Strng) if reverse else _FixKhudawadiEncode(Strng)
