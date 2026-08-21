# -*- coding: utf-8 -*-

# PersianDMG's Persian Arabic-script<->Latin romanization logic, consolidated out
# of PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this
# follows). PersianDMG is one of GeneralMap.semiticISO's 4 pseudo-scripts
# (never a real registered script - dispatched by transliterate.py's
# _resolve_semitic_iso_pivot, same mechanism as the other 3), which
# looks these up by the dynamically-constructed name PersianDMGTarget/
# PersianDMGSource - named directly as that here (with the _pre/_post
# suffix every same-name-both-directions option in this codebase uses,
# since Python doesn't allow two top-level `def PersianDMGTarget` in
# one file) rather than via a `... as PersianDMGTarget` re-export
# alias, so Options.py's auto-discovery (which strips that exact
# suffix) finds them with no re-export needed at all.

# ---- Pre-processing options ----

# internal
def PersianDMGTarget_pre(Strng):
    """Substitute Persian alef (ا) with the DMG romanization symbol ʾ."""
    replacements = [('ا', 'ʾ')]

    for x, y in replacements:
        Strng = Strng.replace(x, y)

    return Strng

# internal
def PersianDMGSource_pre(Strng):
    """Reverse Persian DMG romanization symbols back to Persian alef and normalize DMG-specific consonant/vowel spellings on the source side."""
    replacements = [('ا', 'ʾ')]
    for x, y in replacements:
        Strng = Strng.replace(y, x)

    replacements = [('ḏ', 'ẕ'), ('ḍ', 'ż'), ('ṯ', 's̱'), ('j', 'ǧ'), ('ˀ','ʼ'), ('ʔ', 'ʼ'), ('ȳ', 'ye'), ("ā̂", "ā"), ('\u033D', '')]
    for x, y in replacements:
        Strng = Strng.replace(y, x)

    return Strng

# ---- Post-processing options ----

# internal
def PersianDMGTarget_post(Strng):
    """Converts intermediate Persian romanization to DMG (Deutsche Morgenlandische Gesellschaft) conventions (d-line->z-line, d-dot->z-dot, t-line->s-line-below, j->g-caron, y-macron->ye)."""
    replacements = [('ḏ', 'ẕ'), ('ḍ', 'ż'), ('ṯ', 's̱'), ('j', 'ǧ'), ('ˀ','ʼ'), ('ʔ', 'ʼ'), ('ȳ', 'ye'), ("ā̂", "ā"), ('\u033D', '')]

    for x, y in replacements:
        Strng = Strng.replace(x, y)

    return Strng

# internal
def PersianDMGSource_post(Strng):

    """No-op placeholder (reserved for Persian DMG romanization source-side processing)."""
    return Strng
