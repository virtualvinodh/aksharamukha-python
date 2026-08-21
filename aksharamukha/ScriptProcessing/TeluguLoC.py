# -*- coding: utf-8 -*-

# Telugu's LoC (Library of Congress) romanization logic.


# ---- Pre-processing options ----

# internal
def RomanLocToTelugu_pre(Strng):
    """Normalizes candrabindu before converting LoC Roman text to Telugu."""
    from .RomanLoC import RomanLoCChandrabindu_pre
    Strng = RomanLoCChandrabindu_pre(Strng)

    return Strng

# ---- Post-processing options ----

# internal
def TeluguToRomanLoc_post(Strng):
    """Applies anusvara-to-nasal and candrabindu LoC fixes after converting Telugu to LoC Roman."""
    from .RomanLoC import RomanLoCChandrabindu_post
    from .. import PostProcess
    Strng = PostProcess.AnusvaratoNasalASTISO(Strng)
    Strng = RomanLoCChandrabindu_post(Strng)

    return Strng

# internal
def RomanLocToTelugu_post(Strng):
    """Restores the arasunna-chandrabindu form after converting LoC Roman text to Telugu."""
    from .Telugu import TeluguArasunnaChandrabindu
    return TeluguArasunnaChandrabindu(Strng)
