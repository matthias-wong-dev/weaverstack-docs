# Semantic-model journey evidence — batch 2

## Scope and reading paths

Branch: `docs/item-first-models`. Seven new owning tasks under `docs/semantic-models/`; checkpoint-only edits to the four allowed fixture READMEs. No native definitions, fixture configurations, old pages, Reference, shared guides, tools or navigation changed. The existing semantic-model index already points to these owners and required no edit.

- Native conventions: `native-tmdl.md#hide-relationship-foreign-keys` → `shared-policy.md` → `custom-annotations.md`. Parcel, Delivery, Depot, native partitions and the relationship continue throughout. Shared policy owns the reusable rule; the unmodified standards snapshot retains the original local declaration. Custom Python is optional and comes after native/policy work.
- Source quality: `native-tmdl.md` → `managed-sources.md` → `validation.md#compare-dax-with-source-sql`. Managed-source entry deliberately switches Delivery from inline Import to Warehouse-backed Import, adds Operations/catalogue/source mapping and keeps Depot inline. Validation uses that already loaded/refreshed checkpoint without another provisioning sequence.
- Inline quality: `native-tmdl.md` → `validation.md#1-add-the-dax-assumption`. Only the DAX file is added; existing overlay and configuration remain.
- Later independent techniques: `composition.md` declares the audience-variant snapshot/base/output change; the base does not deploy. `from-tmdl.md` retains the complete standalone model and managed-generation alternative.

## Two transition paragraphs in the pages

**Native → policy** (`native-tmdl.md`):

> You now have the native Parcel model and one local rule, with Delivery and Depot unchanged apart from field visibility. When that convention belongs on several models, share it in `PowerBI/policy.tmdl`. The next task keeps this model and adds common formatting and a native calculation group; it does not ask you to start deployment again.

**Managed source → validation** (`managed-sources.md`):

> After source Load and model refresh, the Warehouse and model should contain the same three delivery rows, but a successful refresh does not establish that the measure is right. Compare DAX with source SQL in this same checkpoint: its existing Test independently sums Delivered in the Warehouse. Keep the loaded source and refreshed model; there is no second provisioning sequence.

## Frozen runtime and interpreter

Behaviour/test pin: `74b4d15ee65ed2740593af1f4d459771b801b132`.
Source worktree: `/opt/data/scratch/Fors/weaver-docs-refresh/product`, HEAD `942f3798fdbc534375b45ee0a7af0aaa7b4773fe`. The fixture checker verifies both pin→HEAD and HEAD→working-tree equality for `src`, `tests` and `pyproject.toml` before importing. This is a product-doc worktree, not a different behaviour revision.

Interpreter: `/opt/data/repos/weaverstack/.venv/bin/python`.

```text
Imported: /opt/data/scratch/Fors/weaver-docs-refresh/product/src/weaver/__init__.py
PYTHONPATH: /opt/data/scratch/Fors/weaver-docs-refresh/product/src:/opt/data/scratch/Fors/weaver-docs-refresh/product/tests:/opt/data/scratch/Fors/weaver-docs-refresh/product/tests/targeted
```

Set `PYTHONDONTWRITEBYTECODE=1`; temporary assembly remains under the profile's scratch directory. The owning-page probe blocks socket connections. No live Fabric/Power BI deployment, refresh, query, credential, tenant or capacity operation was performed.

## Executed checks and exact outputs

Run from the docs worktree with the interpreter/PYTHONPATH above:

```bash
python /opt/data/profiles/editor/cache/scratch/check_semantic_model_journey.py
python tools/check_docs_refresh_examples.py --weaver-checkout /opt/data/scratch/Fors/weaver-docs-refresh/product
python tools/check_journey_examples.py --weaver-checkout /opt/data/scratch/Fors/weaver-docs-refresh/product
python tools/check_reference_examples.py --weaver-checkout /opt/data/scratch/Fors/weaver-docs-refresh/product
```

Here `python` means the exact interpreter given above, not an installed Weaver entrypoint.

**New owning-page probe** (full reproducible source below):

