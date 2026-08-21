# -*- coding: utf-8 -*-

# KhomThai's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# Options is imported LOCALLY inside each function that needs it (not at
# module level) - required to avoid a load-order-dependent circular
# import. See ScriptProcessing/Tamil.py for the full explanation. Calls
# into Thai.py's ThaiReverseVowelSigns go through Options.call_fix(...)
# rather than a qualified ConvertFix.ThaiReverseVowelSigns reference -
# Options.py's auto-discovery finds it directly, no re-export needed.

import re

# ---- Fix (encode/decode conversion logic) ----

# internal
def _FixKhomThaiEncode(Strng):

    """Encodes Khom Thai orthography: expands the โ ligature, reverses vowel sign order, and reorders sara-ai/repha clusters around subscript consonants."""
    from .. import Options
    Strng = Strng.replace('โ','เา')
    Strng = Options.call_fix('ThaiReverseVowelSigns', Strng, False)
    Strng = re.sub('(.\u0E3A)(.\u0E3A)(ใ)', r'\3\1\2', Strng) # reversed
    Strng = re.sub('(.\u0E3A)(ใ)', r'\2\1', Strng) # reversed

    Strng = re.sub('((.\u0E3A)+)(เ)', r'\3\1', Strng) # reversed
    Strng = re.sub('(.\u0E3A)?(.)(ฺร)', r'\3\1\2', Strng) # reversed
    Strng = Strng.replace('เอา', 'โอ')

    Strng = Strng.replace("เอำ", 'เาอํ')
    Strng = Strng.replace('เาอํ', 'โอํ')

    return Strng

# internal
def _FixKhomThaiDecode(Strng):

    """Reverses Khom Thai encoding fixes: restores vowel sign order and collapses เา back into the โ ligature."""
    from .. import Options
    Strng = re.sub('(ใ)(.\u0E3A)(.\u0E3A)', r'\2\3\1', Strng)
    Strng = re.sub('(ใ)(.\u0E3A)', r'\2\1', Strng)

    Strng = re.sub('(ฺร)(.\u0E3A)?(.)', r'\2\3\1', Strng)
    Strng = re.sub('(เ)((.\u0E3A)+)', r'\2\1', Strng)
    Strng = Options.call_fix('ThaiReverseVowelSigns', Strng, True)
    Strng = Strng.replace('เา', 'โ')

    return Strng

# internal
def FixKhomThai(Strng, reverse=False):

    """Dispatches to the Khom Thai encode or decode fix routine depending on conversion direction."""
    return _FixKhomThaiDecode(Strng) if reverse else _FixKhomThaiEncode(Strng)
