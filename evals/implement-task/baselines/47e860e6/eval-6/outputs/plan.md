# Implementation Plan – TC-9201: Add advisory severity aggregation service and endpoint

Skill: `sdlc-workflow:implement-task` (simulated. No repository files are changed and
no Jira, git or Serena calls are made.)

---

## Step 0 – Validate Project Configuration

The CLAUDE.md file (`claude-md-mock.md`) passes all three checks:

- `## Repository Registry`: has one entry, `trustify-backend`. Serena instance is `serena_backend` and path is `./`.
- `## Jira Configuration`: has Project key `TC`, Cloud ID `2b9e35e3-...`, and Feature issue type ID `10142`. It also sets Git Pull Request field `customfield_10875` and GitHub Issue field `customfield_10747`.
- `## Code Intelligence`: has the tool naming convention `mcp__<serena-instance>__<tool>`. The only listed limitation is that rust-analyzer can take 30-60 seconds to index.

Result: configuration is valid, so I continue.

## Step 0.5 – Jira Access

I would try the Atlassian MCP first. If it failed, I would ask the user about the REST fallback. The digest's `sha256-md` tag fits the MCP (markdown) access path.

## Step 1 – Fetch and Parse Task

`jira.get_issue("TC-9201")`

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Description | Service method plus REST endpoint that counts advisory severities for an SBOM |
| Files to Modify | `advisory/service/advisory.rs`, `advisory/endpoints/mod.rs`, `advisory/model/mod.rs`, `server/src/main.rs` (marked "no changes needed") |
| Files to Create | `advisory/model/severity_summary.rs`, `advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs` |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` (new) |
| Implementation Notes | present |
| Acceptance Criteria | 5 items |
| Test Requirements | 4 items |
| Dependencies | None |
| Target PR | not present (default flow) |
| Bookend Type | not present (normal implementation) |
| Review Context | not present |

- All required sections are present, so I do not need to stop and ask for clarification.
- I capture `webUrl` as `https://<site>.atlassian.net/browse/TC-9201` for use in the PR body.
- I read GitHub Issue field `customfield_10747`. If it holds a URL, I parse it into `<owner>/<repo>#<n>` for a `Closes` line. If it is empty, I skip this silently.

## Step 1.5 – Verify Description Integrity

See `digest-match.md`. In short: there is one digest comment, `created == updated` (not edited), and the tag is `sha256-md`, which matches the computed `sha256-md`. The hex digest also **matches**, so I **proceed silently** with no user prompt.

## Step 2 – Verify Dependencies

Dependencies are "None", so nothing needs checking.

## Step 3 – Transition and Assign

1. `jira.user_info()` to get the accountId.
2. `jira.edit_issue("TC-9201", assignee=<accountId>)`.
3. `jira.transition_issue("TC-9201", "In Progress")`.

## Step 4 – Understand the Code (Serena instance `serena_backend`)

I allow for the 30-60 second rust-analyzer indexing delay on first use.

1. `mcp__serena_backend__get_symbols_overview` on:
   - `modules/fundamental/src/advisory/service/advisory.rs` to see `AdvisoryService`, `fetch`, `list` and `search`
   - `modules/fundamental/src/advisory/endpoints/mod.rs` to see the router builder
   - `modules/fundamental/src/advisory/model/mod.rs` to see the module declarations
2. `mcp__serena_backend__find_symbol` with `include_body=true` on:
   - `AdvisoryService/fetch` and `AdvisoryService/list`, for the method signature (`&self, ..., tx: &Transactional<'_>`), how the DB connection is obtained, and the `.context()` usage
   - the handler in `advisory/endpoints/get.rs`, for `Path<Id>` extraction, service injection (`web::Data`/`State`) and the return type `Result<Json<T>, AppError>`
   - `AdvisorySummary` in `advisory/model/summary.rs`, to learn the type of the `severity` field (enum, `Option<String>`, or a CVSS-derived value)
   - `entity/src/sbom_advisory.rs`, for the columns (`sbom_id`, `advisory_id`) and the `Relation` definitions
   - `AppError` in `common/src/error.rs`, for the `NotFound` variant and how `.context()` is implemented
   - the SBOM `fetch` in `sbom/service/sbom.rs` and `sbom/endpoints/get.rs`, to see how an unknown SBOM ID becomes a 404 (needed for the acceptance criterion about matching existing SBOM endpoints)
