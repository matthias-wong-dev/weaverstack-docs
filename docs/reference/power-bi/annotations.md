# Semantic-model annotations

Annotations are native TMDL declarations. Weaver recognizes the following seven names in its reserved namespace. Unknown names in `Weaver` are errors; annotations in an undefined project namespace remain native. Names are dispatched exactly, not repaired or normalized. Built-ins run on the final composed model, with located file/line diagnostics.

| Annotation | Scope | Value | Phase/effect |
| --- | --- | --- | --- |
| `Weaver.Source` | table | canonical managed relation | schema; lineage, and source generation when no partition is authored |
| `Weaver.BaseSemanticModels` | model | one local model name per non-blank line | composition directive, not a handler |
| `Weaver.MeasureTable` | table | exactly `true` | schema; calculated measure selector table |
| `Weaver.Switch` | measure | one measure reference per non-blank line | post-schema; generated value and dynamic format expressions |
| `Weaver.AutoHideColumns` | model or table | one case-sensitive glob per non-blank line | post-schema; sets matching columns' `isHidden` |
| `Weaver.AutoHideForeignKeys` | model | exactly `true` or `false` | post-schema; hides relationship many-side columns when true |
| `Weaver.Exclude` | table or column | exactly `true` or `false` | post-schema; removes the addressed object when true |

Omission means the transformation is not requested. Boolean `false` is a no-op for ForeignKeys and Exclude, not an instruction to reverse an earlier native edit. A local `false` can replace shared policy before execution. These annotations are not a general security policy or a runtime service dependency; executing them again requires Weaver.

## `Weaver.Source`

```tmdl
table Deliveries
    annotation 'Weaver.Source' = Warehouse/Operations/Parcel.Deliveries
```

The value must be `Warehouse/<item>/<schema>.<object>` or `Lakehouse/<item>/Tables/<schema>.<object>`. Lakehouse `Files` and bare or workspace-qualified relation names are unsupported. The annotation declares the source relation and managed lineage; it does not itself load that relation.

For a table with authored partitions, Weaver retains the native partition, mode and authored column types. The declaration provides lineage and available descriptions; it does not broadly replace M or generate every source column. Known lineage can be declared without a catalogue for a known source item, but managed-source metadata generation is a separate boundary.

For a table without an authored partition, Build needs resolved source endpoint and column metadata. Build the managed source first, then the model with catalogue integration. Source columns are generated and refined by authored columns, matched by `sourceColumn` or name. An unmatched authored column must be calculated. Unsupported source types fail; source housekeeping audit/signature columns are omitted unless explicitly authored. Existing table/column descriptions win; otherwise available source descriptions/notes fill them. There is no `Weaver.IncludeDescriptions` annotation.

Generated partitions use M navigation in a model with `defaultMode: import`; otherwise the generation path supplies Direct Lake entity partitions. Their shared SQL expression is reused for tables reading the same item. Direct Lake still needs its service/capacity/source prerequisites. A source annotation is not a grant of credentials. See [source mapping](requirements-and-compatibility.md#source-mapping-and-connections).

## `Weaver.BaseSemanticModels`

```tmdl
model Model
    annotation 'Weaver.BaseSemanticModels' =
        Foundation
        Measures
```

Non-blank lines name local definitions in the same Power BI group, optionally double quoted. Raw bases merge in listed recursive order before the final policy and overlay. Missing/non-local bases, self-reference, cycles and repeated ancestors fail. This does not select a physical base for deployment or inherit base validations. See [composition precedence](tmdl.md#compose-named-models).

## `Weaver.MeasureTable`

```tmdl
table 'Measure selector'
    annotation 'Weaver.MeasureTable' = true
```

Use a bare table. This creates an Import calculated partition from `INFO.VIEW.MEASURES()` with string columns `Measure name`, `Expression`, `Format string definition`, `Description`, `Display folder`, `Table` and `Data category`. It retains separately authored visibility. Ordinary `DataType` and `FormatString` projections are not generated. `false` is rejected.

An authored partition cannot be replaced. The only permitted existing partition is the exact generated same-name calculated partition with the generated expression. Native DAX/function availability and refresh remain service requirements.

## `Weaver.Switch`

```tmdl
ref table Metrics
    measure 'Selected measure' = 0
        annotation 'Weaver.Switch' =
            Metrics[Delivery count]
            Metrics[Late count]
```

Exactly one table in the completed model must carry `Weaver.MeasureTable`. Each reference is `Table[Measure]` (native quoted table names allowed) or a unique unqualified measure name, optionally bracketed. Lookup ignores case. At least one reference is required.

The generated value expression switches on `SELECTEDVALUE('<selector>'[Measure name])`. The dynamic format expression switches by the same measure-name labels, taking a referenced measure's usable dynamic format or its static `formatString`. Missing/ambiguous references, duplicate selector labels, references to another Switch measure and measure-context-dependent formats (`SELECTEDMEASURE`, `SELECTEDMEASURENAME`, `SELECTEDMEASUREFORMATSTRING`, `ISSELECTEDMEASURE`) fail. Qualified references do not permit two identical selector labels from different tables.

This generates a measure, not a calculation group. Shared native calculation groups can be authored in TMDL; no built-in calculation-group annotation is supplied.

## `Weaver.AutoHideColumns`

```tmdl
model Model
    annotation 'Weaver.AutoHideColumns' =
        *Key
        Internal*
```

At model scope all tables are inspected; at table scope only that table. Values are newline-separated non-empty, case-sensitive native glob patterns (`*`, `?`, bracket classes), not regular expressions. Matches receive `isHidden = true`; non-matches are not unhidden. It runs after source generation so inferred columns can match too.

## `Weaver.AutoHideForeignKeys`

```tmdl
model Model
    annotation 'Weaver.AutoHideForeignKeys' = true
```

When true, native relationship cardinality selects each many-side column. Omitted cardinalities default to `from=many`, `to=one`. Both many sides of a many-to-many relation may be hidden. An unaddressable many-side endpoint fails with the relationship name. A model without relationships has no column to change. This is visibility, not RLS/OLS.

## `Weaver.Exclude`

```tmdl
ref table Deliveries
    ref column InternalKey
        annotation 'Weaver.Exclude' = true
```

When true, deletes the table or column and its native references. Exclusion is checked as absence on deployed readback; source inference does not reintroduce an excluded generated column. Removing an object can leave unrelated authored DAX references invalid; verify the final model. `false` retains the object but does not recreate something absent from the composed source. Exclusion is not a substitute for permissions or security validation.

See [Python extension API](../python/semantic-models.md) for custom namespaces, trusted-code boundaries and `schema`/`post_schema` ordering.
