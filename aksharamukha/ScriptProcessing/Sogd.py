# -*- coding: utf-8 -*-

# Sogd's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
#
# SogdReshAyin independently defines the SAME option name in both
# PreProcess.py and PostProcess.py, as two genuinely different functions
# (pre-side does roughly one direction of a transform, post-side roughly
# the inverse) - can't both be a bare top-level `def` of the identical
# name in one file. Suffixed _pre/_post here; PreProcess.py/PostProcess.py
# each re-export their own half under the ORIGINAL (unsuffixed) name via
# `import X_pre as X` / `import X_post as X`, so the public option name
# (post_options=['X']/pre_options=['X']) is completely unchanged.

import re

def _FixSogdEncode(Strng, Source):
    Strng = Strng.replace("𐼹²","𐽄")

    return Strng

def _FixSogdDecode(Strng, Source):
    pass

    return Strng

def FixSogd(Strng, Source, reverse=False):
    return _FixSogdDecode(Strng, Source) if reverse else _FixSogdEncode(Strng, Source)

def SogdReshAyin_pre(Strng):
    Strng = Strng.replace('𐽀', '[\uEA01-\uEA02]') # resh yin

    return Strng

def SogdReshAyin_post(Strng):
    Strng = Strng.replace('𐼽', '𐽀')

    return Strng
