# -*- coding: utf-8 -*-

# Siddham's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
#
# siddhammukta is independently defined in both PreProcess.py and
# PostProcess.py, but both are truly identical no-op stubs (`return
# Strng`, no calls) - defined once here and re-exported unsuffixed to
# both, same reasoning as Grantha.py's egrantamil.

# ---- Fix (encode/decode conversion logic) ----

# internal
def FixSiddham(Strng, reverse=False):
    """Dispatches to the Siddham encode or decode fix routine depending on the reverse flag."""
    return _FixSiddhamDecode(Strng) if reverse else _FixSiddhamEncode(Strng)

# internal
def _FixSiddhamEncode(Strng):
    """No-op placeholder for Siddham encoding; no additional fixes are currently applied."""
    pass

    return Strng

# internal
def _FixSiddhamDecode(Strng):
    ## reverse the alternate forms
    """Reverses alternate Siddham vowel-sign forms (U, UU, I variants, II) back to their standard Unicode vowel signs."""
    Strng = Strng.replace('𑗜', '𑖲') # VS U
    Strng = Strng.replace('𑗝', '𑖳') # VS UU
    Strng = Strng.replace('𑗛', '𑖄') # VS U
    Strng = Strng.replace('𑗘', '𑖂') # VS I1
    Strng = Strng.replace('𑗙', '𑖂') # VS I2
    Strng = Strng.replace('𑗚', '𑖃') # VS II

    return Strng

# ---- Pre-processing options ----

# frontend
def siddhammukta(Strng):
    """Selects the Devanagari-based Siddham font variant (no-op transformation)."""
    return Strng

# ---- Post-processing options ----

# frontend
def UseAlternateI1(Strng):
    """Uses variant I form 1: 𑖂 → 𑗘."""
    Strng = Strng.replace('𑖂', '𑗘')

    return Strng

# frontend
def UseAlternateI2(Strng):
    """Uses variant I form 2: 𑖂 → 𑗙."""
    Strng = Strng.replace('𑖂', '𑗙')

    return Strng

# frontend
def UseAlternateII(Strng):
    """Uses the variant II (long I) form: 𑖃 → 𑗚."""
    Strng = Strng.replace('𑖃',  '𑗚')

    return Strng

# frontend
def UseAlternateU(Strng):
    """Uses the variant U form: 𑖄 → 𑗛."""
    Strng = Strng.replace('𑖄', '𑗛')

    return Strng

# frontend
def UseAlternateVSU(Strng):
    """Uses the variant vowel sign U: 𑖎𑖲𑖚𑖲𑖦𑖲 → 𑖎𑗜𑖚𑗜𑖦𑗜."""
    Strng = Strng.replace('𑖲', '𑗜')

    return Strng

# frontend
def UseAlternateVSUU(Strng):
    """Uses the variant vowel sign UU: 𑖎𑖳𑖚𑖳𑖦𑖳 → 𑖎𑗝𑖚𑗝𑖦𑗝."""
    Strng = Strng.replace('𑖳', '𑗝')

    return Strng