```text
PASS: {"commands": 48, "configs": 3, "pages": 7, "python_blocks": 1} ; 16 byte-identical fixture blocks; 12 assembled Check checkpoints
PASS: native rule; shared policy; foreign-key rule moved to shared policy; custom annotation; Assumption failure edits measure in prior custom/rule overlay; prior overlay restored; native-rule failure; native-rule correction; no-overlay failure; no-overlay correction; standalone TMDL 0; standalone TMDL 1
PASS: effective visibility, relationship/partition preservation, policy precedence/calculation group, shared-rule transfer, custom folder, failure/correction preserve prior overlay; exact catalogue names/readback; authored fixture SHA-256 unchanged; no service execution
```

The production compiler verifies many-side `Delivery.DepotId` hiding, visible one-side `Depot.DepotId`, unchanged partition sources/relationship, local format precedence, Display/Current, the moved shared foreign-key rule, `Parcel metrics`, and failure/correction with prior custom/rule declarations intact. The exact documented shell backup/restoration branches were exercised for both existing and absent overlays. Inline standalone TMDL is compiled; the partition-free managed standalone example is locally Checked, not resolved against fabricated service metadata.

**Existing fixture checker**, rerun after README edits:

```text
Source runtime matches 74b4d15ee65ed2740593af1f4d459771b801b132; checkout HEAD 942f3798fdbc534375b45ee0a7af0aaa7b4773fe
PASS: file Assumption boundary inputs -> passed, failed, invalid, passed
PASS: file DAX/SQL boundary inputs -> passed, failed, invalid, passed
PASS: 6 fixtures; 53 README Weaver commands parsed; no live service exercised
```

It also passed real CLI Check and SHA-256 unchanged assertions for `parcel-powerbi`, `parcel-powerbi-validation`, `parcel-powerbi-standards`, `parcel-powerbi-variants`, `parcel-load-selection`, and `parcel-powerbi-fabric`. Report encoder/binding assertions use explicit offline inventory doubles, not deployed Report readback. DAX/SQL rows above are boundary test inputs, not executed query output.

**Existing journey checker**:

```text
PASS: {'pages': 15, 'commands': 92, 'configs': 9, 'python_calls': 3}; 12 byte-identical fixture blocks; four exact rendered projects Check; local rule/policy/standalone compilation; no network or service execution
```

This existing checker still scans the old owners. Its pass proves retention/regression, not coverage of the new pages; the new probe supplies that coverage without editing integration-owned tooling.

**Reference example checker**:

```text
Validated against /opt/data/scratch/Fors/weaver-docs-refresh/product/src/weaver/__init__.py
{'commands': 103, 'configurations': 6, 'operation_calls': 4, 'dax_files': 2, 'native_edits': 1}
```

**Focused source tests**, run from the product worktree with the same interpreter/PYTHONPATH:

```bash
python -m pytest -q \
  tests/test_semantic_annotation_build_cycle.py \
  tests/test_semantic_annotation_phase_cycle.py \
  tests/test_semantic_composition_build_cycle.py \
  tests/test_semantic_validation_journey_representation.py \
  tests/test_semantic_model_catalogue_free_cycle.py \
  tests/test_semantic_source_build_cycle.py \
  tests/test_semantic_shared_sources_cycle.py \
  tests/test_semantic_annotation_composition_cycle.py
```

```text
91 passed in 67.81s (0:01:07)
```

**Microsoft PBIR schemas**, separate public-schema fetch, no Fabric calls:

```text
PASS: 36 PBIR JSON documents; 8 public Microsoft schemas fetched; no Fabric calls
```

The first schema run failed because `jsonschema` was absent. Installed `jsonschema 4.26.0` and dependencies only into `/opt/data/profiles/editor/cache/scratch/semantic-model-schema-deps`, then reran with that directory prefixed to PYTHONPATH. The shared runtime environment was not modified.

**Contextual route scan**: 52 internal contextual links across the seven tasks and existing index; existing target fragments resolve. Only `../reports/deploy.md` and `../estate/operate.md` await their integration-owned pages. Neither is an invented route: both are approved in `routes.json`. No old Basics/Advanced narrative link remains in these tasks. `#hide-relationship-foreign-keys` and `#compare-dax-with-source-sql` are real canonical headings. The validation readback paragraph is identical to the Fabric fixture README, and all four named catalogue tables are present in pinned `CATALOGUE_TABLES`.

`git diff --check` passed. Native/configuration fixture files are unchanged in the Git diff; only the four allowed READMEs changed.

## Corrections and remaining gates

