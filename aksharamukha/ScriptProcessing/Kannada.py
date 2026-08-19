# -*- coding: utf-8 -*-

# Kannada's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# ConvertFix/PreProcess/PostProcess are imported LOCALLY inside each
# function that needs them (not at module level) - required to avoid a
# load-order-dependent circular import, since these three modules
# re-export names from here. See ScriptProcessing/Tamil.py.

import re
from .. import GeneralMap as GM

# ---- Fix (encode/decode conversion logic) ----

def _FixKannadaEncode(Strng):

    """Retains Indic dandas and inserts a ZWNJ before a nukta after virama (except before pha/ja) when encoding into Kannada."""
    from .. import PostProcess
    Strng = PostProcess.RetainDandasIndic(Strng, 'Kannada', True)
    #Strng = PostProcess.RetainIndicNumerals(Strng, 'Kannada', True)

    Strng = re.sub('(\u0CCD)([^\u0CAB\u0C9C])(\u0CBC)', r'\1' + '\u200C' + r'\2\3', Strng)

    return Strng

def _FixKannadaDecode(Strng):

    """Restores Indic dandas to their generic forms when decoding out of Kannada script."""
    from .. import PostProcess
    Strng = PostProcess.RetainDandasIndic(Strng, 'Kannada')

    return Strng

def FixKannada(Strng, reverse=False):

    """Dispatches to the Kannada encode or decode fix-up routine based on the reverse flag."""
    return _FixKannadaDecode(Strng) if reverse else _FixKannadaEncode(Strng)

# ---- Post-processing options ----

def KannadaSpacingCandrabindu(Strng):

    """Uses the spacing candrabindu form instead of the combining one, e.g. ಯಹಾಁ → ಯಹಾಀ."""
    from .. import PostProcess
    Strng = Strng.replace('\u0C81', '\u0C80')

    return Strng

def KannadaNotRepha(Strng):

    """Prevents ra-virama before a consonant from forming a visual repha ligature, e.g. ಧರ್ಮ → ಧರ‍್ಮ."""
    from .. import PostProcess
    ListC = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, 'Kannada')) + ")"

    Strng = re.sub('ರ್(?=' + ListC + ')', 'ರ‍್', Strng)

    return Strng

def KannadaNakaraPollu(Strng):

    """Converts word-final na-virama to the special Kannada nakaara pollu character, e.g. ಭಗವನ್ → ಭಗವೝ."""
    from .. import PostProcess
    ListC = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, 'Kannada')) + ")"

    Strng = re.sub('(?<!\u0CCD)ನ್(?!' + ListC + ')', '\u0CDD', Strng)

    return Strng
