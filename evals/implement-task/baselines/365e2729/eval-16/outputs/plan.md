# Implementation Plan — TC-9213

**Summary**: Add validated risk classification to the advisory summary builder
**Repository**: trustify-backend (Serena instance: `serena_backend`)
**Target Branch**: main
**Task branch**: `TC-9213` (created from `main` after `git checkout main && git pull`)

## Pre-implementation steps (simulated)

- **Step 0 – Project Configuration**: mock CLAUDE.md has Repository Registry (trustify-backend / serena_backend / `./`), Jira Configuration (Project key TC, Cloud ID, Feature issue type ID 10142), and Code Intelligence with the `mcp__<serena-instance>__<tool>` naming convention. Validation passes.
- **Step 1 – Parse task**: every required section is there: Repository, Target Branch, Description, Files to Modify, Files to Create, API Changes (none), Implementation Notes, Acceptance Criteria, Test Requirements and Dependencies. The task has no Target PR and no Bookend Type, so it uses the default flow. The GitHub Issue field (customfield_10747) would be read from the issue. If it is empty, the step is skipped.
- **Step 1.5 – Digest check**: would fetch comments and compare the `[sdlc-workflow] Description digest:` value. This is not run in the eval.
- **Step 2 – Dependencies**: "None", so nothing to check.
- **Step 3 – Jira**: would assign the issue to the current user and move it to In Progress. This is not run in the eval.
- **Step 4 – Understand the code** (via `mcp__serena_backend__*`):
  - `get_symbols_overview` on `advisory/service/advisory.rs` and `advisory/model/summary.rs`.
  - `find_symbol("AdvisoryService/build_summary", include_body=true)` to confirm what the Implementation Notes say: the struct is filled in field by field and returned, and nothing is merged, bulk-updated or written generically after that.
  - `find_symbol("AdvisorySummary", include_body=true)` to see the derives, serde attributes and how the existing `severity` field is typed.
  - `find_referencing_symbols` on `AdvisorySummary` and `build_summary` to find every struct literal and caller that the new field and new input would affect.
  - `find_symbol("AppError")` in `common/src/error.rs` to find the right variant for a validation failure (for example `BadRequest`) and how `.context()` is used.
  - Siblings for conventions: `sbom/model/summary.rs` (`SbomSummary`), `package/model/summary.rs` (`PackageSummary`, which has a `license` field), and `sbom/service/sbom.rs`. Test siblings: `tests/api/advisory.rs` and `tests/api/sbom.rs`.
  - Symbol deduplication: search the `fundamental` crate and `common` for `RiskClassification`, `risk_classification`, `RISK_LEVELS` and `ALLOWED_RISK`, and for an existing severity enum whose values could be reused. If one with the same value set exists, reuse it instead of declaring a new one.
  - Read `CONVENTIONS.md` at the repo root to get the CI check commands (for example `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo check`) and any code generation commands (for example OpenAPI spec generation).
  - Docs: `README.md`, `docs/api.md`, `CONVENTIONS.md`.

### Discovered conventions (binding for Steps 6–7)

- Error handling: return `Result<T, AppError>` and wrap errors with `.context()`.
- Model types: plain structs in `model/summary.rs` deriving serde and utoipa (`ToSchema`) like their siblings, with fields in snake_case.
- Naming: functions use `verb_noun`, types use PascalCase.
- Tests: integration tests in `tests/api/` against a real PostgreSQL test DB, asserting with `assert_eq!`.

## Files to Modify

### 1. `modules/fundamental/src/advisory/model/summary.rs`

- Add the new field to `AdvisorySummary`, with a doc comment:
  ```rust
  /// Validated risk classification for the advisory: one of `critical`, `high`, `medium`, `low`.
  pub risk_classification: RiskClassification,
  ```
- If Step 4 finds no existing type for this value set, add a doc-commented `RiskClassification` enum in this same model file:
  ```rust
  /// Allowed risk classification levels for an advisory summary.
  #[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize, ToSchema)]
  #[serde(rename_all = "lowercase")]
  pub enum RiskClassification { Critical, High, Medium, Low }
  ```
  It also gets a doc-commented `impl FromStr for RiskClassification` (or `TryFrom<&str>`) that accepts exactly `critical`, `high`, `medium` and `low`. Any other string returns an error. The allowed set lives in one place, the type itself, so it is not repeated as a string list anywhere else.
