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

def _FixKannadaEncode(Strng):

    from .. import PostProcess
    Strng = PostProcess.RetainDandasIndic(Strng, 'Kannada', True)
    #Strng = PostProcess.RetainIndicNumerals(Strng, 'Kannada', True)

    Strng = re.sub('(\u0CCD)([^\u0CAB\u0C9C])(\u0CBC)', r'\1' + '\u200C' + r'\2\3', Strng)

    return Strng

def _FixKannadaDecode(Strng):

    from .. import PostProcess
    Strng = PostProcess.RetainDandasIndic(Strng, 'Kannada')

    return Strng

def FixKannada(Strng, reverse=False):

    from .. import PostProcess
    return _FixKannadaDecode(Strng) if reverse else _FixKannadaEncode(Strng)

def KannadaSpacingCandrabindu(Strng):

    from .. import PostProcess
    Strng = Strng.replace('\u0C81', '\u0C80')

    return Strng

def KannadaNotRepha(Strng):

    from .. import PostProcess
    ListC = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, 'Kannada')) + ")"

    Strng = re.sub('ರ್(?=' + ListC + ')', 'ರ‍್', Strng)

    return Strng

def KannadaNakaraPollu(Strng):

    from .. import PostProcess
    ListC = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, 'Kannada')) + ")"

    Strng = re.sub('(?<!\u0CCD)ನ್(?!' + ListC + ')', '\u0CDD', Strng)

    return Strng
