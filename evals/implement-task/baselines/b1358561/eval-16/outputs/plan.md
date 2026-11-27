# Implementation Plan — TC-9213

**Summary**: Add validated risk classification to the advisory summary builder
**Repository**: trustify-backend
**Target Branch**: main
**Mode**: default (no Target PR, no Bookend Type). Branch `TC-9213` from `main`; open PR -> `main`.

## Pre-implementation steps (simulated, no external calls)

- **Step 0 – Project Configuration**: the mock CLAUDE.md has Repository Registry
  (trustify-backend / serena_backend / `./`), Jira Configuration (project key, Cloud ID,
  Feature issue type ID) and Code Intelligence with the `mcp__<instance>__<tool>` convention. Valid.
- **Step 1 – Parse**: every required section is present (Repository, Target Branch, Description,
  Files to Modify, Files to Create, API Changes, Implementation Notes, Acceptance Criteria,
  Test Requirements, Dependencies). No Target PR, no Bookend Type -> default mode.
- **Step 1.5 – Digest**: would fetch comments and compare the `[sdlc-workflow] Description digest:`
  comment. Not done here (no Jira access).
- **Step 2 – Dependencies**: "None". Nothing to check.
- **Step 3 – Jira**: would assign to the current user and move to In Progress. Not done here.
- **Step 4 – Understand the code** (with `serena_backend`):
  - `get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` and
    `modules/fundamental/src/advisory/model/summary.rs`.
  - `find_symbol("AdvisoryService/build_summary", include_body=true)` to confirm the Implementation
    Notes: it fills `AdvisorySummary` field by field and returns it, with no later merge, bulk update
    or generic write.
  - `find_symbol("AdvisorySummary", include_body=true)` to see the derives (Serialize/Deserialize/
    ToSchema) and the existing `severity` field, so the new field follows the same pattern.
  - `find_referencing_symbols` on `AdvisorySummary` and `build_summary` to find every struct-literal
    construction site and caller that needs the new field or argument.
  - `find_symbol` on `AppError` in `common/src/error.rs` to pick the existing client-error variant
    (for example `AppError::BadRequest`) and the `.context()` usage.
  - Reuse search: `search_for_pattern` for `RiskClassification|risk_classification|"critical"|
    ALLOWED_` to check whether an enum or allowed-value constant already exists (for example next
    to the `severity` handling). If one exists, import it instead of writing a new one.
  - Read `CONVENTIONS.md` at the repo root for naming rules, test conventions and the CI check
    commands used by Step 9 check 14.
  - Sibling conventions: `SbomSummary` and `PackageSummary` (model), `SbomService` (service),
    `tests/api/advisory.rs` and `tests/api/sbom.rs` (tests). Errors use `Result<T, AppError>` with
    `.context()`. Tests follow the `assert_eq!` pattern.
  - Docs: `README.md`, `docs/api.md`. The task has no API Changes, so neither should need an update.

## Files to Modify

### 1. `modules/fundamental/src/advisory/model/summary.rs`

- Add a public field to `AdvisorySummary`, with a doc comment:
  ```rust
  /// Validated risk classification of the advisory: one of `critical`, `high`, `medium`, `low`.
  pub risk_classification: String,
  ```
- Add the allowed set as a single source of truth, next to the model (unless the Step 4 reuse
  search finds an existing definition):
  ```rust
  /// Risk classification values accepted by `AdvisoryService::build_summary()`.
  pub const ALLOWED_RISK_CLASSIFICATIONS: &[&str] = &["critical", "high", "medium", "low"];
  ```
- Keep the struct's existing derives and serde attributes so the field serializes like `severity`.

### 2. `modules/fundamental/src/advisory/service/advisory.rs`

- Add a `risk_classification: &str` input to `AdvisoryService::build_summary()`. If
  `find_referencing_symbols` shows existing callers, update each one. Any caller outside the
  listed files is a Step 9 scope flag that needs user approval.
