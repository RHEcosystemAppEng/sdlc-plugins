# Correctness Sub-Agent

Verify that the PR is functionally correct. This sub-agent performs three checks:
CI status (do all CI checks pass?), acceptance criteria verification (does the code
satisfy every criterion from the task?), and verification commands (do the task's
verification commands produce the expected output?).

This is a pure analysis function. It receives scoped inputs from the orchestrator
via dispatch-template.md and returns structured findings via finding-template.md.

## Inputs

The orchestrator provides these sections in the Agent-Specific Inputs block
(see dispatch-template.md for the full envelope structure):

- **PR Diff** — full diff content for code inspection during acceptance criteria
  verification
- **Task Specification** — Acceptance Criteria, Test Requirements, Verification
  Commands sections from the Jira task description
- **Repository Info** — repository path and Serena instance info for code inspection
- **CI Status** — in **sandbox mode** the head-SHA CI check-run outcomes are
  pre-fetched on the trusted runner and provided here (from `github.check_runs`,
  reduced to name/status/conclusion/details_url); read them directly — there is no
  `gh` CLI or network egress in the sandbox. When a check failed, the failure logs
  are also pre-fetched into a single file whose path is given as **CI Failure
  Logs** (from `github.check_run_logs_path`); Read that file **only** if Check 1
  reaches FAIL, so the large log text stays off context otherwise. An empty path
  means no check failed (or no fetchable log). In **interactive mode** both inputs
  are absent and the sub-agent fetches CI status and logs on demand via `gh` CLI (a
  read operation, not a side effect)

The dispatch envelope also includes **Context** (Jira Task, PR URL, Branch, Base
Branch) and **Classified Review Comments** (all classified comments with IDs,
classifications, and file/line references).

## Checks

### Check 1 — CI Status

Check whether all CI checks on the PR pass.

#### 1a — Fetch CI Status

**Sandbox mode** (CI Status input provided): do **not** run `gh` — read the
pre-fetched check-run outcomes from the CI Status input (each entry has `name`,
`status`, `conclusion`, `details_url`). Map each entry to a status:

- `conclusion` of `success`/`neutral`/`skipped` → pass
- `conclusion` of `failure`/`timed_out`/`cancelled`/`action_required` → failed
- `status` not `completed` (i.e. `queued`/`in_progress`) → pending
- an empty check-runs list → no checks configured (treat as pass; note it in the
  evidence)

**Interactive mode** (no CI Status input): run

```
gh pr checks <pr-number> -R <owner/repo>
```

Report the status (pass/fail/pending) for each check (from either source).

- If all checks pass, record verdict as PASS and skip to Check 2.
- If any checks are pending, record verdict as WARN and skip to Check 2.
- If any checks have failed, proceed to steps 1b–1c below.

#### 1b — Fetch Failure Logs

**Sandbox mode:** do **not** run `gh run view`/`gh run list` — there is no `gh` CLI
or network egress. Instead, if the **CI Failure Logs** input path is non-empty,
`Read` that file: it holds the concatenated `--log-failed` output for every failed
check-run (each section headed by its run ID), pre-fetched on the trusted runner.
Use it as the failure-log source for step 1c. If the path is empty (e.g. the failed
check is a non-Actions check whose log is not reachable that way), fall back to the
PR diff plus the failed check's `name`, `conclusion`, and `details_url` from the
CI Status input. Either way, still emit the `create-sub-task` action (step 1d) and
include the `details_url` so a human can open the full log.

**Interactive mode:** for each failed CI check, fetch the failure logs:

```
gh run view <run-id> --log-failed -R <owner/repo>
```

Extract the `run-id` from the failed check's URL or use:

```
gh run list --branch <pr-branch> --status failure --limit 5 -R <owner/repo>
```

Capture the relevant error output for analysis.

#### 1c — Analyze Failures

For each failed CI check, analyze the failure log to determine:
- **What failed** — the specific test, build step, or lint rule that failed
- **Why it failed** — the root error message or assertion failure
- **What fix is needed** — the concrete code change required to resolve the failure

Use the Serena instance for the task's repository (from Repository Info) or fall
back to Read/Grep/Glob to inspect the relevant source files and understand the
failure context.

#### 1d — Recommend Sub-Tasks

For each CI failure that requires a fix, include a `create-sub-task` action in
the Actions section. The orchestrator is responsible for idempotency checks and
actual sub-task creation — this sub-agent only recommends.

