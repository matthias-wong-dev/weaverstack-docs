# Testing Warehouse data

The [first Table and View](first-project.md) ended with two passing validations. This page explains what they check and what a failure looks like. Use the same `parcel` project; if you are starting here, run the [Table and View task](first-project.md) first.

## Check the result without repeating the ranking query

Open the generated `Warehouse/Operations/tests/Parcel.CurrentStatusMatches.sql`:

<!-- initialise:Warehouse/Operations/tests/Parcel.CurrentStatusMatches.sql -->
```sql
/*
Test ID: Parcel.CurrentStatusMatches

Description: Latest parcel status matches the independently expected rows.

Primary key: Parcel ID
*/
select v.[Parcel ID]
     , v.[Status]
     , v.[Depot]
from (values
    ('P-1001', 'In transit', 'Central'),
    ('P-1002', 'Delivered', 'South')
) as v ([Parcel ID], [Status], [Depot]);

select [Parcel ID]
     , [Status]
     , [Depot]
from [Parcel].[CurrentStatus];
```
<!-- /initialise -->

A Test has two result sets: expected first, then actual. The expected rows state what the sample events mean instead of repeating the View's window function, so a defect in that function shows up as a discrepancy.

## Find events outside the accepted vocabulary

Open the generated `Warehouse/Operations/assumptions/Parcel.StatusIsKnown.sql`:

<!-- initialise:Warehouse/Operations/assumptions/Parcel.StatusIsKnown.sql -->
```sql
/*
Assumption ID: Parcel.StatusIsKnown

Description: Every recorded parcel event has a recognised status.
*/
select [Parcel ID]
     , [Event sequence]
     , [Status]
from [Parcel].[StatusEvent]
where [Status] is null
   or [Status] not in ('Accepted', 'In transit', 'Delivered');
```
<!-- /initialise -->

Every returned row violates the description. No returned rows means the Assumption passes. This check reads all events, including those hidden by the latest-status View, and its relation reference establishes the dependency on `Parcel.StatusEvent`.

## Run both validations

Initialise wrote both files and the first Build installed them, so there is nothing to build. Run them against the loaded data:

```bash
weaver test Warehouse/Operations
```

