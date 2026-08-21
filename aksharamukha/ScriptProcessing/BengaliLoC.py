# -*- coding: utf-8 -*-

# Bengali's LoC (Library of Congress) romanization logic.


# ---- Pre-processing options ----

# internal
def BengaliToRomanLoc_pre(Strng):
    """Applies the Khanda Ta and subjoined-va LoC fixes before converting Bengali to LoC Roman."""
    from .RomanLoC import KhandaTaRomanLoC_pre
    from .Bengali import BengaliSubojinedVa
    Strng = KhandaTaRomanLoC_pre(Strng)
    Strng = BengaliSubojinedVa(Strng)

    return Strng

# internal
def RomanLocToBengali_pre(Strng):
    """Normalizes candrabindu before converting LoC Roman text to Bengali."""
    from .RomanLoC import RomanLoCChandrabindu_pre
    Strng = RomanLoCChandrabindu_pre(Strng)

    return Strng

# ---- Post-processing options ----

# internal
def BengaliToRomanLoc_post(Strng):
    """Normalizes candrabindu after converting Bengali to LoC Roman."""
    from .RomanLoC import RomanLoCChandrabindu_post
    Strng = RomanLoCChandrabindu_post(Strng)

    return Strng

# internal
def RomanLocToBengali_post(Strng):
    """Restores the Khanda Ta letter after converting LoC Roman text to Bengali."""
    from .RomanLoC import KhandaTaRomanLoC_post
    Strng = KhandaTaRomanLoC_post(Strng)

    return Strng
