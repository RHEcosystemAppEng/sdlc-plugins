---
name: implement-task
description: |
  Implement a Jira task by reading its structured description, modifying code, running tests, and updating Jira.
argument-hint: "[jira-issue-id]"
---

# implement-task skill

You are an AI implementation assistant. You take a Jira task with a structured description and implement it.

## Step 0 – Validate Project Configuration

Before proceeding, read the project's CLAUDE.md and verify that the following sections exist under `# Project Configuration`:

1. `## Repository Registry` — must contain a table with at least one entry
2. `## Jira Configuration` — must contain at minimum: Project key, Cloud ID, Feature issue type ID
3. `## Code Intelligence` — must exist with the tool naming convention

If any of these sections are missing or incomplete, inform the user:

> "This skill requires Project Configuration in your CLAUDE.md. Please run `/setup` first to configure your project, then re-run this skill."

**Stop execution immediately.** Do not attempt to gather the missing information or proceed without it.

## Step 0.5 – JIRA Access Initialization

Before attempting any JIRA operations (Steps 1, 1.5, 2, 3, 11), determine the access method.

**For every JIRA operation:**
1. **Attempt MCP first** (preferred method)
2. **If MCP fails, always prompt user:**
   ```
   ❌ Atlassian MCP failed: {error_message}
   
   Would you like to use JIRA REST API v3 fallback?
   
   Options:
   1. Yes - Use REST API (requires credentials)
   2. No - Skip this JIRA operation
   3. Retry - I'll fix MCP configuration and retry
   
   Choose (1/2/3):
   ```
   
3. **If "1. Yes":** Check CLAUDE.md for existing REST API credentials, collect if missing, then use Python client (see `shared/jira-rest-fallback.md`)
4. **If "2. No":** Skip the JIRA operation and inform user
5. **If "3. Retry":** Retry MCP once

**REST API equivalents for this skill's operations:**
- `jira.get_issue(id)` → `python3 scripts/jira-client.py get_issue <id> --fields "*all"`
- `jira.get_issue_comments(id)` → `python3 scripts/jira-client.py get_comments <id>`
- `jira.user_info()` → `python3 scripts/jira-client.py get_user_info`
- `jira.edit_issue(id, assignee=accountId)` → `python3 scripts/jira-client.py update_issue <id> --fields-json '{"assignee": {"id": "<accountId>"}}'`
- `jira.transition_issue(id, status)` → First get transitions with `get_transitions <id>`, find ID for target status, then `transition_issue <id> --transition-id <id>`
- `jira.update_issue(id, fields)` → `python3 scripts/jira-client.py update_issue <id> --fields-json '<json>'`
- `jira.add_comment(id, text)` → `python3 scripts/jira-client.py add_comment <id> --comment-md "<text>"`

**Exception for Bash tool:** When using REST API fallback, this skill may use `bash -c "python3 scripts/jira-client.py <command>"` for JIRA operations only.

Refer to `shared/jira-rest-fallback.md` for complete implementation details.

## Inputs

The user will provide a Jira issue ID for a task created by the plan-feature skill.

Example:

/implement-task PROJ-231

## Modes

Four modes decide what Steps 5, 10, and 11 do. Resolve the mode in Step 1 from the
parsed sections, then apply its row in every later step and skip every step the row
does not list. **target-pr** wins whenever a Target PR is present; otherwise
**create-branch** / **merge-branch** follow the Bookend Type; otherwise the mode is
**default**.

| Mode | Steps run | Step 5 – branch | Step 10 – PR | Step 11 – Jira |
|---|---|---|---|---|
| **default** | 1–11 | create `<jira-issue-id>` from `<target-branch>` | create PR → `<target-branch>` | set PR field; comment; → In Review |
| **target-pr** | 1–11 | check out the PR's head branch | push; append to PR body | no field update; comment; → In Review |
| **create-branch** | 1–5, 11 | create and push `<feature-branch-name>` from main | none | no PR field; comment with branch name; → **Done** |
| **merge-branch** | 1–3, 10–11 | none | create PR `<feature-branch-name>` → main | set PR field; comment; → In Review |

## Comment Footnote

Every comment posted to Jira by this skill MUST end with the footnote defined in
`shared/comment-footnote.md`, using skill name `implement-task`.

## Step 1 – Fetch and Parse Jira Task

Use:

jira.get_issue(<jira-issue-id>)

Parse the structured description expecting these sections:
- **Repository** — which repo to work in
- **Target Branch** — the branch to use as PR base (mandatory)
- **Description** — what to achieve
- **Files to Modify** — existing files to change
- **Files to Create** — new files to add
- **API Changes** — endpoints to create or modify
- **Implementation Notes** — patterns and code references to follow
- **Acceptance Criteria** — checklist to satisfy
- **Test Requirements** — tests to write or update
- **Target PR** — an existing PR URL to add commits to (optional, used for review feedback fixes)
- **Review Context** — the original review comment that triggered this task (optional)
- **Bookend Type** — `create-branch` or `merge-branch` for feature branch bookend tasks (optional)
- **Dependencies** — prerequisite tasks (verify they are Done)

Also capture the issue's `webUrl` field from the API response (e.g. `https://redhat.atlassian.net/browse/PROJ-231`). This URL will be used later to create a clickable link in the PR description.

