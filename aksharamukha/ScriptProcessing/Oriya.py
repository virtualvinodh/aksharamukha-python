# -*- coding: utf-8 -*-

# Oriya's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# ConvertFix/PreProcess/PostProcess are imported LOCALLY inside each
# function that needs them (not at module level) - required to avoid a
# load-order-dependent circular import, since these three modules
# re-export names from here. See ScriptProcessing/Tamil.py.

import re
from aksharamukha.ScriptMap.MainIndic import Oriya

def _FixOriyaEncode(Strng):

    """No-op encode fix for Oriya; no additional orthographic corrections are currently applied."""
    from .. import PostProcess
    pass

    return Strng

def _FixOriyaDecode(Strng):

    """Replaces the alternate va character (ଵ) with the standard Oriya va/wa (ୱ) when decoding out of Oriya."""
    from .. import PostProcess
    Strng = Strng.replace('ଵ','ୱ')

    return Strng

def FixOriya(Strng, reverse=False):

    """Dispatches to the Oriya encode or decode fix routine based on the reverse flag."""
    from .. import PostProcess
    return _FixOriyaDecode(Strng) if reverse else _FixOriyaEncode(Strng)

def OriyaSubojinedVa(Strng):

    """Renders subjoined /va/ using ୱ instead of plain ba, e.g. ସ୍ବ ଦ୍ବ → sva dva."""
    from .. import PostProcess
    Strng = re.sub('(??<![ମବ])(୍ବ)', '୍ୱ', Strng)

    return Strng

def OriyaTargetVa(Strng):

    """Uses ୱ as the target letter for /va/, e.g. ବ → va."""
    from .. import PostProcess
    Strng = Strng.replace('ବ', 'ୱ')

    return Strng

def OriyaVaAlt(Strng):

    """Uses the alternate va character ଵ instead of ୱ, e.g. ଭୱତି → ଭଵତି (enable preserve source)."""
    from .. import PostProcess
    return  Strng.replace('ୱ','ଵ')

def OriyaYYA(Strng):

    """Replaces ya with yya (ୟ) everywhere in the text, e.g. ଯୟାତି ଯଜ୍ଞ → ୟୟାତି ୟଜ୍ଞ."""
    from .. import PostProcess
    return PostProcess.YYAEverywhere(Strng, 'Oriya')

def OriyaVa(Strng):

    """Replaces standalone va with ba (ବ), except when it is subjoined immediately after a virama."""
    from .. import PostProcess

    va = Oriya.ConsonantMap[28]
    OriyaVa = '\u0B2C'

    Strng =  re.sub('(?<!୍)' + va, OriyaVa, Strng)

    return Strng
