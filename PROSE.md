# Documentation prose

This guide governs public documentation in this repository. It complements the product-source prose guide; it does not redefine product behaviour.

## Default

Write for an engineer trying to complete a task, understand Weaver or look up an exact interface. Preserve only the context needed for that job. Put implementation design in the Weaver source repository and maintenance planning in root-level repository files.

## Principles

1. **State the current model.** Describe implemented behaviour directly. Do not document the cleaner product you wish existed.
2. **Use plain, public vocabulary.** Name Weaver documents, logical and physical items, the catalogue, operations and Fabric surfaces as users encounter them. Do not derive public categories from modules or classes.
3. **Give each page one job.** Getting started teaches one first path; Core concepts establishes the mental model; Basics teaches normal work; Advanced explains deeper mechanisms; Reference owns exact interfaces and behaviour.
4. **Lead with actions and outcomes.** In task pages, state the prerequisite, action and observable result before mechanism detail.
5. **Put precision with its owner.** Link to Reference for syntax, defaults, selection, state transitions, outcomes and failure boundaries instead of repeating partial contracts.
6. **Separate fact types.** Say when behaviour is host-specific, an example is illustrative, a format is merely current output or a guarantee is intentionally absent.
7. **Prefer defaults and inference.** Examples should omit fields that merely restate defaults and should let Weaver infer dependencies where supported. Keep declarations required by current source.
8. **Keep examples small and neutral.** Use parcel and logistics names. Never publish production project, tenant, workspace or item identifiers.
9. **Keep the real constraint.** Succinctness must not remove destructive scope, ordering, rollback limits, partial-state consequences or the action needed to recover.
10. **Do not expose the maintenance process.** Public pages do not mention planned coverage, later phases, missing future pages or agent instructions.

## Language

Write as one senior engineer to another. Use direct sentences and concrete nouns. Avoid assurance and sales language such as “powerful”, “seamless”, “robust”, “safe”, “predictable” and “enterprise-grade”; state the mechanism that would justify the adjective.

Do not use “current versions of Weaver” unless a real version distinction matters. Do not say readers “can rely on” a behaviour; define the behaviour or recorded state. Avoid history and arguments against hypothetical alternatives unless compatibility or migration depends on them.

Use `Weaver document` for authored Tables, Folders, Views, Tests, Assumptions, Shortcuts, Warehouse programmables and schema metadata. Do not introduce `resource` or `artefact` as a user-facing umbrella term.

## Page types

### Getting started

Use one ordered route with complete commands or files and an expected result at each step. Keep theory, alternatives and exhaustive options out of the path.

### Core concepts

Explain what users author, bind, run and inspect, and how those parts affect their decisions. Do not mirror the source architecture.

### Basics

Teach normal workflows with defaults and inference first. Include prerequisites, actions, observable results and links to recovery where work can leave partial state.

### Advanced

Explain a deeper mechanism or non-basic operating pattern. State prerequisites and consequential boundaries; do not repeat the complete basic workflow.

### Reference

Be terse, complete and searchable. Specify accepted syntax, defaults, precedence, selection, ordering, state changes, outcomes and failures where relevant. Record current machine representations without promising compatibility that Weaver does not provide.

## Examples and code

Code must be complete enough to run in the stated context. Give fenced blocks a language. Keep metadata inside complete SQL or Python source when that is how users author it.

Descriptive metadata remains descriptive; do not imply that a metadata reference creates an execution dependency. Use explicit `Dependencies` as an override where inference is supported, but preserve explicit declarations where current product rules require them.

## Review

For each changed passage, ask:

1. Which reader task, decision or lookup does this serve?
2. What source and test evidence supports each behavioural claim?
3. Is this the authoritative owner, or should it link elsewhere?
4. Did the edit blur specified behaviour, host behaviour, current output or an example?
5. Can anything be removed without losing a prerequisite, consequence or recovery action?