### Target PR extraction

If the task description contains a **Target PR** section, extract the PR URL. Parse the
URL to extract `owner`, `repo`, and `pr-number` from the pattern
`https://github.com/<owner>/<repo>/pull/<pr-number>`. Store these values for use in
Steps 5, 10, and 11.

When Target PR is present, the task is a review feedback fix — the implementation adds
commits to the existing PR branch instead of creating a new branch and PR. This mode
wins over Target Branch and Bookend Type when more than one is present.

### Target Branch extraction

Extract the branch name from the **Target Branch** section. This is mandatory — every
task description must include it. The value is a single branch name (e.g., `main` for
direct-to-main workflow, or a feature issue ID like `TC-4418` for feature-branch workflow).
Store the value for use in Steps 5 and 10.

### Bookend Type extraction

If the task description contains a **Bookend Type** section, extract the value
(`create-branch` or `merge-branch`). Store the value for use in Steps 5, 10, and 11.

When Bookend Type is present, the task is a feature-branch bookend — it performs
branch or PR operations only. The Modes table lists the steps it runs.

If any required section is missing or the description doesn't follow the template, list the
gaps, ask the user for clarification, and **stop execution immediately** — do not proceed
with any subsequent steps (branching, implementation planning, code changes) until the user
provides the missing information.

### GitHub Issue extraction

Look up the **GitHub Issue custom field** ID from the project's **Jira Configuration**
section in CLAUDE.md (the field is listed as `GitHub Issue custom field: <field-id>`).

- **If configured**, read the custom field value from the fetched issue's fields.
  The value may be a plain URL string or an ADF document containing a URL — extract
  the URL in either case. Parse the GitHub issue URL to extract `owner`, `repo`, and
  `number` from the pattern `https://github.com/<owner>/<repo>/issues/<number>`.
  Store the parsed reference as `<owner>/<repo>#<number>` for use in Step 10.
- **If not configured or the field is empty**, skip silently — this is optional.

## Step 1.5 – Verify Description Integrity

After fetching the task, verify that the description has not been modified since
plan-feature created it. This uses the digest protocol defined in
`shared/description-digest-protocol.md`.

1. **Retrieve issue comments**: fetch all comments on the Jira issue:

   ```
   jira.get_issue_comments(<jira-issue-id>)
   ```

2. **Locate the digest comment**: search for all comments whose body starts with the
   marker string `[sdlc-workflow] Description digest:`. This marker is defined in
   `shared/description-digest-protocol.md`. If multiple comments match (e.g., from
   plan-feature re-runs), select the most recent one by `created` timestamp.

3. **If no digest comment found**: log a warning and proceed normally (backward
   compatibility — tasks created before digest tracking was introduced have no
   digest comment). Do not block execution:

   > "No description digest found — skipping integrity check. This task may have
   > been created before digest tracking was introduced."

