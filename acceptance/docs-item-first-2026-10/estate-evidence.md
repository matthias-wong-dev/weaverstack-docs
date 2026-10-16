# Estate coordination evidence — approved batch 3

## Scope and frozen evidence

- Branch: `docs/item-first-estate`; isolated worktree: `/opt/data/scratch/Fors/weaver-docs-refresh/item-first-estate`.
- Added the eleven assigned estate task pages. Existing `docs/estate/index.md` already links the final progression and was reviewed unchanged. No legacy pages, other item pages, examples, Reference/generated files, navigation, tooling or runtime were changed.
- Behaviour pin: `74b4d15ee65ed2740593af1f4d459771b801b132`. Evidence checkout: `/opt/data/scratch/Fors/weaver-docs-refresh/product`; checkout HEAD remained `942f3798fdbc534375b45ee0a7af0aaa7b4773fe`.
- `git diff --quiet 74b4d15ee65ed2740593af1f4d459771b801b132 -- src tests pyproject.toml` exited 0 before authoring and after verification. Product import resolved to `/opt/data/scratch/Fors/weaver-docs-refresh/product/src/weaver/__init__.py`.
- Reused `/opt/data/repos/weaverstack/.venv/bin/python` with the explicit pinned-source `PYTHONPATH`. Reused the existing locked documentation environment at `../journeys/.venv`; no new environment or dependency installation.
- Read repository AGENTS/PROSE/CONTRIBUTING, product PROSE, the full approved plan and route-map/routes.json before authoring. Route ownership was not changed.

## Retention and technical decisions

| Area | Authored result and retained boundary | Existing evidence |
| --- | --- | --- |
| Connections | Landing Events Folder → Event → CurrentStatus stays intact; optional Dispatch logical Shortcut reads that Event. Complete direct-entry snapshot and assembled addition checked. Dependencies never add an unnamed item. | Existing Lakehouse snapshot, source declaration/Shortcut parsing, `core-concepts/dependencies.md` |
| Mappings | One owner explains whole-project dev/prod binding. First Warehouse StatusEvent/View checkpoint remains separate from source-backed Parcel Operations Delivery/model/Report checkpoint. Both full managed-source configurations are byte-identical to fixtures. Native source mapping, permissions and existing connections are distinct from target naming. | `config.parse_workspace`, both existing `parcel-powerbi-fabric` configurations, native compile/binding checks |
| State | Whole installed estate Health, current status versus history, real catalogue identifiers, registered model/DAX state, no independent Report data/validation health. Inspection needs no new Load/Test. | Catalogue declarations including optional `MIRROR`; Health tests and references |
| Development | Edit → Check → Build preview → Build → Load → Test → Health; ordinary state is not described as mirrored. Separate source-data/model Builds, Report Build only. Mirror introduced after the loop. | Existing Build/Load/Test/Health semantics and authored CLI parser checks |
| Recovery | Reload empties/reset only reached selected Tables; expansion enlarges possible destruction; Folders refused; no rollback. Fault-tolerant continuation can read upstream partial state; threshold refusals still do not apply changes; override does not waive null/unique rules. Wipe's catalogue default disclosed before example; explicit `--unbind` retains catalogue while withdrawing target claims. | Recursive/stale/dry-run/reload/failure/runner, Wipe and workflow tests; exact operation references |
| Mirror | Complete ordinary same-workspace task with existing source/destination catalogue and targets, source read-only, full destination empties warning, settled-plan confirmation if correct, no dry-run or decline/rerun ceremony. Mixed borrowed/local state, source-bound omitted items, preserving materialisation and reset/failure boundaries remain linked. | Existing task setup reused; Mirror plan/boundary tests and retained strategy/reference pages |
| Selection | Full graph, oracle link, case-insensitive whole-name regex, repeated-match union, each pattern must match, independent closure from original seeds, omitted Depot/siblings, explicit item boundary, Lakehouse areas and readiness barriers retained. | Real fixture LoadDag and oracle; recursive selection source tests |
| Concurrency | Full progression and every fenced example retained. Invocation-wide cap 2 is not Spark capacity; resource limits/defaults unchanged, Warehouse per-target limits and shared Spark application qualified. | Real fixture Runner observed peak 2 at Warehouse limits 4 and 1; invocation/resource intersection tests |
| Performance | Fixed workload, work/waits/overhead, Session/workflow timings, endpoint readiness, serial chains, operation history and measured synthetic F64 context retained. | Existing performance page; exact benchmark provenance below |
| Automation | Curated Session → workflow → native Fabric host → destination-specific bundle route. Actual workflow loader/parser used; separate Build calls, finding-vs-execution continuation, no rollback, credentials/auth distinction and installed-state boundaries retained. | Workflow source tests; existing portable/bundle/context pages |

