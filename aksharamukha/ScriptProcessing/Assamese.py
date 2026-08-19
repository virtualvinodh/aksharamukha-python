# -*- coding: utf-8 -*-

# Assamese's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re

def _FixAssameseEncode(Strng):

    from .. import PostProcess
    Ra = "\u09B0"
    AssRa = "\u09F0"

    Strng = PostProcess.KhandaTa(Strng, 'Assamese', False)

    Strng = Strng.replace(Ra,AssRa)

    return Strng

def _FixAssameseDecode(Strng):

    from .. import PostProcess
    Ra = "\u09B0"
    AssRa = "\u09F0"

    Strng = PostProcess.KhandaTa(Strng, 'Assamese', True)

    Strng = Strng.replace(AssRa,Ra)

    return Strng

def FixAssamese(Strng,reverse=False):

    from .. import PostProcess
    return _FixAssameseDecode(Strng) if reverse else _FixAssameseEncode(Strng)
