# Docstrings needing human review

These 516 functions (out of 727 total) had no frontend UI label to source a description from, so their one-line docstrings were drafted by reading the code directly. Spot-check these against the actual conversion behavior before treating them as authoritative.

Frontend-sourced docstrings (211 functions, higher confidence) are not listed here.


## PostProcess.py

- **AmbigousTamilOrthography**: No-op placeholder (reserved for resolving ambiguous Tamil orthography).
- **AnusvaraToNasal**: Converts anusvara followed by a homorganic consonant into the corresponding nasal consonant plus virama (inverse of NasalToAnusvara).
- **AnusvaraToNasalIPA**: Converts the IPA nasalization diacritic before stops into the corresponding homorganic nasal consonant (velar/palatal/dental/retroflex), including after a length mark.
- **ArabicGimelGaGha**: Replaces Arabic jim with ghayn (renders Hebrew/Semitic 'ga' sound as Arabic 'gha').
- **ArabicGimelPaBa**: Replaces Arabic fa with ba (renders Hebrew/Semitic 'pa' sound as Arabic 'ba').
- **AvestanConventions**: Applies Avestan orthographic conventions: inserts nasalization before consonant clusters, softens word-final a before n/m, marks retroflex n before velars/dentals, selects consonant allophones before ii/uu vowels, and picks the ta variant by following context.
- **BalineseJavaneseMoveRepha**: Repositions the Balinese/Javanese repha (pre-base r) sign to follow the consonant cluster (and any anusvara-type sign) it modifies.
- **BalineseRomanLoCFix**: Fixes Balinese LoC romanization diacritics: h-diaeresis -> h, ng-diaeresis -> apostrophe-like sign.
- **BurmeseRomanLoCSource**: Reverses LoC Burmese romanization conventions back to native encoding: drops pure-virama marker, restores superscript-Ga to subjoined y/r/v/h, reassembles vowel+diacritic sequences, undoes glottal-stop marking.
- **BurmeseRomanLoCTarget**: Applies Library of Congress Burmese romanization target conventions: marks tone, folds 'au+glottal' to 'o+glottal', renders visarga as a tone mark, and substitutes a few adhoc lexical characters.
- **ChakmaAVowels**: No-op placeholder (reserved for Chakma inherent-vowel handling).
- **DevanagariAVowels**: Decomposes old-style independent Devanagari vowel letters into the inherent-a consonant carrier plus the corresponding dependent vowel sign.
- **DevanagariRomanLoCFix**: Fixes Devanagari LoC romanization diaeresis-marked digraphs: g-h-diaeresis -> g-underdot h-underdot, t-diaeresis -> t-underdot, s-diaeresis -> s-underdot, h-diaeresis -> h-underdot.
- **Dot2Dandas**: Converts double and single full-stop dots into Devanagari danda punctuation (.. -> double danda, . -> danda).
- **Dot2Pipes**: Converts double and single full-stop dots into ASCII pipe punctuation (.. -> ||, . -> |).
- **FixSemiticRoman**: Fixes Roman Semitic gemination notation (consonant+virama+same consonant -> gemination sign for Arabic-target output) and reorders emphatic-consonant nukta-equivalent markers around their vowel.
- **FixTallA**: Introduces the Tai Tham tall-a vowel sign after specified base or subjoined consonants (including through consonant clusters), and reverses it for consonants with protruding subjoined forms.
- **GurmukhiRomanLoCFix**: Converts nasalized m before homorganic stops into the corresponding nasal consonant (velar/palatal/retroflex/dental/labial) for Gurmukhi LoC romanization.
- **HebrewKatevMalei**: Replaces Hebrew qamats and patach vowel points with aleph, producing ktiv male (full/plene) spelling.
- **HebrewSBLSource**: No-op placeholder (reserved for SBL Hebrew romanization source-side processing).
- **HebrewSBLTarget**: Converts intermediate Hebrew romanization to SBL academic style (v->b-line-below, f->p-macron, d->d-line-below, g->g-line-below, t->t-line-below, o->o-circumflex, etc., undone when geminated).
- **HiraganaaunotDipthong**: No-op placeholder (reserved for preventing au from being read as a Hiragana diphthong).
- **IASTISONasalTilde**: No-op placeholder (reserved for IAST/ISO nasalization tilde handling).
- **IASTPali**: Converts the IAST underlined-l (l with line below) used for retroflex l to the standard Pali l-underdot.
- **IPARemoveCross**: Removes the multiplication-sign (x) marker character from IPA output.
- **ISO233Source**: No-op placeholder (reserved for ISO 233 Arabic romanization source-side processing).
- **ISO233Target**: Converts intermediate Arabic romanization to ISO 233 conventions (j/g->g-caron, h-diaeresis->t-diaeresis, nunation marks aN/iN/uN -> accented vowels, etc.).
- **ISO259Source**: No-op placeholder (reserved for ISO 259 Hebrew romanization source-side processing).
- **ISO259Target**: Converts intermediate Hebrew romanization to ISO 259 conventions (b/p/k dotted, v->b, f->p, s-caron variants, a->a-ring, e->e-cedilla, o/u macron to circumflex forms).
- **InsertGeminationSign**: Replaces consonant+virama+identical-consonant (and consonant+virama+its aspirated counterpart) sequences with a dedicated gemination sign.
- **JapanesePostProcess**: Runs the full Japanese post-processing pipeline (pivot to RomanKana, punctuation/nasalization fixes, consonant fixes, nativize branch, kana encoding) to produce Hiragana/Katakana output.
- **JavaneseRomanLoCFix**: Fixes Javanese LoC romanization diacritics: h-diaeresis -> h, ng-diaeresis -> apostrophe-like sign.
- **KhandaTa**: Forms the Bengali khanda ta (cluster-final ta, U+09CE) from ta+virama when not followed by a joining consonant, or reverses khanda ta back to ta+virama when reverse=True.
- **KhandaTaRomanLoC**: Converts LoC romanized t-line into the Bengali khanda ta letter.
- **KhmerLoCRomanLoCSource**: Reorders Khmer LoC romanization diacritics (bantoc, tone marks) relative to base consonants/vowels, marks subbase-form consonant modifiers, and strips the virama.
- **KhmerLoCRomanLoCTarget**: Normalizes Khmer LoC romanization output: NFC-normalizes, repositions consonant-modifier marks before certain vowels, fixes the 'oh' sequence, collapses double spaces.
- **LatinPipes**: No-op placeholder (reserved for converting pipe punctuation in Latin-script output).
- **LatnInitialVowels**: Replaces word-initial long-vowel forms (a-circumflex, i-macron-circumflex, etc.) with a leading marker letter plus the corresponding plain vowel; helper for the *izeLatn functions.
- **MToAnusvara**: Converts a word/syllable-final labial nasal consonant (ma+virama) not followed by another consonant into anusvara.
- **MalayalamAnusvaraNasal**: Converts anusvara to/from homorganic nasal consonants for Malayalam-specific consonant clusters, accounting for chillu letters.
- **MalayalamChillu**: Forms Malayalam chillu (pure, vowelless) consonant letters from consonant+virama in appropriate contexts, or reverses chillus back to consonant+virama when reverse=True.
- **MalayalamNTA**: Converts the n+ra sequence into n+t-line (Malayalam nta orthographic convention).
- **MalayalamRomanLoCFix**: Fixes Malayalam LoC romanization: doubled r-line -> doubled t-line, u-breve -> a-overdot.
- **MalayalamremoveHistorical**: Replaces the historical Malayalam na letter with the modern na, and the virama-joined na-chillu sequence with the standalone chillu-n.
- **MedievalTamilOrthography**: Restores medieval/pre-reform Tamil orthography for the e/o vowel signs (splits modern e/o/ee/oo forms into their older two-part equivalents).
- **MeeteiMayekremoveHistorical**: Replaces historical/obsolete Meetei Mayek letters and the diaeresis-marked cheitap ee/oo sequences with their modern equivalents.
- **ModiRemoveLong**: Converts long vowel signs and independent vowels in Modi script (i, u, r-vocalic and their vowel-sign forms) to their short equivalents.
- **MultaniAbjad**: Simplifies Multani abjad-style orthography by dropping vowels between consonants in CVC/consonant-cluster contexts, matching its abjad (consonant-only) spelling convention.
- **NasalToAnusvara**: Converts a homorganic nasal consonant followed by virama and a same-varga consonant into anusvara plus that consonant.
- **PersianDMGSBLSource**: No-op placeholder (reserved for Persian DMG romanization source-side processing).
- **PersianDMGTarget**: Converts intermediate Persian romanization to DMG (Deutsche Morgenlandische Gesellschaft) conventions (d-line->z-line, d-dot->z-dot, t-line->s-line-below, j->g-caron, y-macron->ye).
- **PhagsPaRearrange**: Inserts virama before word-final 'Phags-pa consonants (marked by trailing spaces), then converts remaining spaces and Mongolian-style punctuation into 'Phags-pa segment markers.
- **PhoneticMapping**: No-op placeholder (reserved for phonetic remapping).
- **RemoveDiacritics**: Strips a generic set of removable diacritic marks (GM.DiacriticsRemovable) from the string.
- **RemoveDiacriticsTamil**: Strips Tamil-specific removable diacritic marks (GM.DiacriticsRemovableTamil) from the string.
- **RemoveSchwa**: Inserts an explicit virama after script consonants that are not already followed by a vowel sign, suppressing the inherent /a/ (schwa) reading.
- **RetainDandasIndic**: Converts roman '.'/'..'  full stops to native single/double danda punctuation, or reverses danda back to '.'/'..' when reverse=True.
- **RetainGujaratiDanda**: Converts roman full stops to Gujarati danda punctuation.
- **RetainGurmukhiNumerals**: Converts Western Arabic digits to Gurmukhi numerals.
- **RetainIndicNumerals**: Converts Western Arabic digits to the target script's native numerals, or reverses native numerals back to Arabic digits when reverse=True.
- **RetainKannadaDanda**: Converts roman full stops to Kannada danda punctuation.
- **RetainKannadaNumerals**: Converts Western Arabic digits to Kannada numerals.
- **RetainMalayalamDanda**: Converts roman full stops to Malayalam danda punctuation.
- **RetainMalayalamNumerals**: Converts Western Arabic digits to Malayalam numerals.
- **RetainRomanNumerals**: Converts the target script's native numerals to Western Arabic digits, or reverses Arabic digits back to native numerals when reverse=True.
- **RetainTamilDanda**: Converts roman full stops to Tamil danda punctuation.
- **RetainTamilNumerals**: Converts Western Arabic digits to Tamil numerals.
- **RetainTeluguDanda**: Converts roman full stops to Telugu danda punctuation.
- **RetainTeluguNumerals**: Converts Western Arabic digits to Telugu numerals.
- **ReverseGeminationSign**: Expands a dedicated gemination sign back into consonant+virama+consonant (or its aspirated counterpart), inverse of InsertGeminationSign.
- **RomanLoCChandrabindu**: Converts chandrabindu-marked m before consonants into chandrabindu-marked n, per LoC romanization convention.
- **RomanLoCLaUnderscoreDoubleDot**: Replaces l-line-below with l-double-underdot, per LoC romanization convention.
- **RomanLoCSasha**: Replaces s-dot-below (sa) with sh, per LoC romanization convention.
- **RomanLoCVaWa**: Replaces v with w, per LoC romanization convention for scripts where va is rendered as w.
- **SaurashtraHaru**: Replaces specific Saurashtra consonant+virama+ha clusters with the dedicated haru (below-base h) sign.
- **ShanLoCRomanLoCSource**: Restores Shan LoC romanization conventions to native Shan script: undoes subjoined y/r/v marking, strips pure-vowel and glottal markers, reverses ai, and resolves open/closed vowel-consonant ambiguity.
- **ShanLoCRomanLoCTarget**: Reorders Shan LoC romanization glottal-stop and tone-mark combining diacritics relative to the preceding vowel/consonant.
- **SinhalaSannakaNasalization**: Converts Sinhala prenasalized n-breve/m-breve before homorganic consonants into the corresponding nasal consonant (velar/palatal/retroflex/dental/labial).
- **TaiKuen**: No-op placeholder (reserved for Tai Kuen script-specific post-processing).
- **TaiThamHighNga**: Replaces the low-register Tai Tham nga consonant with its high-register variant.
- **TaiThamLao**: No-op placeholder (reserved for Tai Tham Lao-variant post-processing).
- **TaiThamMoveNnga**: Repositions the Tai Tham high-register nga sign to follow the character it attaches to.
- **TaiThamO**: Merges the Tai Tham e-vowel-sign + aa-vowel-sign sequence into the single dedicated o vowel sign.
- **TamilSHADisable**: Replaces Tamil sha (Grantha letter) with sa followed by a superscript '2' marker, disabling the dedicated sha glyph.
- **ThaanaRemoveHistorical**: Replaces the historical Thaana letter naa (retroflex n) with the modern noonu letter.
- **ThaiLaoTranscription**: Bidirectionally converts between segmented Thai/Lao/LaoPali script forms and unsegmented encoded text: inserts/removes the inherent short-a vowel and its conjunct form, handles anusvara-to-nasal conversion, reorders pre-posed vowels around consonant+virama clusters, and fixes r/l vowel-swap and special consonant-cluster spellings (e.g. prahlada, sarva).
- **ThamLoCRomanLoCSource**: Converts Tai Tham LoC romanization back to native encoding: maps cryptogrammic dot to sakot, fixes the aiy vowel+consonant sequence.
- **ThamLoCRomanLoCTarget**: No-op placeholder (reserved for Tai Tham LoC romanization target-side processing).
- **TibetanLoCRomanLoCFix**: Fixes Tibetan LoC romanization: drops the modifier apostrophe on t/n unless followed by s/y respectively, and joins j_h into jh.
- **UrduAlternateUU**: Intended to replace a short-u+wow sequence with wow+hamza-below as an alternate Urdu spelling; the search string is a literal backslash-escaped text, not an actual Unicode sequence, so this currently has no effect.
- **VaToBa**: Replaces va with ba, for target scripts where the va and ba consonants have historically merged.
- **YYAEverywhere**: Replaces every occurrence of the plain ya consonant with the nukta-marked yya (antahstha ya) in the given target script.
- **YaToYYa**: Converts ya into the nukta-marked yya (antahstha ya) after a preceding letter, for scripts (Assamese, Bengali, Oriya, Chakma) that distinguish the two.
- **_japanese_empirical_consonant_fixes**: Applies empirical consonant-cluster fixes for naturalized Japanese romanization (tr/dr->tor/dor, tya/dya/sya palatalization spellings, di/du/ti/tu epenthetic vowels, ye/vye handling).
- **_japanese_encode_to_kana**: Encodes intermediate romanized Japanese text into Hiragana or Katakana via kana2roman, handling consonant/vowel gemination and choonpu (long-vowel) marks.
- **_japanese_nativize_branch_fix**: Branches Japanese post-processing on the nativize flag: resolves r/k gemination marks and applies tokushuon when not nativized, or simplifies yi/ye/wu/wo/she spellings when nativized.
- **_japanese_pivot_to_romankana**: Pivots Japanese text through Telugu/ISO/Inter intermediate scripts en route to a RomanKana representation.
- **_japanese_visarga_nasalization_punctuation**: Expands visarga into vowel-echoed h, assimilates nasal consonants before homorganic stops, and converts ASCII punctuation to Japanese full-width punctuation.
- **arabChaSa**: Replaces Arabic che with sin (renders Persian/Urdu 'cha' sound as Arabic 'sa').
- **arabPaFa**: Replaces Arabic pe with fa (renders Persian/Urdu 'pa' sound as Arabic 'fa').
- **arabizeLatn**: Converts generic Roman Semitic transliteration into Arabic-specific conventions, resolving hamza after consonants into a/a-macron/a-circumflex and normalizing glottal-stop marks.
- **default**: Strips internal token/placeholder characters (U+F001, U+05CC, doubled okina, U+05CD, U+02C2) used during specialized processing.
- **defaultPost**: Applies shared post-processing: numeral/danda retention per postoptions, then normalizes pipe/danda punctuation for the target script.
- **easternsyriac**: No-op placeholder (reserved for Eastern Syriac font-variant handling).
- **estrangelasyriac**: No-op placeholder (reserved for Estrangela Syriac font-variant handling).
- **hebraizeLatn**: Converts generic Roman Semitic transliteration into Hebrew-specific conventions by inserting aleph before word-initial vowels.
- **indicDandas**: No-op placeholder (reserved for the indicDandas post-option).
- **indicNumerals**: No-op placeholder (reserved for the indicNumerals post-option; numeral conversion is handled by RetainIndicNumerals).
- **insertARomanSemitic**: Inserts an inherent /a/ after Semitic consonants (and gemination marks) that are not already followed by an explicit vowel.
- **mDotBelowToAbove**: Converts dot-above anusvara back to dot-below (inverse of mDotAboveToBelow).
- **removeDiacriticsPersian**: No-op placeholder (reserved for stripping Persian diacritics).
- **removeDiacriticsSyriac**: No-op placeholder (reserved for stripping Syriac diacritics).
- **removeSemiticLetters**: Neutralizes emphatic/interdental Semitic consonant letters to plain Latin approximations (t-dot->t, h-dot->h, d-dot/d-line/z-dot->z, w->v, ayin->hamza, s-dot->s).
- **romanFullStop**: No-op placeholder (reserved for the romanFullStop post-option; danda conversion is handled by RetainDandasIndic).
- **romanNumerals**: No-op placeholder (reserved for the romanNumerals post-option; numeral conversion is handled by RetainRomanNumerals).
- **siddhamBija**: No-op placeholder (reserved for Siddham bija/seed-syllable rendering).
- **siddhamap**: No-op placeholder (reserved for Siddham-specific post-processing).
- **syriacVowelsBelow**: No-op placeholder (reserved for lowering Syriac vowel diacritics below the line).
- **syriacWesternOToU**: No-op placeholder (reserved for Western Syriac o-to-u vowel shift).
- **syricizeLatn**: Converts generic Roman Semitic transliteration into Syriac-specific conventions by expanding word-initial long a/e vowels back into hamza plus short vowel.
- **tbadiff**: Restores the khanda-ta+ba sequence to ta+virama+ba, distinguishing it from the regular khanda-ta merger.
- **tokushuon**: Applies Japanese tokushuon (special loanword kana) spelling conventions, e.g. si->suxi, zi->zuxi, yi->ixi, fy->fux, nye->nixe, and context-sensitive hu/hye expansions.
- **urduizeLatn**: Converts generic Roman Semitic transliteration into Urdu-specific conventions, resolving hamza into a/a-circumflex and normalizing glottal-stop marks to hamza.
- **useKtivMale**: No-op placeholder (reserved for switching Hebrew to ktiv male full spelling).
- **verticalSiddham**: No-op placeholder (reserved for vertical Siddham text layout).
- **westernsyriac**: No-op placeholder (reserved for Western Syriac font-variant handling).

