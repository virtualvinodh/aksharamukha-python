# -*- coding: utf-8 -*-

# Takri's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
#
# TakriArchaicKha independently defines the SAME option name in both
# PreProcess.py and PostProcess.py as two different functions - suffixed
# _pre/_post here, aliased back on re-export (see ScriptProcessing/
# DevanagariLimbu.py for the first script this pattern was used on).

import re
from aksharamukha.ScriptMap.MainIndic import Takri

# ---- Pre-processing options ----

# frontend
def TakriArchaicKha_pre(Strng):

    """Temporarily substitutes the archaic Takri kha (𑚋) with a placeholder character before further processing."""
    return Strng.replace('𑚋', '𑚸')

# ---- Post-processing options ----

# frontend
def TakriArchaicKha_post(Strng):

    """Restores the archaic Takri kha (𑚋) from its temporary placeholder character after processing."""
    return Strng.replace('𑚸', '𑚋')

# frontend
def TakriRemoveGemination(Strng):

    """Collapses a geminated consonant (virama followed by the same consonant) into a single consonant, e.g. 𑚄𑚙𑚶𑚙𑚤 → 𑚄𑚙𑚤."""
    Strng = re.sub('(.)' + Takri.ViramaMap[0] + r'\1', r'\1', Strng)

    return Strng