4. **If digest comment found**:
   a. **Check for comment editing**: if the comment's `created` and `updated`
      timestamps are available, compare them. If `updated` is later than `created`,
      warn: "Digest comment was edited after initial posting — integrity cannot be
      fully guaranteed." Proceed with digest comparison regardless. If timestamps
      are not available in the API response, skip this check silently.
   b. **Extract the stored digest**: parse the tagged digest value from the comment
      body (e.g., `sha256-md:a1b2...` or `sha256-adf:a1b2...`). Extract the format
      tag and the hex digest. If the digest uses the legacy untagged format
      (`sha256:<hex>`), log a warning ("Legacy digest format — skipping integrity
      check") and proceed normally.
   c. **Compute the current digest**: extract the description field from the issue
      response. Write it to a temp file and compute the digest using the script:

      ```bash
      python3 scripts/sha256-digest.py "$TMPDIR/desc-<task-key>.txt"
      ```

      The script auto-detects the format and outputs a tagged digest. If the script
      exits non-zero, warn and skip the integrity check — do not block execution.
   d. **Compare format tags**: if the stored tag differs from the computed tag
      (e.g., stored is `sha256-adf` but computed is `sha256-md`), the producer and
      consumer used different API access methods. Log a warning ("Digest format
      mismatch — skipping integrity check") and proceed normally.
   e. **Compare hex digests** (when tags match):
      - **Match**: proceed silently — no additional user prompt, no added latency.
      - **Mismatch**: alert the user that the task description was modified after
        plan-feature created it. Display the expected digest (from the comment) and
        the actual digest (computed from the current description). Ask the user
        whether to:
        1. **Proceed** with the current description as-is
        2. **Stop** so they can re-run plan-feature to regenerate tasks

        **Stop execution immediately** — do not proceed with any subsequent steps
        until the user responds.

## Step 2 – Verify Dependencies

If the task has Dependencies, check each one:

jira.get_issue(<dependency-id>)

Verify status is Done or equivalent. If not, stop and inform the user.

## Step 3 – Transition to In Progress and Assign

Transition the Jira issue to indicate work has started, and assign it to the current user:

1. Retrieve the current user's Jira account ID:

jira.user_info()

2. Assign the task to the current user:

jira.edit_issue(<jira-issue-id>, assignee=<current-user-account-id>)

3. Transition the issue to In Progress:

jira.transition_issue → In Progress

This ensures both ownership and status are reflected in Jira as soon as implementation begins.

## Step 4 – Understand the Code

Inspect the files listed in Files to Modify and Files to Create locations using
the dedicated Serena instance for the task's repository. Look up the correct
Serena Instance name in the **Repository Registry** section of the project's CLAUDE.md.

Tools are called as `mcp__<serena-instance>__<tool>`, where `<serena-instance>` is
the instance name from the Repository Registry.

1. **Overview without full reads**: use `get_symbols_overview` on files to modify to see
   their structure (classes, functions, types) without reading the entire file.
2. **Read only what you need**: use `find_symbol` with `include_body=true` to read the
   specific functions, structs, or components you need to understand or change.
3. **Check backward compatibility**: use `find_referencing_symbols` on any symbol you plan
   to modify to identify all callers and ensure your changes won't break them.
4. **Non-symbolic search**: use `search_for_pattern` for configuration, string literals,
   or patterns not captured as symbols.
5. **Convention conformance analysis**: identify sibling files — files in the same directory
   or module that serve a similar role to the files being modified or created. Use
   `get_symbols_overview` on 2–3 siblings to understand their structure and patterns, or
   Read/Glob if Serena is unavailable.

> **Note:** Check the **Code Intelligence** section of the project's CLAUDE.md for
> per-instance limitations (e.g., some language servers may not support certain operations).
> Adapt your tool usage accordingly.

**Fallback**: if no Serena instance is available for the repository, use Read, Grep, and Glob tools directly.

### Documentation file identification

Identify documentation files related to the code being modified. Look for:
- README files in the same directory or parent directories
- API documentation referenced by or related to modified endpoints
- Architecture or design docs that describe the modified components
- `CONVENTIONS.md` at the repository root
- Setup or configuration guides that cover the modified functionality

Record these files for use during documentation-impact evaluation in Step 6 and
the documentation-currency check in Step 9.

Goals:
- understand the current state of files to be modified
- confirm the patterns referenced in Implementation Notes exist
- identify any conflicts with recent changes
- search for existing utilities, helpers, and shared modules that provide functionality overlapping with the planned changes — if equivalent logic already exists, plan to reuse or extend it rather than writing new code
- identify nearby documentation files that may need updating
- identify established conventions from sibling code for use during implementation

### CONVENTIONS.md lookup

Look up the task's target repository in the **Repository Registry** (CLAUDE.md) and use
the **Path** column to locate the repository root. Check for a `CONVENTIONS.md` file at
that root using the Serena instance for the repository (`list_dir`, `search_for_pattern`).
If no Serena instance is available, use Read or Glob with the absolute path from the
Registry (e.g., `<Path>/CONVENTIONS.md`). If present, read it and follow its conventions
throughout implementation. This includes naming rules, directory structure for new files,
code patterns, and test conventions.

This step is optional — if `CONVENTIONS.md` does not exist, proceed normally.

#### Verification commands extraction

When reading `CONVENTIONS.md`, search for a section that lists CI check commands — look for
headings or labels such as "CI checks", "All CI checks", "Linting", "Pre-commit checks",
"Verification", or similar. Extract every command listed in that section and record them
for use in Step 9's CI verification sub-step.

Also look for any commands that generate code artifacts (e.g., OpenAPI spec generation,
code generation, schema generation). Record these separately — they may produce file
changes that need to be committed alongside the implementation.

If no CI check section is found in `CONVENTIONS.md`, proceed normally — Step 9 will
fall back to standard build/lint checks.

### Convention conformance analysis

Analyze established conventions in sibling code — files in the same directory or module
that serve a similar role. Use `get_symbols_overview` on 2–3 siblings (or Read/Glob if
Serena is unavailable). This applies to both production and test files.

Examine siblings for recurring patterns in:
- Naming conventions (functions, variables, types, files, test names)
- Error handling strategies (return types, error wrapping, logging)
- Option/parameter propagation and API design patterns
- Import organization and module structure
- Test patterns: assertion style, response validation, error case coverage,
  setup/teardown, parameterized test usage

Output the discovered conventions as a structured list organized by category. This list
serves as a binding reference during implementation (Step 6) and test writing (Step 7).

If a convention conflict is detected — the task description contradicts an established
convention — flag it to the user and ask for guidance before proceeding.

**Skill guidance takes precedence over sibling patterns:** When a sibling pattern
conflicts with this skill's built-in quality guidance (e.g., Step 7's "prefer value-based
assertions" vs sibling `.any()` checks), follow the skill guidance. Record the conflict
but do not adopt the sibling pattern.

> **Example:** Error handling: handlers use `Result<T, AppError>` with `.context()`.
> Naming: `verb_noun` pattern. Test assertions: `assert_eq!(resp.status(), StatusCode::OK)`.

## Step 5 – Branch

Apply the **Step 5 – branch** column of the Modes table.

**default** — check out the target branch (Target Branch, Step 1), update it, and create
the task branch:

```
git checkout <target-branch>
git pull
git checkout -b <jira-issue-id>
```

**target-pr** — check out the existing PR branch so the fix commits land on it:

```
gh pr view <pr-number> --json headRefName -R <owner/repo>
git checkout <branch-name>
git pull
```

**create-branch** — create and push the feature branch from main. The branch name is the
parent feature issue ID, not this task's Jira issue ID:

```
git checkout main
git pull
git checkout -b <feature-branch-name>
git push -u origin <feature-branch-name>
```

**merge-branch** — no branch operation.

Completion: the branch named in the Modes row is checked out and clean, or the mode is
merge-branch.

## Step 6 – Implement Changes

The **Description** section is your primary specification — implement exactly what it describes.
Use **Files to Modify**, **Files to Create**, and **API Changes** as your working scope.
Do not plan or implement changes to files outside these sections — if you discover a
file that seems to need modification, flag it in Step 9's scope containment check
instead of adding it to your plan.
Follow the **Implementation Notes** for patterns and code references on how to implement the changes.

**Reuse first:** Before writing new logic, check whether the Implementation Notes list reusable
code (utilities, helpers, shared modules). If they do, use or extend the existing code. If you
discover additional reusable code during implementation that was not listed, prefer reusing it
over creating duplicated logic.

**Follow conventions:** Apply the conventions discovered during Step 4's convention conformance
analysis. When writing new code, match the patterns found in sibling files rather than inventing
new approaches. If any Implementation Notes or task instructions conflict with a discovered
convention, follow the guidance obtained from the user during Step 4.

### Reuse over duplication

When the implementation needs to use a function, method, or utility that exists in another
module or package but is not publicly exported (e.g., a private function in a Rust crate,
an unexported function in a Go package, a non-exported function in a Node.js module),
decide whether to make it public or duplicate it:

1. **Check dependency relationship**: determine whether the source package (where the
   function lives) is already a dependency of the target package (where you need to use it).
   Use the project's dependency manifest (e.g., `Cargo.toml`, `package.json`, `go.mod`,
   `pom.xml`) to verify.
2. **If the dependency already exists**: make the function public (`pub`, `export`, etc.)
   and import it rather than duplicating the code. This follows the DRY principle and
   ensures future bug fixes apply in one place.
3. **If adding a new dependency would be required**: inlining or duplicating the function
   is acceptable — introducing a new cross-package dependency for a single utility may
   not be worth the coupling.
4. **Flag the decision**: when choosing between options 2 and 3, state the choice and
   rationale in the commit message or PR description so reviewers understand why code
   was reused or duplicated.

### Symbol deduplication

Before declaring any new constant, enum, type alias, or configuration map, search the
target package for an existing definition of the same symbol. This applies especially
when the task description references a sibling module — the symbol may already exist there.

1. **Search before declaring**: use `find_symbol`, `search_for_pattern`, or Grep to search
   the target package (not just the file being edited) for the symbol name or its value.
   Include common variations (e.g., `SEVERITY_ORDER`, `severityOrder`, `SeverityOrder`).
2. **If found**: import and reuse the existing definition. If it is not exported, follow
   the "Reuse over duplication" guidance above to decide whether to export it or inline it.
3. **If not found**: declare the new symbol in the most appropriate shared location
   (utilities module, constants file, or the file where it is used if truly local).

> **Example:** Task says "sort remediations by severity". Before declaring
> `const SEVERITY_ORDER = [...]`, grep the package for `SEVERITY_ORDER`. If
> `src/remediation.js` already exports it, import from there instead of redeclaring.

### Serena symbolic editing (preferred)

Use the dedicated Serena instance for the task's repository (look up the instance name
in the project's **Repository Registry**):

- `replace_symbol_body` — rewrite an entire function, method, struct, or component
- `insert_after_symbol` / `insert_before_symbol` — add new code relative to existing symbols
- `rename_symbol` — rename a symbol and automatically update all references

### File-based editing (fallback)

Use Edit/Write tools for non-code files, config files, or when Serena is unavailable.

For each file in Files to Modify:
- Read the current code (or use `get_symbols_overview` + `find_symbol` to read selectively)
- Apply the described changes
- Follow existing patterns

For each file in Files to Create:
- Use the patterns referenced in Implementation Notes
- Ensure proper integration (module registration, imports, etc.)

For API Changes:
- Implement endpoint logic
- Update OpenAPI spec if applicable

### Cross-repo API contract verification

When the task involves writing manual REST calls (`fetch()`, `axios`, etc. rather than
an auto-generated client), verify each endpoint against the backend repository before
writing the call. Look up the backend Serena instance in the Repository Registry
(or use Grep/Read as fallback).

For each endpoint, verify:
1. The endpoint path exists in route definitions and the HTTP method matches.
2. The request body shape or query parameters match what the frontend will send.
3. The response body shape matches what the frontend will consume (field names, types, nesting).
4. When the frontend selects by position (e.g., `items[0]` for "latest"), the backend's
   sort order matches — inspect `ORDER BY` clauses or `.sort()` calls in the query builder.

If any path, method, shape, or sort order does not match, stop and report the discrepancy
(what the task specifies vs what the backend implements, with source file and line).
Include a code comment referencing the backend source file for each verified manual call.

### Code quality practices

After implementing code changes, verify the following quality practices:

- **Documentation on new symbols**: every new struct, class, type, interface, enum, and
  public/exported function must have a documentation comment using the language's
  convention. One line describing what it is and what it's for is sufficient. For
  functions where the name alone does not convey the full intent, add a brief
  explanation of behavior, parameters, or return value so that human reviewers can
  understand the code without reading the implementation.

- **Defensive property access on external data**: when consuming data produced by another
  module, service, or external API, add null/undefined guards before accessing nested
  properties — especially arrays and objects that may be absent even when the upstream
  type signature suggests otherwise. Use the language's idiomatic guard pattern (e.g.,
  optional chaining `?.` in JavaScript/TypeScript, `if let` / `.unwrap_or_default()` in
  Rust, `getattr(obj, 'field', default)` in Python). This applies to any property access
  path where the data crosses a module boundary — the producer's schema may allow null,
  return partial results, or evolve independently.

  > **Example:** Upstream returns `{ cves: string[] | null }`. Before accessing
  > `rem.cves.length` or `rem.cves.join(',')`, guard with `(rem.cves ?? [])` or
  > equivalent.

