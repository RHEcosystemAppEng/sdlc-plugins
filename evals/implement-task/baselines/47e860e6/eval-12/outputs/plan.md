# Implementation Plan — TC-9210: Add severity-sorted remediation list to SBOM risk report

Simulated run of `/sdlc-workflow:implement-task TC-9210`. No repository files were
changed and no external tools (Jira, git, Serena, gh) were called. Each step below
describes what would happen.

## Step 0 — Project Configuration validation

`claude-md-mock.md` contains everything required:
- Repository Registry: `trustify-backend` → Serena instance `serena_backend`, path `./`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID 10142,
  Git PR field `customfield_10875`, GitHub Issue field `customfield_10747`
- Code Intelligence: naming convention `mcp__<instance>__<tool>`. Limitation:
  rust-analyzer can take 30–60 seconds to index on first use.

Result: PASS. Execution continues.

## Step 1 — Parse the task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Files to Modify | `modules/fundamental/src/sbom/service/sbom.rs`, `modules/fundamental/src/sbom/endpoints/get.rs` |
| Files to Create | `tests/api/sbom_remediation.rs` |
| Target PR / Bookend Type | none, so the default flow applies |
| Dependencies | None |
| GitHub Issue (`customfield_10747`) | would be read from the issue. If it is set, `Closes owner/repo#N` goes in the PR body |

Every required section is present, so there is no need to stop for clarification.

## Step 1.5 / 2 / 3 — Integrity, dependencies, Jira

- Step 1.5: fetch comments, find the `[sdlc-workflow] Description digest:` comment,
  and compare it against the digest computed by `scripts/sha256-digest.py`. If no
  digest comment exists, log a warning and continue.
- Step 2: there are no dependencies, so nothing to check.
- Step 3: `jira.user_info()`, then assign TC-9210 to the current user, then transition
  it to **In Progress**.

## Step 4 — Understand the code (Serena `serena_backend`)

- `get_symbols_overview` on `sbom/service/sbom.rs` and `sbom/endpoints/get.rs`.
- `find_symbol("SbomService", include_body=true)`. Read the existing method that
  fetches related advisories through the `sbom_advisory` join (named in the
  Implementation Notes as the pattern to follow).
- `find_symbol` on the `get` handler in `get.rs` and on `SbomDetails`
  (`sbom/model/details.rs`) to learn the current response shape.
- `find_symbol("AdvisorySummary")` (`advisory/model/summary.rs`) to confirm the
  `severity` field's type and nullability, along with the id, title and fix-version fields.
- `find_referencing_symbols` on the `get` handler and `SbomService` methods I touch,
  to check backward compatibility.
- **Symbol deduplication search for `SEVERITY_ORDER`.** The full analysis is in
  `symbol-search.md`. The constant was found in
  `modules/fundamental/src/advisory/service/advisory.rs`.
- Read `CONVENTIONS.md` at the repo root and extract CI check commands (fmt, clippy,
  check, test) and any OpenAPI generation command.
- Sibling conventions, taken from `advisory/service/advisory.rs`,
  `advisory/endpoints/get.rs`, `tests/api/sbom.rs` and `tests/api/advisory.rs`:
  - Handlers return `Result<T, AppError>` and wrap errors with `.context()`.
  - Each module uses the `model/ + service/ + endpoints/` structure.
  - Tests are integration tests against real PostgreSQL and use
    `assert_eq!(resp.status(), StatusCode::OK)`.
  - Naming follows `verb_noun` in snake_case.
- Docs that might need updating: `README.md`, `docs/api.md` (REST API reference),
  and the OpenAPI spec if one is generated.

## How SEVERITY_ORDER is handled (central decision)

**Reuse the existing constant. Do not redeclare it.**

- **Location:** `modules/fundamental/src/advisory/service/advisory.rs`
  (`SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"]`).
- **Why reuse is correct:** the source and target are in the same crate
  (`modules/fundamental`), so the dependency already exists and no `Cargo.toml` change
  is needed. AC 3 also forbids a duplicate definition.
- **Import in `sbom.rs`:**
  ```rust
  use crate::advisory::service::advisory::SEVERITY_ORDER;
  ```
- **If the constant turns out to be private:** change it to
  `pub(crate) const SEVERITY_ORDER` in `advisory.rs`. That is a one-line visibility
  change, using the narrowest visibility that works. `advisory.rs` is **not** in Files
  to Modify, so the change is **flagged in Step 9's scope check for explicit user
  approval** and is not applied silently. If the user refuses, I stop and ask. I do not
  fall back to a duplicate definition.
