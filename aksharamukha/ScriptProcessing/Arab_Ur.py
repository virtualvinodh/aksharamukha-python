# -*- coding: utf-8 -*-

# Arab_Ur's own Fix logic, consolidated out of ConvertFix.py (batch
# migration - see ScriptProcessing/Tamil.py for the pattern this
# follows). No pre/post options exist for this script. Its bare calls
# to FixArab are qualified as CF.FixArab, since FixArab now lives in
# ScriptProcessing/Arab.py.


# ---- Fix (encode/decode conversion logic) ----

def _FixArab_UrEncode(Strng, Source):
    """Applies the shared Arabic fix-up logic (via ConvertFix.FixArab) when encoding text into the Urdu Perso-Arabic script."""
    from .. import ConvertFix as CF
    Strng = CF.FixArab(Strng, Source, False)

    if Source != 'Type':
        ## introduce hamza
        pass

    return Strng

def _FixArab_UrDecode(Strng, Source):
    """Applies the shared Arabic fix-up logic (via ConvertFix.FixArab) when decoding text out of the Urdu Perso-Arabic script."""
    from .. import ConvertFix as CF
    Strng = CF.FixArab(Strng, Source, True)

    pass

    return Strng

def FixArab_Ur(Strng, Source, reverse=False):
    """Dispatches to the Urdu Arabic-script encode or decode fix-up routine based on the reverse flag."""
    return _FixArab_UrDecode(Strng, Source) if reverse else _FixArab_UrEncode(Strng, Source)