- A draft failure probe that blindly appended `table Delivery` to a custom overlay failed real Check with `PowerBI/Parcel/Parcel.tmdl:9: duplicate declaration 'table Delivery'`. The page now instructs editing the existing measure declaration, retaining every other overlay property, and restoring the original bytes. Native-rule-only and absent-overlay entries were also checked. This is an authoring correction, not a runtime change.
- Fixture directories remain complete direct-entry snapshots, not separate repeated setup requirements. The standards snapshot includes the later custom handler; the policy page tells continuing readers to add only policy/local format first and tells direct entrants exactly what is already present.
- No compiled-native-TMDL export command is claimed. Local effective definitions are compiler assertions; readers inspect deployed native definitions through supported service/native tooling.
- Parent still owns old-route migration/fragment forwarding, tooling route ownership, full strict-site/link/browser/search checks, Report and estate integration, and independent reader acceptance. The unchanged old pages temporarily coexist with the new owners until that migration.
- Live deployment/refresh, DAX/SQL query results, catalogue/Health readback, Report rendering/binding and service/licence eligibility remain unobserved gates. All remote outcomes in the pages are expected task results, not evidence from this batch.
- No release, publication, push, PR, Asana, additional delegation or service mutation.

## Reproduce the owning-page probe

Extract this Python fence to a scratch file, use the exact interpreter/PYTHONPATH above, and pass the integrated docs root as its first argument. Set `WEAVER_CHECKOUT` only to the frozen source-equivalent product worktree. Its helper imports are from the existing docs tool and pinned production parser/compiler; it does not substitute a model compiler or graph algorithm.

