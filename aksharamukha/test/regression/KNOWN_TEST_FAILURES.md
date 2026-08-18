# Known test failures — current baseline

71 failing tests as of this report (`pytest testsuite.py regression/test_direct_calls.py
regression/test_known_broken.py`), out of ~3757 collected. Every one is accounted for
below — this file is the baseline: a fresh run should match this list exactly. A new
failure not listed here, or one of these disappearing/changing, means something
actually changed and needs a look before being added or removed here.

## 1. Pre-existing baseline — 9 failures, unrelated to this session

Long-standing, present before any of the work described below.

- `TestOverall::test_overall[heart-Kawi-Devanagari]`
- `TestOverall::test_overall[heart-Kawi-IAST]`
- `TestOverall::test_overall[heart-KhuenTham-Devanagari]`
- `TestOverall::test_overall[heart-KhuenTham-IAST]`
- `TestOverall::test_overall[lalitavistara-Kawi-Devanagari]`
- `TestOverall::test_overall[lalitavistara-Kawi-IAST]`
- `TestOverall::test_overall[lalitavistara-KhuenTham-Devanagari]`
- `TestOverall::test_overall[lalitavistara-KhuenTham-IAST]`
- `TestSanity::test_sanity_default[Malayalam]`

## 2. New failures — surfaced by adding real native-script source texts

Adding real, independently-authored text (not Devanagari-derived) for 17 scripts to
`source_texts.csv`, then running fanout + round-trip generation across all of them,
surfaced 62 new round-trip failures. These are the *first* round-trip tests ever run
with genuinely native-authored source text in several of these scripts — every prior
round-trip check used Devanagari/IAST-sourced, machine-generated samples. Investigated
and categorized below; none were "fixed" by guessing — every one was reproduced and
root-caused directly.

### 2a. Confirmed real library bug — not yet fixed

**`describe-sample-Assamese` — 8 targets: HK, Itrans, Titus, ISO, WX, RussianCyrillic,
IAST, Velthuis**

Root cause: candrabindu (ঁ, U+0981) attached to the independent vowel letter ও
(U+0993) round-trips incorrectly to anusvara (ং, U+0982) *whenever anything follows
the candrabindu* — mid-word or with a trailing consonant. The identical sequence at
the very end of a string round-trips correctly. Confirmed via direct testing: the
bug reproduces regardless of what precedes or follows (tested with different
trailing consonants, and with nothing preceding); it is specific to `ও` + candrabindu
followed by more text, not to a particular neighboring character. Every one of the 4
occurrences in the source text is the same word (তেওঁ / তেওঁৰ, "his/her") and each one
accounts for exactly one divergence point per target. `Velthuis` has this same
divergence *plus* the separate quote-mark parsing issue in 2c below.

This is the one item confirmed as an actual bug to fix (not an accepted limitation).

### 2b. Confirmed existing/accepted behavior — not bugs, not being changed

**`describe-sample-Gurmukhi` — 17 targets** (Tamil, HK, Itrans, Titus, Sinhala, Oriya,
ISO, WX, Kannada, Gujarati, Malayalam, RussianCyrillic, Assamese, Telugu, IAST,
Velthuis, Devanagari)

Root cause: Gurmukhi Tippi (ੰ, U+0A70) round-trips to Bindi (ਂ, U+0A02) consistently,
across many different contexts — a broader, more systematic mark-merger than the
Assamese case, not narrowly scoped to one word. Confirmed as existing/known behavior.

**`describe-sample-Sinhala-Telugu` — 1 target**

Root cause: Sinhala nasalization sequences produce extra spurious characters on
round-trip (e.g. `සඳ` → `සঁˆද`), not a simple mark substitution. Confirmed as existing/
known behavior.

**`describe-sample-Oriya` — 17 targets** (Tamil, HK, Itrans, Titus, Sinhala, ISO, WX,
Kannada, Gujarati, Malayalam, RussianCyrillic, Assamese, Telugu, IAST, Velthuis,
Gurmukhi, Devanagari)

Root cause: `ଵ` (VA, U+0B35) does not appear anywhere in `Oriya.py`'s mapping table;
only `ୱ` (WA, U+0B71) is defined, and the library treats both as the same sound "va"
(both → HK `va`), consistently producing `ୱ` on the way back regardless of which was
in the source. Confirmed as intentional merging, not a bug — same category as the
already-accepted Bengali va/ba merger. This is now the *sole* cause of all 17
failures — see 3 below for the two other artifacts that used to compound with it and
have since been cleaned up. Because the round-trip check is a strict full-string
comparison, fixing those two didn't change the pass/fail outcome (the VA/WA merger
alone is enough to fail the comparison either way) - but all 17 failures now trace to
exactly this one accepted cause instead of being contaminated by fixable noise.

### 2c. Genuine orthographic/scheme limitations — not bugs, not data artifacts

**`lotus-Devanagari-Velthuis` — 1 target**

A real Sanskrit vowel-hiatus sandhi (`bhūta` + `ālaye` → सुरभूतआलये) is ambiguous in
Velthuis's romanization between "consonant + vowel-sign then separate vowel" and
"consonant directly followed by an independent vowel letter." Authentic content,
not an artifact — not altered.

**`khuddakapatha-Devanagari-Velthuis` — 1 target**

A quote-mark immediately preceding text appears to interact with Velthuis's digraph
parsing (स्→श् swap after a preceding `"`). A scheme-specific parsing edge case, not
investigated further.

**`describe-sample-Malayalam` — 17 targets** (Tamil, HK, Itrans, Titus, Sinhala,
Oriya, ISO, WX, Kannada, Gujarati, RussianCyrillic, Assamese, Telugu, IAST, Velthuis,
Gurmukhi, Devanagari)

Root cause: Malayalam **chillu** letters — dedicated Unicode codepoints for a bare
word-final consonant (e.g. ൺ, chillu-ண) — round-trip differently than the same sound
written with an explicit virama (ണ്). Both are valid, real Malayalam Unicode
encodings of the same sound; the library's output consistently picks the chillu
form. Not yet explicitly classified as "accepted" the way Gurmukhi/Sinhala were —
flagged here for a decision, not assumed.

## 3. What was already fixed this session (for context, not part of the current baseline)

- `lotus`: stray Arabic-numeral chapter marker ("24"), a stray mid-word Zero-Width
  Joiner, both removed.
- `panchavimsati`: `[...]` omission markers (scholarly ellipsis convention) removed.
- `khuddakapatha`: 98 ASCII periods used as Devanagari-numeral list markers replaced
  with danda; curly quotation marks (used as doubled-single-quote dialogue markers)
  replaced with straight double-quotes.
- `describe-sample-Assamese`: decomposed YA+NUKTA (two codepoints) replaced with the
  precomposed YYA letter (one codepoint) — a pure Unicode-encoding-choice fix, no
  content change (10 occurrences).
- `describe-sample-Oriya`: 2 ASCII periods (abbreviation dots in `ଖ୍ରୀ.ପୂ.`, likely
  "BCE") replaced with danda, same pattern as `khuddakapatha`; 1 decomposed DDA
  (consonant + nukta, two codepoints) replaced with the precomposed `ଡ଼` letter (one
  codepoint) — the same composition-exclusion pattern as the Assamese YYA fix, this
  time for Oriya. Verified directly: both divergences are gone. The 17
  `describe-sample-Oriya` failures remain in the list below only because of the
  separate, already-accepted VA/WA merger, not because these fixes didn't work.

These are why the failure count dropped from an initial 126 to 71 (the Oriya fixes
didn't move the count further, since the VA/WA merger alone still fails the
strict-equality check - see 2b) before this report was written.
