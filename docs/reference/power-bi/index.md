# Semantic models and Reports reference

Weaver reads native Power BI project definitions, optional TMDL policy/overlays and model-owned DAX validations. Build produces and verifies native service definitions without rewriting the authored project. Models and Reports belong to the same project and operation flow as their managed sources.


- [Project layout](project-layout.md): discovery, identities, native files and validation ownership.
- [TMDL](tmdl.md): policy, overlay and composition precedence; native preservation.
- [Annotations](annotations.md): all seven implemented built-ins, scope and value grammar.
- [Validations](validations.md): DAX findings and comparison with Lakehouse/Warehouse SQL.
- [Requirements and compatibility](requirements-and-compatibility.md): supported modes, permissions, Report binding and source connections.
- [Python extension API](../python/semantic-models.md): trusted custom annotations and live native objects.

The shared [Build](../operation-behaviour/build.md), [Load](../operation-behaviour/load.md), [Test](../operation-behaviour/test.md) and [Health](../operation-behaviour/health.md) pages own operation selection, effects and failure policy. Reports deploy through Build; they have no Load or Test operation. Refresh and validate their semantic model instead.

A native deployed model is not a compiled-TMDL download/export interface. Power BI Desktop does not execute Weaver annotations. Reapplying those transformations requires Weaver.
