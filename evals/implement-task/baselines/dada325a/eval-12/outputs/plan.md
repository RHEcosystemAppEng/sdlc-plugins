# Implementation Plan — TC-9210: Add severity-sorted remediation list to SBOM risk report

Skill: `/sdlc-workflow:implement-task` (dry run: no repo edits, Jira, git, or Serena calls were made)

## Step 0 – Project Configuration validation

The mock CLAUDE.md passes this check:
- Repository Registry: `trustify-backend` → Serena instance `serena_backend`, path `./`
- Jira Configuration: Project key `TC`, Cloud ID, and Feature issue type ID `10142` are all present
  (Git PR field `customfield_10875`, GitHub Issue field `customfield_10747`)
- Code Intelligence: naming convention `mcp__<instance>__<tool>` is present. Limitation: rust-analyzer
  takes 30-60 seconds to index on first use.

## Step 1 – Parsed task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Target PR / Bookend Type | none (default flow) |
| Dependencies | none (Step 2 is a no-op) |
| Files to Modify | `modules/fundamental/src/sbom/service/sbom.rs`, `modules/fundamental/src/sbom/endpoints/get.rs` |
| Files to Create | `tests/api/sbom_remediation.rs` |
| GitHub Issue | read `customfield_10747`; if set, add `Closes <owner>/<repo>#<n>` to the PR body |

All required sections are present, so implementation can proceed.

Step 1.5 (digest check), Step 3 (assign the issue and move it to In Progress): simulated, not executed.

## Step 4 – Code understanding (planned Serena calls)

- `get_symbols_overview` on `sbom/service/sbom.rs` (find `SbomService`, how it fetches related advisories
  through `sbom_advisory` join) and on `sbom/endpoints/get.rs` (find the handler and response type).
- `find_symbol("SbomService/fetch*", include_body=true)` to read the existing advisory-fetching pattern,
  which the Implementation Notes say to follow.
- `find_symbol("SbomDetails")` in `sbom/model/details.rs` and `AdvisorySummary` in
  `advisory/model/summary.rs` to see the `severity` field type (`String` vs `Option<String>`).
- `find_referencing_symbols` on the get handler and on `SbomDetails` (backward compatibility).
- Siblings for conventions: `advisory/service/advisory.rs`, `advisory/endpoints/get.rs`,
  `tests/api/sbom.rs`, `tests/api/advisory.rs`.
- Read `CONVENTIONS.md` at the repo root and pull out its CI check commands (fmt, clippy, check, test).
- Docs to check: `README.md`, `docs/api.md` (REST API reference, since the response shape changes).

Conventions to follow: `Result<T, AppError>` with `.context()`; `model/ + service/ + endpoints/`
layout; tests in `tests/api/` against real PostgreSQL; `assert_eq!(resp.status(), StatusCode::OK)`.
Following the skill rules over sibling patterns, tests use value-based assertions and get doc comments.

## Handling of the `SEVERITY_ORDER` constant (key decision)

The full search log is in `symbol-search.md`. In short:

- **Search before declaring**: search the whole `modules/fundamental` crate for `SEVERITY_ORDER`
  and its variations (`severity_order`, `SeverityOrder`), plus the literal value
  `"critical", "high", ...`.
- **Found** in `modules/fundamental/src/advisory/service/advisory.rs`:
  `SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"]`.
- **Reuse it. Do not redeclare it.** `advisory` and `sbom` are in the same crate, so no new
  dependency is needed. AC #3 explicitly forbids a duplicate definition.
- Import: `use crate::advisory::service::advisory::SEVERITY_ORDER;`
- **Visibility**: if the constant (or the `service` module) is private, widen it to `pub(crate)`.
  That one-word change is in `advisory.rs`, which is **outside** Files to Modify, so I flag it in
  Step 9 scope containment and get explicit user approval before committing. Redeclaring the
  constant is never the fallback.
- **Sort weight** is the index in the slice. Comparison is case-insensitive because the constant
  is lowercase and advisories may store `"Critical"`/`"HIGH"`. Unknown or missing severities rank
  after `"none"` (`SEVERITY_ORDER.len()`), so they can't panic and don't jump ahead of known ones.