- Validate the value before the struct is built, and fail fast:
  ```rust
  if !ALLOWED_RISK_CLASSIFICATIONS.contains(&risk_classification) {
      return Err(AppError::BadRequest(format!(
          "invalid risk_classification '{risk_classification}'; expected one of: critical, high, medium, low"
      )))
      .context("validating advisory risk classification");
  }
  ```
  (Use whichever `AppError` variant and `.context()` form `common/src/error.rs` defines. The
  check is exact and case-sensitive, matching the set given in the task.)
- Set the field in the struct literal: `risk_classification: risk_classification.to_string(),`.
  `build_summary()` does no merge, bulk update or generic write after the struct is filled, so
  this assignment is the last write to the field (see self-review check 16).
- Update the doc comment on `build_summary()` to describe the new argument and the error it
  returns for an invalid value.

## Files to Create

### 3. `tests/api/advisory_summary.rs`

Integration tests that follow `tests/api/advisory.rs` (same test DB setup and `assert_eq!` style),
each with a `///` doc comment and `// Given / // When / // Then` sections:

- `build_summary_accepts_allowed_risk_classification`: parameterized over `critical`, `high`,
  `medium`, `low`. Use `rstest` `#[case]` if the project already uses it; otherwise loop over a
  data array in one test, since the project's existing patterns win. Asserts
  `assert_eq!(summary.risk_classification, case)` on the value, not just `is_ok()`.
- `build_summary_rejects_disallowed_risk_classification`: parameterized over `"severe"`, `""` and
  `"Critical"`. Asserts the result is `Err` and matches the expected `AppError` variant
  (`assert!(matches!(err, AppError::BadRequest(_)))`).
- No override or conflict test. `build_summary()` has no later write path that could replace the
  validated value, so check 16 does not need one.
- Register the file in the test crate if `tests/Cargo.toml` uses explicit `[[test]]` entries or a
  `mod` list. That registration is an out-of-scope file, so it goes to the user for approval in
  Step 9 check 1.

## Acceptance Criteria mapping (Step 8)

| Criterion | How it is satisfied |
|---|---|
| `build_summary()` rejects a `risk_classification` outside the allowed set | Check against `ALLOWED_RISK_CLASSIFICATIONS` before the struct is built; returns `AppError` with `.context()`; covered by the reject test |
| A summary built with a valid classification always carries that value | The field is assigned directly in the struct literal and nothing writes to it afterwards (check 16); covered by the parameterized accept test, which asserts the value |

## Verification (Step 9)

- Run the CI commands listed in `CONVENTIONS.md`. If none are listed, run `cargo fmt --check`,
  `cargo clippy --all-targets -- -D warnings` and `cargo check`.
- Resolve crates with `cargo metadata --no-deps --format-version 1`, then run
  `cargo test -p <fundamental-crate-name>` and `cargo test -p <tests-crate-name>`.
- Any failure stops the work and is reported to the user.

## Commit message

```
feat(advisory): add validated risk classification to advisory summary

Add a risk_classification field to AdvisorySummary and validate it in
AdvisoryService::build_summary() against the allowed set (critical, high,
medium, low). Invalid values return AppError with context before the
summary is returned. build_summary() does no later merge or generic
write, so the validated value cannot be overridden.

Add integration tests in tests/api/advisory_summary.rs covering each
allowed value and rejection of disallowed values.

Implements TC-9213
```
Committed with `git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" ...`.

## Steps 10–11 (simulated)

- Push `TC-9213`. Check for an `upstream` remote to detect a fork. Run `gh pr create --base main`
  with the body `Implements [TC-9213](<webUrl>)`. Add a `Closes owner/repo#N` line only if the
  GitHub Issue field (customfield_10747) is set.
- In Jira: set customfield_10875 to the PR URL as an ADF inlineCard; add a comment with the PR
  link, a summary and any deviations, ending with the implement-task footnote; move to In Review.
