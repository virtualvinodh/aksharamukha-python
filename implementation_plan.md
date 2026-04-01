# Implement ISO7 Mapping for Tamil

The user requested to add support for the `iso7` transliteration scheme for Tamil. Since `aksharamukha` internally uses Devanagari as a pivot alphabet for transliteration, the `iso7` characters mapped to Tamil will be aligned to their respective Devanagari counterparts.

## Proposed Changes

We will create a new file `ISO7.py` in the `aksharamukha/ScriptMap/Roman/` directory based on the structure of `ISO.py`. The arrays `VowelMap`, `SouthVowelMap`, `ConsonantMap`, `SouthConsonantMap`, `AyogavahaMap`, and `Aytham` will be modified to include the specific ISO7 mappings provided by the user. Other mappings will fall back to their default `ISO.py` values to maintain stability for any generic characters.

### `aksharamukha\ScriptMap\Roman\ISO7.py`
#### [NEW] [ISO7.py](file:///c:/Users/Saiyi/Desktop/aksharamukha-python/aksharamukha/ScriptMap/Roman/ISO7.py)
- Duplicate `ISO.py` into `ISO7.py`.
- Apply user's custom ISO7 character mapping into the arrays (e.g. `_k` for Aytham, `.t` for Ta, etc.).

## Verification Plan
### Automated Tests
- Import `aksharamukha.transliterate`.
- Convert the Tamil sentence containing newly mapped characters to `ISO7`.
- Validate that the output matches the provided ISO7 mappings (`;m`, `_k`, `.t`, etc.).
- Convert `ISO7` text back to `Tamil` and verify the integrity of the roundtrip.
