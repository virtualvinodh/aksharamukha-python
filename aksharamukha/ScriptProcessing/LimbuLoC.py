# -*- coding: utf-8 -*-

# LimbuLoC's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re

# ---- Fix (encode/decode conversion logic) ----

def _FixLimbuLoCEncode(Strng):

    """Applies the shared Limbu orthographic fix routine when encoding into Limbu for the LoC romanization."""
    from .. import ConvertFix as CF
    Strng = CF.FixLimbu(Strng, False)

    return Strng

def _FixLimbuLoCDecode(Strng):

    """Applies the shared Limbu orthographic fix routine when decoding out of Limbu, then maps glottal-stop and length markers to LoC-specific symbols."""
    from .. import ConvertFix as CF
    Strng = CF.FixLimbu(Strng, True)
    Strng = Strng.replace('ʔ', '᤹')
    Strng = Strng.replace('꞉', '’')

    return Strng

def FixLimbuLoC(Strng, reverse=False):

    """Dispatches to the Limbu LoC encode or decode fix routine based on the reverse flag."""
    from .. import ConvertFix as CF
    return _FixLimbuLoCDecode(Strng) if reverse else _FixLimbuLoCEncode(Strng)
