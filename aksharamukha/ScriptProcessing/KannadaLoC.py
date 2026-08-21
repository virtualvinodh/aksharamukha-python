# -*- coding: utf-8 -*-

# Kannada's LoC (Library of Congress) romanization logic.


# ---- Pre-processing options ----

# internal
def RomanLocToKannada_pre(Strng):
    """Normalizes candrabindu before converting LoC Roman text to Kannada."""
    from .RomanLoC import RomanLoCChandrabindu_pre
    Strng = RomanLoCChandrabindu_pre(Strng)

    return Strng

# ---- Post-processing options ----

# internal
def KannadaToRomanLoc_post(Strng):
    """Applies anusvara-to-nasal and candrabindu LoC fixes after converting Kannada to LoC Roman."""
    from .RomanLoC import RomanLoCChandrabindu_post
    from .. import PostProcess
    Strng = PostProcess.AnusvaratoNasalASTISO(Strng)
    Strng = RomanLoCChandrabindu_post(Strng)

    return Strng
