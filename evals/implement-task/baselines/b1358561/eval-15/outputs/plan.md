# Implementation Plan — TC-9212

**Summary**: Add validated data classification to the SBOM ingest payload builder
**Repository**: trustify-backend (Serena instance `serena_backend`, path `./`)
**Target Branch**: `main`
**Mode**: **default** (no Target PR, no Bookend Type). Steps 1–11 run: branch `TC-9212` from `main`, open a PR against `main`, set the PR field, comment, and move to In Review.

## Step 0 – Project Configuration check

`claude-md-mock.md` has all three required sections:
- Repository Registry: one entry (`trustify-backend`, `serena_backend`, `./`)
- Jira Configuration: Project key `TC`, Cloud ID, Feature issue type ID `10142` (also the PR field `customfield_10875` and the GitHub Issue field `customfield_10747`)
- Code Intelligence: uses the `mcp__<serena-instance>__<tool>` naming convention

Result: PASS, so execution continues.

## Step 1 – Parsed task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Files to Modify | `modules/fundamental/src/sbom/service/sbom.rs`, `modules/fundamental/src/sbom/model/details.rs` |
| Files to Create | `tests/api/sbom_ingest_payload.rs` |
| API Changes | none |
| Dependencies | none |
| Target PR / Bookend Type | absent, so mode is default |
| GitHub Issue (customfield_10747) | read from the issue. If it is empty, skip it. If it is set, add `Closes <owner>/<repo>#<n>` to the PR body only. |

All required sections are present, so there is nothing to ask the user.

## Steps 1.5 / 2 / 3 – Jira (not executed in this eval)
- 1.5: Fetch the comments and find the `[sdlc-workflow] Description digest:` comment. If there is none, log a warning and continue. If there is one, compare it with `scripts/sha256-digest.py`.
- 2: No dependencies, so there is nothing to check.
- 3: Look up the current user, assign the task to them, and move it to In Progress.

## Step 4 – Understand the code (planned Serena calls)

- `mcp__serena_backend__get_symbols_overview` on `sbom/service/sbom.rs` and `sbom/model/details.rs`.
- `mcp__serena_backend__find_symbol("SbomService/build_ingest_payload", include_body=true)`. This confirms the structure described in the Implementation Notes:
  1. standardized fields are written into a map (`serde_json::Map<String, Value>`);
  2. **`extra_fields` is merged into the same map at the end**, so it runs after every standardized write.
- `find_symbol("SbomDetails", include_body=true)` and `find_referencing_symbols("SbomDetails")`. This finds every struct-literal construction that must also set the new field.
- `find_referencing_symbols("SbomService/build_ingest_payload")`. Callers must keep compiling. The `extra_fields` parameter stays as it is and keeps its name.
- `find_symbol("AppError")` in `common/src/error.rs`, plus `search_for_pattern("\.context\(")`. This shows which `AppError` variant to use for invalid input (for example `AppError::BadRequest` or `AppError::Validation`) and how `.context()` is attached.
- Reuse search: `search_for_pattern("classification|Classification|ALLOWED_")` across `common/` and `modules/`. If an allowed-value enum or validator already exists, reuse it. The fixture doesn't show one, so the plan assumes none exists.
- `CONVENTIONS.md` at the repo root: read it, take the CI-check commands for check 14, and note any codegen commands (for example OpenAPI generation).
- Docs to check for currency: `README.md`, `docs/api.md`, `docs/architecture.md`.

**Conventions from siblings** (`sbom/model/summary.rs`, `advisory/model/summary.rs`, `advisory/service/advisory.rs`, `tests/api/sbom.rs`):
- Errors: `Result<T, AppError>` with `.context(...)`.
- Models: `#[derive(Clone, Debug, Serialize, Deserialize, ToSchema)]` structs with `///` doc comments. Enums use `#[serde(rename_all = "lowercase")]`.
- Naming: `snake_case` functions in a `verb_noun` style and `PascalCase` types.
- Tests: integration tests in `tests/api/` against a real PostgreSQL test DB. HTTP tests assert with `assert_eq!(resp.status(), StatusCode::OK)`. Value assertions use `assert_eq!`.
- Conflict noted: sibling tests have no doc comments. The skill rule wins, so every new test gets a `///` doc comment and given/when/then comments.

## Step 5 – Branch
```
git checkout main
git pull
git checkout -b TC-9212
```

## Step 6 – Changes

### 1. `modules/fundamental/src/sbom/model/details.rs` (modify)

- Add a closed enum that represents the allowed set, so invalid values can't be represented once they are parsed:
  ```rust
  /// Data classification level of an SBOM; only these three values are valid.
  #[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize, ToSchema)]
  #[serde(rename_all = "lowercase")]
  pub enum DataClassification { Public, Internal, Restricted }

  impl DataClassification {
      /// Wire value written to the ingest payload.
      pub fn as_str(&self) -> &'static str { /* "public" | "internal" | "restricted" */ }
  }

  impl FromStr for DataClassification {
      type Err = AppError;
      /// Parses a classification string, rejecting anything outside the allowed set.
      fn from_str(s: &str) -> Result<Self, AppError> { /* match exact lowercase; else Err(AppError::BadRequest(..)) */ }
  }
  ```
  The match is exact and case-sensitive, so `"Public"`, `"secret"` and `""` are all rejected. This is fail-closed.
- Add the field to `SbomDetails`:
  ```rust
  /// Data classification of the SBOM, validated against the allowed set.
  pub data_classification: DataClassification,
  ```
  If `find_referencing_symbols` shows existing constructors that have no classification source, use `Option<DataClassification>` instead. Each construction site outside `details.rs` and `sbom.rs` becomes a Step 9 scope flag that needs user approval.
