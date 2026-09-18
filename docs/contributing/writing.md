# Write or revise a page

Start with the reader's task or decision, then choose the page type. Do not copy source structure into the public navigation.

## Choose one job for the page

| Section | Reader need | Page responsibility |
| --- | --- | --- |
| Get started | Complete the first successful lifecycle | One ordered path with only the context required for the next step. |
| Guides | Complete a specific task | Prerequisites, actions, observable result and recovery links. |
| Core concepts | Reason about Weaver | The public mental model and the consequences of that model. |
| Reference | Look up an interface | Current syntax, fields, accepted values and concise effects. |
| Contracts | Determine specified behaviour | Selection, ordering, state changes, outcomes and failure boundaries. |
| Advanced | Apply a specialised operating pattern | A bounded route with explicit prerequisites and destructive boundaries. |

If a page needs several of these jobs, keep the task in the Guide and link to the authoritative Concept, Reference or Contract page for detail.

## Establish the claim

For each behavioural claim:

1. locate the source path that implements it;
2. find the tests or acceptance journey that exercise it;
3. determine whether the behaviour is general, host-specific or merely current output;
4. link to an existing authoritative documentation page instead of restating its contract.

Source and tests outrank design prose. A real project can establish that an example is realistic, but it does not define a public contract.

Do not document a cleaner product than the one implemented. If a desired workflow conflicts with current behaviour, state the current behaviour and leave the product decision outside the public page.

## Write the page

Write directly for an engineer using Weaver.

- Use public terms: project, Weaver document, logical item, physical Fabric item, catalogue, Build, Load and Test.
- State the mechanism or constraint instead of assurance words such as “safe”, “robust” or “predictable”.
- Keep implementation classes, planner structures and module ownership out of user-facing explanations unless the identifier is itself part of the interface.
- Distinguish a current format from a compatibility guarantee.
- Use relative Markdown links for pages on this site.
- Give code blocks a language and show commands that can be run as written.

Examples use a neutral parcel or logistics domain. Keep each example focused on the page's task rather than extending a single site-wide sample project.

## Connect the journey

A new page is not finished when it is only present in navigation. Add contextual links from the page readers are likely to arrive from, and point the page onward to the next task or the authoritative detail.

Check both directions:

- the section index helps the intended reader choose this page;
- the page links to the relevant Concept, Reference and Contract owners without duplicating them;
- troubleshooting or recovery guidance is reachable where an operation can leave partial state;
- renamed concepts and retired paths no longer appear elsewhere in `docs/`.

Then run the checks in [Validate a change](validation.md).