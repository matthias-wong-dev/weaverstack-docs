# Add a custom model annotation

Set a native measure's display folder with one small Python handler. Use a custom annotation when declarative TMDL and built-ins do not express the convention you need.

## Before you start

Continue [shared modelling standards](shared-policy.md) with the same Parcel model, policy and local format override. Add the handler and annotation below; keep Delivery, Depot, their partitions and your workspace configuration. For direct entry, complete that task first.

**Annotation files are trusted executable Python.** Weaver loads them while parsing a project, including Check. Do not Check or Build an untrusted project. They are not sandboxed metadata, and Power BI Desktop does not execute them.

## 1. Define the handler

Create `PowerBI/annotations/Parcel__DisplayFolder.py`:

```python
"""Place an annotated measure in a native display folder."""

from weaver.semantic_models import Annotation


class Parcel__DisplayFolder(Annotation):
    scopes = frozenset({"measure"})

    def apply(self, target):
        if not self.value:
            self.error("requires a non-empty display folder")
        target.displayFolder = self.value
```

Use one self-contained subclass per file, with matching filename stem and class name. `__` separates namespace segments: `Parcel__DisplayFolder` becomes `Parcel.DisplayFolder`. `Weaver` is reserved for built-ins. `scopes` limits this handler to measures; `apply` changes the live native object and returns nothing.

## 2. Declare its use

The model overlay `PowerBI/Parcel/Parcel.tmdl` contains:

```tmdl
model Model
	annotation 'Weaver.AutoHideForeignKeys' = true

table Delivery
	measure 'Delivery Count'
		formatString: 0 "deliveries"
		annotation 'Parcel.DisplayFolder' = Parcel metrics
```

The handler's `value` reads `Parcel metrics`; assignment writes the measure's native `displayFolder`. It does not introduce a new Weaver-specific property in the deployed model.

## 3. Build and inspect

```bash
weaver check
weaver build --item SemanticModel/Parcel
```

<!-- cli-capture: {"id": "88b-annotation-build", "title": "Build · apply the custom annotation"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Build · apply the custom annotation">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Workspace  Parcel Development
Catalogue  none
Targets
  SemanticModel/Parcel


Build

  Resolve semantic data sources                                                                            0.0s
    Resolve SemanticModel/Parcel                                                                           0.0s
  Read target inventories                                                                                  0.1s
  Read semantic sources                                                                                    0.0s
  Prepare bundle                                                                                           0.0s
Install selection
  SemanticModel/Parcel
    changed                 1
    selected for build      1

→   SemanticModel/Parcel · Deploy semantic definitions · 1 action
<span class="terminal-status-green">✓   SemanticModel/Parcel · Deploy semantic definitions · 1 action                                         20.8s</span>
→   SemanticModel/Parcel · Verify deployed semantic definitions · 1 action
<span class="terminal-status-green">✓   SemanticModel/Parcel · Verify deployed semantic definitions · 1 action                                20.5s</span>
  Install                                                                                                 41.4s
<span class="terminal-status-green">✓ Build                                                                                                   41.7s</span>

Installation
<span class="terminal-status-green">    2 succeeded</span>
    0 failed
    0 skipped
  Report  [local-path]
  Bundle  c12834f2415a23a6f9563e52fdd349f315874111a1413c36013ad132145c572e
</code></pre>
</figure>
<!-- /cli-capture -->

```bash
weaver load SemanticModel/Parcel
```

The deployed Delivery Count measure now has `displayFolder: Parcel metrics` and keeps its `0 "deliveries"` format; its partition is unchanged. Build applied the handler to the deployed definition only. Your authored TMDL still contains just the annotation.

## 4. Read a located diagnostic

Create `failure/Parcel.tmdl` with this complete declaration for the optional failure exercise:

```tmdl
model Model
	annotation 'Weaver.AutoHideForeignKeys' = true

table Delivery
	measure 'Delivery Count'
		annotation 'Parcel.DisplayFolder' = ""
```

Swap it in, Build, then put the normal overlay back. Build refuses before deploying anything, so there is nothing to undo in the workspace:

```bash
cp PowerBI/Parcel/Parcel.tmdl Parcel.tmdl.saved
cp failure/Parcel.tmdl PowerBI/Parcel/Parcel.tmdl
weaver build --item SemanticModel/Parcel
mv Parcel.tmdl.saved PowerBI/Parcel/Parcel.tmdl
```

<!-- cli-capture: {"id": "89-annotation-diagnostic", "title": "Build · located annotation error"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Build · located annotation error">
<figcaption>Terminal output <span class="terminal-exit">exit 1</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Workspace  Parcel Development
Catalogue  none
Targets
  SemanticModel/Parcel


Build

  Resolve semantic data sources                                                                            0.0s
    Resolve SemanticModel/Parcel                                                                           0.0s
  Read target inventories                                                                                  0.1s
  Read semantic sources                                                                                    0.0s
<span class="terminal-status-red">✗ Prepare bundle                                                                                           0.0s</span>
<span class="terminal-status-red">✗ Build                                                                                                    0.3s</span>

<span class="terminal-status-red">error: PowerBI/Parcel/Parcel.tmdl:6: Parcel.DisplayFolder: requires a non-empty display folder</span>
</code></pre>
</figure>
<!-- /cli-capture -->

Run these commands one at a time. In an interactive terminal a refused Build waits at `Enter to retry, Esc to exit`, and a pasted next line would be read as that answer. Press Esc, then run `mv`.

The handler calls `error` for an empty value. The diagnostic identifies the declaration's file and line. Check loads the class and checks declaration shape; handler application occurs during compilation, so the value failure belongs at that boundary.

## Choose a phase only when needed

The supported handler base and native objects come from `weaver.semantic_models`; use that public API rather than compiler internals. `self.error(...)` reports a located failure and stops the transformation.

The default `post_schema` phase sees columns after managed-source completion. This folder handler uses that default. Use `phase = "schema"` only when a handler introduces structure or a managed-source declaration needed for generation. Adding a new managed source during `post_schema` is refused. Composition merges raw bases before handlers run once on the final model.

If the next question is where Delivery comes from, [connect a managed Fabric source](managed-sources.md); if it is whether the measure is right, [validate the model](validation.md). Both keep the modelling conventions you have added.

## Related tasks

- [Look up the supported extension API](../reference/python/semantic-models.md).
- [Prefer a built-in when it fits](../reference/power-bi/annotations.md).
- [Compose model variants](composition.md).