3. `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` and on the advisory router function, to confirm that adding a method and a route breaks no callers.
4. `mcp__serena_backend__search_for_pattern`:
   - `"/api/v2/sbom/"` to find how SBOM-scoped sub-routes are mounted. The new path lives under `/sbom/{id}` but is registered in the advisory module, so I need to check the prefix handling in `advisory/endpoints/mod.rs` and `server/src/main.rs`.
   - `Severity|severity` across the `fundamental` and `common` crates, to look for an existing severity enum or ordering constant before declaring a new one (symbol deduplication)
   - `count|group_by|GROUP BY` in the service layers, to find existing aggregation helpers in `common/src/db/query.rs`
   - `utoipa|#\[utoipa::path` to check whether OpenAPI annotations are used
5. Sibling convention analysis: run `get_symbols_overview` on `advisory/endpoints/get.rs`, `advisory/endpoints/list.rs`, `sbom/endpoints/get.rs`, and the models `advisory/model/summary.rs` and `sbom/model/summary.rs`. For tests, look at `tests/api/advisory.rs` and `tests/api/sbom.rs`.
6. CONVENTIONS.md lookup: read `./CONVENTIONS.md`, which exists according to the repo tree. From it I extract the CI check commands (likely `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo check`, `cargo test`) and any code-generation commands, such as OpenAPI spec generation.
7. Documentation files: `README.md`, `docs/api.md` (REST API reference, which is likely affected by the new endpoint), `docs/architecture.md`, and `CONVENTIONS.md`.

### Expected convention list (to be confirmed against siblings)

- **Naming**: snake_case for modules and functions, and `verb_noun`/noun handlers. The file name `severity_summary.rs` matches the struct name `SeveritySummary`.
- **Error handling**: `Result<T, AppError>`, with `.context("...")` on fallible DB calls.
- **Module structure**: `model/ + service/ + endpoints/`. Each new file gets a `pub mod` entry in its parent `mod.rs`.
- **API design**: handlers extract `Path<Id>`, call the service, and return `Json<T>`. Service methods take `&self, <args>, tx: &Transactional<'_>`.
- **Serialization**: models derive `Serialize, Deserialize, Debug, Clone` (plus `ToSchema` if utoipa is used).
- **Tests**: integration tests run against a real PostgreSQL test DB, and status is checked with `assert_eq!(resp.status(), StatusCode::OK)`.
- **Skill overrides**: value-based assertions on the whole response body, and a doc comment on every test. These apply even if the siblings lack them.

Possible conflict to raise with the user: the route path is `/api/v2/sbom/{id}/advisory-summary`, but the task registers it in `advisory/endpoints/mod.rs`. If the advisory router is nested under a `/api/v2/advisory` prefix, I would need a route outside that prefix. I would check how the router is mounted first. If it can only work by editing `sbom/endpoints/mod.rs` or `server/src/main.rs`, which the task marks as "no changes needed", I would flag it under scope containment rather than quietly widening scope.

## Step 5 – Create Branch

```
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 – Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

```rust
use serde::{Deserialize, Serialize};

/// Aggregated count of unique advisories per severity level for a single SBOM.
#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize)] // + utoipa::ToSchema if used by siblings
pub struct SeveritySummary {
    /// Number of unique advisories rated Critical.
    pub critical: u64,
    /// Number of unique advisories rated High.
    pub high: u64,
    /// Number of unique advisories rated Medium.
    pub medium: u64,
    /// Number of unique advisories rated Low.
    pub low: u64,
    /// Total number of unique advisories linked to the SBOM.
    pub total: u64,
}
```

- `Default` sets every level to 0 (acceptance criterion 4).
- Open question: should `total` include advisories with no severity or an unrecognized one? I plan to make `total` the count of all unique linked advisories. I would note this in the PR and confirm it against the `severity` field type.

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;`, and a `pub use severity_summary::*;` re-export if sibling modules do that.

### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add a method to `AdvisoryService`:

```rust
/// Returns per-severity counts of unique advisories linked to the given SBOM.
///
/// Returns `Ok(None)` when the SBOM does not exist so the endpoint can map it to 404.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<Option<SeveritySummary>, Error> {
    let connection = self.db.connection(tx);

    // 1. Confirm SBOM exists (reuse the same lookup SbomService::fetch / existing sbom entity query uses)
    if sbom::Entity::find_by_id(sbom_id).one(&connection).await
        .context("failed to look up SBOM")?.is_none() {
        return Ok(None);
    }

    // 2. Load DISTINCT advisories linked via sbom_advisory join table
    //    SELECT DISTINCT advisory.id, advisory.severity FROM advisory
    //    JOIN sbom_advisory ON sbom_advisory.advisory_id = advisory.id
    //    WHERE sbom_advisory.sbom_id = $1
    //    (or GROUP BY severity with COUNT(DISTINCT advisory.id) at the DB level)

    // 3. Fold into SeveritySummary, matching severity case-insensitively
    //    critical/high/medium/low; total = number of unique advisories
}
```

