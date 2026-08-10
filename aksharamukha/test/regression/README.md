# Golden-output regression suite

Captures **current** behavior (bugs included) so future refactor steps can be
diffed against a known baseline instead of trusted on faith. Complements the
existing `../testsuite.py` / `../test_texts/` fixtures, which only cover
34 of ~326 `PostProcess` functions and 3 scripts' worth of default-option
behavior.

## Files

- `generate_golden.py` — regenerates the snapshot from current code. Run this
  once before starting a refactor step, or to intentionally update the
  baseline after a confirmed, deliberate behavior change.
- `compare_golden.py` — re-runs the same matrix against current code and
  reports every place output diverges from the saved snapshot. Run this
  after each refactor step. `--verbose` prints every diff instead of a
  summary count. Exits non-zero if anything differs.
- `manifest.json` — when the snapshot was generated, against which git
  commit, and record counts.
- `baseline_hash.json` — SHA-256 of each of the 616 existing
  `test_texts/test_*.txt` fixtures (Devanagari/IAST → every target script,
  no options), so drift in *those* is caught too, not just the new coverage.
- `roundtrip.json` — 752 records: for every target script (minus `IPA`,
  which makes a live unbounded HTTP call — see the audit), forward
  conversion from Devanagari and IAST, and the reverse round-trip back,
  under both `nativize=True` and `nativize=False`. Each record stores the
  output (or exception) for both legs, plus whether the round trip
  reproduced the original text exactly.
- `options.json` — 455 records: every function in `PreProcess.py` and
  `PostProcess.py` that's reachable as a `pre_options=[...]` /
  `post_options=[...]` value, exercised at least once via the public
  `transliterate.process()` API (source/target inferred from the option
  name where it contains a script name, matching the same heuristic
  `PostOptions.py`/`PreOptions.py` use internally).

## What this run already found

Running the generator against the current code (commit `ed86806`) surfaced
36 exceptions in the option sweep, worth fixing independently of any
refactor:

- `removeZW` and `IPAIndic` in `PreProcess.py` crash on any use — both were
  flagged as dead/broken by static reading in the earlier audit; this
  confirms it by actually calling them.
- `OriyaSubojinedVa`'s regex (`PreProcess.py:142`, the `(??<!...)` typo)
  raises `re.error: unknown extension ?? at position 1` — upgrades that
  finding from "looks like a typo" to a live crash.
- `KhmerWordSplit` hard-crashes with `ModuleNotFoundError: khmernltk` — an
  optional dependency that isn't installed/declared, so this pre-option is
  currently unusable as shipped in this environment.
- ~31 more (`AnusvaraToNasal`, `NasalToAnusvara`, `YaToYYa`, `VaToBa`,
  `RetainDandasIndic`, `JapanesePostProcess`, `PreProcess`, `normalize`,
  and others) are internal, multi-argument pipeline helpers that happen to
  live in the same module namespace `transliterate.py` uses for by-name
  option dispatch. They were never meant to be called as a bare
  `post_options=['AnusvaraToNasal']`, but nothing prevents it — if a caller
  (or a UI built from `getmembers(PostProcess, isfunction)`, which is
  exactly how `convert_default` enumerates "available options" today) ever
  passes one of these names, the conversion crashes with a raw `TypeError`
  instead of a clean "not a valid option" error. This is a direct
  consequence of reflection-based dispatch (pattern 01 in the refactor
  audit) rather than a one-off bug.

The round-trip matrix found no crashes (0/752) and, restricted to the
scripts `GeneralMap.ReversibleScripts`/`RomanReversible` actually document
as round-trip-safe with `nativize=False`, exactly one mismatch:
Devanagari/IAST ↔ Bengali — which matches the *existing* test suite's own
`if target_script != 'Bengali':` exclusion in `testsuite.py`, i.e. a known,
already-acknowledged case (the ba/va merger), not a new regression.

## Full per-option test-case coverage

`options.json` above only proves an option *runs*. It doesn't assert
anything, so it can't catch a future change in what an option *does*. The
next layer closes that gap:

- `generate_full_option_coverage.py` — for every option not already covered
  by a hand-authored case in `test_texts/test_postoptions.json`, runs it for
  real (via `transliterate.process(..., post_options=[name])` /
  `pre_options=[name]`) against two realistic sample texts and writes the
  input/output pairs into that fixture as a new characterization test case.
  Existing hand-authored entries are left untouched. Also writes a matching
  new `test_texts/test_preoptions.json` (there was no pre-option fixture at
  all before this), and `known_broken_options.json` for the options that
  can't be exercised this way at all (see below). Also emits
  `coverage_report.json` with the summary counts.
