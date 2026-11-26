# Self-Verification Checks

Procedures for the checks listed in the `implement-task` Step 9 table. Step 9 decides
which checks fire; this file defines how to run each one. Apply every check that fires
and report each as `PASS` or `FLAGGED` before committing.

## 1. Scope containment

1. Run `git diff --name-only` to list all modified and created files.
2. Compare the list against the **Files to Modify** and **Files to Create** parsed in
   Step 1.
3. For each file outside those sections:
   - List the file and explain why it changed.
   - Ask the user to approve or revert it.
   - Obtain explicit approval for every out-of-scope file before committing.

## 2. Untracked files

Run `git status --short`. For each untracked file (`??`) in a directory with modified
files, search the diff for references to its filename (compile-time includes, imports,
config paths, string literals). Flag referenced or proximity-matched files for user
approval before staging; stage untracked files only with that approval.

## 3. Sensitive patterns

Search every change the commit would include — staged and unstaged tracked changes:

```bash
git diff HEAD | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

Flag any match to the user and resolve it before committing.

## 4. Dead parameters

When the implementation removed code that referenced a function parameter:

1. From `git diff`, find functions where removed lines contained the only reference to a
   parameter.
2. Detect dead parameters: underscore-prefixed names (`_version`, `_ctx`), compiler or
   linter warnings about unused parameters, or parameters with zero references in the
   body. The correct fix is removal, not renaming.
3. Remove the parameter, use `find_referencing_symbols` (or Grep) to find every call
   site, and update each caller to drop the argument. For trait/interface methods,
   remove only when no implementation references the parameter.
4. Re-run the tests.

> **Example:** `fn filter_by_status(items: &[Item], version: &str)` no longer uses
> `version`. Remove the parameter and update callers from
> `filter_by_status(items, "1.0")` to `filter_by_status(items)`.

## 5. Duplication

Search for functions, methods, or logic that overlap with the code you wrote — Grep or
Serena's `search_for_pattern` on similar function names, string literals, and
algorithmic patterns. Substantial overlap means the new code should reuse the existing
utility; refactor according to the Step 6 **Reuse** rules before committing.

## 6. Documentation currency

If the implementation changed public APIs, configuration options, or setup steps, verify
that the documentation files identified in Step 4 are still accurate. Update any doc
that describes the changed behavior and was not already updated in Step 6's
**Documentation impact**. Flag only docs that directly describe the modified behavior.

## 7. Documentation scope preservation

For each replaced documentation section, verify the replacement covers every use case,
input type, and scenario the original described. Extract the use cases from removed
lines in the diff (enumerations, conditional branches, listed alternatives) and check
that the added lines address each one. If a use case is absent and the task does not
justify its removal, flag it for user confirmation.

## 8. Eval coverage

If any modified file matches `skills/<skill-name>/SKILL.md`, check whether
`evals/<skill-name>/evals.json` exists. When it does, compare the SKILL.md diff against
the existing assertions and flag new behavior (new steps, output formats, decision
branches) that has no corresponding assertion. Present the gaps and ask whether to add
coverage now, defer, or skip — advisory, never blocking.

## 9. Example consistency

For documentation with composite examples (narrative paired with data structures —
tables, JSON, code snippets), cross-check that every entry in the data structure matches
the narrative and vice versa. Fix mismatches (field names, values, labels, relationships)
before committing.

## 10. Cross-section references

Verify that the same entity (struct, service, module, component) uses consistent file
paths across Files to Modify, Files to Create, and Implementation Notes. When paths
differ, inspect the codebase and resolve the discrepancy. Apply the same validation to
structured documents the implementation creates (eval fixtures, task descriptions).

## 11. Data-flow trace

For each new feature, trace data through its complete lifecycle: input (API request,
file read, user event) → processing (validation, transformation) → output (response,
persistence, UI render). Confirm each stage connects to the next. Fix incomplete paths,
or ask the user to confirm that a missing stage is intentionally out of scope. Report
the traced flows and their completeness.

## 12. Query scope

When implementing batch operations (data migrations, batch updates, or code iterating
database records):

1. Extract the target scope from the task **Description** — type qualifiers, status
   filters, date ranges, category selectors.
2. Check whether each batch query filters to that subset or loads all records.
3. When the task targets a subset and a narrower query is possible at the data source
   (columns, indexes, ORM scopes, API parameters), flag it with the target scope, actual
   query scope, available filter, and performance impact.
4. When filtering cannot be expressed at the query level or the full dataset is needed,
   record the rationale in a comment.

> **Example:** Task: "re-process all SPDX SBOMs". Query: `Document::all()`.
> Flag: `labels->>'type'` supports filtering — use a filtered query instead.

## 13. Contract & sibling parity

Verify that modified or created code honors its type contracts and matches sibling
implementations. Run four checks:

| Check | What to compare | Search method |
|-------|----------------|---------------|
| **Contract** | All methods, properties, and signatures required by implemented interfaces/traits/abstract classes/protocols. Parameter types, return types, nullability must align. | `find_symbol` or Grep to locate the contract definition |
| **Sibling parity** | Cross-cutting concerns: shared capabilities, error handling, logging, configuration options. Reuse the siblings from Step 4. | `get_symbols_overview` on sibling files |
| **Cross-module entity** | When writing to a shared DB entity used by other modules: transaction handling, constraint/conflict handling, data validation, locking strategies. | `search_for_pattern` or Grep for all modules interacting with the same entity |
| **Caller-site** | When calling a shared abstraction (hook, API client, service function): success/error handling, side effects, parameter patterns. Compares how *consumers* invoke it, not the definition. | `find_referencing_symbols` or Grep for all callers of the same abstraction |

For each check, search and compare against the reference, flag anomalies as what the new
code does vs the established pattern, and fix or get user confirmation before
proceeding. Report all four results.

> **Example:** Contract: `StorageProvider` missing `update()` from `Provider` trait.
> Sibling parity: `StorageProvider` missing `info!()` logging present in `S3Provider`/`GcsProvider`.
> Cross-module: `ingestor` uses `ON CONFLICT DO UPDATE` but new code uses plain `insert()`.
> Caller-site: new code uses `window.location.reload()` but 3 existing callers use `queryClient.invalidateQueries()`.

## 14. CI checks from CONVENTIONS.md

Run every CI check command recorded during Step 4's verification-commands extraction, in
sequence. Then run any recorded code generation commands and stage the files they
change — they are part of the deliverable.

**Hard stop:** a non-zero exit from any command stops execution. Report the failing
command and its output; the user decides how to proceed. Do not classify the failure, add
fallback logic, or treat it as non-blocking.

When `CONVENTIONS.md` was absent or had no CI check section, run the project's standard
build or lint step (if one exists) and fix any warnings it reports in files the task
modified.

## 15. Module tests (Rust)

For Rust repositories, run the test suite for every crate containing modified files,
regardless of whether the CI checks include a test command — lint, fmt, and
`cargo check` pass even when test logic is broken.

For each modified file, run `cargo metadata --no-deps --format-version 1` from the
workspace root and resolve the package whose manifest or target source contains the
file. Use that package's `name` as `<crate-name>`; do not derive it from the nearest
`Cargo.toml`, which may be a virtual workspace manifest. Skip files outside every
package. Run:

```bash
cargo test -p <crate-name>
# or, when the project uses nextest:
cargo nextest run -p <crate-name>
```

The same hard stop applies: a non-zero exit stops execution and reports the failure.

> **Note:** If the test context needs a database or external service, attempt the run
> first — many Rust projects bootstrap their own test DB. Skip only when the environment
> is genuinely unavailable, and report clearly that tests did not run.

## 16. Validated-value override paths

When a change adds a validated, security-relevant, or fail-closed value to a function,
trace every later write into the same object or payload. Generic merge or override
parameters — extra-field maps, variadic passthroughs, defaults merges, patch helpers —
can run after the validated assignment and silently replace or drop it.

1. **List later writes**: for each new validated or protective value, enumerate every
   assignment, merge, or bulk update that runs after it in the same function and its
   immediate callees.
2. **Verify none can replace it**: confirm each path preserves the validated value. When
   one can overwrite or remove it, either apply the validated value last or reject a
   conflicting key with the project's fail-fast error handling — never rely on call
   order staying unchanged.
3. **Test the conflict when one exists**: when steps 1–2 find a later write path that can
   replace or remove the validated value, add a test proving a generic override cannot
   change it, not only that the value is set on the happy path. When no such path exists,
   no conflict test is required — do not add a test seam for a conflict the function
   cannot express.

> **Example:** a builder validates a protection level, writes it, then merges a
> caller-supplied extra-fields map. A conflicting key in that map would replace the
> validated level, so the builder must reject it or re-apply the validated value after
> the merge.
