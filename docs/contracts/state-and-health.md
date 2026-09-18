# State and health contract

Health reports the installed estate as it exists when the operation starts. It combines installed catalogue state, current Load and Test state, dependency freshness and, unless disabled, physical inventory. It does not read project source, execute authored work or change the estate.

The report has Load, Tests and Build sections. Each section assesses only its own subjects; the overall status is the worst section status.

## Evidence and scope

Installed evidence comes from the selected catalogue:

- item-to-target bindings and certified objects;
- installed Table, Folder, View, Test, Assumption, dependency and Shortcut declarations;
- current Load and Test status;
- borrowed-object records for a mirrored estate.

Current runtime evidence is keyed by logical object identity. A current status identifies the workflow that produced it and its available start, completion and finding counts. It is not a complete run history. Health reads Load statistics only for the workflow and logical object behind each current Load status; older statistics remain history but are outside that activity window.

With inventory enabled, Health also checks each selected physical target against certified physical objects. Warehouse inventory is read through its SQL endpoint. Lakehouse inventory is read from OneLake without starting Spark; consequently, a Lakehouse View is not declared missing merely because storage inventory cannot list it. `--no-inventory`, or `inventories=False` in Python, omits this evidence. A Green Build section from that mode establishes catalogue consistency only, not physical presence.

Naming no item assesses every target bound by the catalogue. Naming items assesses the targets to which those logical items are installed. An item without an installation is an error. Selection bounds the reported subjects and inventory reads, but freshness still follows managed ancestors outside the selection.

For a borrowed object, current Load state and matching Load statistics come from the source catalogue. Local objects use destination state. The destination catalogue continues to supply installed topology, Tests and Build evidence.

## Green, Amber and Red

Severity order is Green, Amber, then Red. A section with no findings is Green. A section's status is its worst finding; the report status is the worst section.

### Load

Each installed Table or Folder that holds rows is a Load subject, including borrowed objects. Views are not Load subjects, but their Build-established times participate in freshness for descendants.

Load is:

- **Green** when the current generation has settled successfully, is fresh enough and is not behind a managed ancestor;
- **Amber** when no load has settled since Build, the last load completed with rejects, the last clean state is older than the freshness cutoff, a managed ancestor has no settled state for its current generation, or an ancestor was established later;
- **Red** when the current outcome is failed, errored or blocked.

A static object is exempt from age and ancestor-freshness checks after its load-once state is established. Its latest lifecycle touch can still establish freshness for a downstream object.

### Tests

Each installed Test and Assumption is a Tests subject.

Tests is:

- **Green** when the latest installed validation passed and no managed data dependency was established later;
- **Amber** when it has not run since Build, has another non-success state that is not a failure, or passed before a dependency was established again;
- **Red** when the latest validation failed, errored or was blocked.

Elapsed time alone does not make a validation stale. A Test finding can carry discrepancy counts; an Assumption finding can carry its violation count.

### Build

Build health reports contradictions in installed state. These are Red findings:

- a declared Table or Folder is not certified in the Registry;
- a validation declaration lacks its installed validation work;
- an installed dependency cannot be resolved;
- more than one logical installation claims one physical address; or
- inventory proves that a certified physical object is missing in its expected local or borrowed form.

Build health does not compare the catalogue with unbuilt project source.

## Freshness and report time

`as_of` is the oldest acceptable settled Load completion time. It must name an ISO-8601 instant with a time zone and is normalised to UTC. When omitted, it is 24 hours before the operation began.

The report distinguishes:

- the generation time, when Health began;
- the `as_of` cutoff used for age-based Load freshness;
- each finding's available runtime start and completion times.

Age is only one freshness rule. A recently loaded object can still be Amber when an ancestor has no settled current state or was established after it. A validation can be Amber when its dependency moved after it passed, regardless of the age cutoff.

## Findings and activity boundaries

A finding names its section, severity, stable condition code and, where available, logical object, physical target, runtime outcome, workflow, times and failure count. Findings describe non-Green conditions; subject and outcome counts cover the whole assessed section.

The current-Load summary can span several workflow identifiers. A partial run updates only the objects it reached, so untouched objects remain correlated with earlier workflows. Recorded activity contains only matching executed Load statistics. Blocked work can therefore contribute current status and a finding without an activity row.

Health does not claim to reproduce every log entry, terminal message or historical Load. Use [`_.Log` and `_.LoadStatistic`](history.md) for those questions.

## Result and exit semantics

The Python operation returns a `HealthReport`. `is_healthy` is true only for Green. The CLI exits `0` only for Green; Amber, Red and operation errors exit non-zero. Item-resolution, catalogue, authentication and inventory-read failures are command errors rather than fabricated Red findings.

Human output reports the overall status and section findings without depending on terminal colour. `--json` emits one current report with an explicit format version. This contract defines the meanings above, not a fixed set of JSON fields, their order or compatibility across format versions.

## Defined behaviour

The State and health contract specifies that Health:

1. reads installed, current runtime and optional inventory evidence without executing authored work;
2. scopes subjects to installed item bindings while retaining outside ancestry for freshness;
3. derives section and overall status by worst severity;
4. distinguishes pending, rejected and stale Amber states from failed, errored, blocked and inconsistent Red states;
5. uses a zoned `as_of` instant for Load age while also evaluating dependency freshness;
6. reads borrowed Load state from its source and local state from its destination;
7. bounds current activity to statistics that match current Load status; and
8. returns a report whose behavioural meaning is stable without freezing its machine representation.
