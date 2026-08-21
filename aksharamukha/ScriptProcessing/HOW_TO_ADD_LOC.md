# How to add LoC (Library of Congress) romanization support for a script

LoC support for a script is discovered automatically, purely by function
name - there's no registry to edit anywhere. To add it:

## 1. Does the script need its own LoC character mapping?

Some scripts render slightly differently in their LoC-romanized form than
in their ordinary form (e.g. Gurmukhi's bindi vs. tippi). If that's true
for your script:

- Add a character-map table at `ScriptMap/<Family>/<Script>LoC.py`.
- Add a `Fix<Script>LoC` encode/decode function in
  `ScriptProcessing/<Script>LoC.py` (same pattern as any other script's
  `Fix` function - see `ScriptProcessing/Tamil.py`).
- Register the pivot: add `'<Script>'` to `GM.LoCSrcMap` in
  `GeneralMap.py`. This is the one place a new LoC-pivoting script still
  needs a list entry - the pivot is a real distinct script identity, not
  an auto-discoverable option.

If the script's LoC form is identical Unicode to its ordinary form,
skip this step entirely - most scripts do.

## 2. Fill in whichever of the four functions you need

In `ScriptProcessing/<Script>LoC.py` (create the file if it doesn't
exist yet), define any of:

```python
def <Script>ToRomanLoc_pre(Strng):   # runs on native text, before conversion to Roman
def <Script>ToRomanLoc_post(Strng):  # runs on the Roman output, after conversion
def RomanLocTo<Script>_pre(Strng):   # runs on incoming Roman text, before conversion to native
def RomanLocTo<Script>_post(Strng):  # runs on the native output, after conversion
```

(The `_pre`/`_post` suffix is the same convention used everywhere else
in this codebase for a same-name option split across both directions -
see `Options.py`'s auto-discovery docstring.)

None are mandatory. Most scripts only need one or two - e.g. Balinese
only needs `RomanLocToBalinese_pre`/`BalineseToRomanLoc_post` (a pair of
diacritic fixes), while Tibetan needs all four but two of them happen to
share one underlying implementation.

If your function needs a genuinely shared/generic helper (something
already used by several other scripts, like `AnusvaratoNasalASTISO` or
`RomanLoCChandrabindu`), call it as a small wrapper rather than
reimplementing it - see `ScriptProcessing/TeluguLoC.py` for the pattern,
and `ScriptProcessing/RomanLoC.py` for where those shared helpers live.

## 3. That's it

`transliterate.py`'s dispatch finds your functions automatically by
name (see `_apply_loc_option` there) and applies them in the right
order relative to the character-map conversion. No dict, no list, no
registration step anywhere else.

## Sharing a pivot with other scripts (advanced)

A handful of scripts share one underlying LoC pivot rather than each
having their own - e.g. KhuenTham/TaiTham/LaoTham/LueTham all route
through the single `'ThamLoC'` pivot (`ScriptProcessing/ThamLoC.py`).
For these, the lookup tries the script's own name first, then falls
back to the shared pivot name. So three of the four scripts get the
shared behavior automatically for free (define nothing), while the
fourth (KhuenTham) defines its own `RomanLocToKhuenTham_pre` in
`ScriptProcessing/KhuenTham.py` that does its own extra step and then
delegates to the shared pivot-level function. See that file for the
exact pattern if you need it.

## If the script has no dedicated Roman table at all

Tamil and Malayalam's LoC romanization is close enough to plain ISO
15919 that neither has its own `<Script>RomanLoC.py` character-map
table - they fall back to `ISO`/`ISO233` automatically, the same
fallback used for any script with no LoC association at all. Malayalam
still defines its own `MalayalamToRomanLoc_post`/`RomanLocToMalayalam_pre`
functions on top of that fallback (see
`ScriptProcessing/MalayalamLoC.py`); Tamil defines none.
