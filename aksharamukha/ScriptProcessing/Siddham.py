# -*- coding: utf-8 -*-

# Siddham's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
#
# siddhammukta is independently defined in both PreProcess.py and
# PostProcess.py, but both are truly identical no-op stubs (`return
# Strng`, no calls) - defined once here and re-exported unsuffixed to
# both, same reasoning as Grantha.py's egrantamil.

def FixSiddham(Strng, reverse=False):
    return _FixSiddhamDecode(Strng) if reverse else _FixSiddhamEncode(Strng)

def _FixSiddhamEncode(Strng):
    pass

    return Strng

def _FixSiddhamDecode(Strng):
    ## reverse the alternate forms
    Strng = Strng.replace('𑗜', '𑖲') # VS U
    Strng = Strng.replace('𑗝', '𑖳') # VS UU
    Strng = Strng.replace('𑗛', '𑖄') # VS U
    Strng = Strng.replace('𑗘', '𑖂') # VS I1
    Strng = Strng.replace('𑗙', '𑖂') # VS I2
    Strng = Strng.replace('𑗚', '𑖃') # VS II

    return Strng

def UseAlternateI1(Strng):
    Strng = Strng.replace('𑖂', '𑗘')

    return Strng

def UseAlternateI2(Strng):
    Strng = Strng.replace('𑖂', '𑗙')

    return Strng

def UseAlternateII(Strng):
    Strng = Strng.replace('𑖃',  '𑗚')

    return Strng

def UseAlternateU(Strng):
    Strng = Strng.replace('𑖄', '𑗛')

    return Strng

def UseAlternateVSU(Strng):
    Strng = Strng.replace('𑖲', '𑗜')

    return Strng

def UseAlternateVSUU(Strng):
    Strng = Strng.replace('𑖳', '𑗝')

    return Strng

def siddhammukta(Strng):
    return Strng