Selection and concurrency code fences were compared programmatically with their legacy sources: **8 selection and 5 concurrency fences byte-identical**. Only contextual prose/links changed, plus the explicit Spark-capacity clarification. The performance workflow command now names the documented `verify` workflow instead of an unexplained `full` sequence.

Benchmark provenance retained for maintainers: approved plan cites product PR #193, an observed synthetic F64 estate with 3,000 objects and approximately 4.05 billion estate row insertions. Exact times: first Load **61m20**, unchanged Load **7m57**, later day Loads **13m05** and **12m56**. These are not distinct source records, a capacity recommendation or an SLA. Public copy stays around an hour / later measured incremental Loads under 15 minutes. No benchmark was remeasured here.

## Executed checks

| Check | Actual result |
| --- | --- |
| Authored estate extraction and frozen production parsers, network denied | 12 estate pages (including unchanged index); **75 bash + 6 Session + 6 workflow command forms**; 5 complete workspace configs, 2 config additions, 1 Shortcut declaration, 3 Python API calls, 15 catalogue identifier checks |
| Exact rendered/fixture comparison | Both managed-source dev/prod configs byte-identical; fixture hashes unchanged after effective-model compilation; Delivery and Depot remain Import |
| Real local CLI Check | **4 projects valid**: assembled published Landing + Dispatch addition, Warehouse journey, managed-source Parcel, Load-selection snapshot |
| Existing `tools/check_docs_refresh_examples.py --weaver-checkout <product>` | **6 fixtures**, **53 README commands** parsed; real LoadDag exact selection/original-seed union/regex refusal/Lakehouse ambiguity checks; real Runner cap observed 2 under per-Warehouse 4 and 1; authored hashes unchanged; no service execution |
| Existing `tools/check_journey_examples.py --weaver-checkout <product>` | **15 legacy pages, 92 commands, 9 configs, 3 Python calls, 12 byte-identical blocks, 4 exact rendered projects Check**; no network/service execution. This retained-tool check is additional evidence, not substituted for new estate-page checks. |
| Focused existing source tests, explicit network denial, `-m 'not fabric'` | **561 passed in 30.99s**, all core; 17 named existing test files, listed in reproducer below |
| Strict MkDocs build with existing docs interpreter | Exit 0; final run built in **5.30s**, to scratch `estate-site`. No source build warnings; Material printed its upstream MkDocs-2 migration notice. |
| Built estate content link/anchor crawl | **12 pages, 364 internal links/fragments, 0 broken** |
| Built search inventory | **5 live owner pages** present for selection/ancestors/regex, concurrency/Spark, Catalogue/Health, Mirror and dependencies; no search-excluded stub used |
| `git diff --check` | Exit 0; final staged scope inspected separately |
| Additional whole-site `check_fabric_first_story.py` attempt | Stops at line 75 before estate assertions: expects the first product-main link to end `/getting-started/`, but the unchanged product source links to `https://docs.weaverstack.dev/getting-started/first-project/`. Parent-owned guard/product integration issue; no scoped file was changed to bypass it. |

