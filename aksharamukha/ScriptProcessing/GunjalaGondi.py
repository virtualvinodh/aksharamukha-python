# -*- coding: utf-8 -*-

# GunjalaGondi's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from .. import GeneralMap as GM

def _FixGunjalaGondiEncode(Strng):
    """Merges apostrophe-marked vowel-sign sequences into the dedicated Gunjala Gondi combining sign, strips the modifier apostrophes, and drops a trailing virama not followed by a consonant."""
    consList = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'GunjalaGondi')) + ')'

    Strng = re.sub('(\U00011D7A\u02BE)([\U00011D7B\U00011D7C\U00011D80\U00011D81])', '\U00011D95' + r'\1', Strng)
    Strng = re.sub('(\U00011D7A\u02BF)([\U00011D7D\U00011D7E\U00011D82\U00011D83])', '\U00011D95' + r'\1', Strng)

    Strng = Strng.replace('\u02BE', '')
    Strng = Strng.replace('\u02BF', '')

    ## remove final virama when not followed by a consonant
    Strng = re.sub('\U00011D97(?!' + consList + ')' , '', Strng)

    return Strng

def _FixGunjalaGondiDecode(Strng):
    """Currently a no-op decode fix for Gunjala Gondi; returns the string unchanged."""
    consList = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'GunjalaGondi')) + ')'

    pass

    return Strng

def FixGunjalaGondi(Strng, reverse=False):
    """Dispatches to the Gunjala Gondi encode or decode fix routine based on the reverse flag."""
    return _FixGunjalaGondiDecode(Strng) if reverse else _FixGunjalaGondiEncode(Strng)