## PreProcess.py

- **ArabizePersian**: Convert Persian-style kaf and ye (ک ی) back to their Arabic forms (ك ي).
- **ArchaicJnaSimplifyRomanLOC**: Simplify the archaic Javanese jnya glyph ꦘ to the standard nya glyph ꦚ.
- **BalineseJavaneseMoveRepha**: Reposition the repha (pre-base r) sign to follow its consonant cluster and vowel sign in Balinese/Javanese script.
- **BalineseRomanLoCFix**: Replace the left single quotation mark placeholder with ng̈ in Balinese LoC romanization.
- **BurmeseRomanLoCSource**: Normalize LoC Burmese romanization source text: expand ad hoc letter codes to Burmese punctuation, fix visarga/diacritic characters, convert comma/period to danda marks, and simplify o-quote sequences to au.
- **BurmeseRomanLoCTarget**: Apply Burmese LoC target-side normalization: merge asat+virama, reorder subjoined consonants, mark glottal-stop a and pure viramas, and convert dependent vowel+diacritic sequences to independent vowels.
- **DevanagariRomanLoCFix**: Normalize nukta-marked digraphs (g̳h̳, t̤, s̤, h̤) to their LoC diacritic forms for Devanagari romanization.
- **FixSemiticRoman**: Post-process romanized Semitic-script output: resolve aleph/ayin approximations, duplicate geminated consonants, dispatch to script-specific fixups (Arabic/Urdu/Syriac/Hebrew), delete schwas, and map Semitic-specific letters to their Indic-equivalent romanization.
- **HebrewSBLSource**: Reverse SBL Hebrew romanization symbols back to Hebrew letters, restoring begadkefat spirantization and vowel-length distinctions.
- **HebrewSBLTarget**: Substitute Hebrew aleph (א) and geresh (׳) with their SBL romanization symbols (ʾ, ’).
- **IASTLDotRetroflex**: Convert IAST ḷ (retroflex l) to l̤ for Library of Congress-style romanization.
- **IASTPali**: Convert IAST ḷ (retroflex l) to l̤ for Pali romanization.
- **IPAIndic**: Simplify IPA vowels ʊ and ɛ to u and e respectively (note: the function returns None instead of the string, a likely bug).
- **ISO233Source**: Reverse ISO 233 romanization symbols back to Arabic hamza letters and normalize additional consonant/vowel spellings (j/g → ǧ, etc.) on the source side.
- **ISO233Target**: Substitute Arabic hamza letters (أ ء إ) with their ISO 233 romanization symbols (ˈʾ, ¦, ˌʾ).
- **ISO259Source**: Reverse ISO 259 Hebrew romanization symbols back to Hebrew letters, restoring begadkefat forms and gemination marks via Unicode decomposition.
- **ISO259Target**: Substitute Hebrew aleph (א) and geresh (׳) with their ISO 259 romanization symbols (ʾ, ’).
- **ItransLL**: Placeholder pre-processing hook for the ITRANS-LL scheme (currently a no-op passthrough).
- **JapanesePreProcess**: Preprocess Japanese Hiragana/Katakana input by romanizing it via kakasi and normalizing the result into aksharamukha's internal representation.
- **JavaneseRomanLoCFix**: Replace the left single quotation mark placeholder with ng̈ in Javanese LoC romanization.
- **KhandaTaRomanLoC**: Render Bengali khanda ta (ৎ) as ṯ in Library of Congress romanization.
- **KhmerLoCRomanLoCSource**: Denormalize precomposed diacritic vowels to NFD and fix apostrophe/oaḥ sequences for Khmer LoC source text.
- **KhmerLoCRomanLoCTarget**: Apply Khmer LoC target-side fixes: mark the im vowel, reposition the bantoc sign, tag subscript consonant modifiers, reorder tone marks, normalize oya to oy, and drop decorative punctuation.
- **MalayalamRomanLoCFix**: Normalize ṯṯ to ṟṟ and ȧ to ŭ in Malayalam Library of Congress romanization.
- **PersianDMGTarget**: Substitute Persian alef (ا) with the DMG romanization symbol ʾ.
- **PreProcess**: Master pre-processing dispatcher: apply source-script-specific normalizations (case folding, punctuation, alternate schemes like ITRANS/Baraha, diacritic reordering, Unicode normalization) before script conversion begins.
- **RemoveFinal**: Delete the inherent schwa vowel from a word-final consonant (e.g. kama → kam) for the given target script, with special-casing for Khmer and Bengali.
- **RemoveJoiners**: Strip zero-width joiner and zero-width non-joiner characters from the string.
- **RetainDevangariDanda**: Temporarily substitute Devanagari danda/double danda with placeholder box-drawing characters to protect them from further processing.
- **RetainPipeDanda**: Convert pipe-notated danda/double-danda and periods into placeholder characters to protect them during processing.
- **RomanLoCChandrabindu**: Normalize candrabindu written as n̐ to m̐ for Library of Congress romanization.
- **RomanLoCLaUnderscoreDoubleDot**: Convert ḻ to l̤ (or back to ḻ) for Library of Congress romanization depending on direction.
- **RomanLoCSasha**: Replace sh with ṣ for Library of Congress romanization.
- **RomanLoCVaWa**: Replace w with v for Library of Congress romanization, reflecting the va/wa merger.
- **RomanPreFix**: Insert explicit dependent-vowel and virama markers after bare consonants in romanized source text so it matches the internal consonant-vowel representation, handling nukta placement.
- **SanskritLexicaizeHK**: Placeholder pre-processing hook for lexicalizing Sanskrit in Harvard-Kyoto (currently a no-op passthrough).
- **SchwaFinalKhmer**: Delete the word-final inherent schwa vowel for Khmer script output.
- **SchwaFinalKhmerLoC**: Delete the word-final inherent schwa vowel for Khmer Library of Congress romanization.
- **ShanLoCRomanLoCSource**: Placeholder Shan LoC source-side hook (currently a no-op passthrough).
- **ShanLoCRomanLoCTarget**: Apply Shan LoC target-side normalization: unify /aa/ vowel spellings, merge asat+virama, reorder subjoined consonants, and mark glottal-stop a and pure viramas.
- **TaiKuen**: Placeholder Tai Khuen pre-processing hook (currently a no-op passthrough).
- **TaiThamLao**: Placeholder Tai Tham Lao pre-processing hook (currently a no-op passthrough).
- **ThamLoCRomanLoCSource**: Insert a modifier-letter apostrophe before consonants following bare vowels, and expand ʻ to a+vowel-killer, for Tai Tham LoC source text.
- **ThamLoCRomanLoCTarget**: Apply Tai Tham LoC target-side vowel fixes for o/eo/aiy/koi/au sequences, the lue-karan sign, and vowel-killer marking.
- **TibetanLoCRomanLoCFix**: Insert LoC prime marks after bare t and n consonants not already followed by a diacritic, for Tibetan romanization.
- **UnSupThaana**: Placeholder Thaana pre-processing hook for unsupported characters (currently a no-op passthrough).
- **_get_kakasi**: Lazily construct and return a cached pykakasi kana-to-Hepburn romanization converter instance.
- **_japanese_kakasi_romanize**: Convert lowered internal ISO-romanized text to Devanagari, then run it through pykakasi to produce space-joined Hepburn romanization.
- **_japanese_normalize_romanization**: Normalize kakasi's Hepburn romanization output into aksharamukha's internal scheme: merge long vowels, convert digraphs (ch/sh), apply nasalization rules, and honor eiaudipthongs/wasvnukta options.
- **default**: Default no-op pre-processing option that passes the string through unchanged.
- **joinVowelCons**: Merge space-separated consonant+vowel and consonant+consonant sequences back together for the given script.
- **normalize**: Normalize Unicode variants across supported scripts: precompose nukta consonants and vowel signs, fold decomposed/alternate spellings to canonical forms, and standardize script-specific quirks (chillus, ligatures, danda, vowel-sign ordering) before conversion.
- **paliTham**: Placeholder Pali-in-Tai-Tham pre-processing hook (currently a no-op passthrough).
- **perisanizeArab**: Convert Arabic-style kaf and ye (ك ي) to their Persian forms (ک ی).
- **removeChillus**: Expand Malayalam chillu letters (ൺ ൻ ർ ൽ ൾ) into their base consonant plus virama form.
- **removeZW**: Remove zero-width non-joiner and zero-width joiner characters (note: the .replace() calls here are missing their replacement argument and will raise a TypeError, a likely bug).
- **retainLatin**: Temporarily map plain Latin letters to private-use codepoints to shield them from script conversion, with a reverse flag to restore them.
- **semiticizeUrdu**: Convert Urdu-specific letters (ے ڈ ٹ ہ) to their generic Arabic/Semitic equivalents (ي د ت ه) and strip the do-chashme-he (ھ).
- **siddhamUnicode**: Placeholder Siddham Unicode pre-processing hook (currently a no-op passthrough).

