# Aksharamukha, running client-side via WASM

A self-contained demo of aksharamukha running entirely in the browser via
[Pyodide](https://pyodide.org) (CPython compiled to WebAssembly) - no backend,
no network calls once the page is loaded. Everything needed is vendored
locally in this folder; nothing is fetched from a CDN.

## What's here

- `index.html` - the demo page (input script, output script, pre-option,
  post-option, and nativize controls). Script names and pre/post-option
  names are queried live from the loaded package at runtime, not hardcoded -
  so this always reflects whatever's actually in the wheel below.
- `pyodide/` - the Pyodide v0.26.1 core runtime (`pyodide.js`,
  `pyodide.asm.js`, `pyodide.asm.wasm`, `python_stdlib.zip`,
  `pyodide-lock.json`) plus the package wheels aksharamukha's core engine
  needs: `pyyaml`, `regex`, `fonttools`, `requests` (+ its own deps -
  `charset-normalizer`, `idna`, `urllib3`, `certifi`), `micropip` (+ its dep
  `packaging`), and `pykakasi` (+ its deps `jaconv`, `Deprecated`, `wrapt`)
  for Japanese kanji/kana romanization. All of these must sit flat in this
  folder, alongside `pyodide-lock.json` - that's where Pyodide's own package
  resolution (`pyodide.loadPackage`) expects to find them, not a subfolder.
- `wheel/aksharamukha-2.3-py3-none-any.whl` - the actual aksharamukha
  package, built from this repo's source and installed into the Pyodide
  environment with `deps=False` (the deps above are loaded separately via
  `loadPackage`, which resolves faster and fully offline compared to letting
  `micropip` re-resolve everything against PyPI).

## Running it

WASM instantiation and the module fetches Pyodide needs are blocked under a
plain `file://` page in most browsers - this needs to be served over HTTP,
even just locally:

```
cd aksharamukha-wasm
python -m http.server 8000
```

Then open `http://localhost:8000/`. Cold start (fetching + instantiating the
WASM runtime, loading the core deps, installing the wheel) is a few seconds;
every conversion after that is local and fast.

## What doesn't work here

The page itself warns about these inline if you select them (a
`knownLimitation()` check in `index.html`, before attempting the conversion) -
this section is just the fuller explanation:

- **Khmer word-split** (`khmer-nltk`) - needs `python-crfsuite`, a C
  extension with no WASM build available anywhere. A hard blocker, not a
  packaging gap.
- **Tamil -> IPA** (calls a third-party pronunciation API via `requests`) -
  works from a real backend, but that specific API has no CORS headers, so
  it can't be called from browser JS at all, Pyodide or not. Would need a
  small proxy of your own to fix, unrelated to this WASM setup.

Everything else - all ~180 scripts, all other pre/post-options - runs
correctly client-side. Verified against a 303-sample set covering every
distinct script in the project's regression corpus, both as source and
target, with zero mismatches against the native-Python reference output.

## Rebuilding

If the aksharamukha source changes, rebuild the wheel from the repo root and
replace it here:

```
python setup.py bdist_wheel
cp dist/aksharamukha-2.3-py3-none-any.whl aksharamukha-wasm/wheel/
```
