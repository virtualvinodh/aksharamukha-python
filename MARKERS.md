# Marker sentinel inventory

Private-use / rare codepoints used as transient, invisible signals passed
between pipeline stages inside the transliterated string itself (inject
somewhere, check `if marker in Strng`, strip somewhere else). This file is
the map of what currently exists, found by an independent code audit
(2026-08). It documents the current state - it does not fix anything, and
none of the code these entries describe has been renamed to use it yet.
Renaming a use site to a named constant is expected to happen opportunistically,
whenever that function is touched for other reasons - not as a standalone sweep.

Each entry: codepoint(s), every file/function that injects or consumes it,
and whether that use is self-contained (injected and consumed within one
function/file - lower risk) or crosses function/file boundaries (the
injector and consumer have no direct reference to each other, only an
implicit contract on the codepoint - higher risk, easy to break silently).

## `ʾ` (MODIFIER LETTER RIGHT HALF RING)

The single most overloaded sentinel in the codebase - reused independently
for at least 8 unrelated purposes, apparently just because it's a rare
character unlikely to appear in real input, not because of any shared
meaning. A future addition reusing it a 9th time would have no way to know
about the other 8 without reading this file or grepping first.

1. **`ConvertFix.FixHanifiRohingya`** (~line 630-683) - diphthong+nukta
   marker for the y/w diphthong-to-consonant swap. Self-contained (one
   function).
2. **`ConvertFix.FixGunjalaGondi`** (~line 711-726) - temporary marker for
   a vowel-sign disambiguation pass. Self-contained.
3. **`ConvertFix.FixSoyombo`** (~line 728-750) - final-consonant marker,
   set and consumed entirely inside this one function as part of normal,
   unconditional core conversion (runs regardless of any postoption).
   Self-contained, and unrelated to #4 despite sharing the codepoint.
4. **`transliterate.convert()` line ~445 / `PostProcess.SoyomboFinals`** -
   the `SoyomboFinals` *postoption* prepends `ʾ` to the raw input text
   before conversion. Its intended consumer, `PostProcess.SoyomboFinals`,
   is a no-op stub (`return Strng` unchanged) - confirmed during the Phase 0
   bug audit. Empirically this currently has **no observable effect** on
   output either way (tested `Devanagari->Soyombo` with and without the
   postoption: byte-identical results, no leaked marker) - not a visible
   leak, but a non-functional feature. Whether it's supposed to interact
   with #3's mechanism, or was meant to be a separate control, is unresolved
   and needs a real look at Soyombo finals semantics, not a rename.
5. **`transliterate.convert()` line ~271** - appended to Khuen Tham text as
   an "indicator for Khuen text", consumed somewhere in the
   `FixThamLoC`/`FixKhuenTham` family (ConvertFix.py ~3318-3370, the same
   "Tall A" cluster flagged for Phase 2B parameterization).
6. **`ConvertFix.FixWarangCiti`** (~line 2483-2533) - internal staging
   marker, self-contained.
7. **`ConvertFix.FixChakma`** (~line 2807-2841) + **`PreProcess.ChakmaPali`**
   (~line 875-889) + **`PostProcess.ChakmaPali`** (~line 2056-2069) - all
   three stage `ʾ` as a temporary swap partner for the real Chakma
   codepoint `\U00011127`. Three files, but one coordinated pattern specific
   to Chakma (each stage does the same swap-and-restore), not random reuse -
   lower risk than #1-6 despite spanning multiple files.
8. **`ConvertFix.FixThamLoC`** (~line 3318-3330, also `~3500`, `~3539`) -
   "Tall A" TaiTham-family marker, checked with `if 'ʾ' in Strng`.
9. **`PostProcess.HebrewnonFinalShort`** (~line 1025-1047) - Vav/dagesh
   marker for a Hebrew-specific short-vowel rule.

## `Schwa = ''` / `DepV = 'ṿ'`

Defined as identical copy-pasted literals in three separate places instead
of one shared constant:
- `Convert.py:55-56` (local to `convertScript`)
- `ConvertFix.py:169-170` (local to whichever `Fix*` function needs it)
- `PreProcess.py:1228` (local to whichever `PreProcess` function needs it)

Lower risk than `ʾ` - these appear to be the *same* meaning
(schwa-suppression / dependent-vowel marking) reused consistently, just not
factored into one shared definition. A safe, mechanical dedup whenever one
of these three functions is touched.

## ``-``

Two unrelated uses of the same private-use range:
- **`PreProcess.py`** (~line 641-743) - Syriac ligature-disambiguation
  markers (resh/yin/daleth combinations).
- **`PostProcess.JapanesePostProcess`** (~line 873) - stand-ins for full
  stop / double full stop (`。`/`。。`) so they survive the function's
  multiple round-trips through other scripts as pivots.

No overlap in practice (Syriac and Japanese conversions never share a
pipeline), but nothing prevents a collision if that ever changes.

## `׍`, `׌`, `"ʻʻ"` (U+02BB doubled), `˂`, ``

Injected by various pre-processing steps (`transliterate.py:360,401`,
`PreProcess.AlephMaterLectionis`, `PreProcess.ThaiPhonetic`/`LaoPhonetic`/
`UrduShortNotShown`) for Semitic-to-Indic and Thai/Lao/Urdu
phonetic-transcription modes. All 5 are stripped as a final safety net by
**`PostProcess.default()`**, called unconditionally at the end of every
`Convert.convertScript()` call via `Convert.py:340` (`Strng = PP.default(Strng)`).

Initially misread as dead code during this audit - `Convert.py` imports
`PostProcess` under the alias `PP`, and a `git log -S "PostProcess.default("`
search (matching the fully-qualified name) missed the aliased call site.
Confirmed live and correctly wired via `git blame`/manual read plus an
empirical no-leak test across 8 representative conversions. No action
needed here.

## `͏` (COMBINING GRAPHEME JOINER)

Stripped by `PostProcess.defaultPost()` (`transliterate.py:542`, the
*other* end-of-pipeline safety net - runs after postoptions, whereas
`default()` above runs before). Single, simple use; no other file
references it as a marker today.
