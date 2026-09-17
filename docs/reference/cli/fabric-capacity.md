# `weaver fabric capacity`

<!-- BEGIN GENERATED CLI -->
```text
usage: weaver fabric capacity [-h] --resource-group RESOURCE_GROUP
                              --capacity-name CAPACITY_NAME
                              [--subscription-id SUBSCRIPTION_ID]
                              [--non-interactive]
                              {status,resume,suspend}

positional arguments:
  {status,resume,suspend}

options:
  -h, --help            show this help message and exit
  --resource-group RESOURCE_GROUP
  --capacity-name CAPACITY_NAME
  --subscription-id SUBSCRIPTION_ID
                        Azure subscription ID when more than one subscription
                        is available.
  --non-interactive     Do not read stdin, wait for a keypress or open browser
                        sign-in. Missing authorisation or required input is an
                        error.
```
<!-- END GENERATED CLI -->

## Responsibility and selection

`fabric capacity` delegates capacity management to the Azure CLI. The positional action is one of:

- `status` reads the capacity;
- `resume` requests that a suspended capacity resume;
- `suspend` requests that the capacity suspend.

`--resource-group` and `--capacity-name` identify the Azure resource. `--subscription-id` selects a subscription explicitly. If it is omitted, Weaver checks `FABRIC_SUBSCRIPTION_ID` before using the Azure CLI's subscription context.

## Execution

The Azure CLI and its `fabric` capacity commands must be installed and authenticated. Weaver invokes the corresponding Azure operation and reads the returned state and SKU when present.

`resume` and `suspend` do not poll until the requested state is reached. A successful `resume` response that is not yet active is reported as starting.

## Interaction

The command has no confirmation, `--yes` or dry-run option. `resume` and `suspend` act as soon as the Azure CLI accepts the request. `--non-interactive` disables Weaver's browser-sign-in fallback; it does not authenticate or authorise the Azure CLI invocation.

## Output and exit behaviour

Output names the capacity and reports the returned state, followed by the SKU when Azure supplies one. After `resume`, Weaver prints a follow-up status instruction when the returned state is not yet active.

The command exits `0` when the Azure CLI operation succeeds, including when a state transition is still in progress. A missing Azure CLI, unsupported action, authentication or authorisation failure, missing resource, or other non-zero Azure CLI result produces a non-zero status. No stable machine-readable output schema is promised.

## Examples

Read capacity state:

```bash
weaver fabric capacity status \
  --resource-group parcel-platform \
  --capacity-name parcel-development
```

Request a resume in a selected subscription:

```bash
weaver fabric capacity resume \
  --resource-group parcel-platform \
  --capacity-name parcel-development \
  --subscription-id 00000000-0000-0000-0000-000000000000 \
  --non-interactive
```
