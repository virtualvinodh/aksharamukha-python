# -*- coding: utf-8 -*-

# Assamese's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re

# ---- Fix (encode/decode conversion logic) ----

def _FixAssameseEncode(Strng):

    """Applies the khanda-ta fix and converts standard ra to the Assamese ra form (ৰ) when encoding into Assamese."""
    from .. import PostProcess
    Ra = "\u09B0"
    AssRa = "\u09F0"

    Strng = PostProcess.KhandaTa(Strng, 'Assamese', False)

    Strng = Strng.replace(Ra,AssRa)

    return Strng

def _FixAssameseDecode(Strng):

    """Reverses the khanda-ta fix and converts the Assamese ra form (ৰ) back to standard ra when decoding out of Assamese."""
    from .. import PostProcess
    Ra = "\u09B0"
    AssRa = "\u09F0"

    Strng = PostProcess.KhandaTa(Strng, 'Assamese', True)

    Strng = Strng.replace(AssRa,Ra)

    return Strng

def FixAssamese(Strng,reverse=False):

    """Dispatches to the Assamese encode or decode fix routine based on the reverse flag."""
    from .. import PostProcess
    return _FixAssameseDecode(Strng) if reverse else _FixAssameseEncode(Strng)
