# -*- coding: utf-8 -*-

# HebrewSBL's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

# ---- Post-processing options ----

# frontend
def removetddash(Strng):
    """Removes the SBL spirant marks on ḏ ṯ ḡ and marks the plain stops with a modifier colon instead - ḏ ṯ ḡ → d t g & d t g → d꞉ t꞉ g꞉."""
    Strng += '\u05CE'

    Strng = Strng.replace('d', 'd꞉').replace('t', 't꞉').replace('g', 'g꞉')
    Strng = Strng.replace('ḏ', 'd').replace('ṯ', 't').replace('ḡ', 'g').replace('\u05CE', '')

    return Strng

# HebrewSBL is also one of GeneralMap.semiticISO's 4 pseudo-scripts
# (never a real registered script - dispatched by transliterate.py's
# _resolve_semitic_iso_pivot), which looks these up by the
# dynamically-constructed name HebrewSBLTarget/HebrewSBLSource - named
# directly as that here (with the _pre/_post suffix every same-name-
# both-directions option in this codebase uses, since Python doesn't
# allow two top-level `def HebrewSBLTarget` in one file) rather than
# via a `... as HebrewSBLTarget` re-export alias, so Options.py's
# auto-discovery (which strips that exact suffix) finds them with no
# re-export needed at all.

# ---- Pre-processing options ----

# internal
def HebrewSBLTarget_pre(Strng):
    """Substitute Hebrew aleph (א) and geresh (׳) with their SBL romanization symbols (ʾ, ’)."""
    Strng = Strng.replace('א', 'ʾ').replace('׳', '’')

    return Strng

# internal
def HebrewSBLSource_pre(Strng):
    """Reverse SBL Hebrew romanization symbols back to Hebrew letters, restoring begadkefat spirantization and vowel-length distinctions."""
    Strng = Strng.replace('ʾ', 'א',).replace('’', '׳')
    Strng = Strng.replace('\u0307\u00B0', '\u00B0\u0307')

    replacements = [('v', 'ḇ'), ('f', 'p̄'), ('d꞉', 'd'), ('d', 'ḏ'), \
        ('g꞉', 'g'), ('g', 'ḡ'), \
            ('t꞉', 't'), ('t', 'ṯ'),
         ('š̮', 'š'), ('š̪', 'ś'),
        ('o', 'ō'), ('ō', 'ô'), ('ū', 'û'), ('\u033D', 'ĕ')
    ]

    for x, y in replacements:
        Strng = Strng.replace(y, x)

    return Strng

# ---- Post-processing options ----

# internal
def HebrewSBLTarget_post(Strng):
    """Converts intermediate Hebrew romanization to SBL academic style (v->b-line-below, f->p-macron, d->d-line-below, g->g-line-below, t->t-line-below, o->o-circumflex, etc., undone when geminated)."""
    replacements = [('v', 'ḇ'), ('f', 'p̄'), ('d', 'ḏ'), ('ḏ꞉', 'd'), \
        ('g', 'ḡ'), ('ḡ꞉', 'g'),\
            ('t', 'ṯ'), ('ṯ꞉', 't'),
         ('š̪', 'ś'), ('š̮', 'š'),
        ('ō', 'ô'), ('o', 'ō'), ('ū', 'û'), ('\u033D', 'ĕ')
    ]

    for x, y in replacements:
        Strng = Strng.replace(x, y)

    Strng = Strng.replace('ĕ꞉', '꞉ĕ')

    if '\u05CE' in Strng:
        Strng = Strng.replace('ḏ', 'd').replace('ṯ', 't').replace('ḡ', 'g').replace('\u05CE', '')

    Strng = Strng.replace('\u00B0\u0307', '\u0307\u00B0')

    return Strng

# internal
def HebrewSBLSource_post(Strng):

    """No-op placeholder (reserved for SBL Hebrew romanization source-side processing)."""
    return Strng
