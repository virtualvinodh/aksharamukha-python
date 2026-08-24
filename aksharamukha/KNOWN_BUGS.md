# Known bugs found while documenting Fix/pre-option/post-option functions

Surfaced while drafting docstrings for the ~750 functions across
`ConvertFix.py`/`PreProcess.py`/`PostProcess.py`/`ScriptProcessing/*.py`.
All are pre-existing (predate the ScriptProcessing consolidation), already
documented in-place in their docstrings, and intentionally left unfixed
for now - deferred until the ScriptProcessing migration has settled into
a stable one-to-one-parity baseline, so any behavior change is easy to
attribute to the fix itself rather than getting mixed into migration
verification noise.

## Real correctness bugs

- **`ScriptProcessing/Oriya.py:39` `OriyaSubojinedVa`** - the regex
  contains a stray double `??` (`'(??<![ମବ])'`), likely a typo for a
  single `?` negative lookbehind marker.

- **`Urdu` -> `Arab` maps Peh (پ) to Feh (ف) instead of Beh (ب)** -
  found while checking whether `transliterate.py`'s commented-out
  Urdu/Shahmukhi/Arab/Arab-Fa normalization block (see
  `_resolve_semitic_indic_naming`) was still needed. Reproduction:
  `transliterate.process('Urdu', 'Arab', 'پانی')` ("paani", water)
  comes out as `فاني` ("faani") - the Urdu/Persian-only letter پ
  (Peh, has no standard Arabic equivalent) becomes ف (Feh) rather
  than the linguistically expected ب (Beh), the nearest standard
  Arabic letter. Root cause not traced - Arab/Urdu aren't handled by
  the usual `ScriptMap/{MainIndic,EastIndic,NonIndic,Roman}`
  character-list files (no literal `ك`/`پ`/`ف` found anywhere under
  `ScriptMap/`), so this likely routes through the Semitic-specific
  dispatch path rather than a per-script map worth grep-ing for
  directly.

## Fixed since this file was written

- **`PreProcess.py:868` `removeZW`** - both `.replace()` calls were
  missing their replacement argument, raising `TypeError` on any use.
  Not exposed in the frontend (`in_frontend: false` in
  `frontend_backend_manifest.json`) and not called internally by
  anything else, so only reachable via a direct
  `pre_options=['removeZW']` API call - fixed anyway rather than left
  broken-by-convenience. Fixed to `Strng.replace("‌", "").replace
  ("‍", "")`; moved out of `known_broken_options.json` and given a
  real case in `test_preoptions.json` (`test_known_broken.py`'s own
  docstring asks for exactly this once a tracked bug starts working).

- **`PreProcess.py:872` `IPAIndic`** - ended with a bare `return`
  (implicitly `None`) instead of `return Strng`. Same exposure profile as
  `removeZW` above (`in_frontend: false`, no internal callers) - fixed to
  `return Strng`, moved out of `known_broken_options.json`, given a real
  case in `test_preoptions.json`.

## Stale entries removed (not real bugs in current code)

- **`RomanLoCLaUnderscoreDoubleDot`** - this file used to describe a
  duplicate-definition bug in `PreProcess.py:41`/`:61` (a dead first
  definition missing `return`, shadowed by a working second definition).
  That code no longer exists - the LoC redesign (predates this entry
  being written) split it into two properly-defined functions in
  `ScriptProcessing/RomanLoC.py`: `RomanLoCLaUnderscoreDoubleDot_pre`
  (line 34, `l̤ → ḻ`) and `_post` (line 84, `ḻ → l̤`), both of which
  correctly `return Strng`. The bug description was carried over into
  this file without re-verifying it against the migrated code. The
  `_pre` function's own docstring repeated the identical stale claim
  ("missing its return statement") about itself, and
  `DOCS_NEEDING_REVIEW.md` had the same claim duplicated as two
  identical bullets in a row - both corrected.

- **`PersianDMG` -> `Arab-Fa` (reverse direction) used to crash** -
  `transliterate.py`'s `_resolve_semitic_iso_pivot()` looks up
  `<pseudo-target> + 'Source'` (e.g. `'PersianDMGSource'`) as both a
  pre- and post-option whenever the source is one of the 4
  `GeneralMap.semiticISO` pseudo-scripts. `ISO259Source`,
  `ISO233Source`, and `HebrewSBLSource` all existed (in both
  `PreProcess.py` and `PostProcess.py`), but `PersianDMGSource` didn't
  exist anywhere - `PreProcess.py` had no Persian entry at all, and
  `PostProcess.py` had a same-shaped no-op placeholder but misnamed
  `PersianDMGSBLSource` (leftover from being copy-pasted off the
  `HebrewSBLSource` block above it, "SBL" never stripped out). Fixed
  by adding a real `PersianDMGSource` to `PreProcess.py` (built the
  same way `ISO233Source` reverses `ISO233Target`: undo its own
  pre-stage swap, then undo `PostProcess.py`'s post-stage
  substitutions), renaming `PersianDMGSBLSource` ->
  `PersianDMGSource` in `PostProcess.py`, and adding a
  `_verify_semitic_iso_consistency()` assertion at import time in
  `transliterate.py` so a future 5th `semiticISO` entry missing either
  half fails at import instead of crashing deep in
  `Options.call_pre_option`/`call_post_option` the first time a real
  conversion hits it.

## Frontend-label / code-direction mismatches

Not necessarily bugs in the *code* - could equally be a stale/wrong
label on the frontend side. Documented per what the code actually does,
not what the label implies. Worth a native-script speaker's sanity
check before trusting either direction:

- `ScriptProcessing/Arab.py` `ArabAtoAleph`
- `ScriptProcessing/Thai.py` `ThaiVisargaSaraA`
- `ScriptProcessing/Bengali.py` `khandatabatova`
- `ScriptProcessing/Hebr_Ar.py` `gainGimel`

See also `DOCS_NEEDING_REVIEW.md` for the broader list of code-derived
(unlabeled) docstrings worth spot-checking.