<!-- cli-capture: {"id": "14-warehouse-test", "title": "Test · both generated validations"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Test · both generated validations">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Test

  Read catalogue                                                                                           3.0s
Workspace  Parcel Development
Catalogue  Warehouse/Catalogue
Targets
  Warehouse/Operations

  Build run graph                                                                                          0.0s
→   Test Warehouse/Operations/Parcel.CurrentStatusMatches
→   Test Warehouse/Operations/Parcel.StatusIsKnown
<span class="terminal-status-green">✓   Test Warehouse/Operations/Parcel.StatusIsKnown                                                         1.7s</span>
<span class="terminal-status-green">✓   Test Warehouse/Operations/Parcel.CurrentStatusMatches                                                  7.7s</span>
  Execute                                                                                                  7.9s
  Record what the run did                                                                                  0.9s
<span class="terminal-status-green">✓ Test                                                                                                    11.8s</span>

<span class="terminal-status-green">test passed</span>

Test summary
<span class="terminal-status-green">    2 passed</span>
    0 failed
  Workflow: 487b69ed9b984916b74bdc7e3243fcd7
</code></pre>
</figure>
<!-- /cli-capture -->

Test runs installed validations; it does not load their inputs. A failed validation ran and found a discrepancy or violation. An `invalid` result means the validation could not run, which is neither a finding nor a pass. [Test behaviour](../reference/operation-behaviour/test.md) owns the exact outcome and recording rules.

When you add or edit a validation, `weaver check` and `weaver build --item Warehouse/Operations` install it first. Data that has not changed needs no Load.

<details markdown="1">
<summary>Optional: inspect a failed Test, restore it and try source-file testing</summary>

## Optional: make one discrepancy visible

Replace `Warehouse/Operations/tests/Parcel.CurrentStatusMatches.sql` with this complete version. It deliberately expects the wrong status for `P-1002`:

```sql
/*
Test ID: Parcel.CurrentStatusMatches

Description: Latest parcel status matches the independently expected rows.

Primary key: Parcel ID
*/
select v.[Parcel ID]
     , v.[Status]
     , v.[Depot]
from (values
    ('P-1001', 'In transit', 'Central'),
    ('P-1002', 'In transit', 'South')
) as v ([Parcel ID], [Status], [Depot]);

select [Parcel ID]
     , [Status]
     , [Depot]
from [Parcel].[CurrentStatus];
```

Install the edited Test and select it for diagnostics:

```bash
weaver check
weaver build --item Warehouse/Operations
weaver test Warehouse/Operations --name 'Parcel[.]CurrentStatusMatches'
```

<!-- cli-capture: {"id": "19-failed-warehouse-test", "title": "Test · deliberate discrepancy"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Test · deliberate discrepancy">
<figcaption>Terminal output <span class="terminal-exit">exit 1</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Test

  Read catalogue                                                                                           2.8s
Workspace  Parcel Development
Catalogue  Warehouse/Catalogue
Targets
  Warehouse/Operations

  Build run graph                                                                                          0.0s
→   Test Warehouse/Operations/Parcel.CurrentStatusMatches
<span class="terminal-status-red">✗   Test Warehouse/Operations/Parcel.CurrentStatusMatches  (1 missing, 1 unexpected)                       6.1s</span>
  Execute                                                                                                  6.2s
  Record what the run did                                                                                  0.5s
<span class="terminal-status-red">✗ Test                                                                                                     9.5s</span>

<span class="terminal-status-red">test failed</span>

<span class="terminal-status-red">  failed     Test        Warehouse/Operations/Parcel.CurrentStatusMatches  (1 missing, 1 unexpected)</span>

Test summary
    0 passed
<span class="terminal-status-red">    1 failed</span>
  Workflow: c70289748d8d4bbab7172dcdd44a003e

  Warehouse/Operations/Parcel.CurrentStatusMatches:
    {&#x27;_weaver_side&#x27;: &#x27;expected&#x27;, &#x27;_weaver_sk&#x27;: 1, &#x27;Parcel ID&#x27;: &#x27;P-1002&#x27;, &#x27;Status&#x27;: &#x27;In transit&#x27;, &#x27;Depot&#x27;: &#x27;South&#x27;}
    {&#x27;_weaver_side&#x27;: &#x27;actual&#x27;, &#x27;_weaver_sk&#x27;: 1, &#x27;Parcel ID&#x27;: &#x27;P-1002&#x27;, &#x27;Status&#x27;: &#x27;Delivered&#x27;, &#x27;Depot&#x27;: &#x27;South&#x27;}
</code></pre>
</figure>
<!-- /cli-capture -->

```bash
weaver health --item Warehouse/Operations
```

<!-- cli-capture: {"id": "20-health-failed-test", "title": "Health · recorded failed validation"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Health · recorded failed validation">
<figcaption>Terminal output <span class="terminal-exit">exit 1</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Health

  Read catalogue                                                                                           2.6s
  Check installed items                                                                                    0.1s
  Read installed objects                                                                                   0.7s
<span class="terminal-status-green">✓ Health                                                                                                   3.4s</span>

<span class="terminal-status-red">Weaver Health  Red</span>

<span class="terminal-status-green">Load    Green</span>
  Last load activity   0h 1m ago
<span class="terminal-status-green">  1 succeeded</span>

<span class="terminal-status-red">Tests   Red</span>
<span class="terminal-status-red">  1 failed · 1 succeeded</span>
<span class="terminal-status-red">  Red    Warehouse/Operations/Parcel.CurrentStatusMatches</span>
<span class="terminal-status-red">          the last run failed</span>

<span class="terminal-status-green">Build   Green</span>
  Installed estate consistent (10 objects)

Slowest loads
  Warehouse/Operations/Parcel.StatusEvent     4.9s

Largest changes
  Warehouse/Operations/Parcel.StatusEvent     read 3  +3 ~0 -0 !0
</code></pre>
</figure>
<!-- /cli-capture -->

The finding is one missing row (`P-1002`, `In transit`, `South`) and one unexpected row (`P-1002`, `Delivered`, `South`). Test exits non-zero; Health records Tests as Red. The selector is a case-insensitive whole-name regular expression, so `[.]` matches the literal dot.

Change `P-1002` back to `Delivered`, then install and rerun the Test:

```bash
weaver check
weaver build --item Warehouse/Operations
weaver test Warehouse/Operations
weaver health --item Warehouse/Operations
```

<!-- cli-capture: {"id": "23-health-restored", "title": "Health · restored validation"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Health · restored validation">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Health

  Read catalogue                                                                                           2.6s
  Check installed items                                                                                    0.1s
  Read installed objects                                                                                   0.7s
<span class="terminal-status-green">✓ Health                                                                                                   3.4s</span>

<span class="terminal-status-green">Weaver Health  Green</span>

<span class="terminal-status-green">Load    Green</span>
  Last load activity   0h 1m ago
<span class="terminal-status-green">  1 succeeded</span>

<span class="terminal-status-green">Tests   Green</span>
<span class="terminal-status-green">  2 succeeded</span>

<span class="terminal-status-green">Build   Green</span>
  Installed estate consistent (10 objects)

Slowest loads
  Warehouse/Operations/Parcel.StatusEvent     4.9s

Largest changes
  Warehouse/Operations/Parcel.StatusEvent     read 3  +3 ~0 -0 !0
</code></pre>
</figure>
<!-- /cli-capture -->

Both validations passed and the item returned to Green.

To try edited SQL against deployed data before installing it, use file mode:

```bash
weaver test Warehouse/Operations --source . --file 'Warehouse/Operations/tests/Parcel.CurrentStatusMatches.sql'
```

<!-- cli-capture: {"id": "24-source-file-test", "title": "Test · source file against deployed data"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Test · source file against deployed data">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Test

  Read validations                                                                                         0.1s
  Execute                                                                                                  6.0s
<span class="terminal-status-green">✓ Test                                                                                                     6.1s</span>

<span class="terminal-status-green">test passed</span>

Test summary
<span class="terminal-status-green">    1 passed</span>
    0 failed
</code></pre>
</figure>
<!-- /cli-capture -->

`--file` selects file mode even with a catalogue configured. File mode records no Test status or history, which is why its output has no workflow identifier. `--source` alone does not select file mode. [Test CLI](../reference/cli/test.md) covers repeatable file and name selectors. [Test](../reference/weaver-documents/test.md) and [Assumption](../reference/weaver-documents/assumption.md) define the complete SQL forms.

A row only in expected is missing; a row only in actual is unexpected. A changed row produces one of each. The optional `Primary key` correlates the diagnostic rows without changing that comparison. The actual query establishes the dependency on `Parcel.CurrentStatus`.

</details>

These checks now describe the result you expect, but the event feed is still a constant in a SQL file. [Loading changes](incremental.md) uses a changing-source example: the same parcels arrive through an external Warehouse, and a keyed Table consumes updates and cancellations without rebuilding its definition.
