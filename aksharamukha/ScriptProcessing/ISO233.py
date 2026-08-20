# -*- coding: utf-8 -*-

# ISO233's Arabic<->Latin romanization logic, consolidated out
# of PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this
# follows). ISO233 is one of GeneralMap.semiticISO's 4 pseudo-scripts
# (never a real registered script - dispatched by transliterate.py's
# _resolve_semitic_iso_pivot, same mechanism as the other 3). Re-exported
# into PreProcess.py/PostProcess.py under the original ISO233Target/
# ISO233Source names so that mechanism - and the existing test fixtures -
# keep working unchanged.

# ---- Pre-processing options ----

def ArabToISO233Pre(Strng):
    """Substitute Arabic hamza letters (أ ء إ) with their ISO 233 romanization symbols (ˈʾ, ¦, ˌʾ)."""
    replacements = [('أ', 'ˈʾ'), ('ء', '¦'), ('إ', 'ˌʾ')]

    for x, y in replacements:
        Strng = Strng.replace(x, y)

    return Strng

def ISO233ToArabPre(Strng):
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

def ArabToISO233Post(Strng):
    """Converts intermediate Arabic romanization to ISO 233 conventions (j/g->g-caron, h-diaeresis->t-diaeresis, nunation marks aN/iN/uN -> accented vowels, etc.)."""
    replacements = [('j', 'ǧ'), ('g', 'ǧ'), ('ḧ', 'ẗ'), ('ḫ', 'ẖ'), ('a̮', 'ỳ'), ('ˀ', 'ˈ'), \
        ('aⁿ', 'á'), ('iⁿ', 'í'), ('uⁿ', 'ú'), ('ā̂', 'ʾâ'), ('\u033D', '')]

    for x, y in replacements:
        Strng = Strng.replace(x, y)

    return Strng

def ISO233ToArabPost(Strng):

    """No-op placeholder (reserved for ISO 233 Arabic romanization source-side processing)."""
    return Strng