- If the project keeps model fields as `String` (for example, if `severity` is a `String`), keep the field as `String` to match siblings. In that case the validation helper in the service checks it against a single `const ALLOWED_RISK_CLASSIFICATIONS: [&str; 4]`.
- Derives and serde attributes match the existing `AdvisorySummary` fields.

### 2. `modules/fundamental/src/advisory/service/advisory.rs`

- Add a `risk_classification: &str` input to `AdvisoryService::build_summary()`. Its exact form (direct parameter or a field on an existing input struct) follows the current signature found in Step 4.
- Validate it before the struct is populated:
  ```rust
  let risk_classification = RiskClassification::from_str(risk_classification)
      .map_err(|_| AppError::BadRequest(format!("invalid risk_classification '{risk_classification}'")))
      .context("validating advisory risk_classification")?;
  ```
  The variant and error-message style follow `common/src/error.rs`.
- Assign the validated value in the field-by-field population of `AdvisorySummary`: `risk_classification,`.
- Leave the rest unchanged. The struct is still returned directly, with no merge or override step after it.
- Update the `build_summary` doc comment to mention the new validated input and its error case.
- Update any callers of `build_summary` that `find_referencing_symbols` reports. If a caller is outside the listed files (for example an endpoint), flag it under Step 9 scope containment instead of editing it without approval.

## Files to Create

### 3. `tests/api/advisory_summary.rs`

Integration tests that follow the `tests/api/advisory.rs` setup (test DB fixture, `AdvisoryService` construction):

- `build_summary_accepts_each_allowed_classification`: covers the four allowed values. The project uses `rstest`, if Step 4 confirms that, so this is a parameterized case (`#[case("critical", RiskClassification::Critical)]` and so on). Without `rstest` it is a table-driven loop. Each case asserts `assert_eq!(summary.risk_classification, expected)`, checking the value itself and not just that the call succeeded.
- `build_summary_rejects_disallowed_classification`: passes something like `"severe"` (plus `""` and `"CRITICAL"` if matching is case-sensitive) and asserts the result is `Err` with the expected `AppError` variant.
- Every test function gets a `///` doc comment and `// Given` / `// When` / `// Then` sections.
- **No override-conflict test.** `build_summary()` has no generic merge, extra-field map, or patch path after the assignment, so a generic override has no way to replace the validated value. Under the skill's rule, no conflict test is required, and no test seam is added for a conflict the function cannot express.
- Register the new test file the same way the existing `tests/api/*.rs` files are registered (for example a `mod advisory_summary;` entry or a `[[test]]` target in `tests/Cargo.toml`, depending on the current layout). If registering it means editing a file outside the listed scope, flag that in Step 9.

## API Changes

None. If `AdvisorySummary` is serialized in an existing endpoint response, the new field shows up there. If that happens, the OpenAPI generation command from CONVENTIONS.md would be run in Step 9, and any regenerated spec would be flagged and committed with the change.

## Acceptance Criteria mapping

| Criterion | Satisfied by |
|---|---|
| `build_summary()` rejects a `risk_classification` outside the allowed set | Validation through `RiskClassification::from_str` returns `AppError` with `.context()` before the struct is built; covered by `build_summary_rejects_disallowed_classification` |
| A summary built with a valid classification always carries that value | The validated value is assigned in the struct literal and the struct is returned with no later write path; the parameterized test asserts the exact value for all four classifications |

## Commit message

```
feat(advisory): add validated risk classification to advisory summary

Add a risk_classification field to AdvisorySummary and validate it in
AdvisoryService::build_summary(). Only critical, high, medium and low
are accepted; any other value is rejected with AppError before the
summary is returned. Add integration tests covering each allowed value
and a disallowed value.

Implements TC-9213
```

Command: `git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "<message above>"`

## PR (Step 10, simulated)

- No `upstream` remote is assumed, so the command is `gh pr create --base main`.
- The PR body includes `Implements [TC-9213](<webUrl>)`, plus `Closes <owner>/<repo>#<n>` if the GitHub Issue field is set.

## Jira update (Step 11, simulated)

- Set customfield_10875 to the PR URL using ADF `inlineCard`.
- Add a comment with the PR link, a summary of the changes and any deviations, ending with the implement-task footnote.
- Move the issue to In Review.