- **Stable ordering**: use `slice::sort_by_key`, which is stable in Rust, so advisories with the
  same severity keep their fetch order (this covers Test Requirement #3).

## Step 5 – Branch

```
git checkout main && git pull && git checkout -b TC-9210
```

## Step 6 – Changes per file

### 1. `modules/fundamental/src/sbom/service/sbom.rs` (modify)

- Add the import `use crate::advisory::service::advisory::SEVERITY_ORDER;`
- Add the new struct (doc-commented). It derives the same serde/utoipa traits used by sibling
  response models:
  ```rust
  /// A single remediation entry: an advisory affecting the SBOM, with its severity and fix version.
  #[derive(Clone, Debug, Serialize, Deserialize, PartialEq, Eq, ToSchema)]
  pub struct RemediationItem {
      pub advisory_id: String,
      pub severity: String,
      pub title: String,
      pub fix_version: Option<String>,
  }
  ```
  (`fix_version` is `Option` because not every advisory has a fix. The final types will match
  the advisory entity fields found in Step 4.)
- Add a private helper:
  ```rust
  /// Returns the sort rank of a severity string using `SEVERITY_ORDER` (lower = more severe).
  /// Unknown severities rank after all known ones.
  fn severity_rank(severity: &str) -> usize {
      SEVERITY_ORDER
          .iter()
          .position(|s| s.eq_ignore_ascii_case(severity))
          .unwrap_or(SEVERITY_ORDER.len())
  }
  ```
- Add a method to `SbomService`. It follows the existing related-advisory fetch pattern
  (join through `sbom_advisory`), returns `Result<Vec<RemediationItem>, AppError>` with `.context()`:
  ```rust
  /// Builds the remediation list for an SBOM, sorted by descending severity
  /// (Critical > High > Medium > Low > None). Ties keep their original order.
  pub async fn remediations(&self, sbom_id: Id, tx: &C) -> Result<Vec<RemediationItem>, AppError> {
      let advisories = /* existing related-advisory query pattern */ .context("fetching SBOM advisories")?;
      let mut items: Vec<RemediationItem> = advisories.into_iter().map(|a| RemediationItem {
          advisory_id: a.id.to_string(),
          severity: a.severity.clone().unwrap_or_default(),   // defensive: severity may be NULL
          title: a.title.clone().unwrap_or_default(),
          fix_version: a.fix_version.clone(),
      }).collect();
      items.sort_by_key(|i| severity_rank(&i.severity));     // stable sort
      Ok(items)
  }
  ```
- Unit tests in the existing `#[cfg(test)]` module (if one exists) for `severity_rank`: mixed case,
  unknown values, and `"none"` ranking last among the known values.

### 2. `modules/fundamental/src/sbom/endpoints/get.rs` (modify)

- In the GET `/api/v2/sbom/{id}` handler, call `service.remediations(id, &tx).await?` next to the
  existing details fetch.
- Add `remediations: Vec<RemediationItem>` to the response. Because `sbom/model/details.rs`
  (`SbomDetails`) is **not** in Files to Modify, the in-scope approach is a response wrapper in
  `get.rs`, with `#[serde(flatten)]` so the existing JSON fields stay unchanged (backward compatible):
  ```rust
  /// SBOM details response extended with a severity-sorted remediation list.
  #[derive(Serialize, ToSchema)]
  pub struct SbomDetailsResponse {
      #[serde(flatten)]
      pub details: SbomDetails,
      pub remediations: Vec<RemediationItem>,
  }
  ```
  Update the handler's return type and its `#[utoipa::path]` response annotation.
  - Scope flag: adding the field directly to `SbomDetails` in `model/details.rs` would match
    convention better. I'd raise this with the user in Step 4/9 and only touch that file with
    their approval.
- An empty advisory set gives `"remediations": []`, never null or missing.

### 3. `tests/api/sbom_remediation.rs` (create)

These follow the patterns in `tests/api/sbom.rs` (test DB setup, ingest fixture, HTTP call,
`assert_eq!(resp.status(), StatusCode::OK)`). Each test gets a `///` doc comment and
Given/When/Then comments. Assertions check values, not just counts.

- `/// Verifies remediations are sorted Critical > High > Medium > Low > None.`
  `test_remediations_sorted_by_severity`: ingest an SBOM linked to advisories inserted in the
  order low, critical, none, high, medium. Assert that the `severity` sequence equals
  `["critical","high","medium","low","none"]` and that each `advisory_id` is in the expected position.
- `/// Verifies an SBOM with no advisories returns an empty remediations list.`
  `test_remediations_empty_when_no_advisories`: assert that `body["remediations"] == json!([])`.
- `/// Verifies advisories of equal severity keep a stable relative order.`
  `test_remediations_stable_for_equal_severity`: insert three `high` advisories (A, B, C) plus one
  critical. Assert the critical comes first, then the `advisory_id` order `[A, B, C]` is unchanged.
- I won't add parameterization here: the three tests differ in setup and assertions (Meszaros
  heuristic), and the sibling tests don't use `rstest`.
