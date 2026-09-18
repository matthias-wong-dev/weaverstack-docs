# Signatures and change-detection contract

Build compares the selected authored estate with the installed estate recorded in the catalogue and with current physical inventory. Signatures identify whether an installed definition still represents what Weaver would install; inventory establishes whether the certified physical object is actually present in the expected form.

A signature is an equality token, not a public content digest. Its algorithm, encoding and length are not part of this contract.

## What counts as a detectable change

For selected items, Weaver detects changes that alter the installable meaning of a document or generated work. This includes, where applicable:

- authored structure, query, Python or SQL body;
- installed metadata such as descriptions, lineage, keys, load behaviour and declared dependencies;
- a Shortcut's destination and source identity;
- generated Load or validation work derived from a document; and
- a change in Weaver's installation implementation for generated or managed physical work.

The comparison is against the installed certification, not file modification times or source-control history. Rewriting a file without changing its interpreted installable meaning need not select physical work. Conversely, generated work can change after a Weaver implementation change even when authored source is unchanged.

Build also detects certified objects that are absent from the selected target or present in a different physical form. Such an object is not treated as unchanged merely because its recorded signature matches.

## New, unchanged, changed and impacted

Within the selected items:

- **new** means the declared installable object is not present in the expected physical form;
- **unchanged** means its installed signature matches and physical reconciliation confirms the expected form;
- **changed** means the installed signature does not represent the selected declaration or generated work;
- **impacted** means an existing selected descendant must be reconciled because a changed or stale upstream object can affect what it installs.

Changed objects are impact roots. Impact follows the managed dependency graph through existing descendants selected for the same Build. A new object is installed, but newness alone does not classify all existing descendants as impacted. Cross-item impact reaches a consumer only when that consumer's item is selected.

A selected consumer can also be stale when an installed producer behind a logical Shortcut was rebuilt later. Weaver selects the stale Shortcut path and affected selected consumers even if their source signatures still match. Once the consumer has been rebuilt against the newer producer, the same state converges to unchanged.

An unchanged Build selects no physical or catalogue work. A changed Build does not republish unrelated unchanged catalogue tables merely because some other table changed.

## Physical reconciliation and pruning

Signatures do not establish physical existence or ownership. Build compares catalogue certification with target inventory before deciding what to retain, install or remove.

- A matching certified object in the expected form can remain unchanged.
- A certified object missing physically loses the claims that describe it and is handled as new work if still declared and selected.
- An object whose installed physical kind differs from the declared kind is reconciled to the selected declaration.
- A physical object with no Weaver certification does not become Weaver-owned merely because its name matches a declaration.
- Removing a declaration from a selected item removes the obsolete certification and permits pruning within that item's managed target scope.
- Objects and catalogue rows outside the selected items remain outside reconciliation.

`Prohibit rebuild` prevents replacement of an existing owned data object when a change would otherwise rebuild it. It does not suppress installation of a genuinely new object. A retained protected object keeps its applicable runtime state.

## Certification and runtime state

`_.Registry` records the installed signature only for work Build certifies. Physical presence without certification is not enough, and a declaration is not certified merely because it was discovered.

When Build replaces or refreshes installed work, the resulting object is certified again, including an unchanged descendant rebuilt because of impact. A borrowed mirrored object remains borrowed while unchanged; selected changed or impacted borrowed work becomes local when successfully installed.

Rebuilding a loadable object resets its current bookmark and Load state. Rebuilding a Test or Assumption resets its current Test state. Current state for unaffected objects and append-only operational history remain unchanged. Physical reconciliation alone does not erase runtime state before the selected lifecycle determines that the corresponding installed generation is being replaced or removed.

## Boundaries

This contract does not expose:

- signature hash algorithms, byte encodings or salts;
- bundle identity algorithms;
- internal planning node names or action ordering;
- a guarantee that every textual edit changes a signature;
- a guarantee that signatures are portable between different object kinds or execution engines; or
- permission to compare or manufacture catalogue signatures outside Weaver.

A signature should be compared only in the context of the same installed logical object and its Weaver-managed physical form.

## Defined behaviour

The Signatures and change-detection contract specifies that Weaver:

1. compares selected installable meaning with installed certification rather than timestamps or source-control state;
2. detects authored, generated and supported installation-implementation changes;
3. confirms physical presence and form separately from signature equality;
4. leaves a matching selected object unchanged and performs no work at a settled fixed point;
5. selects changed roots and existing selected descendants affected through managed dependencies;
6. does not widen impact into unselected items;
7. removes obsolete or disproved claims only within the selected managed boundary;
8. certifies rebuilt and refreshed work, including impacted descendants;
9. preserves unaffected current state and history while resetting state owned by rebuilt work; and
10. treats signature representation and internal installation sequencing as implementation details.
