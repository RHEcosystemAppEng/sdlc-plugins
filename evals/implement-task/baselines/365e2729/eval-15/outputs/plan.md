# Implementation Plan — TC-9212

**Summary**: Add validated data classification to the SBOM ingest payload builder
**Repository**: trustify-backend (Serena instance: `serena_backend`)
**Target Branch**: main → task branch `TC-9212`
**Mode**: Default flow (no Target PR, no Bookend Type)

## Pre-implementation steps (simulated)

- **Step 0**: Project Configuration validated: Repository Registry (trustify-backend / serena_backend), Jira Configuration (Project key TC, Cloud ID, Feature issue type ID 10142), and Code Intelligence (naming convention `mcp__<instance>__<tool>`) are all present.
- **Step 1**: Every required section is present (Repository, Target Branch, Description, Files to Modify, Files to Create, API Changes, Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies). No Target PR and no Bookend Type. The GitHub Issue field (customfield_10747) would be read. If it is empty, it is skipped.
- **Step 1.5**: Digest comment would be located and compared. It is not available in the eval, so the plan proceeds as if the digests match.
- **Step 2**: Dependencies: none.
- **Step 3**: Assign to current user, transition to In Progress (simulated, not executed).
- **Step 4**: Serena (`mcp__serena_backend__*`) would be used:
  - `get_symbols_overview` on `modules/fundamental/src/sbom/service/sbom.rs` and `modules/fundamental/src/sbom/model/details.rs`
  - `find_symbol("SbomService/build_ingest_payload", include_body=true)` to confirm the "write standardized fields, then merge `extra_fields` last" structure
  - `find_referencing_symbols` on `build_ingest_payload` to enumerate callers (ingestor `modules/ingestor/src/graph/sbom/mod.rs` likely) — the signature changes by adding a `data_classification` argument, so callers must be checked (see Scope notes)
  - `find_symbol("AppError")` in `common/src/error.rs` for the right variant (e.g. `AppError::BadRequest` / validation variant) and `.context()` usage
  - Siblings: `model/summary.rs` (SbomSummary), `advisory/model/details.rs`, `tests/api/sbom.rs`, `tests/api/advisory.rs`
  - `CONVENTIONS.md` at repo root: read and extract CI check commands (e.g. `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo check`) for Step 9
  - Symbol deduplication: grep the workspace for `data_classification`, `DataClassification`, `ALLOWED_CLASSIFICATIONS` before declaring anything new

### Discovered conventions (binding for Steps 6/7)
- Errors: `Result<T, AppError>` with `.context()` wrapping
- Models: plain serde structs with `#[derive(Clone, Debug, Serialize, Deserialize, ToSchema)]` in `model/`
- Tests: integration tests in `tests/api/` against real PostgreSQL test DB; `assert_eq!` on concrete values
- Naming: snake_case functions, `verb_noun`; test names `test_<behavior>` style

## Files to Modify

### 1. `modules/fundamental/src/sbom/model/details.rs`
- Add a documented enum for classification (if no existing definition is found by the dedup search):
  ```rust
  /// Data sensitivity classification attached to an SBOM ingest payload.
  #[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize, ToSchema)]
  #[serde(rename_all = "lowercase")]
  pub enum DataClassification { Public, Internal, Restricted }
  ```
  with `impl DataClassification { pub fn as_str(&self) -> &'static str }` and `impl FromStr` (documented) that returns an error for any value other than `public` / `internal` / `restricted`. The `FromStr` impl gives one validation point that both the service and the model use, so the allowed set is not duplicated.
- Add a documented field to `SbomDetails`:
  ```rust
  /// Data classification of the SBOM (`public`, `internal` or `restricted`).
  pub data_classification: Option<DataClassification>,
  ```
  It is `Option` so that existing SBOMs and existing constructors that have no classification keep working. Every place that constructs `SbomDetails` (found via `find_referencing_symbols`) gets `data_classification: None`, or the value when one is known.

### 2. `modules/fundamental/src/sbom/service/sbom.rs` — `SbomService::build_ingest_payload()`
- Add a `data_classification: &str` parameter. The existing `extra_fields` parameter keeps its name and type and is passed through unchanged, as the Implementation Notes require.
- At the top of the function, validate the value and return early on failure:
  ```rust
  let classification: DataClassification = data_classification
      .parse()
      .map_err(|_| AppError::BadRequest(format!("invalid data_classification: {data_classification}")))
      .context("validating SBOM ingest payload data_classification")?;
  ```
  The exact variant follows `common/src/error.rs`.