- **No hard-coded severity strings anywhere in the new code.** The rank is always
  derived from the constant's array position.
- The commit body and PR description record the decision: "Reuses `SEVERITY_ORDER`
  from `advisory::service::advisory` (same crate) instead of redeclaring it."

## Step 5 — Branch

```
git checkout main && git pull && git checkout -b TC-9210
```

## Step 6 — Changes per file

### 1. `modules/fundamental/src/sbom/service/sbom.rs` (modify)

- Add `use crate::advisory::service::advisory::SEVERITY_ORDER;`.
- Add a new documented struct:
  ```rust
  /// A single remediation entry for an SBOM, derived from an affecting advisory.
  #[derive(Clone, Debug, Serialize, Deserialize, PartialEq, Eq, ToSchema)]
  pub struct RemediationItem {
      pub advisory_id: String,
      pub severity: String,
      pub title: String,
      pub fix_version: Option<String>,
  }
  ```
  The derives follow sibling model structs (serde, plus `utoipa::ToSchema` if siblings
  use it). `RemediationItem` was searched for and does not exist (see `symbol-search.md`).
- Add a private rank helper built on the reused constant:
  ```rust
  /// Returns the sort rank of a severity string based on `SEVERITY_ORDER`;
  /// unknown or missing severities sort after "none".
  fn severity_rank(severity: &str) -> usize {
      SEVERITY_ORDER
          .iter()
          .position(|s| s.eq_ignore_ascii_case(severity))
          .unwrap_or(SEVERITY_ORDER.len())
  }
  ```
  If the advisory service already has an equivalent helper, reuse that instead.
- Add a method on `SbomService`, following the existing related-advisory fetch pattern
  (same `ConnectionTrait` / transaction parameter style and `.context()` error wrapping):
  ```rust
  /// Builds the remediation list for an SBOM, sorted by descending severity
  /// (Critical > High > Medium > Low > None) using `SEVERITY_ORDER`.
  pub async fn fetch_remediations<C: ConnectionTrait>(&self, sbom_id: Id, connection: &C)
      -> Result<Vec<RemediationItem>, Error>
  ```
  - Fetch the advisories linked to the SBOM using the existing pattern
    (the `sbom_advisory` join).
  - Map each advisory to a `RemediationItem`, guarding defensively against null or
    missing data: `severity.unwrap_or_default()`, `title.unwrap_or_default()`, and
    `fix_version` kept as an `Option`.
  - Sort with `items.sort_by_key(|i| severity_rank(&i.severity))`. `sort_by_key` is a
    **stable** sort, so advisories with the same severity keep their fetch order (Test
    Requirement 3). If the fetch order is not deterministic, add a secondary
    `ORDER BY advisory id` in the query so the base order is stable.
  - If there are no advisories, return an empty `Vec`.

### 2. `modules/fundamental/src/sbom/endpoints/get.rs` (modify)

- After fetching the SBOM details, call `service.fetch_remediations(id, &tx).await`
  and add `.context(...)` the same way sibling handlers do.
- Add a `remediations` field to the response for `GET /api/v2/sbom/{id}`. To stay
  within scope, define a documented response wrapper in `get.rs`:
  ```rust
  /// SBOM details response including the severity-sorted remediation list.
  #[derive(Serialize, ToSchema)]
  pub struct SbomDetailsResponse {
      #[serde(flatten)]
      pub details: SbomDetails,
      pub remediations: Vec<RemediationItem>,
  }
  ```
  The existing JSON fields stay the same and `remediations` is added alongside them,
  so the change is backward compatible. Update the handler's `utoipa` response
  annotation if one exists.
- Alternative (flagged, not applied): add `remediations` directly to `SbomDetails` in
  `sbom/model/details.rs`, and move `RemediationItem` into `sbom/model/`. That fits the
  module pattern better but touches a file outside Files to Modify, so it would only
  be done with user approval.

### 3. `tests/api/sbom_remediation.rs` (create)

Each test gets a `///` doc comment and Given/When/Then sections. Assertions check
values, not just lengths:

1. `/// Verifies remediations are sorted Critical > High > Medium > Low > None.`
   `test_remediations_sorted_by_severity`. Ingest an SBOM linked to advisories with
   severities inserted in a scrambled order (low, critical, none, high, medium). Assert
   status `OK` and
   `assert_eq!(severities, vec!["critical","high","medium","low","none"])`. Also assert
   the `advisory_id` order.
2. `/// Verifies an SBOM with no advisories returns an empty remediation list.`
   `test_remediations_empty_when_no_advisories`. Assert status `OK` and
   `assert_eq!(body["remediations"], json!([]))`.
