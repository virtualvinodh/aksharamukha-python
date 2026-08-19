# -*- coding: utf-8 -*-

# Ranjana's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

# ---- Post-processing options ----

def ranjanalantsa(Strng):
    """Applies Lantsa Tibetan calligraphic style by replacing the Tibetan syllable separator with a plain space: बुद्धः → བུདྡྷཿ."""
    Strng = Strng.replace('་', ' ')
    return Strng

def ranjanawartu(Strng):
    """Applies Wartu Tibetan calligraphic style by replacing the Tibetan syllable separator with the Wartu mark plus space: बुद्धः → བུདྡྷཿ."""
    Strng = Strng.replace('་', '࿎ ')
    return Strng
