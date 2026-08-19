# -*- coding: utf-8 -*-

# Pallava's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def kawitan(Strng):

    """Selects the Kawitan Pallava/Kawi font style: ꦥꦭ꧀ꦭꦮ ꦒ꧀ꦫꦤ꧀ꦡ (no-op transformation)."""
    return Strng

def sundapura(Strng):

    """Selects the Sundapura Pallava/Kawi font style: ꦥꦭ꧀ꦭꦮ ꦒ꧀ꦫꦤ꧀ (no-op transformation)."""
    return Strng
