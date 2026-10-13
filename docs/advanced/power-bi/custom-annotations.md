# Add a custom model annotation

Set a native measure's display folder with one small Python handler. Use a custom annotation when declarative TMDL and built-ins do not express the convention you need.

## Before you start

Use the independent [standards project](https://github.com/matthias-wong-dev/weaverstack-docs/tree/docs/progressive-journeys-refresh/examples/parcel-powerbi-standards) and the [ordinary deployment prerequisites](../../basics/power-bi/deploy-pbip.md). Work from the example directory and edit its development workspace configuration.

**Annotation files are trusted executable Python.** Weaver loads them while parsing a project, including Check. Do not Check or Build an untrusted project. They are not sandboxed metadata, and Power BI Desktop does not execute them.

## 1. Define the handler

The fixture's `PowerBI/annotations/Parcel__DisplayFolder.py` is complete:

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
weaver check .
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
```

Inspect the deployed Delivery Count measure: its display folder is `Parcel metrics`, its format is `0 "deliveries"`, and the original partition remains. The Report should show `2 deliveries`. Compilation does not rewrite authored native files.

## 4. Read a located diagnostic

Use the supplied empty-value overlay, restoring the normal one even if Build refuses:

```bash
cp PowerBI/Parcel/Parcel.tmdl Parcel.tmdl.saved
cp failure/Parcel.tmdl PowerBI/Parcel/Parcel.tmdl
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
mv Parcel.tmdl.saved PowerBI/Parcel/Parcel.tmdl
```

The handler calls `error` for an empty value. The diagnostic identifies the declaration's file and line. Check loads the class and checks declaration shape; handler application occurs during compilation, so the value failure belongs at that boundary.

## Choose a phase only when needed

The default `post_schema` phase sees columns after managed-source completion. This folder handler uses that default. Use `phase = "schema"` only when a handler introduces structure or a managed-source declaration needed for generation. Adding a new managed source during `post_schema` is refused. Composition merges raw bases before handlers run once on the final model.

Cleanup is limited to this fixture's newly created Report/model, Reports first.

## Related tasks

- [Look up the supported extension API](../../reference/python/semantic-models.md).
- [Prefer a built-in when it fits](../../reference/power-bi/annotations.md).
- [Compose model variants](model-composition.md).