Each recommended action should include:
- **Title** — concise description of the CI fix needed (e.g., "Fix failing lint
  check: unused import in handler.rs")
- **Relevant files** — files implicated in the failure
- **Root cause** — the CI check name, failure log excerpt, and error summary

#### Verdict

- **PASS** — all CI checks pass
- **WARN** — some checks are pending, none failed
- **FAIL** — one or more CI checks failed

Evidence: list each CI check with its status. For failures, include the analysis
from step 1c.

### Check 2 — Acceptance Criteria Verification

For each criterion in the **Acceptance Criteria** section of the Task Specification,
verify it is satisfied by inspecting the code in the PR Diff.

1. **Read changed code**: inspect the PR Diff to identify the code changes relevant
   to each criterion. Cross-reference with Repository Info to understand the
   file structure.

2. **Verify with code intelligence**: if a Serena instance is available (from
   Repository Info), use:
   - `find_symbol` with `include_body=true` to inspect specific functions, structs,
     or components relevant to each criterion
   - `find_referencing_symbols` to confirm new symbols are properly referenced and
     integrated
   - `search_for_pattern` for configuration values, string literals, or patterns
     referenced in the criteria

3. **Fallback**: if no Serena instance is available, use Read, Grep, and Glob
   tools to inspect the PR branch directly.

4. **Determine per-criterion verdict**:
   - **PASS** — the criterion is satisfied by the code changes
   - **FAIL** — the criterion is not satisfied or cannot be verified from the diff

5. **Evidence**: for each criterion, state what was checked and what was found.
   For FAIL verdicts, explain what is missing or incorrect.

6. **Review comment correlation**: check Classified Review Comments for any
   comments referencing acceptance criteria gaps. If a reviewer flagged a missing
   criterion, include the comment ID in the Related review comments field.

#### Verdict

- **PASS** — all acceptance criteria are satisfied
- **WARN** — all criteria are satisfied but some verification was indirect or
  approximate (e.g., could not fully verify a runtime behavior from static analysis)
- **FAIL** — one or more criteria are not satisfied

Evidence: list each criterion with its individual pass/fail status and verification
details.

### Check 3 — Verification Commands

If the Task Specification includes a **Verification Commands** section, run each
command and check the result against the expected outcome.

For each command:

1. Run the command via shell access.
2. Compare the output to the expected outcome described in the task.
3. Record PASS if the output matches, FAIL if it does not.

If no Verification Commands section exists in the Task Specification, proceed to
the eval infrastructure detection below before recording N/A.

#### 3b — Eval Infrastructure Change Detection

Scan the PR diff file list for changes to eval infrastructure — specifically files
matching `plugins/sdlc-workflow/skills/run-evals/scripts/*.py` or
`plugins/sdlc-workflow/skills/run-evals/SKILL.md`.

If eval infrastructure changes are detected:

1. **Discover existing baselines**: list directories matching
   `evals/*/baselines/latest/` in the repository. Each match represents a skill
   with baseline eval data.
2. **Generate verification commands**: for each discovered baseline, generate a
   command that runs the modified render script against that baseline:
   ```
   python3 plugins/sdlc-workflow/skills/run-evals/scripts/render_summary.py \
     --results evals/<skill>/baselines/latest/ \
     --skill <skill> \
     --output /tmp/verify-<skill>-summary.md
   ```
   If `aggregate_benchmark.py` was also modified, additionally generate:
   ```
   python3 plugins/sdlc-workflow/skills/run-evals/scripts/aggregate_benchmark.py \
     --results evals/<skill>/baselines/latest/
   ```
3. **Run the generated commands** and verify they complete successfully (exit
   code 0). The expected outcome is that the scripts run without errors against
   existing baseline data — this confirms backward compatibility of the
   infrastructure changes.
4. **Include results in the verdict**: if any generated command fails, record
   the check as FAIL with the failing command and its output.

If no eval infrastructure changes are detected, skip this sub-step — it does not
affect the verdict when the PR does not touch run-evals files.

#### Verdict

- **PASS** — all verification commands (task-specified and auto-generated) produce the expected output
- **FAIL** — one or more commands produce unexpected output
- **N/A** — no verification commands were specified in the task AND no eval infrastructure changes detected

Evidence: for each command, show the command run, the expected output, and the
actual output. For PASS results, a brief confirmation is sufficient.

## Output Format

Return results using the structure defined in finding-template.md.

The Verdicts table must include exactly three rows:

| Check | Verdict | Summary |
|---|---|---|
| CI Status | <PASS\|WARN\|FAIL> | <one-line summary> |
| Acceptance Criteria | <PASS\|WARN\|FAIL> | <one-line summary> |
| Verification Commands | <PASS\|FAIL\|N/A> | <one-line summary> |

The Findings section must include one subsection per check, using the format:

```
### <check name> -- <verdict>
```

PASS checks get a brief confirmation. Non-PASS checks get full details and evidence.

The Actions section is omitted if there are no actions. When CI failures are
detected (Check 1 verdict is FAIL), include one `create-sub-task` action per
failure recommending the fix:

```markdown
### create-sub-task: <short title describing the CI fix>

**Type:** create-sub-task
**Title:** <concise CI fix description>
**Relevant files:** <files implicated in the failure>
**Root cause:** <CI check name, failure excerpt, and error summary>
```

## Constraints

- **MUST NOT** perform Jira mutations (create issues, transition issues, post
  comments, update fields) — constraint 1.22
- **MUST NOT** post PR comments or replies — constraint 1.23
- **MUST** return responses using the structured finding template from
  finding-template.md — constraint 1.24
- **MUST NOT** modify code or auto-merge
- **MUST** process all three checks and return verdicts for each, even if all
  are PASS (use N/A for Verification Commands when no commands are specified)
