# CLI-behaviour contract

The Weaver CLI parses one command, applies one interaction policy and reports one command outcome. Command-specific arguments and current result fields belong to the [CLI reference](../reference/cli.md); this contract defines the shared behavioural boundary.

## Parsing and help

The command parser owns command names, positional arguments, options, mutually exclusive choices and required values. Parsing completes before a command handler runs. An unknown command or option, a missing required value or an invalid parser-level combination is rejected without starting the requested operation.

A bare `weaver` invocation prints top-level help and performs no operation. `--help` and command help print the parser's current usage and options and complete successfully. Parser usage errors are written as parser diagnostics and complete with a non-success status. Exact option sets and generated synopsis text are documented on each command's Reference page.

Workflow and Session entries use the same command parser as standalone invocations. A workflow parses every entry before its first operation. The interactive Session keeps running after help, a usage error or a command failure.

## Interactive and non-interactive input

An invocation can prompt only when input is an interactive terminal and `--non-interactive` is absent. Piped input is not treated as an operator available for an unexpected confirmation.

`--non-interactive` is an input policy. It prevents stdin questions, single-key retry waits and browser sign-in. Required input or authorisation that is missing under that policy is an error. It does not select credentials and does not grant permission to mutate anything.

Some interactive source commands offer an edit-and-retry choice after a supported source error. Non-interactive and JSON invocations make one attempt. Commands that do not define a retry loop do not acquire one merely because a terminal is present.

`weaver session` is itself interactive and does not take `--non-interactive`. When its input is a non-terminal stream, it reads ordinary command lines until end-of-file; it does not turn nested commands into implicitly authorised operations.

## Destructive authorisation

`--yes` grants the command-specific authorisation that would otherwise be requested. It does not make the invocation non-interactive, choose a workspace, authenticate, suppress a plan or repair invalid input.

A destructive command settles and displays the scope it will change before asking for confirmation. Declining an available prompt changes nothing. When a prompt is unavailable, authorisation is refused unless the command received `--yes`. An unattended destructive invocation therefore needs both `--non-interactive` and `--yes`.

A confirmed Workflow authorises its displayed sequence once. Nested commands receive that authorisation and do not ask again. `--non-interactive` propagates into every Workflow entry and can only make the entry's input policy stricter.

Only commands that expose an authorisation boundary accept `--yes`. Its absence on another command is not a dry-run guarantee; use that command's documented execution mode.

## Human output and machine output

In human mode, normal command results and requested reports are written to stdout. Errors and progress belong to stderr. Terminal colour and symbols may improve presentation but are not the only carrier of status.

For a command that supports `--json`, stdout contains one JSON result or failure document after parsing succeeds. Prompts are not allowed to contaminate that document; a required authorisation becomes a JSON failure unless it was supplied. Progress remains on stderr or is suppressed. Parser help and parser errors occur before this JSON boundary and retain parser output semantics.

JSON is a rendering mode, not approval, non-interactive credentials or a compatibility promise. The exact current fields, nesting and format versions belong to the command and Python result Reference pages. A command that always returns a machine document, or exposes no `--json`, is identified on its own Reference page.

## Status and exit semantics

A successful completed command returns a success process status. A rejected request, failed operation, unsuccessful report or missing required authorisation returns a non-success status. Argument parsing errors are parser failures rather than operation reports.

Report-bearing commands decide success from the report's semantics. For example, an unsuccessful Load or Test report is non-success even when the report itself was rendered completely. Health is successful only for a Green report. A command that submits asynchronous work can succeed when the documented submission boundary succeeds; that status does not assert a later remote outcome.

Interactive cancellation before execution is not universally a failure. A Workflow declined at its available confirmation, and setup cancelled before it changes state, complete without claiming that work ran. Destructive commands define their own cancellation status in Reference; callers should distinguish “nothing ran” from “the requested operation succeeded”.

A Workflow stops at the first entry whose handler returns non-success or raises a Weaver error. Earlier effects remain and later entries do not run. An interactive Session instead returns to its prompt after a failed command; the process eventually exits successfully through `exit`, `quit` or end-of-file rather than using an earlier command failure as its final status.

## Interruption

At an interactive Session prompt, `Ctrl-C` abandons the current input and presents a clean prompt. During a Session command, interruption stops that command, reports `interrupted` and keeps the Session open. A pasted multiline entry stops after its first interrupted or failed command.

The source retry prompt treats `Ctrl-C`, end-of-file and Escape as declining the retry while preserving the original failure.

Standalone commands do not define a separate cross-platform signal-to-status contract here. An interrupt can stop the process and leave the operation at its documented partial-state boundary. Automation must use the operation's idempotence and recovery contract rather than assuming interruption rolls work back or emits a final JSON document.

## Defined behaviour

The CLI-behaviour contract specifies that Weaver:

1. completes parser validation before invoking a command handler;
2. prints help without running an operation and rejects usage errors as parser failures;
3. prompts only on an interactive input stream when interaction is permitted;
4. treats `--non-interactive` as input suppression and `--yes` as separate authorisation;
5. keeps human results on stdout and errors or progress on stderr;
6. emits one stdout JSON document after successful parsing when a command's JSON mode applies;
7. derives success or failure from the command or report semantics rather than from rendering completion;
8. stops a Workflow at its first unsuccessful entry while keeping an interactive Session alive after command failures; and
9. handles prompt and Session interruption as described without promising rollback or a universal standalone signal status.

See the [CLI reference](../reference/cli.md), [Workflow](workflow.md), [Runtime](runtime.md), and [State and health](state-and-health.md).
