# -*- coding: utf-8 -*-

# Telugu's LoC (Library of Congress) romanization logic.


# ---- Pre-processing options ----

def RomanLocToTeluguPre(Strng):
    """Normalizes candrabindu before converting LoC Roman text to Telugu."""
    from .RomanLoC import RomanLoCChandrabindu_pre
    Strng = RomanLoCChandrabindu_pre(Strng)

    return Strng

# ---- Post-processing options ----

def TeluguToRomanLocPost(Strng):
    """Applies anusvara-to-nasal and candrabindu LoC fixes after converting Telugu to LoC Roman."""
    from .RomanLoC import RomanLoCChandrabindu_post
    from .. import PostProcess
    Strng = PostProcess.AnusvaratoNasalASTISO(Strng)
    Strng = RomanLoCChandrabindu_post(Strng)

    return Strng

def RomanLocToTeluguPost(Strng):
    """Restores the arasunna-chandrabindu form after converting LoC Roman text to Telugu."""
    from .Telugu import TeluguArasunnaChandrabindu
    return TeluguArasunnaChandrabindu(Strng)
