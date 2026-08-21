# -*- coding: utf-8 -*-

# Arab_Ur's own Fix logic, consolidated out of ConvertFix.py (batch
# migration - see ScriptProcessing/Tamil.py for the pattern this
# follows). No pre/post options exist for this script. Its calls to
# FixArab (now living in ScriptProcessing/Arab.py) go through
# Options.call_fix('FixArab', ...) - Options.py's auto-discovery finds
# it directly, no ConvertFix.py re-export needed.


# ---- Fix (encode/decode conversion logic) ----

# internal
def _FixArab_UrEncode(Strng, Source):
    """Applies the shared Arabic fix-up logic (via ConvertFix.FixArab) when encoding text into the Urdu Perso-Arabic script."""
    from .. import Options
    Strng = Options.call_fix('FixArab', Strng, Source, False)

    if Source != 'Type':
        ## introduce hamza
        pass

    return Strng

# internal
def _FixArab_UrDecode(Strng, Source):
    """Applies the shared Arabic fix-up logic (via ConvertFix.FixArab) when decoding text out of the Urdu Perso-Arabic script."""
    from .. import Options
    Strng = Options.call_fix('FixArab', Strng, Source, True)

    pass

    return Strng

# internal
def FixArab_Ur(Strng, Source, reverse=False):
    """Dispatches to the Urdu Arabic-script encode or decode fix-up routine based on the reverse flag."""
    return _FixArab_UrDecode(Strng, Source) if reverse else _FixArab_UrEncode(Strng, Source)