- Deduplication (acceptance criterion 3): use `COUNT(DISTINCT advisory.id)` grouped by severity, or `SELECT DISTINCT`. This ensures duplicate `sbom_advisory` rows are counted once.
- Performance (acceptance criterion 5, under 200ms for 500 advisories): aggregate in the database with a single grouped query on the indexed `sbom_advisory.sbom_id`, rather than loading full `AdvisorySummary` rows. I would check that an index on `sbom_advisory(sbom_id)` exists in the migration and flag it if missing. A migration is out of scope.
- Severity mapping: if the codebase has a severity enum, I reuse it (symbol deduplication). Otherwise I match on the stored value. I will not declare a new severity constant until a search confirms none exists.
- Errors: every DB call is wrapped with `.context(...)`, following `common/src/error.rs`.
- Reuse: I reuse the SBOM existence check that `SbomService` already has. `SbomService` and `AdvisoryService` are in the same crate, so no new dependency is needed. If the helper is private, I make it `pub(crate)` rather than duplicating it.
- The exact signature (`Option` versus a direct `AppError::NotFound`) will follow how `AdvisoryService::fetch` reports a missing entity.

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

```rust
/// GET /api/v2/sbom/{id}/advisory-summary — returns severity counts of unique advisories for an SBOM.
pub async fn severity_summary(
    service: web::Data<AdvisoryService>,   // or State<...>, matching get.rs
    db: web::Data<Database>,
    Path(id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    let tx = db.begin().await?; // match get.rs transactional usage
    match service.severity_summary(id, &tx).await.context("failed to compute advisory severity summary")? {
        Some(summary) => Ok(Json(summary)),
        None => Err(AppError::NotFound(format!("SBOM {id} not found"))), // same variant SBOM get uses
    }
}
```

This follows `advisory/endpoints/get.rs`: extract `Path<Id>`, call the service, and return JSON. It also gets a utoipa `#[utoipa::path(...)]` annotation if siblings have one.

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

- Add `mod severity_summary;`.
- Register `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))`, using the same `Router::new().route(...)` style and path syntax (`:id` or `{id}`, depending on the Axum version) as the existing routes. If siblings apply caching middleware (tower-http) in the route builder, I add the same here.

### 6.6 `server/src/main.rs`

No changes. The task says routes auto-mount through module registration. I would confirm this during Step 4.

### 6.7 Code quality

- Every new struct, field and public function gets a `///` doc comment.
- Guard defensively against a null or unknown `severity` on advisory rows: treat it as counting toward `total` only.

### 6.8 Documentation impact

The task has no Documentation Updates section. `docs/api.md` documents the REST API and probably needs an entry for the new endpoint, but it is **not** in Files to Modify. I would flag it for user approval in Step 9 rather than editing it unilaterally. If code generation is configured in CONVENTIONS.md, its output (for example an OpenAPI spec) is committed with the change.

## Step 7 – Write Tests: `tests/api/advisory_summary.rs`

These follow the setup in `tests/api/advisory.rs`: test DB bootstrap, fixture ingestion and the HTTP client. They use value-based assertions on the whole struct and a `///` doc comment plus Given/When/Then on every test.

```rust
/// Verifies that an SBOM with known advisories returns correct per-severity counts.
#[tokio::test]
async fn severity_summary_returns_counts_for_known_advisories() {
    // Given an SBOM linked to 2 critical, 1 high, 3 medium, 1 low advisories
    // When GET /api/v2/sbom/{id}/advisory-summary
    // Then status is 200 and body equals the expected summary
    assert_eq!(resp.status(), StatusCode::OK);
    assert_eq!(body, SeveritySummary { critical: 2, high: 1, medium: 3, low: 1, total: 7 });
}

/// Verifies that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn severity_summary_returns_404_for_unknown_sbom() { ... assert_eq!(resp.status(), StatusCode::NOT_FOUND); }

/// Verifies that an SBOM with no linked advisories returns all-zero counts.
#[tokio::test]
async fn severity_summary_returns_zeros_when_no_advisories() {
    // ... assert_eq!(body, SeveritySummary::default()) with explicit zeros
}

/// Verifies that duplicate sbom_advisory links to the same advisory are counted once.
#[tokio::test]
async fn severity_summary_deduplicates_advisory_links() {
    // Given one high advisory linked twice to the same SBOM
    // Then body == SeveritySummary { high: 1, total: 1, ..Default::default() }
}
```