3. `/// Verifies advisories with equal severity keep a stable relative order.`
   `test_remediations_stable_for_equal_severity`. Use several "high" advisories plus one
   "critical". Assert the critical one comes first, then the high ones as an exact
   `advisory_id` sequence in insertion/id order.
4. Optional: check that each item has `advisory_id`, `severity`, `title` and
   `fix_version` with the expected values (AC 4).

Tests 1 and 3 have different setups and assertions, so they stay as separate tests,
following the Meszaros heuristic. The sibling tests do not use `rstest`, so I do not
introduce it.

- Register the file with the test harness if `tests/` needs it, for example a
  `[[test]]` entry in `tests/Cargo.toml` or a `mod sbom_remediation;` in the harness
  root. If registration requires editing a file not listed in the task, flag it in
  Step 9.
- Run `cargo test -p <tests crate>` and `cargo test -p fundamental`. The crate names
  come from `cargo metadata --no-deps --format-version 1`.

### Documentation

If `docs/api.md` documents `GET /api/v2/sbom/{id}`, add the `remediations` field to it.
Regenerate the OpenAPI spec if `CONVENTIONS.md` lists a generation command. Both are
scoped doc updates and are reported in Step 9.

## Step 7 / 8 — Tests and acceptance criteria

| AC | How it is satisfied |
|---|---|
| `remediations` field in GET /api/v2/sbom/{id} | `SbomDetailsResponse.remediations` in get.rs. Covered by tests 1 and 2 |
| Sorted Critical > High > Medium > Low > None | `sort_by_key(severity_rank)` over `SEVERITY_ORDER`. Covered by test 1 |
| Uses existing `SEVERITY_ORDER`, no duplicate | `use crate::advisory::service::advisory::SEVERITY_ORDER;`. Step 9 duplication grep confirms exactly one definition |
| RemediationItem has advisory_id, severity, title, fix_version | struct in sbom.rs. Covered by test 4 |

## Step 9 — Self-verification

- **Scope containment:** expected diff is `sbom/service/sbom.rs`, `sbom/endpoints/get.rs`
  and `tests/api/sbom_remediation.rs`. Possible out-of-scope items, each needing user
  approval:
  (a) `advisory/service/advisory.rs`, a one-line `pub(crate)` visibility change, only
  if the constant is private;
  (b) a test harness registration file, if one is needed;
  (c) `docs/api.md` or the OpenAPI spec, if the endpoint is documented there.
- **Duplication check:**
  `search_for_pattern("SEVERITY_ORDER\\s*:")` and
  `search_for_pattern("\"critical\",\\s*\"high\"")` across the repo. Both must match only
  the definition in advisory.rs.
- **CI:** run every command from `CONVENTIONS.md` (for example `cargo fmt --check`,
  `cargo clippy -- -D warnings`, `cargo check`). Any non-zero exit is a hard stop.
  Also run the crate-level `cargo test -p` for the `fundamental` and `tests` crates.
- **Data flow:** HTTP GET → `get` handler → `SbomService::fetch_remediations`
  (DB: `sbom_advisory` join to `advisory`) → map to `RemediationItem` → sort by
  `SEVERITY_ORDER` rank → `SbomDetailsResponse.remediations` → JSON. Every stage
  connects to the next.
- **Contract and sibling parity:** handler error handling matches its siblings
  (`.context()`), the service method signature matches other `SbomService` methods,
  and the response type derives `ToSchema` like its siblings.
- **Sensitive-pattern check:** run on the staged diff.

## Step 10 — Commit and PR

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(sbom): add severity-sorted remediation list to SBOM details

Adds RemediationItem and SbomService::fetch_remediations, sorted by the
existing SEVERITY_ORDER constant reused from advisory::service::advisory
(same crate, no duplicate definition). Exposes it as `remediations` on
GET /api/v2/sbom/{id}.

Implements TC-9210"
```

Check for an `upstream` remote to detect a fork, then run
`gh pr create --base main ...`. The PR body contains
`Implements [TC-9210](<webUrl>)`, notes the SEVERITY_ORDER reuse decision (and any
visibility change), and adds `Closes owner/repo#N` if the GitHub Issue field is set.

## Step 11 — Jira

- Set `customfield_10875` to the PR URL as an ADF `inlineCard`.
- Add a comment containing the PR link, a summary of the changes, and any deviations
  (for example an approved `pub(crate)` change in advisory.rs). The comment ends with
  the `implement-task` footnote.
- Transition the issue to **In Review**.
