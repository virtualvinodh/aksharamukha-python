# Workbench: CSV-driven test case authoring

A loop for adding real test coverage without hand-editing JSON: fill in a
CSV, run a script, review the results in a CSV, mark the ones you want,
merge them into the real fixtures.

## Web UI

`python app.py` starts a local Flask server (opens your browser to it
automatically, `http://127.0.0.1:8848`) that's a UI on top of the exact
same CSV files described below - no separate data model, no build step,
no npm. It's a straight substitute for opening the CSVs in a spreadsheet:

- **Source Texts / Fan-out / Option Tests tabs**: editable tables (click a
  cell to edit, `+ Add row`, `✕` to remove, `Save` writes the CSV).
- **Options Catalog tab**: read-only, searchable; each row has a `+ test`
  button that sends it straight to the Option Test Requests table with
  `kind`/`option_name` filled in.
- **Run** buttons call the exact same `run_requests.py` functions the
  command line uses, then reload the results table underneath.
- Results tables render `approve` as a checkbox and highlight error rows
  red / meaningful rows green so you can scan instead of reading every
  cell.
- **Preview import** / **Apply import** at the top call
  `import_approved.py` (dry-run vs. `--apply`), with the log shown
  in a panel under the tab bar. Apply asks for confirmation first.

Nothing here talks to anything but your own filesystem - it's `127.0.0.1`
only, and the "API" is just CSV read/write plus calls into the same
`run_requests.py`/`import_approved.py` used from the command line, so the
two stay interchangeable: edit a CSV by hand, or through the browser,
either way `python run_requests.py` and the web UI see the same data.

## The loop

1. **Add texts** — `source_texts.csv`. Add a row: `id, script, label, text`.
2. **Ask for conversions** — `fanout_requests.csv`:
   - `mode=all_scripts` — your text converted to every script (~150 rows out).
   - `mode=round_trip` — your text → a target script → back, reporting whether
     you get the original back exactly. Leave `target_script` blank to run
     it against every script `GeneralMap` documents as round-trip-safe
     (`ReversibleScripts`/`RomanReversible`); fill it in to force a specific
     script (including a non-"reversible" one, just to see how far it drifts).
3. **Browse options** — `options_catalog.csv` (regenerate with
   `python generate_options_catalog.py` whenever
   `../frontend_backend_manifest.json` changes). Read-only reference: every
   option's name, whether it currently works, whether the frontend exposes
   it, which scripts it's wired to.
4. **Ask for option test cases** — `option_test_requests.csv`:
   `kind, option_name, source_script, target_script, input_text, extra_args`.
   Leave `extra_args` blank for ordinary single-argument options. For the
   ~32 options that need more than that (see `../promote_direct_call_options.py`),
   the runner already knows their real arguments and uses them automatically;
   only fill in `extra_args` yourself to override that or to supply
   arguments for an option it doesn't already know.
5. **Run it**: `python run_requests.py` → writes `fanout_results.csv` and
   `option_test_results.csv`. Nothing here touches the real fixtures.
6. **Review**: open the two results CSVs (Excel/Sheets/whatever). Check
   `output`/`error`/`meaningful`/`matches_original`. Fill `approve` with
   `yes` on the rows you want kept.
7. **Merge**: `python import_approved.py` previews what would change
   (dry-run by default); `python import_approved.py --apply` actually
   writes it — option cases go into `test_texts/test_postoptions.json` /
   `test_preoptions.json` (same schema `TestPostOptions`/`TestPreOptions`
   in `testsuite.py` already read, so they run under plain `pytest`
   immediately), fan-out/round-trip cases go into a new
   `regression/roundtrip_user.json`, kept separate from the
   auto-generated `roundtrip.json` so a re-run of `generate_golden.py`
   never overwrites your hand-picked cases.

## Notes from building this

- `run_option()` in `run_requests.py` mirrors the actual investigation from
  the `known_broken_options.json` correction: it tries the public
  `post_options=[name]`/`pre_options=[name]` path first, and only falls
  back to a direct call (with either your `extra_args` or the ones already
  discovered in `promote_direct_call_options.py`) if that fails with a
  missing-argument `TypeError`. The `how_called` column in the results
  tells you which path was actually used.
- For a direct-call option, "meaningful" compares the output against the
  *original input text*, not the full pipeline's converted output - those
  are naturally different scripts and comparing them would mark
  everything "meaningful" for the wrong reason. This was wrong in the
  first version of this tool; caught by running it end-to-end on a real
  example (`RemoveFinal` on IAST text, which should be a no-op, was
  showing as "meaningful" before the fix).
- `import_approved.py` defaults to dry-run. Approving a row is a decision
  about what belongs in the test suite; the merge step should never
  surprise you by writing something you didn't ask for.
