# -*- coding: utf-8 -*-

# Buginese's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re

def _FixBugineseEncode(Strng):

    from .. import PostProcess
    Strng = Strng.replace("ᨂ\u02BEᨀ","ᨃ")
    Strng = Strng.replace("ᨆ\u02BEᨄ","ᨇ")
    Strng = Strng.replace("ᨊ\u02BEᨑ","ᨋ")
    Strng = Strng.replace("ᨎ\u02BEᨌ","ᨏ")

    Strng = PostProcess.InsertGeminationSign(Strng, 'Buginese')

    Strng = Strng.replace('\u02BE', '')

    return Strng

def _FixBugineseDecode(Strng):

    from .. import PostProcess
    Strng = Strng.replace("ᨃ", "ᨂ\u02BEᨀ")
    Strng = Strng.replace("ᨇ", "ᨆ\u02BEᨄ")
    Strng = Strng.replace("ᨋ", "ᨊ\u02BEᨑ")
    Strng = Strng.replace("ᨏ", "ᨎ\u02BEᨌ")

    return Strng

def FixBuginese(Strng, reverse=False):

    from .. import PostProcess
    return _FixBugineseDecode(Strng) if reverse else _FixBugineseEncode(Strng)