### Documentation impact

After implementing code changes, evaluate whether documentation needs updating:

1. Check if the task includes a **Documentation Updates** section — if so, apply those updates.
2. If no Documentation Updates section exists, check the documentation files identified in Step 4:
   - If public APIs, CLI commands, or endpoints were added or changed, update related API docs.
   - If configuration options or setup steps were modified, update related guides.
   - If architectural patterns were changed, update architecture docs.
3. Keep documentation updates lightweight and scoped — only update docs directly impacted by the changes.

## Step 7 – Write Tests

Implement the tests described in Test Requirements.

**Follow test conventions:** Apply the test conventions discovered during Step 4's test
convention analysis. When writing new tests, match the assertion patterns, response
validation style, error case coverage, and naming conventions found in sibling test files
rather than inventing new approaches.

**Skill guidance overrides sibling patterns:** The test conventions from Step 4 are
defaults. The guidance below (value-based assertions, parameterized tests, test
documentation) is the skill's explicit quality standard and takes precedence over
conflicting sibling patterns. Note any deviation in the convention output.

**Prefer value-based assertions over length-only checks:** When verifying collections or
response data, assert on the actual values — not just the count. Assert on specific items
or key fields so that test failures reveal *what* changed, not just *how many*. Length
checks alone hide regressions behind a passing count and prevent subsequent assertions
from running.