The first scratch checker attempts exposed two harness mistakes, not product/content failures: the ordinary catalogue tuple excludes optional `MIRROR`, and repository items are `WeaverItem` objects rather than IDs. The scratch checker was corrected to the source declarations and rerun successfully. No product or fixture code was changed to obtain a pass.

## Continuous reader route and transitions

`estate/index` → `connected-items` → `environments` → `catalogue-and-health` → `development-cycle` → `operate` → `recovery` → optional `mirror` → `selective-runs` → `concurrency` → `performance` → `automation-and-deployment`.

- Connection to mapping: “Once the connections work, map development and production without changing those logical source identities.”
- Mapping to state: “With one configuration selecting the intended estate, read Catalogue and Health to see what was installed and what happened there.”
- State to development explicitly preserves the existing installed results; ordinary development precedes optional Mirror. Operations can also be entered directly with no source change/Build.
- Separate snapshots are explicit: Landing + Dispatch; Warehouse StatusEvent/View; managed-source Operations Delivery + Parcel with inline Depot; fine-control DAG; portable native execution. No fake unified runnable estate was constructed.

This is an author read-through, not the independent or human editorial acceptance reserved for the later batch. The long recovery page retains destructive/action-specific rules rather than collapsing them into a short pointer; finer selection/concurrency remain complete focused pages.

## Limits and unresolved gates

No unsupported syntax or new runtime discrepancy was found in this assigned surface. Local Check establishes declarations, not service behaviour. No credentials, capacity, Fabric tenant, live SQL/DAX query, model refresh, Report binding/rendering, runtime publication/admission, Mirror/Wipe mutation, release, deployment, GitHub/Asana or delegated work occurred. Frozen-source offline tests use their existing explicit boundary inputs, not fabricated live responses.

Remote behaviour remains the independent acceptance gate, especially the Dispatch SQL-endpoint readback, source-backed model refresh/reconciliation, actual Report binding, and Mirror/Wipe effects. Whole-site migration/search ranking/visual review and generated-reference integration remain parent-owned. Published-package/source version alignment remains the existing preview publication constraint. No publication or human acceptance is claimed.

## Reproduce the authored check

Save the following as a scratch Python file and run with the pinned `PYTHONPATH` and reused product interpreter. It denies network access and checks only authored shape, source signatures and complete local projects.