## ScriptProcessing/Ahom.py

- **AhomClosed**: Converts open Ahom vowel signs for i, u, e, and o into their closed-syllable forms before a final consonant or anusvara.
- **FixAhom**: Dispatches to the Ahom encode or decode fix-up routine based on the reverse flag.
- **_FixAhomDecode**: Reverses Ahom encoding fixes: splits merged ligatures, reconstructs closed-syllable e/o forms, and restores vowel-before-anusvara order.
- **_FixAhomEncode**: Reorders Ahom vowel signs and anusvara into correct visual order and merges two consonant+vowel sequences into single ligature characters.

## ScriptProcessing/Arab.py

- **ArabRemoveAdditions**: Reverts extended Arabic letters back to their standard base forms: ڨ→ج, ڤ→ف, پ→ف.
- **FixArab**: Dispatches to the Arabic encode or decode fix routine depending on conversion direction.
- **_FixArabDecode**: Reverses Perso-Arabic punctuation, normalizes alef/tatweel, and reorders shadda-kasra when decoding from Arabic.
- **_FixArabEncode**: Applies Perso-Arabic punctuation normalization when encoding text into Arabic script.

## ScriptProcessing/Arab_Fa.py

- **FixArab_Fa**: Applies the shared Perso-Arabic script fixes (via ConvertFix.FixArab) used for Farsi text.

## ScriptProcessing/Arab_Ur.py

- **FixArab_Ur**: Dispatches to the Urdu Arabic-script encode or decode fix-up routine based on the reverse flag.
- **_FixArab_UrDecode**: Applies the shared Arabic fix-up logic (via ConvertFix.FixArab) when decoding text out of the Urdu Perso-Arabic script.
- **_FixArab_UrEncode**: Applies the shared Arabic fix-up logic (via ConvertFix.FixArab) when encoding text into the Urdu Perso-Arabic script.

## ScriptProcessing/Assamese.py

- **FixAssamese**: Dispatches to the Assamese encode or decode fix routine based on the reverse flag.
- **_FixAssameseDecode**: Reverses the khanda-ta fix and converts the Assamese ra form (ৰ) back to standard ra when decoding out of Assamese.
- **_FixAssameseEncode**: Applies the khanda-ta fix and converts standard ra to the Assamese ra form (ৰ) when encoding into Assamese.

## ScriptProcessing/Avestan.py