**Prefer parameterized tests for repetitive cases:** When multiple test cases exercise
the same behavior with different inputs and expected outputs, use the project's
parameterized test mechanism instead of writing individual test functions for each case.
Apply the Meszaros heuristic as the decision boundary: parameterize when tests share the
same algorithm (setup, action, assertion structure) with different data; use individual
tests when behavior, setup, or assertions differ between cases. If the test body would
need conditionals to handle parameter variations, use separate tests instead. Common
mechanisms include JUnit 5 `@ParameterizedTest`, Mocha/Jest `forEach`/data arrays,
pytest `@pytest.mark.parametrize`, Go table-driven tests, and Rust `rstest`. However,
if the sibling test analysis in Step 4 shows the project does not use parameterized
tests, do not introduce them — follow the project's existing test patterns instead.

**Document every test function:** Add a documentation comment before every test function
explaining what it verifies — a single line using the language's doc comment convention
(e.g., `///` in Rust, `/** */` in Java/TypeScript, `"""` docstring in Python). This applies
regardless of whether sibling tests have documentation; AI-generated tests introduce this
as a new standard that overrides the "Follow test conventions" guidance above for
documentation specifically.

For non-trivial tests — those with distinct setup, action, and assertion phases — also add
given-when-then section comments (`// Given`, `// When`, `// Then`) inside the test body to
make the structure navigable at a glance. A test is trivial (skip given-when-then) when it
has a single assertion with no distinct setup phase.

> **Example (Rust):**
>
> ```rust
> /// Verifies that an SBOM with no dependencies produces an empty risk score.
> #[test]
> fn test_empty_sbom_risk_score() {
>     // Given an SBOM with no dependencies
>     let sbom = create_test_sbom(vec![]);
>
>     // When calculating the risk score
>     let score = calculate_risk(&sbom);
>
>     // Then the score should be zero
>     assert_eq!(score, RiskScore::default());
> }
> ```
>
> The doc comment convention varies by language — use `///` for Rust, `/** */` for
> Java/TypeScript, `"""docstring"""` for Python, `//` doc comments for Go, etc.

### Eval assertion/fixture consistency

When adding or changing eval cases, verify every assertion against both:

1. **Explicit requirements** — use the task's Description and Acceptance Criteria, plus
   any authoritative contract, to establish what behavior is required.
2. **Fixture semantics** — inspect supplied fixture values and relationships to confirm
   the assertion describes them correctly.

Assertions must not add constraints that the contract does not state. In particular,
requiring a value on every row does not imply that values must be unique across rows.
Repeated fixture values are valid unless the applicable requirement explicitly requires
uniqueness.

If an assertion conflicts with the stated requirements or supplied fixture, do not
silently change the fixture or contract to make the assertion pass. Correct the assertion
to match the authoritative requirement and fixture, or ask the user when the source of
truth is unclear.

Run the project's test command and fix any failures before proceeding. Step 9 resolves
the exact command: the CI checks recorded from `CONVENTIONS.md`, or the per-crate test
rule for Rust repositories.