- The enum lives in `details.rs` because that file is in scope and is the model file that uses it. It is declared here because no shared definition exists (Reuse rule 3).

### 2. `modules/fundamental/src/sbom/service/sbom.rs` (modify) — `SbomService::build_ingest_payload()`

- Validate the classification before anything is written. The raw value comes from the caller or `SbomDetails` and is parsed with `DataClassification::from_str(raw).context("invalid data_classification for SBOM ingest payload")?`. An invalid value returns `AppError` and nothing is sent. This satisfies AC1.
- Write the standardized fields as today, then insert `"data_classification" => Value::String(classification.as_str().into())`.
- **Close the override path.** `extra_fields` is merged last, so a caller-supplied `"data_classification"` key would silently replace the validated value. That would break AC2 ("a valid classification always carries that value") and could carry an unvalidated string into the payload. Fix, using the project's fail-fast pattern:
  ```rust
  /// Keys owned by the validated payload builder that extra_fields may not override.
  const RESERVED_PAYLOAD_KEYS: &[&str] = &["data_classification"];
  ...
  if let Some(key) = extra_fields.keys().find(|k| RESERVED_PAYLOAD_KEYS.contains(&k.as_str())) {
      return Err(AppError::BadRequest(format!("extra_fields may not override reserved key `{key}`")))
          .context("conflicting extra_fields key in SBOM ingest payload");
  }
  ```
  This check runs before the merge. The merge itself does not change, and `extra_fields` keeps its name and type, so existing callers still compile and behave the same unless they send the reserved key.
  - Why reject instead of re-applying the value after the merge: a silent re-apply would hide a caller's mistaken intent. Rejecting is fail-fast and does not depend on statements staying in a particular order. This choice and its reason go in the commit body.
  - Defense in depth: after the merge, add `debug_assert_eq!(payload.get("data_classification"), Some(&Value::String(classification.as_str().into())))`.
- Add a `///` doc comment update on `build_ingest_payload` that describes the new validation and the reserved-key rule.

### 3. `tests/api/sbom_ingest_payload.rs` (create)

Each test has a `///` doc comment and given/when/then comments. Assertions check values, not lengths.

- `build_ingest_payload_accepts_allowed_classification`: parameterized with `rstest` over `public`, `internal` and `restricted`, but only if `rstest` is already a dev-dependency (Step 4 checks this). Otherwise use a loop over a table, as sibling tests do. Each case asserts `assert_eq!(payload["data_classification"], json!(value))`. This covers TR1 and AC2.
- `build_ingest_payload_rejects_disallowed_classification`: parameterized over `"secret"`, `"Public"` and `""`. Each case asserts `is_err()` and checks the error variant or message. This covers TR1/TR2 and AC1.
- `build_ingest_payload_rejects_extra_fields_override_of_classification`: valid `internal` plus `extra_fields = {"data_classification": "public"}`. Asserts an error and that no payload is produced. This is the conflict test that check 16 requires.
- `build_ingest_payload_preserves_unrelated_extra_fields`: valid classification plus `extra_fields = {"source": "scanner-x"}`. Asserts `payload["source"] == "scanner-x"` and `payload["data_classification"] == "restricted"`. This shows existing passthrough still works.

Possible registration need: `tests/Cargo.toml` (or `tests/api/main.rs` / `mod` list) may need an entry for the new test file. That file is not listed in the task, so it becomes a Step 9 scope flag that needs user approval before commit.

### Documentation impact
The task has no Documentation Updates section and no public HTTP API changes (API Changes: none). No docs are in Files to Modify, so no doc edits are made. If `docs/api.md` or `docs/architecture.md` describes the ingest payload fields, it is flagged under check 6 for user approval and not edited without it.

## Step 7 – Run tests
`cargo test -p <crate>` for the crates that own the modified files, resolved with `cargo metadata` (see self-review check 15). Also run the test package that contains `tests/api/`.

## Step 8 – Acceptance criteria
- AC1 (reject a classification outside the set): `FromStr` plus the `?` in the builder. Covered by the rejection test.
- AC2 (a valid classification always carries its value): the builder writes it, and the reserved-key rejection means `extra_fields` cannot replace it. Covered by the accept tests and the override-conflict test.

## Step 10 – Commit message

```
feat(sbom): add validated data_classification to ingest payload

Add a DataClassification enum (public | internal | restricted) to the
SBOM model and an SbomDetails.data_classification field. 
SbomService::build_ingest_payload() now parses the classification and
returns AppError with context for any value outside the allowed set,
before the payload is built or sent.

Because extra_fields is merged into the payload last, a caller-supplied
"data_classification" key could silently replace the validated value.
The builder now rejects extra_fields containing reserved keys
(fail-fast) instead of relying on write order. Other extra_fields keys
are merged unchanged; the parameter name and type are untouched.

The enum is declared in sbom/model/details.rs since no shared
classification type exists in the codebase.

Implements TC-9212
```
Run with `git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "..."`.

PR: `gh pr create --base main` (if an `upstream` remote exists, use the fork form `-R <upstream> --head <fork-owner>:TC-9212`). The body includes `Implements [TC-9212](<webUrl>)`, plus `Closes owner/repo#N` if the GitHub Issue field is set.

## Step 11 – Jira (not executed)
Set `customfield_10875` to the PR URL in ADF `inlineCard` form. Post a comment with the PR link, a summary, and the deviation (the reserved-key rejection for `extra_fields`), ending with the implement-task footnote. Move the issue to In Review.