- **FixAvestan**: Dispatches to the Avestan encode or decode fix routine depending on the reverse flag.
- **_FixAvestanDecode**: Reverses Avestan orthographic fixes, expanding the aM/AM, ii/uu, and TTE/BHA/ZHA/NGVA/AO ligatures back into their component sequences.
- **_FixAvestanEncode**: Applies Avestan orthographic fixes: aM/AM ligatures, ya/va to long ii/uu after vowels or consonants, and TTE/BHA/ZHA/NGVA/AO ligature substitutions.

## ScriptProcessing/Balinese.py

- **BalineseMoveRepha_post**: Post-processing step that repositions the Balinese repha sign (ᬃ) back to its rendered position.
- **BalineseMoveRepha_pre**: Pre-processing step that repositions the Balinese repha sign (ᬃ) relative to its base consonant.
- **FixBalinese**: Dispatches to the Balinese encode or decode fix routine depending on conversion direction.
- **_FixBalineseDecode**: Removes the Balinese repha sign, expands the archaic jña ligature, and converts a-based vowel spellings back to precomposed independent vowels when decoding.
- **_FixBalineseEncode**: Inserts the Balinese repha sign (preposed ra) when encoding text into Balinese script.

## ScriptProcessing/BatakSima.py

- **FixBatakSima**: Dispatches to the Simalungun Batak encode or decode fix-up routine based on the reverse flag.
- **_FixBatakSimaDecode**: Replaces the Simalungun Batak sequence ᯙᯯ back with the standard vowel-sign-U form ᯙᯮ when decoding.
- **_FixBatakSimaEncode**: Replaces the vowel-sign-U sequence ᯙᯮ with the Simalungun Batak equivalent ᯙᯯ when encoding.

## ScriptProcessing/Bengali.py

- **BengaliConjunctVB**: Merges ZWNJ-separated virama+ba clusters into a normal conjunct (so kva/kba render alike) and converts khanda-ta+ba to ta+virama+ba.
- **FixBengali**: Dispatches to the Bengali encode or decode fix routine based on the reverse flag.
- **_FixBengaliDecode**: Reverses the khanda-ta fix when decoding out of Bengali.
- **_FixBengaliEncode**: Inserts a ZWNJ before bare ba after a virama, fixes subjoined bva rendered as va-with-nukta, and applies the khanda-ta fix when encoding into Bengali.

## ScriptProcessing/Bhaiksuki.py

- **FixBhaiksuki**: Dispatches to the Bhaiksuki encode or decode fix routine depending on the reverse flag.
- **_FixBhaiksukiDecode**: Replaces the Bhaiksuki word-divider punctuation mark with a plain ASCII space.
- **_FixBhaiksukiEncode**: Replaces the plain ASCII space with the Bhaiksuki word-divider punctuation mark.

## ScriptProcessing/Buginese.py

- **FixBuginese**: Dispatches to the Buginese encode or decode fix-up routine based on the reverse flag.
- **_FixBugineseDecode**: Expands merged Buginese prenasalized consonants (e.g. ᨃ→ᨂʾᨀ) back into their component consonant sequences.
- **_FixBugineseEncode**: Merges prenasalized consonant sequences (e.g. ᨂʾᨀ→ᨃ) into single letters, inserts the gemination sign, and strips glottal-stop markers.

## ScriptProcessing/Buhid.py

- **FixBuhid**: Dispatches to the Buhid encode or decode fix-up routine based on the reverse flag.
- **_FixBuhidDecode**: No-op decode step for Buhid script; gemination-sign removal is currently unimplemented.
- **_FixBuhidEncode**: Inserts the Buhid gemination sign into the string when encoding into Buhid script.

## ScriptProcessing/Burmese.py

- **FixBurmese**: Dispatches to the Burmese encode or decode fix routine depending on conversion direction.
- **_FixBurmeseDecode**: Reverses Burmese encoding fixes: expands subjoined consonants, kinzi, repha, tall-a, and medials back to explicit virama sequences.
- **_FixBurmeseEncode**: Encodes Burmese script orthography: converts virama to subjoined forms, inserts kinzi/repha, forms tall-a, reorders medials, and applies script-specific ligatures.

## ScriptProcessing/Chakma.py