```python
"""Offline authored estate checks; exercises pinned production parsers."""
import ast
import inspect
import json
import re
import shlex
import shutil
import socket
import sys
import tempfile
from pathlib import Path

ROOT = Path('/opt/data/scratch/Fors/weaver-docs-refresh/item-first-estate')
PRODUCT = Path('/opt/data/scratch/Fors/weaver-docs-refresh/product')
sys.path[:0] = [str(PRODUCT / 'src'), str(PRODUCT / 'tests'), str(ROOT / 'tools')]
import weaver
import yaml
from weaver.config import parse_workspace
from weaver_cli.main import build_parser, main as cli_main
from weaver.catalogue.tables import CATALOGUE_TABLES, MIRROR
CATALOGUE_TABLES = (*CATALOGUE_TABLES, MIRROR)
from check_docs_refresh_examples import compile_models, hashes, model

assert Path(weaver.__file__).resolve().is_relative_to(PRODUCT / 'src')
def blocked(*args, **kwargs):
    raise AssertionError('Offline check attempted network access')
socket.socket.connect = blocked
socket.create_connection = blocked

counts = dict(pages=0, bash_commands=0, session_commands=0, workflow_commands=0,
              workspace_configs=0, config_fragments=0, shortcuts=0, python_calls=0,
              catalogue_identifiers=0, assembled_checks=0, synchronized_blocks=0)
for path in sorted((ROOT / 'docs/estate').glob('*.md')):
    counts['pages'] += 1
    body = path.read_text()
    assert len(re.findall(r'^# ', body, re.M)) == 1
    for language, header, content in re.findall(r'^```(\w+)([^\n]*)\n(.*?)^```', body, re.M | re.S):
        if language == 'bash':
            for line in content.replace('\\\n', ' ').splitlines():
                if line.startswith('weaver '):
                    build_parser().parse_args(shlex.split(line)[1:])
                    counts['bash_commands'] += 1
        if language == 'text':
            for line in content.splitlines():
                if line.startswith('weaver> '):
                    command = line.removeprefix('weaver> ')
                    if command != 'exit':
                        build_parser().parse_args(shlex.split(command))
                        counts['session_commands'] += 1
        if language == 'yaml':
            raw = yaml.safe_load(content)
            if 'workspace' in raw:
                parse_workspace(raw)
                counts['workspace_configs'] += 1
            elif 'workflows' in raw:
                from weaver_cli.workflow import load_workflow, workflow_words
                with tempfile.TemporaryDirectory(prefix='estate-workflow-') as tmp:
                    workflow_path = Path(tmp)/'workflow.yml'
                    workflow_path.write_text(content)
                    for name in raw['workflows']:
                        commands, _ = load_workflow(name, file=str(workflow_path))
                        for command in commands:
                            build_parser().parse_args(workflow_words(command))
                            counts['workflow_commands'] += 1
            elif 'execution' in raw:
                parse_workspace({'workspace':'Parcel Operations', **raw})
                counts['config_fragments'] += 1
            elif 'logical' in raw:
                counts['shortcuts'] += 1
            else:
                assert 'Add under targets' in header
                parse_workspace({'workspace':'Parcel Development', 'targets':raw})
                counts['config_fragments'] += 1
        if language == 'python':
            tree = ast.parse(content)
            for call in ast.walk(tree):
                if isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute) and isinstance(call.func.value, ast.Name) and call.func.value.id == 'weaver':
                    signature = inspect.signature(getattr(weaver, call.func.attr))
                    for keyword in call.keywords:
                        assert keyword.arg in signature.parameters, (path, keyword.arg)
                    counts['python_calls'] += 1
    for identifier in set(re.findall(r'`(_\.[A-Za-z]+)`', body)):
        assert identifier in {t.qualified for t in CATALOGUE_TABLES}, (path, identifier)
        counts['catalogue_identifiers'] += 1

# Synchronize complete published files with their unchanged native fixture.
def blocks(name, language):
    return re.findall(r'^```'+language+r'[^\n]*\n(.*?)^```', (ROOT/'docs/estate'/name).read_text(), re.M|re.S)
fixture = ROOT/'examples/parcel-powerbi-fabric'
for env in ('dev', 'prod'):
    config = (fixture/f'workspace-{env}.yml').read_text()
    assert config in blocks('environments.md', 'yaml')
    counts['synchronized_blocks'] += 1
before = hashes(fixture)
effective = model(compile_models(fixture))
assert effective.tables['Delivery'].partitions['Delivery'].mode == 'import'
assert effective.tables['Depot'].partitions['Depot'].mode == 'import'
assert hashes(fixture) == before

# Assemble the published connection addition with the existing Landing snapshot.
with tempfile.TemporaryDirectory(prefix='estate-authored-') as tmp:
    project = Path(tmp)/'connected'
    shutil.copytree(ROOT/'examples/parcel-lakehouse', project)
    target = project/'Warehouse/Dispatch/shortcuts.yml'
    target.parent.mkdir(parents=True)
    shortcut = next(b for b in blocks('connected-items.md','yaml') if b.startswith('logical:'))
    target.write_text(shortcut)
    assert cli_main(['check',str(project)]) == 0
    counts['assembled_checks'] += 1
    from check_docs_refresh_examples import parse
    parsed = parse(project)
    assert any(str(item.identity)=='Warehouse/Dispatch' for item in parsed.items)

# Actual source checker on unchanged complete direct-entry projects.
for name in ('parcel-warehouse-journey','parcel-powerbi-fabric','parcel-load-selection'):
    assert cli_main(['check',str(ROOT/'examples'/name)]) == 0
    counts['assembled_checks'] += 1

print(json.dumps({'product_import':weaver.__file__, 'network':'denied', **counts}, indent=2))
```