## Step 8 – Verify Acceptance Criteria

Go through each Acceptance Criterion and verify it is satisfied.
If any criterion cannot be met, stop and explain to the user.

## Step 9 – Self-Verification

Before committing, verify that all changes are in scope and free of common errors.

### Scope containment

1. Run `git diff --name-only` to list all modified and created files.
2. Compare the list against the **Files to Modify** and **Files to Create** parsed in Step 1.
3. If any file is out-of-scope (not listed in either section):
   - List the out-of-scope file(s).
   - Explain why each was modified.
   - Ask the user to approve or revert each out-of-scope change.
   - Do **not** proceed to commit without explicit user approval for every out-of-scope file.

### Untracked file check

Run `git status --short` and filter untracked files (`??`) in directories with
modified files. For each, search the staged diff for references to its filename
(compile-time includes, imports, config paths, string literals). Flag referenced
or proximity-matched untracked files for user approval before staging — do not
automatically stage untracked files.

### Dead parameter detection

When the implementation removes code that references function parameters, scan the
modified functions for parameters that are no longer used in the function body.

1. **Identify candidates**: from `git diff`, find functions where removed lines
   contained the only reference to a parameter.
2. **Detect dead parameters**: look for underscore-prefixed parameters (`_version`,
   `_ctx`), compiler/linter warnings about unused parameters, or parameters with
   zero references in the function body. The correct fix is removal, not renaming.
3. **Remove dead parameters**: remove the parameter from the signature, use
   `find_referencing_symbols` (or Grep) to find all call sites, and update every
   caller to remove the corresponding argument. For trait/interface methods, only
   remove if no implementation references the parameter.
4. **Re-run tests** to confirm nothing broke.

> **Example:** `fn filter_by_status(items: &[Item], version: &str)` no longer uses
> `version` after a code change. Remove the parameter and update all callers from
> `filter_by_status(items, "1.0")` to `filter_by_status(items)`.

### Validated-value override paths

When a change adds a validated, security-relevant, or fail-closed value to a function,
trace every later write into the same object or payload. Generic merge or override
parameters — extra-field maps, variadic passthroughs, defaults merges, patch helpers —
can run after the validated assignment and silently replace or drop it.

1. **List later writes**: for each new validated or protective value, enumerate every
   assignment, merge, or bulk update that runs after it in the same function and its
   immediate callees.
2. **Verify none can replace it**: confirm each path preserves the validated value.
   When one can overwrite or remove it, either apply the validated value last or reject
   a conflicting key with the project's fail-fast error handling — never rely on call
   order staying unchanged.
3. **Test the conflict when one exists**: when steps 1–2 find a later write path
   that can replace or remove the validated value, add a test proving a generic
   override cannot change it, not only that the value is set on the happy path.
   When no such path exists, no conflict test is required — do not add a test seam
   for a conflict the function cannot express.

> **Example:** a builder validates a protection level, writes it, then merges a
> caller-supplied extra-fields map. A conflicting key in that map would replace the
> validated level, so the builder must reject it or re-apply the validated value after
> the merge.

### Sensitive-pattern check

Search every change this commit would include — staged and unstaged tracked changes:

git diff HEAD | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'

If any match is found, flag it to the user and resolve it before committing.

### Documentation currency

If the implementation changed public APIs, configuration options, or setup steps,
verify that related documentation files (identified in Step 4) are still accurate.
If a doc file describes behavior that was changed and was not already updated in
Step 6, update it now. This check is lightweight — only flag docs that directly
describe the modified behavior.

### Documentation scope preservation

For each replaced documentation section, verify the replacement still covers all use
cases, input types, and scenarios the original described. Extract use cases from
removed lines in the diff (enumerations, conditional branches, listed alternatives),
then check the added lines address each one. If any use case is absent and the task
doesn't justify its removal, flag for user confirmation before proceeding.

### Eval coverage currency

If any modified file matches `skills/<skill-name>/SKILL.md`, check whether
`evals/<skill-name>/evals.json` exists. If it does, compare the SKILL.md diff
against existing eval assertions and flag new behavior (new steps, output formats,
decision branches) that has no corresponding assertion. Present gaps to the user
and ask whether to add coverage now, defer, or skip — advisory only, do not block.

### Example consistency

If the implementation wrote or modified documentation with composite examples (narrative
text paired with data structures — tables, JSON, code snippets), cross-check that every
entry in the data structure matches the narrative and vice versa. Fix any mismatches
(field names, values, labels, relationships) before proceeding.

### Cross-section reference consistency

Verify that the same entity (struct, service, module, component) uses consistent
file paths across Files to Modify, Files to Create, and Implementation Notes. If
the same entity is associated with different paths across sections, resolve by
inspecting the actual codebase before implementing. Apply the same validation to
any structured documents the implementation creates (eval fixtures, task descriptions).

### Duplication check

Search for functions, methods, or logic in the repository that overlap with the code you wrote.
Use Grep or Serena's `search_for_pattern` to look for similar function names, string literals,
or algorithmic patterns. If you find that your new code substantially duplicates existing
utilities or helpers, refactor to reuse the existing code before proceeding.

### CI checks from CONVENTIONS.md

