# -*- coding: utf-8 -*-

# DevanagariLimbu's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
#
# LimbuDevanagariConvention independently defines the SAME option name in both
# PreProcess.py and PostProcess.py, as two genuinely different functions
# (pre-side does roughly one direction of a transform, post-side roughly
# the inverse) - can't both be a bare top-level `def` of the identical
# name in one file. Suffixed _pre/_post here; PreProcess.py/PostProcess.py
# each re-export their own half under the ORIGINAL (unsuffixed) name via
# `import X_pre as X` / `import X_post as X`, so the public option name
# (post_options=['X']/pre_options=['X']) is completely unchanged.

import re

def LimbuDevanagariConvention_pre(Strng):
    Strng = Strng.replace('ए़', 'ऎ')
    Strng = Strng.replace('ओ़', 'ऒ')
    Strng = Strng.replace('े़', 'ॆ')
    Strng = Strng.replace('ो़', 'ॊ')
    Strng = Strng.replace('ः', '꞉')

    return Strng

def LimbuDevanagariConvention_post(Strng):
    Strng = Strng.replace('ऎ', 'ए़')
    Strng = Strng.replace('ऒ', 'ओ़')
    Strng = Strng.replace('ॆ', 'े़')
    Strng = Strng.replace('ॊ', 'ो़')
    Strng = Strng.replace('꞉', 'ः')

    return Strng
