# Known bugs found while documenting Fix/pre-option/post-option functions

Surfaced while drafting docstrings for the ~750 functions across
`ConvertFix.py`/`PreProcess.py`/`PostProcess.py`/`ScriptProcessing/*.py`.
All are pre-existing (predate the ScriptProcessing consolidation), already
documented in-place in their docstrings, and intentionally left unfixed
for now - deferred until the ScriptProcessing migration has settled into
a stable one-to-one-parity baseline, so any behavior change is easy to
attribute to the fix itself rather than getting mixed into migration
verification noise.

## Open

- **Hiragana/Katakana source text with embedded Latin letters loses the
  Latin letters** - e.g. `process('Hiragana', 'IAST', 'こんにちは ABC 世界')`
  gives `' kŏnniciha   a  a  a   sĕkaï'`: `ABC` becomes three separate
  `a`s instead of surviving as `ABC`. Two compounding bugs:
  1. `PreProcess.retainLatin()` is meant to shield plain Latin letters
     from conversion by mapping each to a private-use codepoint before
     any script conversion runs, then mapping back afterward. Its table
     is built as `latn_basic_lower + latn_basic_upper` with no
     separating space between the two halves, so the last lowercase
     token (`ō`) and the first uppercase token (`A`) fuse into one
     unmatched entry, `'ōA'`, after the `.split(' ')`. Neither `ō` nor
     `A` ever gets shielded as a result - only `B` onward do.
  2. Even the letters that *do* get shielded don't survive: for a
     Hiragana/Katakana source, `PreProcess._japanese_kakasi_romanize()`
     runs `Convert.convertScript(txt.lower(), "ISO", "Devanagari")` on
     the *entire* string - private-use shield codepoints included -
     before handing it to `pykakasi`. That ISO->Devanagari pass doesn't
     know about the shield codepoints and turns each one into a bare
     inherent-vowel `अ`, which `pykakasi`/the later pipeline stages then
     render as a stray `a`. `retainLatin`'s shielding assumption (safe
     until explicitly reversed) doesn't hold across this particular
     pivot step. Not fixed yet - reported, not touched.

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

- **`ScriptProcessing/Oriya.py:44` `OriyaSubojinedVa`** - the regex
  contained a stray double `??` (`'(??<![ମବ])'`), a typo for a single `?`
  negative lookbehind marker; raised `re.error: unknown extension ?? at
  position 1` on any use. Unlike `removeZW`/`IPAIndic`, this one is
  `in_frontend: true` with a real user-facing label ("ସ୍ବ ଦ୍ବ → sva dva")
  - any real site visitor selecting it hit a hard crash. Fixed to
  `'(?<![ମବ])(୍ବ)'`; verified end-to-end against the docstring's own
  example (`sva dva` exactly) and that the negative lookbehind's intended
  exclusions (`ମ୍ବ`/`ବ୍ବ`, genuine /mb/ and /bb/ clusters) still don't
  convert. Moved out of `known_broken_options.json`, given a real case in
  `test_preoptions.json` covering both the fix and the exclusion.

- **`ScriptProcessing/Arab.py:72` `ArabRemoveAdditions` maps Peh (پ) to
  Feh (ف) instead of Beh (ب)** - `transliterate.process('Urdu', 'Arab',
  'پانی')` ("paani", water) came out as `فاني` ("faani") instead of
  `باني` ("baani"). Traced to `ArabRemoveAdditions`, an `# internal`
  postoption applied unconditionally whenever `nativize=True` (the
  default) and the target is plain `Arab`, via
  `PostOptions._TARGET_DEFAULT_OPTIONS['Arab']`. Its own docstring
  claimed `پ→ف` as the "standard base form" - wrong on both phonetic
  grounds (/b/ is the cross-linguistic standard substitute for missing
  /p/, preserving place+manner and differing only in voicing; /f/ is a
  bigger jump - different place *and* manner) and shape-derivation
  grounds (پ's base letter-shape is ب's tooth-shape family, not ف's).
  Confirmed broader than just Urdu: the same corruption hit
  Shahmukhi->Arab, Arab-Fa->Arab, and even Arab->Arab with literal Peh
  in the input - every path where nativize defaults kick in for an Arab
  target, regardless of source. A sibling function,
  `arabicRemoveAdditionsPhonetic`, already had the correct `پ→ب` mapping
  and a docstring explicitly contrasting itself against this exact wrong
  behavior ("`/g j p b/ → /غ ج ب ب/` not `/ج ج ف ب/`") - but its guard in
  `transliterate.py:648` checks `src` *after*
  `_resolve_semitic_indic_naming` has already renamed `'Urdu'`/
  `'Shahmukhi'` to `'Arab-Ur'`/`'Arab-Pa'` (both genuinely
  `is_semitic`), so it never actually fires for the two sources most
  likely to carry native Peh - leaving `ArabRemoveAdditions`'s wrong
  mapping to run unopposed on every path. Fixed the one character in
  `ArabRemoveAdditions` (`پ→ب` instead of `پ→ف`) rather than touching the
  guard, since that's what actually runs unconditionally and fixes every
  observed case uniformly; the `ڨ→ج`/`ڤ→ف` mappings on the same line are
  untouched and still correct. Updated two test fixtures that had
  hardcoded the old wrong expectation (`test_postoptions.json`'s
  `ArabRemoveAdditions` case, `test_direct_options.json`'s
  `post::ArabRemoveAdditions` case).

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
