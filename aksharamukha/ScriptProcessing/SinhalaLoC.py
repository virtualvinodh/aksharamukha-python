# -*- coding: utf-8 -*-

# Sinhala's LoC (Library of Congress) romanization logic.


# ---- Pre-processing options ----

# internal
def RomanLocToSinhalaPre(Strng):
    """Normalizes candrabindu before converting LoC Roman text to Sinhala."""
    from .RomanLoC import RomanLoCChandrabindu_pre
    Strng = RomanLoCChandrabindu_pre(Strng)

    return Strng

# ---- Post-processing options ----

# internal
def SinhalaToRomanLocPost(Strng):
    """Applies anusvara-to-nasal, prenasalization, and candrabindu LoC fixes after converting Sinhala to LoC Roman."""
    from .RomanLoC import RomanLoCChandrabindu_post
    from .. import PostProcess
    from .Sinhala import SinhalaSannakaNasalization
    Strng = PostProcess.AnusvaratoNasalASTISO(Strng)
    Strng = SinhalaSannakaNasalization(Strng)
    Strng = RomanLoCChandrabindu_post(Strng)

    return Strng
