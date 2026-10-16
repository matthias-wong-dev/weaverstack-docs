# TMDL policy, overlays and composition

Native semantic-model parts remain the base definition. `PowerBI/policy.tmdl` and `PowerBI/<project>/<Model>.tmdl` are partial native declarations merged into that base. A named TMDL file without a same-name native directory can define a standalone model. Weaver edits addressed native spans rather than reconstructing every object from an internal schema.

## Addressing and merge rules

Object identity is its native kind and case-insensitive name at each parent path. Table, column, measure, relationship, role, hierarchy, partition and annotation identities remain separate. Names containing spaces use native single-quote syntax. Extension root objects start at column zero; each child adds one tab or four spaces. A root must be a named object; overlays address model content, not a `database` object.

| Declaration | Behaviour |
| --- | --- |
| `ref table Deliveries` | Requires an existing table; a missing reference fails with source file/line. |
| `table Deliveries` | Merges that table if present, otherwise creates it. |
| Explicit scalar/native property | Replaces the addressed value. |
| Explicit expression/header assignment | Replaces the addressed expression, preserving authored expression text. |
| Named child | Merges recursively by identity; other children remain. |
| Omitted property or object | Leaves the base value/object in place. Omission is not deletion. |
| `///` description | Replaces the addressed description when supplied. |
| `Weaver.Exclude = true` | Removes its table/column during final annotation execution. |

A child-bearing `ref` can refine an existing object. Missing parents, multiple matching declarations, duplicate declarations within an overlay, malformed indentation/properties and unclosed expression fences fail with located diagnostics. A root `model Model` must address the base model's native name. Unknown native properties and object kinds remain opaque unless explicitly edited; Fabric still validates their native meaning.

```tmdl
model Model
    annotation 'Weaver.AutoHideForeignKeys' = true

ref table Deliveries
    ref measure 'Delivery count'
        formatString: 0
```

This fragment changes the policy and one existing measure property. It does not replace the whole model/table or remove measures omitted from the fragment.

## Policy and local precedence

For a model without bases, merge native definition, shared `PowerBI/policy.tmdl`, then the same-name local TMDL file. A standalone named TMDL file, with no native directory, takes the local position: policy merges first and the file's explicit values win. Later explicit values win; omitted values remain. A local `false` can disable a shared Boolean annotation before handlers execute. All final annotations then act on the composed definition, not separately on every source layer.

## Compose named models

At model scope, `Weaver.BaseSemanticModels` lists one local model name per non-blank line, optionally double quoted. These are names, not `SemanticModel/` targets or cross-project paths.

```tmdl
model Model
    annotation 'Weaver.BaseSemanticModels' =
        Foundation
        Measures
```

Composition recursively visits bases in listed order, merges their raw native definitions and local overlays, then the variant's native definition, the shared policy once for the final variant and its local overlay. The variant's explicit values therefore override its bases and shared policy. A later base overrides an earlier one on the same addressed property. Native `definition.pbism` and database metadata follow the later native contributor when supplied.

Self-reference, missing/non-local bases, cycles and repeated ancestry fail. A diamond that reaches the same ancestor twice is not silently deduplicated. `ref` declarations in a target overlay resolve after bases have been assembled. Base reuse does not add a physical base deployment to the selected variant; select base items explicitly if you also want to deploy them. Validation directories are owned by the variant, not inherited from bases.

## Preservation and deployment boundary

Unaddressed native TMDL, unknown neighbouring properties, comments and expression whitespace remain in the package; addressed spans may be reindented into the target's style. Authored source files are not rewritten. Deployed TMSL readback uses typed named collections for verification; it does not make `model.bim` a supported authored base or expose an unrestricted JSON merge interface.

Build verifies deployed readback for required edits, removals and generated structure before catalogue certification. Fabric normalization may produce warnings; missing required edits fail. Native passthrough is not a promise to preserve every service-side RLS, partition or manual edit across deployment, nor a guarantee of lossless bidirectional Desktop round-tripping.

Use [Annotations](annotations.md) for generation and exclusion, [Project layout](project-layout.md) for filenames and [Python extension API](../python/semantic-models.md) when a native overlay cannot express the transformation. No public compiled-TMDL export is provided by this reference.