- Write the validated value into the standardized-field map: `payload.insert("data_classification", classification.as_str().into())`.
- **Protect the validated value from the later `extra_fields` merge.** This is the fix for the override path. The merge currently runs last, so a caller could pass `extra_fields = {"data_classification": "anything"}` and silently replace the validated value, or set it to null and drop it. Before merging, reject a conflicting key using the project's fail-fast error handling:
  ```rust
  if extra_fields.contains_key("data_classification") {
      return Err(AppError::BadRequest(
          "extra_fields must not override data_classification".into(),
      ))
      .context("merging extra_fields into SBOM ingest payload");
  }
  ```
  Rejecting the key, rather than quietly re-applying the value after the merge, makes the conflict visible to the caller. It also keeps the guarantee even if someone later reorders the statements in the function. The validated value is written by the standardized-field step, and nothing after that step can replace it.
- Doc comment on `build_ingest_payload` updated to describe the new parameter, the allowed values, and the two error cases (invalid value; conflicting `extra_fields` key).
- Callers of `build_ingest_payload` must pass the new argument. This is in scope only for the files listed above. Any caller outside the listed files (for example, ingestor code) is flagged for user approval in Step 9 scope containment and is not silently edited. If the user prefers to avoid touching other files, the parameter could instead take a default. The plan asks the user rather than guessing.

## Files to Create

### 3. `tests/api/sbom_ingest_payload.rs`
Integration tests that follow the `tests/api/sbom.rs` setup. Every test has a `///` doc comment. Non-trivial tests have `// Given / // When / // Then` sections.

1. `test_build_ingest_payload_accepts_allowed_classifications`: a parameterized `rstest` with cases `public`, `internal`, `restricted`, used only if the project already uses rstest. Otherwise it is one table-driven loop over the three values. Each case asserts `assert_eq!(payload["data_classification"], json!(<value>))`, which is a value-based assertion.
2. `test_build_ingest_payload_rejects_disallowed_classification`: passes `"secret"`, plus `""` and `"PUBLIC"` (case-sensitivity), and asserts that the call returns `Err` with the expected `AppError` variant and that no payload is produced.
3. `test_build_ingest_payload_extra_fields_cannot_override_classification`: builds with `data_classification = "restricted"` and `extra_fields = {"data_classification": "public", "other": "x"}`. It asserts the call is rejected with the expected `AppError`, so the validated value can never be replaced through the generic merge. This test exists because the Step 9 override-path check found a real later write (the `extra_fields` merge).
4. `test_build_ingest_payload_preserves_unrelated_extra_fields`: valid classification plus non-conflicting extra fields. It asserts both `payload["data_classification"] == "internal"` and `payload["other"] == "x"`. This is a regression check that the existing merge behavior still works for other keys.

Test module registration in `tests/Cargo.toml` or a test `mod` file may be needed if the crate lists test targets explicitly. That would be an out-of-scope file and is flagged in Step 9 for approval.

## Acceptance Criteria mapping
- Rejects a classification outside the allowed set: covered by the `FromStr` validation and test 2.
- A payload built with a valid classification always carries that value: covered by the early validated write plus the rejection of conflicting `extra_fields` keys, and by tests 1, 3 and 4.

## Commit message

```
feat(sbom): add validated data_classification to ingest payload

Add a data_classification field (public, internal, restricted) to
SbomService::build_ingest_payload() and SbomDetails. Invalid values are
rejected with AppError before the payload is built. Because extra_fields
is merged after the standardized fields, a conflicting
"data_classification" key in extra_fields is now rejected so the
validated value cannot be overridden or dropped.

Implements TC-9212
```
Committed with `git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)"`.

## PR (simulated)
`gh pr create --base main` (fork detection first). The body contains `Implements [TC-9212](<webUrl>)`, plus `Closes <owner>/<repo>#<n>` if the GitHub Issue field is set.

## Jira (simulated)
Set customfield_10875 to the PR URL as ADF inlineCard. Add a comment with the PR link, the summary, and the deviation note about rejecting the `extra_fields` conflict. Use the `implement-task` footnote. Transition to In Review.
