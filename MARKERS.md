# Marker sentinel inventory

Private-use / rare codepoints used as transient, invisible signals passed
between pipeline stages inside the transliterated string itself (inject
somewhere, check `if marker in Strng`, strip somewhere else). This file is
the map of what currently exists, found by an independent code audit
(2026-08). It documents the current state - it does not fix anything unless
noted, and most of the entries below have not been renamed/retired yet.
Renaming a use site to a named constant is expected to happen opportunistically,
whenever that function is touched for other reasons - not as a standalone sweep.

Each entry: codepoint(s), every file/function that injects or consumes it,
and whether that use is self-contained (injected and consumed within one
function/file - lower risk) or crosses function/file boundaries (the
injector and consumer have no direct reference to each other, only an
implicit contract on the codepoint - higher risk, easy to break silently).

## `ʾ` (MODIFIER LETTER RIGHT HALF RING)

The single most overloaded sentinel in the codebase - reused independently
for at least 7 remaining unrelated purposes (one retired, #5 below),
apparently just because it's a rare character unlikely to appear in real
input, not because of any shared meaning. A future addition reusing it
again would have no way to know about the others without reading this
file or grepping first.

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
5. **Retired 2026-08-24.** Was: appended to Khuen Tham text by
   `ScriptProcessing/KhuenTham.py`'s `RomanLocToKhuenTham_pre`, consumed
   by `ConvertFix._FixTaiThamFamily` (via `ScriptProcessing/ThamLoC.py`'s
   `FixThamLoC` - the only one of the three ThamLoC-family Fix wrappers
   that passes `marker_cleanup=True`; `FixKhuenTham`/`FixLueTham` never
   checked it, since Khuen conversions pivot through the shared
   `'ThamLoC'` target before the Fix dispatch runs). Now:
   `RomanLocToKhuenTham_pre` sets `ctx.is_khuen_target = True` instead of
   appending the marker; `_FixTaiThamFamily` (now `ctx=None`-aware, with
   `ctx` threaded through all three wrappers) checks
   `ctx.is_khuen_target` instead of scanning the string. Same pattern as
   the already-retired Thai/Lao `transcription_mode` below - see
   `Context.py`'s `is_khuen_target` field. Verified via a clean
   16,126-sample corpus regen plus the dedicated
   `test/loc_tham_test_cases.py` TaiTham↔RomanLoC round-trip suite.
6. **`ConvertFix.FixWarangCiti`** (~line 2483-2533) - internal staging
   marker, self-contained.
7. **`ConvertFix.FixChakma`** (~line 2807-2841) + **`PreProcess.ChakmaPali`**
   (~line 875-889) + **`PostProcess.ChakmaPali`** (~line 2056-2069) - all
   three stage `ʾ` as a temporary swap partner for the real Chakma
   codepoint `\U00011127`. Three files, but one coordinated pattern specific
   to Chakma (each stage does the same swap-and-restore), not random reuse -
   lower risk than #1-6 despite spanning multiple files.
8. **`ConvertFix._FixTaiThamFamily`** (~line 3295-3327, formerly split
   across `FixThamLoC`/`FixLueTham`/`FixKhuenTham`) - "Tall A" TaiTham-family
   marker, checked with `if 'ʾ' in Strng`.
9. **`PostProcess.HebrewnonFinalShort`** (~line 1025-1047) - Vav/dagesh
   marker for a Hebrew-specific short-vowel rule.

## `Schwa = U+F000` / `DepV = U+1E7F` ('ṿ')

Defined as identical copy-pasted literals in three separate places instead
of one shared constant:
- `Convert.py:55-56` (local to `convertScript`)
- `ConvertFix.py:169-170` (local to whichever `Fix*` function needs it)
- `PreProcess.py:1228` (local to whichever `PreProcess` function needs it)

Lower risk than `ʾ` - these appear to be the *same* meaning
(schwa-suppression / dependent-vowel marking) reused consistently, just not
factored into one shared definition. A safe, mechanical dedup whenever one
of these three functions is touched.

## U+EA01-U+EA06 (private use)

Two unrelated uses of the same private-use range:
- **`PreProcess.py`** (~line 641-743) - Syriac ligature-disambiguation
  markers (resh/yin/daleth combinations).
- **`PostProcess.JapanesePostProcess`** (~line 873) - stand-ins for full
  stop / double full stop (`。`/`。。`) so they survive the function's
  multiple round-trips through other scripts as pivots.

No overlap in practice (Syriac and Japanese conversions never share a
pipeline), but nothing prevents a collision if that ever changes.

## `׍`, `׌`, `˂`, U+F001

Injected by `transliterate.py:360,401` and `PreProcess.AlephMaterLectionis`
for Semitic-to-Indic transcription modes. Stripped as a final safety net by
**`PostProcess.default()`**, called unconditionally at the end of every
`Convert.convertScript()` call via `Convert.py:340` (`Strng = PP.default(Strng)`).

Initially misread as dead code during this audit - `Convert.py` imports
`PostProcess` under the alias `PP`, and a `git log -S "PostProcess.default("`
search (matching the fully-qualified name) missed the aliased call site.
Confirmed live and correctly wired via `git blame`/manual read plus an
empirical no-leak test across 8 representative conversions. No action
needed here.

## `"ʻʻ"` (U+02BB doubled) - Thai/Lao/Urdu transcription mode

**Retired 2026-08-24.** 5 real injection points fed this one marker, not
the 3 an earlier pass of this file assumed - that undercount caused a real
regression (`TestPreOptions[ThaiOrthography]`/`TestPreOptions[LaoTranscription]`
broke when only 3 of the 5 were migrated to the new mechanism below; caught
by the full suite, fixed same session by an exhaustive grep instead of
trusting the earlier partial list): `ScriptProcessing/Thai.py`'s
`ThaiPhonetic`/`ThaiOrthography`, `ScriptProcessing/LaoPali.py`'s
`LaoPhonetic`/`LaoTranscription`, and `ScriptProcessing/Urdu.py`'s
`UrduShortNotShown` - all five now no-ops. 3 consumption points, all
retired: `ConvertFix.FixThai`, `ConvertFix.FixLaoPali`, and (this session)
`ConvertFix._FixUrduShahmukhiDecode` - deliberately deferred past the
Thai/Lao retirement alongside `FixKhamtiShan`/`FixTaiLaing`/`FixShan`,
since it's a large `reverse=`-fused function (`FixUrduShahmukhi` dispatches
to a ~150-line `_FixUrduShahmukhiEncode`/`_FixUrduShahmukhiDecode` pair)
and tracing its actual control flow required reading both branches in
full, not just grepping for the marker - the marker check turned out to
gate a genuine two-branch if/else with different vowel-insertion logic in
each branch (unlike Khuen Tham's simple optional-cleanup case just above),
so only the *condition* was swapped, not the branch bodies.

All three scripts now share one mechanism: `transliterate.py`'s
`_prepare_for_core_conversion` computes `ctx.transcription_mode` once, up
front, from `preoptions` membership (`'ThaiPhonetic' in preoptions or
'LaoPhonetic' in preoptions or 'ThaiOrthography' in preoptions or
'LaoTranscription' in preoptions or 'UrduShortNotShown' in preoptions`),
and each consumer (`FixThai`, `FixLaoPali`, `_FixUrduShahmukhiDecode`)
declares `ctx=None` and reads `ctx.transcription_mode` instead of scanning
`Strng` for the marker. `ctx` reaches `_FixUrduShahmukhiDecode` via the
existing `Options.call_fix("Fix"+Source...,reverse=True,optional=True,
ctx=ctx)` dispatch in `Convert.py` (built this session for the Khuen Tham
retirement, already ctx-aware everywhere) through `Urdu.FixUrdu`/
`Shahmukhi.FixShahmukhi` -> `ConvertFix.FixUrduShahmukhi` -> `_FixUrduShahmukhiDecode`,
each now threading `ctx=None` alongside `reverse`. Verified via a
same-vs-different-output smoke test: unvoweled Urdu consonant text (the
real-world case this mode exists for) decodes to garbage without the
preoption and to correctly-voweled Roman text with it, confirming the
ctx-based flag reaches the same branch the old marker did - plus a clean
16,126-sample corpus regen and the full pytest suite matching baseline.

## `͏` (COMBINING GRAPHEME JOINER)

Stripped by `PostProcess.defaultPost()` (`transliterate.py:542`, the
*other* end-of-pipeline safety net - runs after postoptions, whereas
`default()` above runs before). Single, simple use; no other file
references it as a marker today.
