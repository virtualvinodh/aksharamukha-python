# -*- coding: utf-8 -*-

# ISO233's Arabic<->Latin romanization logic, consolidated out
# of PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this
# follows). ISO233 is one of GeneralMap.semiticISO's 4 pseudo-scripts
# (never a real registered script - dispatched by transliterate.py's
# _resolve_semitic_iso_pivot, same mechanism as the other 3), which
# looks these up by the dynamically-constructed name ISO233Target/
# ISO233Source - named directly as that here (with the _pre/_post
# suffix every same-name-both-directions option in this codebase uses,
# since Python doesn't allow two top-level `def ISO233Target` in one
# file) rather than via a `... as ISO233Target` re-export alias, so
# Options.py's auto-discovery (which strips that exact suffix) finds
# them with no re-export needed at all.

# ---- Pre-processing options ----

# internal
def ISO233Target_pre(Strng):
    """Substitute Arabic hamza letters (أ ء إ) with their ISO 233 romanization symbols (ˈʾ, ¦, ˌʾ)."""
    replacements = [('أ', 'ˈʾ'), ('ء', '¦'), ('إ', 'ˌʾ')]

    for x, y in replacements:
        Strng = Strng.replace(x, y)

    return Strng

# internal
def ISO233Source_pre(Strng):
    """Reverse ISO 233 romanization symbols back to Arabic hamza letters and normalize additional consonant/vowel spellings (j/g → ǧ, etc.) on the source side."""
    replacements = [('أ', 'ˈʾ'), ('ء', '¦'), ('إ', 'ˌʾ')]

    for x, y in replacements:
        Strng = Strng.replace(y, x)

    replacements = [('j', 'ǧ'), ('g', 'ǧ'), ('ḧ', 'ẗ'), ('ḫ', 'ẖ'), ('a̮', 'ỳ'), \
        ('aⁿ', 'á'), ('iⁿ', 'í'), ('uⁿ', 'ú'), ('ā̂', 'ʾâ'), ('ˀ', 'ˈ')]

    for x, y in replacements:
        Strng = Strng.replace(y, x)

    return Strng

# ---- Post-processing options ----

# internal
def ISO233Target_post(Strng):
    """Converts intermediate Arabic romanization to ISO 233 conventions (j/g->g-caron, h-diaeresis->t-diaeresis, nunation marks aN/iN/uN -> accented vowels, etc.)."""
    replacements = [('j', 'ǧ'), ('g', 'ǧ'), ('ḧ', 'ẗ'), ('ḫ', 'ẖ'), ('a̮', 'ỳ'), ('ˀ', 'ˈ'), \
        ('aⁿ', 'á'), ('iⁿ', 'í'), ('uⁿ', 'ú'), ('ā̂', 'ʾâ'), ('\u033D', '')]

    for x, y in replacements:
        Strng = Strng.replace(x, y)

    return Strng

# internal
def ISO233Source_post(Strng):

    """No-op placeholder (reserved for ISO 233 Arabic romanization source-side processing)."""
    return Strng
