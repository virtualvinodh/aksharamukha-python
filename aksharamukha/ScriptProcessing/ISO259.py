# -*- coding: utf-8 -*-

# ISO259's Hebrew<->Latin romanization logic, consolidated out
# of PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this
# follows). ISO259 is one of GeneralMap.semiticISO's 4 pseudo-scripts
# (never a real registered script - dispatched by transliterate.py's
# _resolve_semitic_iso_pivot, same mechanism as the other 3). Re-exported
# into PreProcess.py/PostProcess.py under the original ISO259Target/
# ISO259Source names so that mechanism - and the existing test fixtures -
# keep working unchanged.

import unicodedata

# ---- Pre-processing options ----

# internal
def HebrewToISO259Pre(Strng):
    """Substitute Hebrew aleph (א) and geresh (׳) with their ISO 259 romanization symbols (ʾ, ’)."""
    Strng = Strng.replace('א', 'ʾ').replace('׳', '’')

    return Strng

# internal
def ISO259ToHebrewPre(Strng):
    """Reverse ISO 259 Hebrew romanization symbols back to Hebrew letters, restoring begadkefat forms and gemination marks via Unicode decomposition."""
    Strng = Strng.replace('ʾ', 'א',).replace('’', '׳')
    Strng = Strng.replace('\u0307\u00B0', '\u00B0\u0307')

    replacements = [('ḵ', 'k'), ('v', 'b'), ('f', 'p'), ('b', 'ḃ'), ('p', 'ṗ'), ('k', 'k̇'), ('꞉', '\u0307'),\
        ('š̮', 'š'), ('š', 's̀'), ('š̪', 'ś'),
        ('ā', 'å'), ('e', 'ȩ'), ('ō', 'ŵ'), ('ū', 'ẇ'), ('\u033D', '°'), ('ĕ', 'ḝ')
    ]

    for x, y in replacements:
        Strng = Strng.replace(y, x)

    Strng = unicodedata.normalize('NFD', Strng)
    Strng = Strng.replace('\u0307', '꞉')
    Strng = unicodedata.normalize('NFC', Strng)

    return Strng

# ---- Post-processing options ----

# internal
def HebrewToISO259Post(Strng):
    """Converts intermediate Hebrew romanization to ISO 259 conventions (b/p/k dotted, v->b, f->p, s-caron variants, a->a-ring, e->e-cedilla, o/u macron to circumflex forms)."""
    replacements = [('b', 'ḃ'), ('p', 'ṗ'), ('k', 'k̇'), ('ḵ', 'k'), ('v', 'b'), ('f', 'p'), ('꞉', '\u0307'),\
         ('š̪', 'ś'), ('š̮', 'š'), ('š', 's̀'),
        ('ā', 'å'), ('e', 'ȩ'), ('ō', 'ŵ'), ('ū', 'ẇ'), ('\u033D', '°'), ('ĕ', 'ḝ')
    ]

    for x, y in replacements:
        Strng = Strng.replace(x, y)

    Strng = Strng.replace('\u00B0\u0307', '\u0307\u00B0')

    return Strng

# internal
def ISO259ToHebrewPost(Strng):

    """No-op placeholder (reserved for ISO 259 Hebrew romanization source-side processing)."""
    return Strng
