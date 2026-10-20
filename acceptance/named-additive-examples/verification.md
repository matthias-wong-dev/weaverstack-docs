# Named, additive examples — local verification

Runtime head: `bf908f4754eca4d10a56afd218e9e18d423636d7`, following the implementation at `80af419be021388c5e5d26dd0ce89cc8eed2fb65` and native-only correction at `89e93c78f8497454b4544e7919567cc078dbad11`. The final follow-up changes only import spacing in two bundled Python files; their ASTs remain identical. Coordinated existing draft PRs: weaverstack #222 and weaverstack-docs #3. This correction supersedes the prior example-archive and beginner inspection-harness preparation; it does not rewrite those historical reports into current-head acceptance.

## Interface and ownership

```bash
weaver initialise --workspace "Parcel Development" --project-folder ./parcel \
  --warehouse Operations --example Parcel

# Later, against that same project:
weaver initialise --workspace "Parcel Development" --project-folder ./parcel \
  --lakehouse Landing --example Parcel
```

```python
weaver.initialise(project_folder, workspace="Parcel Development",
                  warehouse="Operations", example="Parcel")
```

The exact names are Parcel and Sales; omitted means no example content. The CLI requires the name, rejects unknown names with available choices, and has no boolean/no-example alternative. Interactive selection is None / Parcel / Sales.

Existing item-owned sources retain their bytes and meaning. Warehouse seed Tables remain Tables; additional logical Shortcuts and loadable cross-item Tables have distinct identities. The native model remains inline. Additional Import models compose its native foundation and add managed-source Tables, rather than replacing its original partitions.

Native-only Initialise creates no catalogue Warehouse or Fabric Environment unless explicitly requested. Adding a data item supplies missing support. Explicit existing bindings and edited source/configuration survive. Unedited generated workflow/README metadata may update for the new selection; edited metadata is preserved. Unsafe file/path/name/binding conflicts refuse before source writes or resource creation. The ownership receipt is written after source files.

## Runtime and built-wheel results

| Check | Actual result |
| --- | --- |
| Final-head Windows/Python 3.13 CI | **7,773 passed; 7 POSIX-pty retry cases skipped on Windows; 325 deselected**, run [38769495444](https://github.com/matthias-wong-dev/weaverstack/actions/runs/38769495444), exact head verified |
| Linux/Python 3.11 full suite | **7,780 passed; 325 deselected** at `89e93c78f8497454b4544e7919567cc078dbad11`, before the two-file AST-identical import-spacing cleanup. The redundant slow Linux rerun was stopped after final-head Windows CI passed. |
| Named/additive regression subset | **63 cases**, included in the full total |
| Broader focused Initialise/CLI/cycle suite | **174 passed**; overlaps the full suite, not additional coverage |
| Wheel | `weaverstack-0.9.0.dev16746776803276843971-py3-none-any.whl`, built locally, not released |
| Installed-wheel generation | **21 projects**: seven selections for None, Parcel and Sales |
| Installed-wheel additive comparison | **24 proper smaller/larger subset pairs**, all item-owned source bytes retained |
| Installed-wheel extension | **10 orders** across both examples, plus unchanged-selection idempotence |
| Isolated import | Every loaded Weaver/CLI module resolved under the separately installed wheel target; execution started outside either checkout and refused network connections |
| Generated native Report schemas | **14 PBIR JSON documents** from Parcel/Sales wheel generation passed the public Microsoft schemas |

The source regressions change business data in Python/T-SQL, alter native DAX, edit configuration/README text, then extend and check preservation. They also exercise collision/refusal without partial writes, target retention, parser/Check, effective model compilation, native-partition preservation, real Catalogue projection and acyclic production LoadDag construction. The combined Lakehouse/Warehouse case includes a consuming Table and supported SQL-endpoint readiness barrier.

These are source/runtime checks with explicit offline inventory, SQL-column and installation inputs. They are not deployed-state observations or service Build/Load execution. The wheel driver is retained in `tools/check_installed_examples.py`; [its actual output](installed-wheel-results.json) and [the exact file matrix](generated-file-matrix.md) accompany this report.

## Documentation and reader checks

- Strict locked MkDocs build passed.
- All four reference generators passed against the coordinated runtime: CLI, public Python, semantic extensions and catalogue.
- **22 documentation tests** passed, with three subtests reported separately.
- **16 marked generated-file excerpts** matched the generator. Marker counts are checked so a blank line or malformed marker cannot silently skip a displayed source.
- Continuing-project gates passed: Lakehouse source → incremental addition → Warehouse extension; Warehouse source → incremental addition → native extension; native rule → shared policy → custom annotation → managed-source addition → reconciliation → composition/standalone extensions; native Report and both environment mappings; estate mapping and exact production LoadDag selections.
- Canonical route gate retained **114 original routes, 872 original fragments and 35 canonical owners**; 27 compatibility routes remain.
- Paired crawl: **162 HTML pages, 23,279 local links/assets and 276 cross-site links; zero broken links or fragments**.
- Browser: **50 broad documentation states**, followed by **five final-source states** for the sole rendered page affected by import spacing, at 390/1280 widths, light/dark and mobile no-JavaScript, with page-overflow checks and real clipboard/source comparison. Collapsed optional controls were not counted as tested copy controls.
- Product Sales disclosure: four viewport/JavaScript states passed. Its example starts with one Warehouse using named `--example Sales` syntax.
- Mobile JavaScript drawer/back navigation and a visible, hit-tested AutoHideForeignKeys search result worked. No-JavaScript cross-section navigation was exercised through the section overview and ordinary task link, not certified as every submenu control.
- Selected mobile Warehouse, dark native-rule and mobile Report-mapping screenshots were inspected. Screenshots remain task-local QA evidence, not publication captures or Fabric evidence.

The native introduction now uses Check → Build → refresh → ordinary DAX → a small AutoHideForeignKeys overlay → ordinary field-list observation. The Report introduction uses normal lineage/model-binding observation. No beginner hash snapshots or long query/inspection/binding scripts remain. All 18 example ZIPs and `tools/package_examples.py` are deleted; no alternative distribution mechanism replaces them. Maintained source fixtures and the unrelated Build-bundle archive reference remain legitimate technical material.

Navigation, page ordering, routes, sidebar and shared visual assets were not reorganised. Product-site changes are confined to the necessary named Sales example on Get started; approved positioning elsewhere remains untouched.

The seven Windows skips are the POSIX-pty cases in `tests/test_retry_cycle.py`, guarded by `hasattr(os, "fork")`. The named-example cases passed. Full repository Ruff checks and format checks passed over all 807 files, including bundled Python resources.

## Limits and stop boundary

No live Fabric Build/Load, Spark/T-SQL execution, DAX evaluation, model refresh, Report rendering, connection/licensing acceptance or matching released-PyPI acceptance was performed. Public Microsoft schema retrieval is not a Fabric test. No Fabric capacity, tenant settings, service connections or remote environments were changed or provisioned.

Managed-source Import operation still needs existing supported service connections and permissions. Initialise refuses conflicting new declaration paths rather than merging or overwriting arbitrary user-authored files. Initialisation is not a Wipe, rebuild or reload of existing data.

The two existing draft PR branches are the delivery targets. Do not merge, release or publicly publish. Human page-by-page review and the later real capture phase remain Matthias's next boundary; publication remains held for a matching release and explicit approval.