```python
"""Check the seven new owning pages with pinned production functions, offline."""
import ast
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import socket
import subprocess
import sys
import tempfile

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '/opt/data/scratch/Fors/weaver-docs-refresh/item-first-models').resolve()
SOURCE = Path(os.environ.get('WEAVER_CHECKOUT', '/opt/data/scratch/Fors/weaver-docs-refresh/product')).resolve()
sys.path[:0] = [str(SOURCE/'src'), str(SOURCE/'tests'), str(SOURCE/'tests/targeted'), str(ROOT/'tools')]
from check_docs_refresh_examples import compile_models, hashes, model, parse, refuse_network, item
from weaver_cli.main import build_parser, main
from weaver.config import parse_workspace
from weaver.catalogue.tables import CATALOGUE_TABLES
import weaver
import yaml
assert Path(weaver.__file__).resolve().is_relative_to(SOURCE/'src')
print('Imported:', weaver.__file__)
print('PYTHONPATH:', os.environ.get('PYTHONPATH'))
socket.socket.connect = refuse_network
socket.create_connection = refuse_network
DOC = ROOT/'docs/semantic-models'
PAGES = ['native-tmdl','managed-sources','validation','shared-policy','custom-annotations','composition','from-tmdl']
def blocks(page, language):
    return re.findall(r'^```'+language+r'[^\n]*\n(.*?)^```', (DOC/(page+'.md')).read_text(), re.M|re.S)
counts = dict(pages=len(PAGES),commands=0,configs=0,python_blocks=0)
for page in PAGES:
    for block in blocks(page,'bash'):
        for line in block.replace('\\\n',' ').splitlines():
            if line.startswith('weaver '):
                build_parser().parse_args(shlex.split(line)[1:]); counts['commands'] += 1
    for block in blocks(page,'yaml'):
        parse_workspace(yaml.safe_load(block)); counts['configs'] += 1
    for block in blocks(page,'python'):
        ast.parse(block); counts['python_blocks'] += 1
sync = [
 ('native-tmdl','yaml','parcel-powerbi','workspace-dev.yml'),
 ('native-tmdl','tmdl','parcel-powerbi','PowerBI/Parcel/Parcel.SemanticModel/definition/relationships.tmdl'),
 ('managed-sources','yaml','parcel-powerbi-fabric','workspace-dev.yml'),
 ('managed-sources','tmdl','parcel-powerbi-fabric','PowerBI/Parcel/Parcel.tmdl'),
 ('managed-sources','tmdl','parcel-powerbi-fabric','PowerBI/Parcel/Parcel.SemanticModel/definition/tables/Delivery.tmdl'),
 ('managed-sources','tmdl','parcel-powerbi-fabric','PowerBI/Parcel/Parcel.SemanticModel/definition/expressions.tmdl'),
 ('validation','dax','parcel-powerbi-validation','PowerBI/Parcel/assumptions/Parcel/Parcel.PositiveDeliveryCount.dax'),
 ('validation','tmdl','parcel-powerbi-validation','failure/Parcel.tmdl'),
 ('validation','dax','parcel-powerbi-fabric','PowerBI/Parcel/tests/Parcel/Parcel.DeliveryReconciles.dax'),
 ('validation','tmdl','parcel-powerbi-fabric','failure/Parcel.tmdl'),
 ('shared-policy','tmdl','parcel-powerbi-standards','PowerBI/policy.tmdl'),
 ('custom-annotations','python','parcel-powerbi-standards','PowerBI/annotations/Parcel__DisplayFolder.py'),
 ('custom-annotations','tmdl','parcel-powerbi-standards','PowerBI/Parcel/Parcel.tmdl'),
 ('custom-annotations','tmdl','parcel-powerbi-standards','failure/Parcel.tmdl'),
 ('composition','tmdl','parcel-powerbi-variants','PowerBI/Parcel/ParcelOperations.tmdl'),
 ('composition','tmdl','parcel-powerbi-variants','PowerBI/Parcel/ParcelExecutive.tmdl'),
]
for page,lang,fixture,path in sync:
    assert (ROOT/'examples'/fixture/path).read_text() in blocks(page,lang), (page,path)
readback = re.search(r"Inspect Delivery's metadata row.*?mapping failed\.", (DOC/'validation.md').read_text(), re.S).group()
assert readback in (ROOT/'examples/parcel-powerbi-fabric/README.md').read_text()
names = set(re.findall(r'`(_\.[A-Za-z]+)`', (DOC/'validation.md').read_text()))
assert {'_.SemanticModelTable','_.Dependency','_.SemanticModelTest','_.TestStatus'} <= names <= {t.qualified for t in CATALOGUE_TABLES}
assert 'SemanticModelSource' not in (DOC/'validation.md').read_text()
before = hashes(ROOT/'examples')
checks = []
def check(trial, name):
    assert main(['check',str(trial),'--json','--non-interactive']) == 0
    checks.append(name)
def assert_native(effective, original):
    assert effective.relationships['Delivery_Depot'].fromColumn == 'Delivery.DepotId'
    for table in ('Delivery','Depot'):
        assert effective.tables[table].partitions[table].source == original.tables[table].partitions[table].source
    assert effective.tables['Delivery'].columns['DepotId'].isHidden is True
    assert effective.tables['Depot'].columns['DepotId'].isHidden is None
with tempfile.TemporaryDirectory(prefix='semantic-model-owning-pages-') as directory:
    temp=Path(directory)
    trial=temp/'continuous'
    shutil.copytree(ROOT/'examples/parcel-powerbi',trial)
    original=model(compile_models(trial))
    overlay=trial/'PowerBI/Parcel/Parcel.tmdl'
    overlay.write_text(blocks('native-tmdl','tmdl')[-1])
    check(trial,'native rule')
    assert_native(model(compile_models(trial)),original)
    (trial/'PowerBI/policy.tmdl').write_text(blocks('shared-policy','tmdl')[0])
    overlay.write_text(blocks('shared-policy','tmdl')[-1])
    check(trial,'shared policy')
    policy=model(compile_models(trial)); assert_native(policy,original)
    assert policy.tables['Delivery'].measures['Delivery Count'].formatString == '0 "deliveries"'
    assert policy.tables['Delivery'].measures['InternalCost'].formatString == '#,##0.00'
    assert policy.tables['Display'].calculationGroup.calculationItems['Current'].expression == 'SELECTEDMEASURE()'
    # Move the rule to shared policy exactly as the new page directs.
    policy_text=blocks('shared-policy','tmdl')[0]
    header=blocks('shared-policy','tmdl')[1].rstrip()
    (trial/'PowerBI/policy.tmdl').write_text(header+policy_text[policy_text.index('\n\ntable Delivery'):])
    overlay.write_text(blocks('shared-policy','tmdl')[-1].replace("    annotation 'Weaver.AutoHideForeignKeys' = true\n",''))
    check(trial,'foreign-key rule moved to shared policy')
    assert_native(model(compile_models(trial)),original)
    handler=trial/'PowerBI/annotations/Parcel__DisplayFolder.py'; handler.parent.mkdir()
    handler.write_text(blocks('custom-annotations','python')[0])
    overlay.write_text(blocks('custom-annotations','tmdl')[0])
    check(trial,'custom annotation')
    custom=model(compile_models(trial)); assert_native(custom,original)
    assert custom.tables['Delivery'].measures['Delivery Count'].displayFolder == 'Parcel metrics'
    saved=overlay.read_bytes()
    overlay.write_text(re.sub(r"^([ \t]*measure 'Delivery Count')(?: =.*)?$", r'\1 = -1', overlay.read_text(), count=1, flags=re.M))
    check(trial,'Assumption failure edits measure in prior custom/rule overlay')
    failed=model(compile_models(trial)); assert_native(failed,original)
    assert failed.tables['Delivery'].measures['Delivery Count'].expression == '-1'
    overlay.write_bytes(saved)
    check(trial,'prior overlay restored')
    restored=model(compile_models(trial)); assert_native(restored,original)
    assert restored.tables['Delivery'].measures['Delivery Count'].expression == 'SUM(Delivery[Delivered])'
    assert restored.tables['Delivery'].measures['Delivery Count'].displayFolder == 'Parcel metrics'
    # The actual native-to-validation entry has only the model-level rule.
    for start in ('native-rule', 'no-overlay'):
        direct = temp/start
        shutil.copytree(ROOT/'examples/parcel-powerbi-validation', direct)
        path=direct/'PowerBI/Parcel/Parcel.tmdl'
        prior=blocks('native-tmdl','tmdl')[-1].encode() if start=='native-rule' else None
        if prior is not None: path.write_bytes(prior)
        path.write_text((prior.decode() if prior else '')+'\n'+blocks('validation','tmdl')[0])
        check(direct, start+' failure')
        effective=model(compile_models(direct))
        assert effective.tables['Delivery'].measures['Delivery Count'].expression == '-1'
        if prior is not None:
            assert effective.tables['Delivery'].columns['DepotId'].isHidden is True
            path.write_bytes(prior)
        else: path.unlink()
        check(direct, start+' correction')
        effective=model(compile_models(direct))
        assert effective.tables['Delivery'].measures['Delivery Count'].expression == 'SUM(Delivery[Delivered])'
        assert path.read_bytes() == prior if prior is not None else not path.exists()
        # Exercise the page's exact backup/restoration shell branches in one shell.
        backup=next(b for b in blocks('validation','bash') if 'had_overlay=false' in b)
        restore=next(b for b in blocks('validation','bash') if 'test "$had_overlay"' in b)
        restore='\n'.join(line for line in restore.splitlines() if not line.startswith('weaver '))
        candidate=direct/'candidate.tmdl'
        candidate.write_text((prior.decode() if prior else '')+'\n'+blocks('validation','tmdl')[0])
        subprocess.run(['bash','-c',backup+'\ncp candidate.tmdl PowerBI/Parcel/Parcel.tmdl\n'+restore],cwd=direct,check=True)
        assert path.read_bytes() == prior if prior is not None else not path.exists()
        assert not (direct/'Parcel.tmdl.saved').exists()
    for i,text in enumerate(blocks('from-tmdl','tmdl')):
        trial=temp/f'standalone-{i}'
        path=trial/'PowerBI/Parcel/ParcelSummary.tmdl'; path.parent.mkdir(parents=True); path.write_text(text)
        if i: shutil.copytree(ROOT/'examples/parcel-powerbi-fabric/Warehouse',trial/'Warehouse')
        check(trial,f'standalone TMDL {i}')
        if not i:
            effective=model(compile_models(trial),'ParcelSummary')
            assert effective.tables['Delivery'].partitions['Delivery'].mode == 'import'
            assert effective.tables['Delivery'].measures['Delivery Count'].expression == 'SUM(Delivery[Delivered])'
assert hashes(ROOT/'examples') == before
print('PASS:',json.dumps(counts,sort_keys=True),f'; {len(sync)} byte-identical fixture blocks; {len(checks)} assembled Check checkpoints')
print('PASS:', '; '.join(checks))
print('PASS: effective visibility, relationship/partition preservation, policy precedence/calculation group, shared-rule transfer, custom folder, failure/correction preserve prior overlay; exact catalogue names/readback; authored fixture SHA-256 unchanged; no service execution')
```