## Reproduce focused source tests

Run the following from the product checkout with the same interpreter and pinned `PYTHONPATH`:

```python
"""Run the named existing source tests with network access refused."""
import socket
import sys
from pathlib import Path
PRODUCT = Path('/opt/data/scratch/Fors/weaver-docs-refresh/product')
sys.path[:0] = [str(PRODUCT/'src'),str(PRODUCT/'tests')]
import weaver
import pytest
assert Path(weaver.__file__).resolve().is_relative_to(PRODUCT/'src')
def denied(*args, **kwargs):
    raise AssertionError('Offline test attempted network access')
socket.socket.connect = denied
socket.create_connection = denied
paths = [
    'tests/targeted/test_load_recursive_selection_cycle.py',
    'tests/targeted/test_load_stale_selection_boundary.py',
    'tests/targeted/test_load_dry_run_cycle.py',
    'tests/targeted/test_reload_run_cycle.py',
    'tests/targeted/test_load_failure_cycle.py',
    'tests/targeted/test_load_contract_declaration.py',
    'tests/targeted/test_invocation_concurrency_boundary.py',
    'tests/targeted/test_invocation_api_concurrency_boundary.py',
    'tests/targeted/test_health_operation_boundary.py',
    'tests/test_mirror_plan_boundary.py',
    'tests/test_mirror_boundary.py',
    'tests/test_wipe_plan_declaration.py',
    'tests/test_wipe_mutation_boundary.py',
    'tests/test_workflow_cycle.py',
    'tests/test_config_declaration.py',
    'tests/test_workspace_config_discovery_declaration.py',
    'tests/test_run_cycle.py',
]
print('Pinned import:',weaver.__file__)
print('Existing source test files:',len(paths),'network denied')
raise SystemExit(pytest.main(['-q','-m','not fabric',*paths]))
```

## Reproduce built link and search checks

Run after the strict build to the stated scratch site path:

```python
"""Crawl authored estate content links/anchors and built search entries."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

SITE = Path('/opt/data/profiles/editor/cache/scratch/estate-site')
class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = set()
        self.links = []
        self.article = False
        self.feed(path.read_text())
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'article':
            self.article = True
        if self.article and tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])
    def handle_endtag(self, tag):
        if tag == 'article':
            self.article = False

cache={}
def parsed(path):
    path=path.resolve()
    if path not in cache:
        cache[path]=Page(path)
    return cache[path]
count=0
for path in sorted((SITE/'estate').glob('*/index.html'))+[SITE/'estate/index.html']:
    for href in parsed(path).links:
        url=urlsplit(href)
        if url.scheme or url.netloc:
            continue
        dest=SITE/url.path.lstrip('/') if url.path.startswith('/') else path.parent/url.path
        if not url.path:
            dest=path
        elif url.path.endswith('/') or dest.is_dir():
            dest=dest/'index.html'
        assert dest.is_file(), (path,href,dest)
        if url.fragment:
            assert unquote(url.fragment) in parsed(dest).ids,(path,href)
        count+=1
search=json.loads((SITE/'search/search_index.json').read_text())['docs']
required={
 'estate/selective-runs/':('ancestors','descendants','regex'),
 'estate/concurrency/':('concurrency','Spark'),
 'estate/catalogue-and-health/':('Health','Catalogue'),
 'estate/mirror/':('Mirror',),
 'estate/connected-items/':('dependencies',),
}
for location, terms in required.items():
    entries=[d for d in search if d['location'].split('#')[0]==location]
    assert entries,location
    combined=' '.join(d['text']+' '+d['title'] for d in entries)
    assert all(term.lower() in combined.lower() for term in terms),(location,terms)
print(json.dumps({'estate_pages':12,'internal_content_links_and_fragments':count,'broken':0,'live_search_owners':len(required)},indent=2))
```
