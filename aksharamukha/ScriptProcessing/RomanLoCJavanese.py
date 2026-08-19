# -*- coding: utf-8 -*-

# RomanLoCJavanese's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def JavaneseSimplified(Strng):
    """Simplifies the jny consonant cluster to ny under the simplified Javanese romanization mapping."""
    Strng = Strng.replace('jny', 'ny')
    return Strng