If `CONVENTIONS.md` was loaded in Step 4 and verification commands were extracted,
run every CI check command recorded during the verification commands extraction.
Execute each command in sequence.

**Hard stop on failure:** If any CI check command exits with a non-zero status,
**stop execution immediately** — do not proceed to Step 10 (Commit and Push).
Report the failure to the user, including the command that failed and its output.
Do not attempt to classify the failure (e.g., infrastructure vs. code), do not
add fallback logic, and do not treat any failure as non-blocking. Every non-zero
exit is a hard stop. The user decides how to proceed.

1. **Run all CI check commands**: execute each command extracted from the
   `CONVENTIONS.md` CI checks section (e.g., formatting, linting, type checking,
   compilation). These commands are project-specific — do not hardcode or assume
   which tools the project uses.
2. **Run code generation commands**: if any code generation commands were extracted
   (e.g., OpenAPI spec generation, schema generation, code scaffolding), run them
   now. If they produce file changes, stage those changes for commit alongside the
   implementation — they are part of the deliverable.
3. **Fix failures**: if any CI check command fails, fix the underlying issue and
   re-run the failing command until it passes. Do not skip failing checks. If the
   failure cannot be fixed (e.g., missing infrastructure, unavailable tools), stop
   and report to the user — do not proceed to commit.

If `CONVENTIONS.md` was not found or contained no CI check section, run the project's
standard build or lint step (if one exists) and fix any warnings it reports in files
this task modified.

### Module-level test requirement (Rust)

For Rust repositories, run the test suite for every crate containing modified files,
regardless of whether `CONVENTIONS.md` CI checks include a test command. Lint, fmt,
and `cargo check` pass even when test logic is broken — a separate test run is required
before committing.

For each modified file, run `cargo metadata --no-deps --format-version 1` from the workspace root and resolve the package whose manifest or target source contains the file. Use that package's `name` as `<crate-name>`; do not derive it from the nearest `Cargo.toml`, which may be a virtual workspace manifest. Skip modified files that do not belong to any package or crate.
Run:

```
cargo test -p <crate-name>
```

or, if the project uses nextest:

```
cargo nextest run -p <crate-name>
```

Apply the same hard-stop rule: if the test command exits non-zero, stop immediately,
report the failure, and do not proceed to Step 10.

> **Note:** If the test context requires a database or external service, attempt the
> run first — many Rust projects bootstrap their own test DB. Only skip if the
> environment is genuinely unavailable, and report clearly that tests were not run.

### Data-flow trace

For each new feature, trace data through its complete lifecycle: input (API request,
file read, user event) → processing (validation, transformation) → output (response,
persistence, UI render). Confirm each stage connects to the next. Flag incomplete
paths (missing or disconnected stages) and fix before committing, or ask the user to
confirm if the missing stage is intentionally out of scope. Output the traced flows
and their completeness status to the user.

### Query-scope verification

When implementing batch operations (data migrations, batch updates, or any code
iterating database records), verify the query scope matches the task's target scope.

1. **Extract target scope**: scan the task **Description** for subset-restricting
   language — type qualifiers, status filters, date ranges, category selectors.
2. **Compare query scope**: check whether each batch query filters to the target
   subset or loads all records indiscriminately.
3. **Flag scope mismatches**: if the task targets a subset but a narrower query is
   possible at the data source (via columns, indexes, ORM scopes, or API
   parameters), flag for review with: target scope, actual query scope, available
   filter, and performance impact.
4. **Accept intentional broad queries**: when filtering cannot be expressed at the
   query level or the full dataset is needed, document the rationale in a comment.

> **Example:** Task: "re-process all SPDX SBOMs". Query: `Document::all()`.
> Flag: `labels->>'type'` supports filtering — use filtered query instead.

### Contract & sibling parity

Verify that modified or created code fully honors its type contracts and maintains
parity with sibling implementations. Run four checks using the pattern below:

| Check | What to compare | Search method |
|-------|----------------|---------------|
| **Contract** | All methods, properties, and type signatures required by implemented interfaces/traits/abstract classes/protocols. Parameter types, return types, nullability must align. | `find_symbol` or Grep to locate the contract definition |
| **Sibling parity** | Cross-cutting concerns: shared capabilities, error handling, logging, configuration options. Reuse siblings from Step 4. | `get_symbols_overview` on sibling files |
| **Cross-module entity** | When writing to a shared DB entity used by other modules: transaction handling, constraint/conflict handling, data validation, locking strategies. | `search_for_pattern` or Grep for all modules interacting with the same entity |
| **Caller-site** | When calling a shared abstraction (hook, API client, service function): success/error handling, side effects, parameter patterns. Compares how *consumers* invoke it, not the definition. | `find_referencing_symbols` or Grep for all callers of the same abstraction |

For each check: identify targets, search and compare against the reference (siblings,
cross-module peers, or existing callers), flag anomalies with what the new code does vs
the established pattern, and fix or ask the user to confirm before proceeding.

Output all four check results to the user before proceeding.

> **Example:** Contract: `StorageProvider` missing `update()` from `Provider` trait.
> Sibling parity: `StorageProvider` missing `info!()` logging present in `S3Provider`/`GcsProvider`.
> Cross-module: `ingestor` uses `ON CONFLICT DO UPDATE` but new code uses plain `insert()`.
> Caller-site: new code uses `window.location.reload()` but 3 existing callers use `queryClient.invalidateQueries()`.

