# -*- coding: utf-8 -*-

# Assamese's LoC (Library of Congress) romanization logic.


# ---- Pre-processing options ----

# internal
def AssameseToRomanLocPre(Strng):
    """Applies the Khanda Ta LoC romanization fix before converting Assamese to LoC Roman."""
    from .RomanLoC import KhandaTaRomanLoC_pre
    Strng = KhandaTaRomanLoC_pre(Strng)

    return Strng

# internal
def RomanLocToAssamesePre(Strng):
    """Normalizes candrabindu before converting LoC Roman text to Assamese."""
    from .RomanLoC import RomanLoCChandrabindu_pre
    Strng = RomanLoCChandrabindu_pre(Strng)

    return Strng

# ---- Post-processing options ----

# internal
def AssameseToRomanLocPost(Strng):
    """Normalizes candrabindu after converting Assamese to LoC Roman."""
    from .RomanLoC import RomanLoCChandrabindu_post
    Strng = RomanLoCChandrabindu_post(Strng)

    return Strng

# internal
def RomanLocToAssamesePost(Strng):
    """Restores the Khanda Ta letter after converting LoC Roman text to Assamese."""
    from .RomanLoC import KhandaTaRomanLoC_post
    Strng = KhandaTaRomanLoC_post(Strng)

    return Strng
