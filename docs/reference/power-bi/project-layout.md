# Power BI project layout

Power BI source belongs under `PowerBI/<project>/`. A project groups local model definitions and Reports; the directory name is a selector, not the logical model name.

```text
PowerBI/
├── policy.tmdl
├── annotations/
│   └── Parcel__HideKeys.py
└── Parcel/
    ├── Parcel.pbip
    ├── Parcel.SemanticModel/
    │   ├── definition.pbism
    │   └── definition/
    │       ├── database.tmdl
    │       ├── model.tmdl
    │       └── tables/Deliveries.tmdl
    ├── Parcel.Report/
    │   ├── definition.pbir
    │   └── definition/...
    ├── Parcel.tmdl
    ├── Summary.tmdl
    ├── tests/
    │   └── Parcel/Parcel.CountMatches.dax
    └── assumptions/
        └── Parcel/Parcel.PositiveCount.dax
```

This tree illustrates locations; native `definition/` contents must be a complete project, not literal ellipsis files. Native Report definitions may also use the supported `report.json` form. Native semantic definitions require TMDL `definition/` with `definition.pbism`; `model.bim` is not a supported authored base in this project path. See [Requirements and compatibility](requirements-and-compatibility.md).

## Model discovery and identity

- Every discovered `<Name>.SemanticModel` directory declares `SemanticModel/<Name>`.
- Every direct `PowerBI/<project>/<Name>.tmdl` declares that model too. If the exact same-name native directory exists, this file is its overlay, not a second model. Without the native directory it supplies a standalone model definition.
- Multiple named models may coexist. Case-only duplicates or duplicate native definitions are refused with both paths. Logical model names must be unique across the parsed project, not merely within one Power BI group.
- A `.pbip` entrypoint is optional for discovery. When present, its `artifacts[].report.path` must be a relative forward-slash path to a discovered Report inside the same Power BI group. Invalid or escaping references fail parsing.
- `PowerBI` selects all Power BI items for Build; `PowerBI/Parcel` selects that group's models and Reports. Load/Test project selectors resolve only semantic models. Exact `SemanticModel/Name` and `Report/Name` select individual logical items where the operation supports them.

`PowerBI/policy.tmdl` applies to all models but declares no separate model. It is merged before each final model's local overlay. `PowerBI/annotations/` is not a Power BI group. It holds one matching `<Namespace>__<Name>.py` class/file per custom annotation, shared across all project models. Nested annotation directories and annotations inside `.SemanticModel` are refused.

## Report discovery and association

`<Name>.Report` declares `Report/<Name>`. Its `definition.pbir` must contain exactly one native `datasetReference.byPath` or `.byConnection` with a non-empty `path` or `connectionString`, respectively.

Association precedence is:

1. a same-name semantic model in that Power BI group, including a standalone `<Name>.tmdl`;
2. otherwise, `byPath` resolved relative to the Report directory to a local model in that group;
3. otherwise, an unrelated `byConnection` remains as authored.

A `byPath` that cannot resolve locally is an error. A same-name association takes precedence even over an authored `byConnection`. Linked deployment resolves the physical model target and rewrites the deployment payload, not the authored `definition.pbir`. See [binding requirements](requirements-and-compatibility.md#report-binding).

## Validation ownership

DAX files belong at `PowerBI/<project>/tests/<Model>/<Schema.Object>.dax` or `assumptions/<Model>/<Schema.Object>.dax`. The owner must be an exact local model definition. The metadata ID must match the filename and validation directory kind. Tests and Assumptions share one identity namespace per model; variants own their validations and do not inherit a base's Tests through composition.

Native `.pbi` cache content is excluded from deployment definitions. Report changes and caches do not change the model source signature. Source preparation does not overwrite authored native bytes.

Use [TMDL](tmdl.md) for merge and composition rules, [Validations](validations.md) for complete DAX metadata, and [Shared selection](../operation-behaviour/shared-selection-and-identity.md) for target grammar. The retired `extension.tmdl` layout is replaced by `PowerBI/policy.tmdl` and named `<Model>.tmdl` files; do not use the old filename as an unnamed universal overlay.