- `test_known_broken.py` — a pytest file asserting that each of the 36
  not-safely-callable options still fails *the same way* (`pytest.raises`
  on the recorded exception type). A newly-green test here is a signal to
  go move that option into a real fixture, not a bug in the test.
- `testsuite.py` gained one new class, `TestPreOptions`, mirroring the
  existing `TestPostOptions` exactly, now that `test_preoptions.json`
  exists for it to read.

**Result: 451 of the 455 options (326 post + 125 pre) now have a real,
asserted test case; the remaining 4 are confirmed, genuinely broken and
tracked as such — up from 34 with any real coverage at all.**

| | total | real test case | genuinely broken (tracked) |
|---|---|---|---|
| post-options | 326 | 326 (34 hand-authored + 271 via `post_options=[name]` + 21 via direct call) | 0 |
| pre-options | 129 | 125 (114 via `pre_options=[name]` + 11 via direct call) | 4 |

### A correction made along the way, worth keeping in mind

The first pass called every option through the single public mechanism,
`transliterate.process(..., post_options=[name])` /`pre_options=[name])` -
which only ever invokes `getattr(module, name)(txt)` with **one** argument
(`transliterate.py:455` and `:522`). 36 options failed that way with
`TypeError: missing N required positional argument(s)`, and got dumped into
`known_broken_options.json` as "broken."

That conflated two very different things: a handful of options really are
broken (4), and 32 are correctly-designed multi-argument options that
*do* have a real, working call site elsewhere in the codebase - in
`PostOptions.py`'s per-script default-option table, or called directly from
`ConvertFix.py`/`Convert.py`/`transliterate.py` with the right extra
argument(s) already supplied. `promote_direct_call_options.py` greps each
of the 36 names for its actual caller, calls it exactly that way (via
`ast` extraction rather than hand-retyping for the two cases needing a
non-ASCII script character - a Javanese repha, a set of Tai Tham
consonants - since a look-alike glyph typed by hand would fail silently,
not loudly), and promotes the 32 that succeed into `test_direct_options.json`
with real assertions, run by `test_direct_calls.py`. Two of those 32 needed
a second look even after the first "it runs now" pass: `RomanPreFix` only
works when called with `Source='Inter'` - the pipeline reassigns `Source`
to the pivot script two lines before calling it (`Convert.py:96-99`), so the
original script name it's invoked with in this test suite is never what it
actually sees in production, and passing the original name at all throws a
`re.error` for every script, not just the one first tried. `PhagsPaArrange`
turned out to take the *source* script as its second argument (triggered
when `Target == 'PhagsPa'`), not the literal string `'PhagsPa'` as first
guessed from the option's own name.

**Only 4 are actually broken, all confirmed independent of calling
convention:** `removeZW` and `IPAIndic` (both flagged by static reading in
the earlier refactor audit, now confirmed by execution), `OriyaSubojinedVa`
(a live `re.error` from the `(??<!...)` typo), and `KhmerWordSplit` (missing
`khmernltk` dependency).

Of the working cases (generated + direct-call combined), a good chunk are
**present but not visibly triggered** by the `heart`/`lalitavistara` sample
texts - they run, don't crash, and the test locks in that they stay a
no-op on this input, but they don't exercise the option's interesting code
path. See `coverage_report.json` for the exact breakdown. Improving that
ratio means hand-picking inputs that actually trigger each option's trigger
condition, which is a linguistics task, not a mechanical one - a good next
slice to do a handful at a time rather than in one more automated pass.

All 499 `TestPostOptions`/`TestPreOptions` cases, all 68 `test_direct_calls`
cases, and all 4 `test_known_broken` cases pass as of commit `ed86806`.
Running the *full* existing `testsuite.py` alongside them also surfaced 9
pre-existing failures unrelated to this work (confirmed by stashing these
changes and re-running: the failures are identical with or without them) -
`Kawi`/`KhuenTham` baseline conversion no longer matches their
`test_texts/test_Devanagari_{Kawi,KhuenTham}_*.txt` fixtures, and one
`TestSanity` Malayalam case fails. Worth investigating separately; not
caused by and not fixed by anything in this directory.
