# -*- coding: utf-8 -*-

# Oriya's LoC (Library of Congress) romanization logic.


# ---- Pre-processing options ----

# internal
def RomanLocToOriyaPre(Strng):
    """Normalizes candrabindu before converting LoC Roman text to Oriya."""
    from .RomanLoC import RomanLoCChandrabindu_pre
    Strng = RomanLoCChandrabindu_pre(Strng)

    return Strng

# ---- Post-processing options ----

# internal
def OriyaToRomanLocPost(Strng):
    """Applies anusvara-to-nasal and candrabindu LoC fixes after converting Oriya to LoC Roman."""
    from .RomanLoC import RomanLoCChandrabindu_post
    from .. import PostProcess
    Strng = PostProcess.AnusvaratoNasalASTISO(Strng)
    Strng = RomanLoCChandrabindu_post(Strng)

    return Strng
