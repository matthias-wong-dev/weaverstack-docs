# Control a Fabric capacity

Use `weaver fabric capacity` to inspect, resume or suspend the Azure resource that supplies Fabric capacity. These commands wrap the Azure CLI; they do not open a Weaver Session, inspect a workspace or read a catalogue.

Capacity changes affect every workload assigned to that resource, not only the Weaver command or workspace you intend to run.

## Prerequisites

- The Azure CLI with its `fabric capacity` commands installed.
- An Azure CLI sign-in authorised to read and change the capacity.
- The Azure resource group and capacity name.
- An explicit subscription ID when the Azure CLI context does not identify the intended subscription unambiguously.

Pass `--subscription-id` on the command or set `FABRIC_SUBSCRIPTION_ID`. An explicit option takes precedence over the environment variable; otherwise Weaver uses the Azure CLI subscription context.

## Inspect state before changing it

```bash
weaver fabric capacity status \
  --resource-group parcel-platform \
  --capacity-name parcel-development \
  --subscription-id 00000000-0000-0000-0000-000000000000
```

The result names the capacity and reports the state returned by Azure, plus the SKU when available. A successful command proves only that Azure accepted and answered this request. It does not test Fabric workspace access or Weaver project configuration.

## Resume and confirm the transition

Request a resume:

```bash
weaver fabric capacity resume \
  --resource-group parcel-platform \
  --capacity-name parcel-development \
  --subscription-id 00000000-0000-0000-0000-000000000000
```

The command returns after Azure accepts the operation. It does not poll until the capacity becomes active. A zero exit status may therefore be followed by a starting state.

Poll deliberately with `status` until Azure reports `Active` before starting work that needs the capacity:

```bash
weaver fabric capacity status \
  --resource-group parcel-platform \
  --capacity-name parcel-development \
  --subscription-id 00000000-0000-0000-0000-000000000000
```

Then run the intended Weaver or notebook operation. Capacity state and workspace readiness are separate boundaries: an active capacity does not prove that the caller can access a workspace, that an Environment is published or that a Fabric item exists.

## Suspend only after work has settled

Check the Fabric jobs and Weaver operations sharing the capacity outside this command. When they have finished, request suspension:

```bash
weaver fabric capacity suspend \
  --resource-group parcel-platform \
  --capacity-name parcel-development \
  --subscription-id 00000000-0000-0000-0000-000000000000
```

Suspend also returns when Azure accepts the request rather than when the final state is reached. Run `status` again when your operating procedure requires confirmation.

The command has no confirmation prompt, `--yes` option or dry-run mode. `resume` and `suspend` act immediately when Azure accepts them. Do not place unconditional suspension after a `--no-wait` notebook submission: that submission returns before the notebook reaches a terminal result.

## Run from unattended automation

Authenticate the Azure CLI before the job, then prevent Weaver's browser-sign-in fallback:

```bash
weaver fabric capacity resume \
  --resource-group parcel-platform \
  --capacity-name parcel-development \
  --subscription-id 00000000-0000-0000-0000-000000000000 \
  --non-interactive
```

`--non-interactive` does not authenticate or authorise the Azure CLI request. A missing CLI, expired sign-in, wrong subscription, insufficient Azure permission or missing resource makes the command fail.

A bounded automation sequence should:

1. resume the capacity;
2. poll `status` until it is active, with an external timeout;
3. run the workload and wait for its real terminal outcome;
4. check whether other workloads still require the capacity; and
5. suspend it, then confirm the state if required.

Weaver does not provide the polling loop or decide whether other workloads have finished. Keep those estate-wide decisions in the scheduler or operating procedure that knows the shared capacity.

See [`weaver fabric capacity`](../reference/cli/fabric-capacity.md) for exact syntax, subscription selection and exit behaviour. Use [Push and run a Fabric notebook](fabric-notebooks.md) for the adjacent notebook lifecycle.