## Step 10 – Commit and Push

Commit following the Conventional Commits specification (https://www.conventionalcommits.org/en/v1.0.0/):

git commit --trailer="Assisted-by: <tool> (<model>)" -m "<type>[optional scope]: <description>

[optional body]

Implements <JIRA-ID>"

Where type is one of: feat, fix, refactor, test, docs, chore, etc.
Use a scope when relevant (e.g. `feat(api): add AIBOM endpoint`).
The footer MUST reference the Jira issue ID.
Always include `--trailer="Assisted-by: <tool> (<model>)"` to attribute AI assistance.
Substitute `<tool>` and `<model>` with the name of the AI tool and model you are running as (for example `OpenCode (GPT-6.1 Sol)` or `Claude Code (Claude Opus 4.1)`).

### Fork detection

Before creating a PR, detect whether the working directory is a fork by checking
for an `upstream` remote:

```
git remote get-url upstream 2>/dev/null
```

- If the command succeeds, an `upstream` remote exists — the user is working in a fork.
  Parse `<upstream-owner/repo>` from the upstream remote URL and `<fork-owner>` from
  the origin remote URL. Handle both HTTPS (`https://github.com/<owner>/<repo>.git`)
  and SSH (`git@github.com:<owner>/<repo>.git`) URL formats.
- If the command fails, no upstream remote exists — skip fork-specific flags and use
  the default `gh pr create` behavior.

Apply the **Step 10 – PR** column of the Modes table.

**default** — push the task branch and open a pull request against `<target-branch>`
(always pass `--base` explicitly):

```
gh pr create --base <target-branch> ...                                          # no fork
gh pr create -R <upstream-owner/repo> --head <fork-owner>:<branch> --base <target-branch> ...   # fork
```

Write the PR description with:

- `Implements [<JIRA-ID>](<webUrl>)` — a Markdown link so the Jira issue is clickable;
  `<webUrl>` is the URL captured in Step 1 (e.g. `https://redhat.atlassian.net/browse/PROJ-231`).
- `Closes <owner>/<repo>#<number>` when a GitHub issue reference was extracted in Step 1.
  This line belongs in the PR description only, never in the commit message.

**target-pr** — push the new commits to the existing branch and extend its description:

```
git push
gh pr edit <pr-number> -R <owner/repo> --body "<updated-description>"
```

Append a Summary bullet describing this fix and preserve the existing description content.

**merge-branch** — open the merge PR. The feature branch already holds every commit, so
no new commit is needed:

```
gh pr create --base main --head <feature-branch-name> ...                                        # no fork
gh pr create -R <upstream-owner/repo> --head <fork-owner>:<feature-branch-name> --base main ...  # fork
```

Reference the feature issue in the description and list the tasks implemented on the branch.

## Step 11 – Update Jira

Apply the **Step 11 – Jira** column of the Modes table. Every comment ends with the
footnote from `shared/comment-footnote.md` (skill name `implement-task`).

**PR custom field.** Look up the **Git Pull Request custom field** ID in the project's
**Jira Configuration** (CLAUDE.md). When configured, set it to the PR URL — the field
requires ADF (Atlassian Document Format), not a plain string:

jira.update_issue(<jira-issue-id>, fields={"<field-id>": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})

When the field is not configured, skip it — the comment still carries the link.

**Comment and transition per mode:**

- **default** — comment with the PR link, a summary of changes made, and any deviations
  from the plan; set the PR field; transition to **In Review**.
- **target-pr** — comment with the Target PR link, a summary of the fix, and the review
  feedback that triggered it; leave the PR field as the original task set it; transition
  to **In Review**.
- **create-branch** — comment that the feature branch was created, naming it; skip the PR
  field (there is no PR); transition to **Done**.
- **merge-branch** — set the PR field to the merge PR URL; comment with the merge PR link
  and a summary of the feature branch; transition to **In Review**.

## Important Rules

- Do not guess — use the Serena instance specified in the project's **Repository Registry** (CLAUDE.md) for the target repo, with tools like `get_symbols_overview`, `find_symbol`, `find_referencing_symbols` to inspect code before modifying it. Check the **Code Intelligence** section for per-instance limitations. Fall back to Read/Grep/Glob for repos without a Serena instance.
- Follow the Implementation Notes closely — they reference real code patterns.
- If the structured description is incomplete, ask the user for clarification and **stop execution**. Do not draft an implementation plan, create branches, or proceed with any subsequent steps until the user provides the missing information.
- Keep changes strictly within **Files to Modify** and **Files to Create** — do not add, plan, or propose modifications to files outside these sections. If an out-of-scope file needs changes, flag it in Step 9's scope containment check for user approval.
- Every commit must reference the Jira issue ID.
- If the same test fails 3 times with the same error, stop and ask the user for guidance — do not retry the same approach.
- If the same file is edited more than 5 times for the same change, stop and reassess your approach — present the problem and proposed alternatives to the user.
- If a build or compile error persists after 2 fix attempts, stop and present the error and proposed alternatives to the user — do not keep trying the same fix.
