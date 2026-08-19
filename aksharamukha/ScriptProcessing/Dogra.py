# -*- coding: utf-8 -*-

# Dogra's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

# ---- Post-processing options ----

def olddogra(Strng):

    """Uses older/alternate Dogra letterforms for select vowel signs - 𑠂 𑠄 𑠈 𑠘 𑠧 → 𑠂 𑠄 𑠈 𑠘 𑠧."""
    return Strng

def DograShaKha(Strng):
    """Replaces Dogra SHA with KHA - 𑠨 → 𑠋."""
    Strng = Strng.replace('𑠨', '𑠋')

    return Strng
