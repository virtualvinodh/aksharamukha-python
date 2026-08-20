# -*- coding: utf-8 -*-

# Multani's own Fix/post-option logic, consolidated out of
# ConvertFix.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from .. import GeneralMap as GM

# ---- Fix (encode/decode conversion logic) ----

# internal
def _FixMultaniEncode(Strng):
    """Strips nukta joiner marks and merges nukta+consonant sequences into dedicated Multani plosive characters."""
    Strng = Strng.replace('\u02BE','').replace('\u02BF','')
    Strng = Strng.replace('ˍ\U0001128C', '\U0001128D').replace('ˍ\U00011282','\U00011293') ## Plosives


    return Strng

# internal
def _FixMultaniDecode(Strng):
    """Expands the dedicated Multani plosive characters back into their nukta+consonant component sequences."""
    Strng = Strng.replace('\U0001128D','ˍ\U0001128C').replace('\U00011293','ˍ\U00011292') ## Plsosives

    return Strng

# internal
def FixMultani(Strng, reverse=False):
    """Dispatches to the Multani encode or decode fix routine depending on the reverse flag."""
    return _FixMultaniDecode(Strng) if reverse else _FixMultaniEncode(Strng)

# ---- Post-processing options ----

# internal
def MultaniAbjad(Strng):
    """Simplifies Multani abjad-style orthography by dropping vowels between consonants in CVC/consonant-cluster contexts, matching its abjad (consonant-only) spelling convention."""
    ListAll = "(" + "|".join(GM.CrunchSymbols(GM.Characters, 'Multani') + ["𑊓", "𑊍"]) + ")"
    ListC = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, 'Multani') + ["𑊓", "𑊍"]) + ")"
    ListV = "(" + "|".join(GM.CrunchSymbols(GM.Vowels, 'Multani') + ["𑊓", "𑊍"]) + ")"

    Strng = re.sub(ListC + ListV + ListC, r'\1\3', Strng)
    Strng = re.sub('('+ ListC + '{2,})' + ListV, r'\1', Strng)
    Strng = re.sub(ListV + ListC + ListV, r'\1\2', Strng)

    return Strng

