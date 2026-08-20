# -*- coding: utf-8 -*-

# Khojki's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# ConvertFix/PreProcess/PostProcess are imported LOCALLY inside each
# function that needs them (not at module level) - required to avoid a
# load-order-dependent circular import, since these three modules
# re-export names from here. See ScriptProcessing/Tamil.py.

import re

# ---- Fix (encode/decode conversion logic) ----

# internal
def _FixKhojkiEncode(Strng):

    """Converts approximated Sindhi consonant sequences to their dedicated Khojki characters, inserts the gemination sign, moves shadda after its consonant, reorders shadda+nukta, and encodes spaces as the Khojki word separator."""
    from .. import PostProcess
    sindhi = ['\U0001120B', '\U00011211', '\U0001121C', '\U00011222']
    sindhiapprox = ['ˍ\U0001120A', 'ˍ\U00011210', 'ˍ\U00011216', 'ˍ\U00011221']

    for x, y in zip(sindhi, sindhiapprox):
        Strng = Strng.replace(y, x)
    Strng = PostProcess.InsertGeminationSign(Strng, 'Khojki')
    # Move Shadda after consonant
    Strng = re.sub('(\U00011237)(.)', r'\2\1', Strng)
    # Reverse : Shadda + Nukta
    Strng = Strng.replace('𑈷𑈶', '𑈶𑈷')
    #Strng = re.sub('(' + GM.Germination['Khojki'] + ')', r'\2', Strng)
    # WordSeparatror
    Strng = Strng.replace(' ', '\U0001123A')

    return Strng

# internal
def _FixKhojkiDecode(Strng):

    """Reverses the word separator, Sindhi consonant substitution, shadda/nukta ordering, and gemination sign transformations applied when encoding Khojki."""
    from .. import PostProcess
    sindhi = ['\U0001120B', '\U00011211', '\U0001121C', '\U00011222']
    sindhiapprox = ['ˍ\U0001120A', 'ˍ\U00011210', 'ˍ\U00011216', 'ˍ\U00011221']

    # Reverse Word Separator
    Strng = Strng.replace('\U0001123A', ' ')

    for x, y in zip(sindhi, sindhiapprox):
        Strng = Strng.replace(x, y)
    # Reverse : Nukta + Shadda
    Strng = Strng.replace('𑈶𑈷', '𑈷𑈶')
    # Move Shadda before consonant
    Strng = re.sub('(.)(\U00011237)', r'\2\1', Strng)
    Strng = PostProcess.ReverseGeminationSign(Strng, 'Khojki')

    return Strng

# internal
def FixKhojki(Strng, reverse=False):

    """Dispatches to the Khojki encode or decode fix routine based on the reverse flag."""
    return _FixKhojkiDecode(Strng) if reverse else _FixKhojkiEncode(Strng)

# ---- Post-processing options ----

# internal
def KhojkiRRI(Strng):

    """Decomposes the Khojki vocalic RI/RII ligature characters into their constituent letter sequences."""
    Strng = Strng.replace('\U00011241', '\U00011235\U00011226\U0001122D')
    Strng = Strng.replace('\U00011240', '\U00011202')

    return Strng

# frontend
def KhojkiQa(Strng):

    """Uses the dedicated Khojki qa ligature instead of ka+nukta, e.g. 𑈈𑈶 → 𑈿."""
    Strng = Strng.replace('𑈈𑈶', '\U0001123F')

    return Strng

# frontend
def KhojkiRetainSpace(Strng):

    """Replaces the Khojki word-separator character with a plain space."""
    Strng = Strng.replace('\U0001123A', ' ')

    return Strng
