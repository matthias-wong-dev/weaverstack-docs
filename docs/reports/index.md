# Reports

Keep the native Report beside its model. Weaver resolves their link to the deployed model, so moving the project between workspaces does not mean editing its authored definition.

Native Report deployment works in [both Power BI operating modes](../semantic-models/index.md#two-ways-to-use-weaver-with-power-bi). Without a Catalogue, include the linked local Semantic Model in the same Build. With a Catalogue, the supported Report-only Build can use a compatible, already-certified installed model. [Report binding](../reference/power-bi/requirements-and-compatibility.md#report-binding) gives the exact rules.

[Deploy a native Report](deploy.md), then use [development and production configurations](environments.md) to choose the linked model in each workspace.

Reports are deployed through Build. Their data refresh and validation belong to the semantic model, not a separate Report Load or Test. [Coordinate your estate](../estate/index.md) brings those model results together with the rest of the project.
