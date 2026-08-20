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

- **`PreProcess.py:1392` `removeZW`** - both `.replace()` calls are
  missing their replacement argument (`Strng.replace("‌").replace("‍")`).
  `str.replace()` requires two arguments; this raises `TypeError` if the
  option is ever invoked. Registered as a live pre-option
  (`Options.PRE_OPTIONS`), so it's reachable, just broken.

- **`PreProcess.py:1403` `IPAIndic`** - ends with a bare `return`
  (implicitly returns `None`) instead of `return Strng`. Any caller
  expecting the transformed string gets `None` instead.

- **`PreProcess.py:41` and `:61` `RomanLoCLaUnderscoreDoubleDot`** -
  defined twice under the identical name. The first definition (line 41,
  `Strng.replace('ḻ', 'l̤')`, no `return` statement) is dead - silently
  shadowed by the second definition (line 61, the reverse mapping
  `l̤ → ḻ`, which does return). Only the second is ever reachable.

- **`ScriptProcessing/Oriya.py:39` `OriyaSubojinedVa`** - the regex
  contains a stray double `??` (`'(??<![ମବ])'`), likely a typo for a
  single `?` negative lookbehind marker.

## Fixed since this file was written

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