- Registration: if `tests/Cargo.toml` uses explicit `[[test]]` entries or a `tests/api/main.rs`
  `mod` list, the new file has to be registered there. That file is out of scope, so I'd flag
  it in Step 9 for approval.

### Documentation impact

The `GET /api/v2/sbom/{id}` response gains a `remediations` field. The task has no Documentation
Updates section and `docs/api.md` is not in scope, so I'd flag `docs/api.md` (and the regenerated
OpenAPI spec, if `CONVENTIONS.md` lists a codegen command) in Step 9 rather than editing them silently.

## Steps 7–8 – Tests and acceptance criteria

Run `cargo test -p trustify-module-fundamental` and the integration tests crate. The crate name
is resolved through `cargo metadata`.

| AC | How it is satisfied |
|---|---|
| `remediations` field in GET /api/v2/sbom/{id} | `SbomDetailsResponse` in `get.rs` |
| Sorted Critical > High > Medium > Low > None | `sort_by_key(severity_rank)` |
| Uses existing `SEVERITY_ORDER`, no duplicate | `use crate::advisory::service::advisory::SEVERITY_ORDER`, no new constant |
| RemediationItem has advisory_id, severity, title, fix_version | struct in `sbom.rs` |

## Step 9 – Self-verification

- **Scope containment**: expected diff is `sbom/service/sbom.rs`, `sbom/endpoints/get.rs`, and
  `tests/api/sbom_remediation.rs`. Files that may need changes and require user approval:
  `advisory/service/advisory.rs` (only if the constant must become `pub(crate)`),
  `sbom/model/details.rs` (optional convention alignment), test registration file, `docs/api.md`, OpenAPI spec.
- **Duplication check**: grep `"critical"` under `modules/fundamental`. Only `advisory.rs` should match.
- **CI checks** from `CONVENTIONS.md` (e.g. `cargo fmt --check`, `cargo clippy -- -D warnings`,
  `cargo test`): any failure is a hard stop.
- **Data flow**: DB (`sbom_advisory` join → `advisory`) → `SbomService::remediations` (map + sort)
  → `get.rs` handler → JSON `remediations`. Every stage connects.
- **Contract and sibling parity**: the new method uses the same error handling and transaction
  parameter as the other `SbomService` methods. The response struct derives the same traits as
  sibling models.
- **Sensitive-pattern check**: run on the staged diff.

## Steps 10–11 – Commit, PR, Jira (not executed)

```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(sbom): add severity-sorted remediation list to SBOM details

Reuses the existing SEVERITY_ORDER constant from the advisory module
(same crate) instead of redeclaring it.

Implements TC-9210"
gh pr create --base main ...   # body: "Implements [TC-9210](<webUrl>)" (+ "Closes ..." if GitHub issue set)
```

Jira steps: set `customfield_10875` to the PR URL (ADF inlineCard), add a comment with a summary
and any deviations (including approved out-of-scope edits) plus the `implement-task` footnote,
then move the issue to **In Review**.