- **ChakmaGemination**: Applies or reverses Chakma consonant gemination rules involving explicit and subjoining virama forms before vowel signs.
- **ChakmaPali_post**: Post-processes Chakma Pali text: reverses gemination and Ya/vA substitutions, then maps vowel-A to visarga and subjoined consonants to explicit virama per Pali convention.
- **ChakmaPali_pre**: Pre-processes Chakma text for Pali conversion by normalizing Ya/vA consonant forms and inserting the inherent vowel-A sign where absent.
- **FixChakma**: Dispatches to the Chakma encode or decode fix routine depending on the reverse flag.
- **_FixChakmaDecode**: Reverses Chakma inherent vowel-A insertion, ai/ei ligature formation, gemination, and y/r/l/n subjoining-virama rules back to their component forms.
- **_FixChakmaEncode**: Inserts the Chakma inherent vowel-A sign (Chakma's default vowel being AA), forms ai/ei ligatures, subjoins virama before y/r/l/n, and applies consonant gemination.

## ScriptProcessing/Cham.py

- **FixCham**: Dispatches to the Cham encode or decode fix-up routine based on the reverse flag.
- **_FixChamDecode**: Reverses Cham subjoined consonant ligatures and final-h forms when decoding; the non-final-to-final consonant merge is not reversible.
- **_FixChamEncode**: Forms Cham subjoined consonant ligatures (ya/ra/la/va), converts consonants to word-final forms before virama, and builds final-h (ꩍ) forms.

## ScriptProcessing/Devanagari.py

- **AnuChandraEq**: Converts the chandrabindu to the anusvara for the given script, treating the two as equivalent.
- **FixDevanagari**: Dispatches to the Devanagari encode or decode fix routine depending on conversion direction.
- **_FixDevanagariDecode**: Strips the schwa accent, reverses Prishthamatra vowel-sign spelling, and decodes ॽ, ॹ, and Sindhi implosive letters to their approximate spellings.
- **_FixDevanagariEncode**: Maps ʔ and Sindhi implosive letters to Devanagari equivalents, blocks RRA from forming conjuncts (except before ya/ha), and encodes apostrophe-marked Kashmiri oe/ooe vowels.

## ScriptProcessing/DevanagariLimbu.py

- **LimbuDevanagariConvention_post**: Restores Limbu-convention short e/o and visarga codepoints back to standard Devanagari nukta forms after processing.
- **LimbuDevanagariConvention_pre**: Converts Devanagari short e/o (nukta forms) and visarga to Limbu-convention codepoints (ऎ/ऒ/ॆ/ॊ/꞉) before processing.

## ScriptProcessing/DivesAkuru.py

- **DivesAkuruAlternateIndVowels_post**: Expands standalone Dives Akuru independent vowels into y-based sequences and switches to the alternate ya glyph (e.g. 𑤁→𑤥𑤰).
- **DivesAkuruAlternateIndVowels_pre**: Collapses y-based vowel sequences (e.g. 𑤥𑤰) into their standalone Dives Akuru independent vowel letters (e.g. 𑤁).
- **FixDivesAkuru**: Dispatches to the Dives Akuru encode or decode fix-up routine based on the reverse flag.
- **_FixDivesAkuruDecode**: Reverses Dives Akuru homorganic nasal signs, subjoining virama, alternate ya, and repha/subjoined-ya conjuncts back to explicit sequences.
- **_FixDivesAkuruEncode**: Converts explicit virama+consonant into subjoining virama and forms special ra/ya conjuncts (repha, subjoined ya) for Dives Akuru.

## ScriptProcessing/Grantha.py

- **FixGrantha**: Dispatches to the Grantha encode or decode fix-up routine based on the reverse flag.
- **_FixGranthaDecode**: Reverses the Grantha-specific accent, anusvara, and ZWNJ mappings applied during encoding when decoding back to the internal representation.
- **_FixGranthaEncode**: Maps accent and anusvara-variant marks to Grantha-specific Unicode codepoints and inserts a ZWNJ after visarga-virama when encoding.

## ScriptProcessing/Gujarati.py

- **FixGujarati**: Dispatches to the Gujarati encode or decode fix routine depending on conversion direction.
- **_FixGujaratiDecode**: Retains Indic dandas and expands the Gujarati letter ૹ back into nukta-marked ja/sha when decoding.
- **_FixGujaratiEncode**: Retains Indic dandas and merges nukta-marked ja/sha into the dedicated Gujarati letter ૹ when encoding.

## ScriptProcessing/GunjalaGondi.py

- **FixGunjalaGondi**: Dispatches to the Gunjala Gondi encode or decode fix routine based on the reverse flag.
- **_FixGunjalaGondiDecode**: Currently a no-op decode fix for Gunjala Gondi; returns the string unchanged.
- **_FixGunjalaGondiEncode**: Merges apostrophe-marked vowel-sign sequences into the dedicated Gunjala Gondi combining sign, strips the modifier apostrophes, and drops a trailing virama not followed by a consonant.

## ScriptProcessing/Gurmukhi.py

- **FixGurmukhi**: Dispatches to the Gurmukhi encode or decode fix routine depending on the reverse flag.
- **GurmukhiCandrabindu**: Replaces the Gurmukhi candrabindu sign (ਁ) with anusvara (ਂ), since Gurmukhi does not distinguish them.
- **GurmukhiTippiBindu**: Converts Gurmukhi Bindu (ਂ) to Tippi (ੰ) after specific consonants, vowels, and vowel signs where Tippi is conventional.
- **GurmukhiTippiGemination**: Replaces the Addak gemination mark (ੱ) with Tippi before ਨ or ਮ, reflecting pronunciation of geminated nasals.
- **_FixGurmukhiDecode**: Reverses Gurmukhi encoding fixes: RU/LU vowel correction, Indic numerals, gemination sign, nn/mm-halant normalization, Tippi-to-Bindu, and Yakaash conjuncts.
- **_FixGurmukhiEncode**: Applies Gurmukhi encoding fixes: RU/LU vowel correction, doubled Aunkar to bracketed AA, gemination-sign insertion, Indic-numeral retention, and Vedic svara consonant doubling.

## ScriptProcessing/GurmukhiLoC.py

- **FixGurmukhiLoC**: Dispatches to the Gurmukhi LoC encode or decode fix routine based on the reverse flag.
- **_FixGurmukhiLoCDecode**: Reverses ru/lu correction, restores the doubled ava sign from parenthesized ā, retains Indic numerals, and reverses the gemination sign for LoC Gurmukhi decoding.
- **_FixGurmukhiLoCEncode**: Corrects ru/lu vowel signs, collapses a doubled ava sign into parenthesized ā, inserts the gemination sign, retains Indic numerals, and expands addak+Vedic-svara sequences for LoC Gurmukhi encoding.

## ScriptProcessing/HanifiRohingya.py

- **FixHanifiRohingya**: Dispatches to the Hanifi Rohingya encode or decode fix routine depending on conversion direction.
- **_FixHanifiRohingyaDecode**: Reverses Hanifi Rohingya encoding: removes vowel carriers, expands gemination and diphthongs, and restores tone marks and punctuation.
- **_FixHanifiRohingyaEncode**: Encodes Hanifi Rohingya orthography: inserts vowel carriers, gemination marks, diphthong signs, tone letters, sukun, and Perso-Arabic punctuation.
- **_hanifi_rohingya_lookups**: Builds regex character-class strings for Hanifi Rohingya consonants and vowels used by the encode/decode fixers.

## ScriptProcessing/Hebr.py

- **FixHebr**: Dispatches to the Hebrew encode or decode fix-up routine based on the reverse flag.
- **_FixHebrDecode**: Moves the Hebrew geresh (׳) mark back to appear before adjacent vowel points when decoding.
- **_FixHebrEncode**: Moves the Hebrew geresh (׳) mark to appear after adjacent vowel points instead of before them when encoding.

## ScriptProcessing/Hebrew.py

- **FixHebrew**: Dispatches to the Hebrew encode or decode fix routine based on the reverse flag.
- **HebrewVetVav**: Converts vav to vet after short vowels when not followed by a dagesh, and normalizes bet+holam sequences.
- **HebrewnonFinalShort**: Marks a short vowel on a word-final letter by temporarily inserting a helper heh, then restores the corresponding final (sofit) consonant form once resolved.
- **_FixHebrewDecode**: Reconstructs the internal representation from surface Hebrew script: restores final letters to medial forms, reorders diacritics, approximates missing consonant/vowel distinctions, expands dagesh gemination, and resolves shva na versus shva nach.
- **_FixHebrewEncode**: Builds surface Hebrew script from the internal representation: inserts default patah, fixes nasal assimilation before certain consonants, reorders dagesh/vowel diacritics, marks gemination with dagesh, and applies final letter forms.

## ScriptProcessing/IAST.py

- **FixIAST**: Dispatches to the IAST encode or decode fix-up routine based on the reverse flag.
- **RomanLoCSLaDotLaUnderscore_post**: Reverses the LoC-style ḻ diacritic substitution, restoring the standard ḻ representation.
- **RomanLoCSLaDotLaUnderscore_pre**: Converts the IAST ḻ (la with dot below) to an l+diaeresis-below form and normalizes an l+underscore variant to ḻ, for LoC-style romanization.
- **_FixIASTDecode**: Normalizes the alternate IAST anusvara spelling ṁ to the standard m-with-dot-below form.
- **_FixIASTEncode**: No-op placeholder for IAST encoding; returns the string unchanged.

## ScriptProcessing/IPA.py

- **FixIPA**: Dispatches to the IPA encode or decode fix routine depending on conversion direction.
- **_FixIPADecode**: Reverses IPA encoding fixes: restores tilde/length-mark order and removes the visarga echo vowel.
- **_FixIPAEncode**: Reorders tilde before the length mark, appends a short echo vowel after visarga-derived h, and fixes a schwa ligature when encoding to IPA.

## ScriptProcessing/Itrans.py

- **swapEeItrans_post**: Post-processing step that restores ITRANS e/o vowel distinctions, mapping short vowels to lowercase and long vowels to uppercase E/O.
- **swapEeItrans_pre**: Pre-processing step that temporarily swaps ITRANS 'e'/'o' and '^e'/'^o' markers to disambiguate short and long e/o vowels before conversion.

## ScriptProcessing/Javanese.py

- **FixJavanese**: Dispatches to the Javanese encode or decode fix routine depending on conversion direction.
- **JavaneseMoveRepha_post**: Post-processing step that repositions the Javanese repha sign (ꦂ) back to its rendered position.
- **JavaneseMoveRepha_pre**: Pre-processing step that repositions the Javanese repha sign (ꦂ) relative to its base consonant.
- **_FixJavaneseDecode**: Removes the Javanese repha, expands the archaic jña and ra agung letters, restores subjoining cakra/pengkal forms to virama+consonant, and reverses a-based vowel spellings.
- **_FixJavaneseEncode**: Inserts the Javanese repha and converts virama+ra/ya sequences into the subjoining cakra/pengkal forms when encoding.

## ScriptProcessing/Kaithi.py

- **FixKaithi**: Dispatches to the Kaithi encode or decode fix routine depending on conversion direction.
- **_FixKaithiDecode**: Replaces the Kaithi word separator ⸱ with a space when decoding.
- **_FixKaithiEncode**: Replaces spaces with the Kaithi word separator ⸱ when encoding.

## ScriptProcessing/Kannada.py

- **FixKannada**: Dispatches to the Kannada encode or decode fix-up routine based on the reverse flag.
- **_FixKannadaDecode**: Restores Indic dandas to their generic forms when decoding out of Kannada script.
- **_FixKannadaEncode**: Retains Indic dandas and inserts a ZWNJ before a nukta after virama (except before pha/ja) when encoding into Kannada.

## ScriptProcessing/Kawi.py

- **FixKawi**: Dispatches to the Kawi encode or decode fix routine depending on the reverse flag.
- **KawiMoveRepha_post**: Moves the Kawi repha (superscript RA) mark from after back to before the consonant/vowel cluster it modifies, reversing the rendering-order adjustment.
- **KawiMoveRepha_pre**: Moves the Kawi repha (superscript RA) mark from before to after the consonant/vowel cluster it modifies, for correct rendering order.
- **_FixKawiDecode**: Reverses Kawi encoding rules: expands subjoining virama and repha, normalizes alternate tall-A, decomposes JÑA and independent i/u/e vowels, and splits alternate ai/au ligatures.
- **_FixKawiEncode**: Applies Kawi encoding rules: subjoining virama+consonant, ra-repha formation, and disambiguating the tall-A vowel sign after specific consonant clusters.

## ScriptProcessing/KhamtiShan.py

- **FixKhamtiShan**: Dispatches to the Khamti Shan encode or decode fix-up routine based on the reverse flag.
- **_FixKhamtiShanDecode**: Reverses Khamti Shan medial sign conversions back into virama+ra/ya/wa consonant sequences.
- **_FixKhamtiShanEncode**: Converts virama+ra/ya/wa consonant sequences into Myanmar medial signs and reorders medial-sign combinations for Khamti Shan encoding.

## ScriptProcessing/Kharoshthi.py

- **FixKharoshthi**: Converts decimal numerals in the text to or from Kharoshthi numeral notation.
- **KharoshthiNumerals**: Finds decimal numbers in the text and converts them to Kharoshthi additive numerals, or reverses Kharoshthi digits back to decimal.
- **kharoshthiNumber**: Converts a single integer into its Kharoshthi additive numeral representation using thousand/hundred/twenty/ten/unit signs.

## ScriptProcessing/Khmer.py

- **FixKhmer**: Dispatches to the Khmer encode or decode fix routine depending on conversion direction.
- **_FixKhmerDecode**: Expands the subjoining coeng mark back to explicit virama, restores the ra-repha ligature to ra+virama+consonant, and splits the i-anusvara ligature apart.
- **_FixKhmerEncode**: Converts virama+consonant sequences to the subjoining coeng form, introduces the ra-repha ligature, and merges the i vowel sign with anusvara into their ligature.

## ScriptProcessing/KhmerLoC.py

- **FixKhmerLoC**: Applies the shared Khmer fix-up logic (via ConvertFix.FixKhmer) targeting the Library of Congress romanization scheme.

## ScriptProcessing/Khojki.py

- **FixKhojki**: Dispatches to the Khojki encode or decode fix routine based on the reverse flag.
- **KhojkiRRI**: Decomposes the Khojki vocalic RI/RII ligature characters into their constituent letter sequences.
- **_FixKhojkiDecode**: Reverses the word separator, Sindhi consonant substitution, shadda/nukta ordering, and gemination sign transformations applied when encoding Khojki.
- **_FixKhojkiEncode**: Converts approximated Sindhi consonant sequences to their dedicated Khojki characters, inserts the gemination sign, moves shadda after its consonant, reorders shadda+nukta, and encodes spaces as the Khojki word separator.

## ScriptProcessing/KhomThai.py

- **FixKhomThai**: Dispatches to the Khom Thai encode or decode fix routine depending on conversion direction.
- **_FixKhomThaiDecode**: Reverses Khom Thai encoding fixes: restores vowel sign order and collapses เา back into the โ ligature.
- **_FixKhomThaiEncode**: Encodes Khom Thai orthography: expands the โ ligature, reverses vowel sign order, and reorders sara-ai/repha clusters around subscript consonants.

## ScriptProcessing/Khudawadi.py

- **FixKhudawadi**: Dispatches to the Khudawadi encode or decode fix-up routine based on the reverse flag.
- **_FixKhudawadiDecode**: Converts precomposed Khudawadi implosive letters back into their approximated Sindhi digraph form when decoding.
- **_FixKhudawadiEncode**: Converts approximated Sindhi implosive-consonant digraphs (e.g. ˍ𑊼) into their precomposed Khudawadi implosive letters when encoding.

## ScriptProcessing/KhuenTham.py

- **FixKhuenTham**: Applies the shared Tai Tham family fix-up, with ra-haam swap enabled, for Khuen Tham script conversion.

## ScriptProcessing/Lao.py

- **FixLao**: Dispatches to the Lao encode or decode fix routine depending on the reverse flag.
- **LaoTranscribe**: Applies or reverses Lao short-a/conjunct-a transcription rules via the shared Thai/Lao transcription routine.
- **_FixLaoDecode**: Reverses Lao encoding fixes: restores aspirate consonants from their unaspirated pseudo-nukta forms, restores vowel-sign order, reverses transcription, and splits the AM ligature back to AA+Anusvara.
- **_FixLaoEncode**: Applies Lao encoding fixes: maps aspirate consonants marked with a pseudo-nukta to their unaspirated forms, reverses vowel-sign order, transcribes tone/vowel spelling, and merges AA+Anusvara into the AM ligature.

## ScriptProcessing/Lao2.py

- **FixLao2**: Delegates Lao2 script fix-up to the shared Lao encode/decode logic.

## ScriptProcessing/LaoPali.py

- **FixLaoPali**: Dispatches to the Lao Pali encode or decode fix routine depending on conversion direction.
- **LaoPaliTranscribe**: Converts between orthographic and colloquial Lao phonetic transcription using the short-a and conjunct short-a signs.
- **LaoPhonetic_post**: Post-processes Lao phonetic text: reorders subjoined y/r/l/v/h consonants, reapplies transcription, and restores native consonant letters (ທ→ດ, ພ→ບ).
- **LaoPhonetic_pre**: Applies Lao phonetic normalization before conversion: ດ→ທ, ບ→ພ, drops the nikkhahit off ງໍ, and strips a combining mark.
- **LaoTranscription_post**: Post-processing step that applies Lao Pali transcription and removes the short-a sign before a final virama-like mark.
- **LaoTranscription_pre**: Placeholder pre-processing step for Lao transcription mode; currently a no-op.
- **_FixLaoPaliDecode**: Decodes Lao Pali text: restores vowel sign order, optionally applies phonetic transcription, and expands the AM vowel sign back into AA+anusvara.
- **_FixLaoPaliEncode**: Encodes Lao Pali text: reverses vowel sign order, optionally applies phonetic transcription, and ligates AA+anusvara into the AM vowel sign.

## ScriptProcessing/LaoTham.py

- **FixLaoTham**: Applies the shared Tai Tham script orthographic fixes (via ConvertFix.FixTaiTham) used for the Lao Tham variant.

## ScriptProcessing/Latn.py

- **FixLatn**: Dispatches to the Latin-script encode or decode fix-up routine based on the reverse flag.
- **_FixLatnDecode**: Reorders visarga back before a preceding vowel or combining mark when decoding out of Latin script.
- **_FixLatnEncode**: Reorders visarga to precede an adjacent vowel or combining mark and strips a spurious 'a' before an aspiration marker when encoding to Latin.

## ScriptProcessing/Lepcha.py

- **FixLepcha**: Dispatches to the Lepcha encode or decode fix-up routine based on the reverse flag.
- **_FixLepchaDecode**: Reverses Lepcha subjoined consonant clusters and rang vowel-sign reordering; word-final consonant merging is not reversible.
- **_FixLepchaEncode**: Forms Lepcha subjoined consonant clusters, converts consonants to their word-final forms, and reorders the rang vowel sign around final consonants.

## ScriptProcessing/Limbu.py

- **FixLimbu**: Dispatches to the Limbu encode or decode fix routine depending on conversion direction.
- **LimbuSpellingSaI_post**: Post-processing step that removes the sa-i sign prefix from Limbu final-consonant letters, restoring the standard consonant+virama spelling.
- **LimbuSpellingSaI_pre**: Pre-processing step that prefixes Limbu final-consonant letters with the sa-i sign for an alternate spelling convention.
- **LimburemoveHistorical**: Replaces obsolete/historical Limbu letter pairs with their modern equivalents.
- **_FixLimbuDecode**: Reverses subjoined and dedicated final-consonant letters back to virama sequences, and restores Limbu punctuation to ASCII equivalents.
- **_FixLimbuEncode**: Converts virama+ya/ra/va to subjoined consonant letters, maps consonant+virama to dedicated Limbu final-consonant letters, and substitutes punctuation with Limbu equivalents.

## ScriptProcessing/LimbuLoC.py

- **FixLimbuLoC**: Dispatches to the Limbu LoC encode or decode fix routine based on the reverse flag.
- **_FixLimbuLoCDecode**: Applies the shared Limbu orthographic fix routine when decoding out of Limbu, then maps glottal-stop and length markers to LoC-specific symbols.
- **_FixLimbuLoCEncode**: Applies the shared Limbu orthographic fix routine when encoding into Limbu for the LoC romanization.

## ScriptProcessing/LueTham.py

- **FixLueTham**: Applies the shared Tai Tham family fix-up, without ra-haam swap, for Lue Tham script conversion.

## ScriptProcessing/Mahajani.py

- **FixMahajani**: Dispatches to the Mahajani encode or decode fix routine depending on the reverse flag.
- **_FixMahajaniDecode**: Expands the Mahajani rupee-sign Unicode ligature back into its multi-character component sequence.
- **_FixMahajaniEncode**: Converts the multi-character Mahajani rupee-sign sequence into its single Unicode ligature and strips joiner marks.

## ScriptProcessing/Makasar.py

- **FixMakasar**: Dispatches to the Makasar encode or decode fix-up routine based on the reverse flag.
- **_FixMakasarDecode**: Expands the Makasar killer sign (Anka) marking a doubled consonant back into the repeated consonant sequence.
- **_FixMakasarEncode**: Inserts the gemination sign and collapses a doubled Makasar consonant into a single consonant plus the killer sign (Anka).

## ScriptProcessing/Malayalam.py

- **FixMalayalam**: Dispatches to the Malayalam encode or decode fix-up routine based on the reverse flag.
- **MalayalamPrakrit_post**: Converts anusvara to the Prakrit anusvara-above character and inserts gemination marks after Prakrit-specific processing.
- **MalayalamPrakrit_pre**: Reverses gemination marks and converts the Prakrit anusvara-above character to a regular anusvara before Prakrit-specific processing.
- **_FixMalayalamDecode**: Expands chillu codepoints and archaic chillu letters back to consonant-plus-virama form and restores dandas/numerals when decoding out of Malayalam.
- **_FixMalayalamEncode**: Converts chillu consonants to their Unicode chillu codepoints and retains Malayalam dandas and numerals when encoding into Malayalam.

## ScriptProcessing/Marchen.py

- **FixMarchen**: Dispatches to the Marchen encode or decode fix routine based on the reverse flag.
- **_FixMarchenDecode**: Converts Sanskrit tsa-series letters to their ja-series equivalents and expands Marchen subjoined letters back into glottal-marker+consonant sequences.
- **_FixMarchenEncode**: Converts glottal-stop-prefixed consonant markers into their dedicated Marchen subjoined letters and strips leftover marker characters.

## ScriptProcessing/MasaramGondi.py

- **FixMasaramGondi**: Dispatches to the Masaram Gondi encode or decode fix routine depending on conversion direction.
- **_FixMasaramGondiDecode**: Expands the KSSA/JNYA/TRA and kra/rka ligatures back to their consonant+virama sequences in Masaram Gondi.
- **_FixMasaramGondiEncode**: Ligates the KSSA/JNYA/TRA conjuncts and the special kra/rka consonant clusters into their dedicated Masaram Gondi code points, and drops a trailing virama not followed by a consonant.

## ScriptProcessing/MeeteiMayek.py

- **FixMeeteiMayek**: Dispatches to the Meetei Mayek encode or decode fix routine depending on the reverse flag.
- **_FixMeeteiMayekDecode**: Expands the dedicated Meetei Mayek final-consonant characters back into their consonant+virama component sequences.
- **_FixMeeteiMayekEncode**: Converts eight specific consonant+virama sequences into their dedicated Meetei Mayek final-consonant Unicode characters.

## ScriptProcessing/Mon.py

- **FixMon**: Dispatches to the Mon encode or decode fix-up routine based on the reverse flag.
- **_FixMonDecode**: Reverses Mon medial consonant signs and nga/nya disambiguation back to Burmese-style virama sequences.
- **_FixMonEncode**: Applies Burmese base fixes plus Mon-specific medial consonant signs and nga/nya letter disambiguation for encoding.

## ScriptProcessing/Mongolian.py

- **FixMongolian**: Dispatches to the Mongolian encode or decode fix routine based on the reverse flag.
- **_FixMongolianDecode**: Inserts the free-variation selector after a bare aleph-vowel (ᠠ) when it is not already present.
- **_FixMongolianEncode**: Removes redundant free-variation-selector markers before consonants/vowels, reorders consonant clusters before vowels with the Mongolian bowed-tooth marker, and converts the modifier apostrophe to a zero-width joiner.

## ScriptProcessing/Mro.py

- **FixMro**: Dispatches to the Mro encode or decode fix routine depending on conversion direction.
- **_FixMroDecode**: Expands the dedicated Mro precomposed consonant letters back to their base consonant forms.
- **_FixMroEncode**: Merges specific Mro consonant + diacritic sequences into their dedicated precomposed consonant letters.

## ScriptProcessing/Multani.py

- **FixMultani**: Dispatches to the Multani encode or decode fix routine depending on the reverse flag.
- **_FixMultaniDecode**: Expands the dedicated Multani plosive characters back into their nukta+consonant component sequences.
- **_FixMultaniEncode**: Strips nukta joiner marks and merges nukta+consonant sequences into dedicated Multani plosive characters.

## ScriptProcessing/Nandinagari.py

- **FixNandinagari**: Dispatches to the Nandinagari encode or decode fix-up routine based on the reverse flag.
- **_FixNandinagariDecode**: Reverses the Nandinagari prishtamatra (right-side vowel matra) substitution when decoding.
- **_FixNandinagariEncode**: No-op placeholder for Nandinagari encoding; returns the string unchanged.

## ScriptProcessing/Newa.py

- **FixNewa**: Dispatches to the Newa encode or decode fix routine depending on conversion direction.
- **_FixNewaDecode**: No-op Newa decode fixer; currently performs no transformation.
- **_FixNewaEncode**: Placeholder Newa encode fixer; repha insertion after ra+virama is currently disabled (commented out).

## ScriptProcessing/OldPersian.py

- **FixOldPersian**: Applies Old Persian cuneiform syllable-spelling and numeral-sign conversions, dispatching by conversion direction.
- **OldPersianNumeral**: Converts decimal numbers to Old Persian cuneiform numeral signs (hundred/twenty/ten/two/one units) and back.
- **OldPersianSyllable**: Converts Old Persian consonant+vowel-sign sequences into their dedicated CV syllabic cuneiform signs and back, handling word dividers and ambiguous a-vowel readings.

## ScriptProcessing/Oriya.py

- **FixOriya**: Dispatches to the Oriya encode or decode fix routine based on the reverse flag.
- **OriyaVa**: Replaces standalone va with ba (ବ), except when it is subjoined immediately after a virama.
- **_FixOriyaDecode**: Replaces the alternate va character (ଵ) with the standard Oriya va/wa (ୱ) when decoding out of Oriya.
- **_FixOriyaEncode**: No-op encode fix for Oriya; no additional orthographic corrections are currently applied.

## ScriptProcessing/PhagsPa.py

- **FixPhagsPa**: Dispatches to the 'Phags-pa encode or decode fix-up routine based on the reverse flag.
- **PhagsPaArrange**: Inserts spaces between consonant-vowel syllable clusters when arranging 'Phags-pa output for Indic-derived source scripts.
- **_FixPhagsPaDecode**: Reconstructs viramas between 'Phags-pa syllables, expands aspirate letter markers, and reverses subjoined consonant and candrabindu placement when decoding.
- **_FixPhagsPaEncode**: Reorders candrabindu and subjoined consonants, removes viramas, and inserts syllable-separating spaces for 'Phags-pa encoding.

## ScriptProcessing/Rejang.py

- **FixRejang**: Dispatches to the Rejang encode or decode fix routine depending on conversion direction.
- **_FixRejangDecode**: Expands the dedicated Rejang final ra and na signs back to consonant+virama+ra/na sequences.
- **_FixRejangEncode**: Converts consonant+virama+ra and consonant+virama+na sequences into the dedicated Rejang final ra and na signs.

## ScriptProcessing/RomanColloquial.py

- **FixRomanColloquial**: Delegates to the shared readable/colloquial Roman transliteration routine with colloquial-style rendering enabled.

## ScriptProcessing/RomanLoCDevanagari.py

- **HindiMarathiRomanLoCFix_post**: Reverses the Hindi/Marathi LoC substitutions: ṣ→'sh', ḻ→ḷ, l̳→l̤.
- **HindiMarathiRomanLoCFix_pre**: Substitutes 'sh'→ṣ, ḷ→ḻ, and l̤→l̳ before Hindi/Marathi Library of Congress romanization.

## ScriptProcessing/RomanReadable.py

- **FixRomanReadable**: Delegates to the shared readable/colloquial Roman transliteration routine with standard readable-style rendering.

## ScriptProcessing/RussianCyrillic.py

- **CyrillicPali_post**: Reverses the Cyrillic Pali l diacritic swap, л̤ → л̣, after conversion.
- **CyrillicPali_pre**: Swaps the Cyrillic Pali l-with-dot-below diacritic (л̣) to a distinct combining form (л̤) before conversion.

## ScriptProcessing/Santali.py

- **FixSantali**: Dispatches to the Santali encode or decode fix routine depending on conversion direction.
- **_FixSantaliDecode**: Expands the dedicated Santali ligature back to its component signs, maps the gitit sign to an apostrophe, and restores original ahad/gaahlaa order.
- **_FixSantaliEncode**: Ligates the Santali vowel-modifier+ahad sign combination into its dedicated letter and reorders the gaahlaa+ahad sequence.

## ScriptProcessing/Saurashtra.py

- **FixSaurashtra**: Dispatches to the Saurashtra encode or decode fix-up routine based on the reverse flag.
- **_FixSaurashtraDecode**: Expands the precomposed Saurashtra ha-virama letter into its virama-plus-ha sequence when decoding, e.g. ꢴ → ꣄ꢲ.
- **_FixSaurashtraEncode**: Inserts a ZWNJ within the ksha conjunct to prevent unwanted ligation when encoding into Saurashtra, e.g. ꢒ꣄ꢰ → ꢒ꣄‍ꢰ.

## ScriptProcessing/Shahmukhi.py

- **FixShahmukhi**: Applies the shared Perso-Arabic Shahmukhi/Urdu fix routine to encode or decode Shahmukhi text based on the reverse flag.

## ScriptProcessing/Shan.py

- **FixShan**: Dispatches to the Shan encode or decode fix routine depending on conversion direction.
- **_FixShanDecode**: Reverses Shan encoding: expands medial ligatures back to virama+consonant clusters and restores medial order.
- **_FixShanEncode**: Encodes Shan script: forms ြ/ျ/ဝ medial ligatures from virama clusters, reorders medials, and fixes the shya conjunct.

## ScriptProcessing/Sharada.py

- **FixSharada**: Dispatches to the Sharada encode or decode fix routine based on the reverse flag.
- **_FixSharadaDecode**: Reverses the Assamese khanda-ta fix when decoding out of Sharada; other corrections are currently disabled.
- **_FixSharadaEncode**: Applies the Assamese khanda-ta fix and inserts a ZWNJ between virama- or nukta-marked consonants and a following nukta letter when encoding into Sharada.

## ScriptProcessing/Siddham.py

- **FixSiddham**: Dispatches to the Siddham encode or decode fix routine depending on the reverse flag.
- **_FixSiddhamDecode**: Reverses alternate Siddham vowel-sign forms (U, UU, I variants, II) back to their standard Unicode vowel signs.
- **_FixSiddhamEncode**: No-op placeholder for Siddham encoding; no additional fixes are currently applied.

## ScriptProcessing/Sinhala.py

- **FixSinhala**: Dispatches to the Sinhala encode or decode fix-up routine based on the reverse flag.
- **SinhalaChandrbinduAnusvara**: Converts the Sinhala chandrabindu sign into the anusvara sign.
- **SinhalaDefaultConjuncts**: Inserts ZWJ to form default Sinhala consonant conjuncts before ya/ra and other special consonant clusters.
- **SinhalaPali_post**: Swaps Sinhala long e/o vowel forms with the Southern short-vowel equivalents used for Pali, or reverses the swap.
- **SinhalaPali_pre**: Pre-converts Southern short e/o vowel forms to standard Sinhala long vowel forms before processing Pali text.
- **_FixSinhalaDecode**: Reverses Sinhala conjunct formation, numeral retention, the ja-nya conjunct, and doubled-a notation, and strips ZWJ joiners.
- **_FixSinhalaEncode**: Forms default Sinhala conjuncts, retains native numerals, and merges the ja-nya conjunct and doubled-a (ආ) notation.

## ScriptProcessing/Sogd.py

- **FixSogd**: Dispatches to the Sogdian encode or decode fix routine depending on conversion direction.
- **SogdReshAyin_post**: Merges disambiguated Sogdian resh and ayin letters back into the Resh-Ayin ligature (𐼽 → 𐽀).
- **SogdReshAyin_pre**: Disambiguates the Sogdian Resh-Ayin ligature by expanding it to a bracketed [resh-ayin] marker (𐽀).
- **_FixSogdDecode**: No-op placeholder for Sogdian decoding; no reverse transformation is currently applied.
- **_FixSogdEncode**: Merges the disambiguated Sogdian letter-plus-marker sequence into its dedicated final-form letter (𐼹² → 𐽄).

## ScriptProcessing/Sogo.py

- **SogoReshAyinDaleth_post**: Replaces a Sogdian private-use character with the resh-ayin-daleth ligature character after processing.
- **SogoReshAyinDaleth_pre**: Replaces the Sogdian resh-ayin-daleth ligature character with a bracketed private-use-area placeholder sequence before processing.

## ScriptProcessing/SoraSompeng.py

- **FixSoraSompeng**: Dispatches to the Sora Sompeng encode or decode fix routine based on the reverse flag.
- **_FixSoraSompengDecode**: Inserts an inherent schwa after consonants not followed by a vowel and collapses specific consonant+schwa+vowel-length sequences when decoding out of Sora Sompeng.
- **_FixSoraSompengEncode**: Drops the inherent schwa marker after consonants and expands a standalone schwa into its full vowel-letter sequence when encoding into Sora Sompeng.

## ScriptProcessing/Soyombo.py

- **FixSoyombo**: Dispatches to the Soyombo encode or decode fix routine depending on conversion direction.
- **_FixSoyomboDecode**: Reverses Soyombo encoding: expands the KSSA ligature, gemination marks, and final consonant forms back to their base sequences.
- **_FixSoyomboEncode**: Encodes Soyombo script: forms the KSSA ligature, fixes shka, marks gemination, applies final consonant forms, and drops trailing viramas.

## ScriptProcessing/Sundanese.py

- **FixSundanese**: Dispatches to the Sundanese encode or decode fix-up routine based on the reverse flag.
- **SundaneseRemoveHistoric**: Replaces historic Sundanese vocalic-r/l consonant letters and the archaic pamaeh sign with their modern letter-plus-panyecek combinations.
- **_FixSundaneseDecode**: Restores the Sundanese repha sign to ra-plus-virama, reverses historic conjuncts, and expands subjoined consonants back to virama-plus-consonant when decoding.
- **_FixSundaneseEncode**: Converts ra-virama after a consonant to the Sundanese repha sign and subjoins virama-plus-ya/ra/la into their combining consonant forms when encoding.

## ScriptProcessing/Tagbanwa.py

- **FixTagbanwa**: Dispatches to the Tagbanwa encode or decode fix routine based on the reverse flag.
- **_FixTagbanwaDecode**: No-op decode fix for Tagbanwa; no additional corrections are currently applied.
- **_FixTagbanwaEncode**: Inserts the gemination sign for doubled consonants when encoding into Tagbanwa.

## ScriptProcessing/TaiLaing.py

- **FixTaiLaing**: Dispatches to the Tai Laing encode or decode fix routine depending on conversion direction.
- **_FixTaiLaingDecode**: Reverses medial-sign ordering and expands the Tai Laing medial ra/ya/wa signs back to virama+consonant sequences.
- **_FixTaiLaingEncode**: Converts virama+medial ra/ya/wa sequences into their dedicated Tai Laing medial signs and reorders medial-sign combinations to the correct rendering order.

## ScriptProcessing/TaiTham.py

- **FixTaiTham**: Dispatches to the Tai Tham encode or decode fix-up routine based on the reverse flag.
- **_FixTaiThamDecode**: Reverses Tai Tham subjoining, ligature, and tall-A vowel fixes back to standard consonant-plus-virama sequences when decoding.
- **_FixTaiThamEncode**: Applies Tai Tham-specific subjoining of ra/la, the mai kang lai and great-sa ligatures, tall-A vowel forms, and conjunct reordering when encoding.

## ScriptProcessing/Takri.py

- **TakriArchaicKha_post**: Restores the archaic Takri kha (𑚋) from its temporary placeholder character after processing.
- **TakriArchaicKha_pre**: Temporarily substitutes the archaic Takri kha (𑚋) with a placeholder character before further processing.

## ScriptProcessing/Tamil.py

- **FixTamil**: Dispatches to the Tamil encode or decode fix-up routine based on the reverse flag.
- **TamilNaToNNa**: Converts dental na (ந) to alveolar ன after vowels, except when followed by த், per Tamil orthographic convention.
- **TamilTranscribeCommon**: Implements shared Tamil phonetic transcription rules: intervocalic/post-nasal consonant voicing, sandhi assimilations, and letter simplifications.
- **TamilpredictDentaNa**: Restores dental na (ந) in place of ன for a hardcoded list of Sanskrit-derived words that conventionally take dental na.
- **_FixTamilDecode**: Reverses Tamil vocalic ru/lu correction, danda/numeral retention, and diacritic ordering, and restores grantha visarga and the ஷ² ligature.
- **_FixTamilEncode**: Corrects Tamil vocalic ru/lu forms, retains dandas and native numerals, and reorders superscript diacritics before Vedic accent marks.

## ScriptProcessing/TamilExtended.py

- **FixTamilExtended**: Dispatches to the Tamil-Grantha extended encode or decode fix routine depending on conversion direction.
- **TamilpredictDentaNaExtended**: Corrects ambiguous nna/dental-na spellings back to dental na for a hardcoded list of known Sanskrit-derived words in Tamil-Grantha extended text.
- **_FixTamilExtendedDecode**: Repositions zero-width joiners relative to Vedic svara marks and inserts a ZWNJ after every virama when decoding Tamil-Grantha extended text.
- **_FixTamilExtendedEncode**: Normalizes the ksha and shra conjuncts, uses the older-style AU vowel sign, and repositions zero-width joiners relative to Vedic svara marks when encoding Tamil-Grantha extended text.

## ScriptProcessing/TamilGrantha.py

- **FixTamilGrantha**: Dispatches to the Tamil Grantha encode or decode fix routine depending on the reverse flag.
- **_FixTamilGranthaDecode**: Reverses the Tamil Grantha pre-base vowel-sign reordering, restoring consonant+vowel-sign order from the joiner-marked visual sequence.
- **_FixTamilGranthaEncode**: Reorders Tamil Grantha pre-base vowel signs (e/E/ai, o/O/au) to precede their consonant using joiner marks, matching Tamil script visual ordering.

## ScriptProcessing/Telugu.py

- **FixTelugu**: Dispatches to the Telugu encode or decode fix-up routine based on the reverse flag.
- **TeluguRemoveAeAo**: Removes the candra-sign-plus-ZWSP sequence used to mark short e/o vowels in Telugu.
- **TeluguRemoveNukta**: Removes the nukta combining mark from Telugu text.
- **_FixTeluguDecode**: Restores Indic dandas and numerals and normalizes candrabindu to arasunna when decoding out of Telugu script.
- **_FixTeluguEncode**: Retains Indic dandas and numerals when encoding into Telugu script.

## ScriptProcessing/Thaa.py

- **FixThaa**: Dispatches to the Thaana encode or decode fix routine based on the reverse flag.
- **_FixThaaDecode**: Applies Perso-Arabic punctuation fixes when decoding out of Thaana.
- **_FixThaaEncode**: Applies Perso-Arabic punctuation fixes when encoding into Thaana.

## ScriptProcessing/Thaana.py

- **FixThaana**: Dispatches to the Thaana encode or decode fix routine depending on the reverse flag.
- **_FixThaanaDecode**: Reverses Thaana encoding fixes: approximates Arabic-loan consonants to native Thaana letters, inserts sukun on bare consonants, restores the inherent-vowel sign before vowel signs, and reverses gemination/punctuation mapping.
- **_FixThaanaEncode**: Applies Thaana encoding fixes: gemination-sign insertion, removal of redundant inherent-vowel sign before vowel signs, and Arabic-to-Thaana punctuation mapping.

## ScriptProcessing/Thai.py

- **FixThai**: Dispatches Thai fix logic: reverses vowel sign order, resolves digraph conjuncts, and optionally applies phonetic transcription.
- **ThaiDigraphConjuncts**: Reorders vowel-consonant-virama-consonant sequences to form Thai digraph conjunct clusters, or reverses them.
- **ThaiReverseVowelSigns**: Reorders leading Thai vowel signs to/from consonant-first internal order and forms the AM/IM ligatures (◌ํ, ◌ึ).
- **ThaiSajjhayaOrthography_post**: Post-processes Thai (or Lao Pali) text into Sajjhāya orthography, inserting joiners between consonant clusters and reordering digraphs.
- **ThaiSajjhayaOrthography_pre**: Pre-processes text for Thai Sajjhāya orthography by converting anusvara/tone marks to the subscript virama sign and dropping the short-a conjunct.
- **ThaiSajjhayawithA_post**: Post-processes text into nativized Sajjhāya-with-a orthography by applying transcription with anusvara restoration.
- **ThaiSajjhayawithA_pre**: Strips the short-a sign then applies the Thai Sajjhāya orthography pre-processing.

## ScriptProcessing/ThamLoC.py

- **FixThamLoC**: Core Tai Tham (LoC variant) encode/decode logic: delegate to the shared Tai Tham family fixer with marker cleanup enabled and ra-haam swapping disabled.

## ScriptProcessing/Tibetan.py

- **FixTibetan**: Dispatches to the Tibetan encode or decode fix routine based on the reverse flag, optionally swapping native Tibetan letter forms.
- **TibetanRemoveBa**: Converts va to ba throughout, including within ra-zur and wa-zur subjoined clusters.
- **TibetanRemoveVirama**: Strips the explicit Tibetan virama sign from the text.
- **_FixTibetanDecode**: Expands subjoined Tibetan letters back to consonant+virama sequences, normalizes decomposed aspirate conjuncts, restores vocalic ri/li clusters, converts tsheg back to space, restores bracket forms, and optionally swaps native Tibetan letters for their Sanskrit-transliteration equivalents.
- **_FixTibetanEncode**: Converts consonant+virama sequences to subjoined Tibetan letters, fixes wa-zur/ya-zur/ra-zur subjoined clusters, encodes spaces as tsheg, maps decomposed dzha+nukta to za, and converts ASCII brackets to Tibetan bracket forms.

## ScriptProcessing/TibetanLoC.py

- **FixTibetanLoC**: Core Tibetan (LoC romanization variant) encode/decode logic: delegate to the shared Tibetan fixer without native-form swapping.

## ScriptProcessing/Ugar.py

- **FixUgar**: Dispatches to the Ugaritic encode or decode fix routine depending on the reverse flag.
- **_FixUgarDecode**: Strips the Ugaritic word-divider wedge character from the text.
- **_FixUgarEncode**: Merges a marked consonant+2 sequence into its dedicated Ugaritic letter and replaces spaces with the Ugaritic word-divider wedge character.

## ScriptProcessing/Urdu.py

- **FixUrdu**: Core Urdu encode/decode logic: delegate to the shared Shahmukhi orthography fixer.

## ScriptProcessing/Wancho.py

- **FixWancho**: Core Wancho encode/decode entry point: encode into Wancho script by default, or decode out of it back to internal representation when reverse=True.
- **_FixWanchoDecode**: Decode native Wancho script back to its romanized representation: expand tone codepoints to ASCII escapes, split fused nasalization/anusvara vowels into vowel+marker sequences, and expand merged ligatures.
- **_FixWanchoEncode**: Encode romanized input into native Wancho script: convert ASCII tone-mark escapes to tone codepoints, fuse nasalization/anusvara markers with their vowels, and merge digraph/WA ligatures into single codepoints.

## ScriptProcessing/WarangCiti.py

- **FixWarangCiti**: Dispatches to the Warang Citi encode or decode fix routine depending on conversion direction.
- **WarangCitiModernOrthogaphy**: Converts to modern Warang Citi orthography by removing aspirate-ligature joiners and replacing the obsolete letter 𑣝 with 𑣞.
- **_FixWarangCitiDecode**: Lowercases the text, reinserts the inherent vowel after bare consonants, restores the nukta ligature and AA vowel sign, and reorders vowel signs when decoding Warang Citi.
- **_FixWarangCitiEncode**: Marks consonant clusters with ZWJ, removes/restores the inherent and AA vowel signs, and merges the Warang Citi nukta letter sequence into its ligature when encoding.

## ScriptProcessing/ZanabazarSquare.py

- **FixZanabazarSquare**: Dispatches to the Zanabazar Square encode or decode fix routine depending on the reverse flag.
- **_FixZanabazarSquareDecode**: Reverses Zanabazar Square encoding fixes: expands subjoining virama and repha, TSA-series to CA-series consonants, contextual y/r/l/v forms, alternate ai/au, the KSSA conjunct, and the Mongolian final mark.
- **_FixZanabazarSquareEncode**: Applies Zanabazar Square encoding fixes: converts virama+consonant to subjoining form and merges the KSSA conjunct sequence into its dedicated character.