- I do not parameterize. The four tests differ in setup and assertions, so they fail the Meszaros heuristic.
- Registration: if `tests/Cargo.toml` or a test `main.rs`/`mod.rs` declares modules explicitly, adding `advisory_summary` there would be an out-of-scope edit. I would flag it in Step 9.
- Run: `cargo test -p <tests-crate>` and `cargo test -p trustify-module-fundamental` (crate names resolved with `cargo metadata`).

## Step 8 – Verify Acceptance Criteria

| AC | Verification |
|---|---|
| Returns `{critical, high, medium, low, total}` | Struct fields plus the known-advisories test |
| 404 for missing SBOM, consistent with SBOM endpoints | Same `AppError` variant as `sbom/endpoints/get.rs`, plus the 404 test |
| Unique advisories only | `COUNT(DISTINCT advisory.id)`, plus the dedup test |
| Missing levels default to 0 | `Default` derive, plus the zeros test |
| Under 200ms for 500 advisories | Single grouped DB query on indexed `sbom_id`. I time it with a 500-advisory fixture locally, or report it as not measured if the fixture isn't practical |

## Step 9 – Self-Verification

- **Scope containment**: `git diff --name-only` should list only the 3 modified files (advisory service, endpoints mod, model mod) and the 3 created files. I flag for approval any change to `docs/api.md`, `tests/Cargo.toml` or the test module registration, `sbom/endpoints/mod.rs`, or a migration.
- **Untracked files**: check `git status --short` for stray files near the changed directories.
- **Dead parameters**: none are expected, because nothing is removed.
- **Sensitive patterns**: run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`.
- **Documentation currency**: `docs/api.md` (flagged as described above).
- **Duplication check**: grep for existing severity aggregation or count helpers, and reuse them if found.
- **Cross-section consistency**: paths agree across Files to Modify, Files to Create and Implementation Notes (for example `advisory/model/summary.rs` versus the new `severity_summary.rs`).
- **CI checks**: run every command from CONVENTIONS.md, plus code generation. **Any non-zero exit is a hard stop.**
- **Rust module tests**: `cargo test -p <crate>` for each crate that has modified files. Hard stop on failure.
- **Data-flow trace**: HTTP GET → `Path<Id>` → `AdvisoryService::severity_summary` → SBOM existence check → grouped DISTINCT query over `sbom_advisory`⨝`advisory` → fold into `SeveritySummary` → `Json` 200, or `AppError::NotFound` 404. Every stage is connected.
- **Query scope**: the query filters by `sbom_id` at the DB level and does not load all advisories.
- **Contract and sibling parity**: the method signature matches `fetch`/`list`; the handler matches `get.rs` (extractors, error wrapping, caching middleware); for the cross-module entity, the change is read-only on `sbom_advisory`, so there are no write or transaction concerns; for the caller site, the SBOM existence check is used the same way as in `sbom/endpoints/get.rs`.

## Step 10 – Commit and Push

```
git add <in-scope files>
git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add SBOM advisory severity summary endpoint

Add AdvisoryService::severity_summary and GET /api/v2/sbom/{id}/advisory-summary
returning unique-advisory counts per severity level (critical/high/medium/low/total).

Implements TC-9201"
git push -u origin TC-9201
```

- Fork detection: run `git remote get-url upstream`. If it exists, use `gh pr create -R <upstream> --head <fork-owner>:TC-9201 --base main`. Otherwise use `gh pr create --base main`.
- PR body: summary, test plan, `Implements [TC-9201](<webUrl>)`, and `Closes <owner>/<repo>#<n>` if the GitHub Issue field is set.

## Step 11 – Update Jira

1. `jira.update_issue("TC-9201", {"customfield_10875": ADF doc with inlineCard <PR-URL>})`.
2. `jira.add_comment` (ADF) with the PR link, a summary of changes, and any deviations (for example the flagged `docs/api.md` change or the choice of `total` semantics). It ends with a rule and the footnote: "This comment was AI-generated by [sdlc-workflow/implement-task](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10."
3. `jira.transition_issue("TC-9201", "In Review")`.
