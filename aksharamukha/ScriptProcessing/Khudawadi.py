# -*- coding: utf-8 -*-

# Khudawadi's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

# ---- Fix (encode/decode conversion logic) ----

def _FixKhudawadiEncode(Strng):
    """Converts approximated Sindhi implosive-consonant digraphs (e.g. ˍ𑊼) into their precomposed Khudawadi implosive letters when encoding."""
    sindhi = ['𑊽', '𑋃', '𑋉', '𑋕']
    sindhiapprox = ['ˍ𑊼', 'ˍ𑋂', 'ˍ𑋈', 'ˍ𑋔']

    for x, y in zip(sindhi, sindhiapprox):
        Strng = Strng.replace(y,x)

    return Strng

def _FixKhudawadiDecode(Strng):
    """Converts precomposed Khudawadi implosive letters back into their approximated Sindhi digraph form when decoding."""
    sindhi = ['𑊽', '𑋃', '𑋉', '𑋕']
    sindhiapprox = ['ˍ𑊼', 'ˍ𑋂', 'ˍ𑋈', 'ˍ𑋔']

    for x, y in zip(sindhi, sindhiapprox):
        Strng = Strng.replace(x,y)

    return Strng

def FixKhudawadi(Strng, reverse=False):
    """Dispatches to the Khudawadi encode or decode fix-up routine based on the reverse flag."""
    return _FixKhudawadiDecode(Strng) if reverse else _FixKhudawadiEncode(Strng)
