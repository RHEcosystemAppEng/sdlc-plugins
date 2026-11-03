# Implementation Plan – TC-9201: Add advisory severity aggregation service and endpoint

## Step 0 – Check the project configuration
The mock CLAUDE.md has every section this skill needs:
- Repository Registry: `trustify-backend`, Serena instance `serena_backend`, path `./`
- Jira Configuration: Project key TC, Cloud ID, and Feature issue type ID 10142 are present. Git PR field `customfield_10875` and GitHub Issue field `customfield_10747` are also set.
- Code Intelligence: uses the `mcp__<serena-instance>__<tool>` naming. One limitation: rust-analyzer can take 30–60s to index the first time.

The configuration is valid, so I continue.

## Step 0.5 – Jira access
Every Jira call tries MCP first. If MCP fails, I ask the user whether to use the REST API v3 fallback via `scripts/jira-client.py`.

## Step 1 – Read the task
| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Target PR | none (this is the normal flow) |
| Bookend Type | none |
| Dependencies | None |
| GitHub Issue (customfield_10747) | read from the issue. If it is set, store `<owner>/<repo>#<n>` for a `Closes` line in the PR. If it is empty, skip it. |
| webUrl | saved from the issue so the PR body can link to it |

Every required section is present, so there are no gaps to ask about.

**Files to Modify:**
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`
- `server/src/main.rs`: the task says no changes are needed because routes mount automatically. I will open it to confirm and leave it alone.

**Files to Create:**
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

## Step 1.5 – Check that the description is unchanged
See `digest-match.md`. One digest comment was found, tagged `sha256-md`. Its `created` and `updated` timestamps are the same. The computed digest matches the stored one, so I continue silently with no prompt.

## Step 2 – Dependencies
None, so there is nothing to check.

## Step 3 – Move to In Progress and assign
1. `jira.user_info()` to get the accountId
2. `jira.edit_issue(TC-9201, assignee=<accountId>)`
3. `jira.transition_issue(TC-9201 → In Progress)`

## Step 4 – Read the existing code (Serena `serena_backend`)
- `mcp__serena_backend__get_symbols_overview` on `advisory/service/advisory.rs`, `advisory/endpoints/mod.rs`, `advisory/endpoints/get.rs`, `advisory/model/mod.rs` and `advisory/model/summary.rs`.
- `find_symbol(include_body=true)` on `AdvisoryService/fetch` and `AdvisoryService/list`. This shows the signature pattern `&self, …, tx: &Transactional<'_>`, how the DB connection is handled, and how `.context()` is used.
- `find_symbol` on the `get` handler in `endpoints/get.rs`. This shows the `Path<Id>` extraction, how the service is injected (`web::Data`/`State`), and how errors are mapped.
- `find_symbol` on `AdvisorySummary` to read the `severity` field's type, which could be an enum or an `Option<String>`/CVSS-based value.
- `find_symbol` on the `sbom_advisory` entity in `entity/src/sbom_advisory.rs` to get its columns (`sbom_id` and `advisory_id`) and its relations.
- `find_symbol` on `AppError` in `common/src/error.rs` to find the NotFound variant and how `.context()` is used.
- Look at how existing SBOM endpoints return 404 (`sbom/endpoints/get.rs`, `SbomService::fetch`) so the new endpoint behaves the same way.
- `find_referencing_symbols` on `AdvisoryService` and on the advisory router function. Adding a method and a route should not break any existing callers.
- `search_for_pattern` for `severity_summary|SeveritySummary|count_by_severity` and for the `Severity` enum. If any of these already exist, I reuse them (symbol deduplication).
- **CONVENTIONS.md** is at the repo root (`./CONVENTIONS.md`). I read it, follow it, and note its CI check commands and any code-generation commands (for example OpenAPI generation).
- **Documentation to check**: `README.md`, `docs/api.md` (REST API reference) and `docs/architecture.md`. I record these for the documentation-impact review.
- **Siblings to compare**: `advisory/endpoints/get.rs` and `list.rs`, `sbom/endpoints/get.rs`, `advisory/model/summary.rs` and `details.rs`, and `tests/api/advisory.rs` and `sbom.rs`.

**Expected conventions** (to be confirmed against the siblings):
- Errors: handlers return `Result<T, AppError>` and wrap errors with `.context("…")`.
- Naming: snake_case `verb_noun` service methods and one handler file per endpoint.
- Layout: each module has `model/`, `service/` and `endpoints/`, with routes registered in `endpoints/mod.rs`.
- Models: `#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq, ToSchema)]`, which needs checking against `summary.rs`.
- Tests: integration tests in `tests/api/` against real PostgreSQL, asserting with `assert_eq!(resp.status(), StatusCode::OK)`.

**Possible conflict to check**: the task places the route `/api/v2/sbom/{id}/advisory-summary` under the **advisory** module's router, whose base path is `/api/v2/advisory`. During Step 4 I will check whether the advisory router is mounted with a prefix. If it is, the route has to be registered so that it still resolves to `/api/v2/sbom/{id}/advisory-summary`, for example with an absolute path or a router that has no prefix. If doing that would break the module's convention, I raise it with the user before implementing.

## Step 5 – Create the branch
```
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 – Make the changes

### 6.1 `modules/fundamental/src/advisory/model/severity_summary.rs` (new)
```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Counts of unique advisories per severity level for a single SBOM.
#[derive(Serialize, Deserialize, Debug, Clone, Default, PartialEq, Eq, ToSchema)]
pub struct SeveritySummary {
    /// Number of unique advisories with Critical severity.
    pub critical: u64,
    /// Number of unique advisories with High severity.
    pub high: u64,
    /// Number of unique advisories with Medium severity.
    pub medium: u64,
    /// Number of unique advisories with Low severity.
    pub low: u64,
    /// Total number of unique advisories linked to the SBOM.
    pub total: u64,
}
```
`Default` makes every count start at 0, which satisfies the acceptance criterion that all severity levels default to 0.

### 6.2 `modules/fundamental/src/advisory/model/mod.rs`
Add `pub mod severity_summary;` and, if the module re-exports its types, `pub use severity_summary::*;`.

### 6.3 `modules/fundamental/src/advisory/service/advisory.rs`
Add a method that follows the same pattern as `fetch`/`list`:
```rust
/// Aggregates unique advisory counts by severity for the given SBOM.
///
/// Returns `Ok(None)` when the SBOM does not exist so the endpoint can map it to 404.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<Option<SeveritySummary>, Error> {
    let conn = self.db.connection(tx);
    // 1. Confirm SBOM exists (reuse SbomService-style lookup / entity::sbom::Entity::find_by_id)
    // 2. Select DISTINCT advisory.id, advisory.severity
    //    FROM sbom_advisory JOIN advisory ON advisory.id = sbom_advisory.advisory_id
    //    WHERE sbom_advisory.sbom_id = $1
    // 3. Fold rows into SeveritySummary, matching on severity (case-insensitive / enum);
    //    unknown/None severities count toward total only
    // .context("Failed to aggregate advisory severities")?
}
```
- **Deduplication**: use `SELECT DISTINCT` on the advisory ID, or `COUNT(DISTINCT advisory.id)` grouped by severity, so duplicate `sbom_advisory` rows are counted once.
- **Performance (<200ms for 500 advisories)**: a single grouped/distinct query that uses the `sbom_advisory.sbom_id` index, with no N+1 lookups. If the `severity` column can be grouped on at the database level, use `GROUP BY severity` with `COUNT(DISTINCT id)` and fill in the struct from the result.
- **Severity values**: map them using the type `AdvisorySummary.severity` actually uses. If a shared `Severity` enum or parser exists, reuse it rather than writing new string matching.
- Use the query helpers in `common/src/db/query.rs` if they apply.
- Treat the data defensively: a severity of `None` or an unrecognized value still adds to `total` but to no named bucket.

### 6.4 `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (new)
Follows the pattern in `get.rs`:
```rust
/// Returns aggregated advisory severity counts for an SBOM.
#[utoipa::path(get, path = "/api/v2/sbom/{id}/advisory-summary",
    responses((status = 200, body = SeveritySummary), (status = 404)))]
pub async fn get_severity_summary(
    service: web::Data<AdvisoryService>, // or State<...>, matching get.rs
    db: web::Data<Database>,
    Path(id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    match service.severity_summary(id, &db.into()).await
        .context("Failed to fetch advisory severity summary")? {
        Some(summary) => Ok(Json(summary)),
        None => Err(AppError::NotFound(format!("SBOM {id} not found"))), // match SBOM get 404 behavior
    }
}
```

### 6.5 `modules/fundamental/src/advisory/endpoints/mod.rs`
Add `mod severity_summary;` and register the route the same way the existing ones are registered:
`.route("/api/v2/sbom/{id}/advisory-summary", get(severity_summary::get_severity_summary))`. I will adjust the path to match the router prefix found in Step 4. If the module keeps an OpenAPI path list, add the handler to it.

### 6.6 `server/src/main.rs`
No change. Routes mount automatically when the module is registered. I will confirm this in Step 4.

### Documentation impact
If `docs/api.md` lists endpoints, it would need the new `GET /api/v2/sbom/{id}/advisory-summary`. That file is not in Files to Modify, so I **raise it in Step 9's scope check for user approval** and do not edit it myself. If CONVENTIONS.md lists OpenAPI generation, I run it and include the regenerated spec, marked as generated output.

## Step 7 – Tests: `tests/api/advisory_summary.rs` (new)
These follow the conventions in `tests/api/advisory.rs` (test DB setup, HTTP client, `assert_eq!(resp.status(), StatusCode::OK)`). Every test gets a `///` doc comment and Given/When/Then comments. Assertions check the actual values: the whole `SeveritySummary` struct is compared with `assert_eq!`.

1. `/// Verifies a valid SBOM with known advisories returns correct per-severity counts.`
   `test_advisory_summary_returns_correct_counts`: ingest an SBOM linked to e.g. 2 Critical, 1 High, 3 Medium and 0 Low advisories, then assert the body equals `SeveritySummary { critical: 2, high: 1, medium: 3, low: 0, total: 6 }`.
2. `/// Verifies a non-existent SBOM ID returns 404.`
   `test_advisory_summary_unknown_sbom_returns_404`: assert `StatusCode::NOT_FOUND`.
3. `/// Verifies an SBOM with no advisories returns all-zero counts.`
   `test_advisory_summary_no_advisories_returns_zeros`: assert the body equals `SeveritySummary::default()`.
4. `/// Verifies duplicate SBOM-advisory links are counted once.`
   `test_advisory_summary_deduplicates_advisories`: link the same advisory twice, then assert `critical: 1, total: 1`.

These four cases differ in setup and in what they assert, so they stay as separate tests rather than being parameterized. If `tests/Cargo.toml` or a test `main.rs` needs a `mod advisory_summary;` line, I raise that in the scope check.

Run: `cargo test -p <tests-crate>` and `cargo test -p trustify-module-fundamental`. Crate names come from `cargo metadata --no-deps --format-version 1`. All failures get fixed before moving on.

## Step 8 – Acceptance criteria
| Criterion | How it is met |
|---|---|
| GET returns `{critical, high, medium, low, total}` | `SeveritySummary` is serialized; covered by test 1 |
| 404 when the SBOM doesn't exist | the service returns `None` and the handler returns `AppError::NotFound`; covered by test 2 |
| Unique advisories only | DISTINCT on advisory ID; covered by test 4 |
| Levels default to 0 | `#[derive(Default)]`; covered by test 3 |
| <200ms for 500 advisories | one indexed aggregate query with no N+1; I will check with a quick timing on seeded data or with EXPLAIN |

## Step 9 – Self-checks
- **Scope**: `git diff --name-only` should list only the six in-scope files. `server/src/main.rs` should be unchanged. Any extra file, such as `docs/api.md`, a test module registration or a generated OpenAPI spec, needs explicit user approval.
- **Untracked files**: `git status --short`. Untracked files near the changes are flagged, never staged automatically.
- **Dead parameters**: not expected, since no code is removed.
- **Secrets**: `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`.
- **Docs**: check that `docs/api.md` and `README.md` are still accurate, and flag them if not.
- **Duplication**: search for existing severity counting or aggregation helpers and refactor to use them if found.
- **CI**: run every CI command listed in CONVENTIONS.md (for example `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo check`) plus any code generation. **Any non-zero exit stops the work.**
- **Rust module tests**: `cargo test -p` for each crate with changes. Any failure stops the work.
- **Data flow**: HTTP GET `{id}` → `Path<Id>` → `AdvisoryService::severity_summary` → SBOM existence check → distinct join query on `sbom_advisory`+`advisory` → fold into `SeveritySummary` → `Json` response (200), or `AppError::NotFound` (404). Every stage connects to the next.
- **Query scope**: the query is filtered by `sbom_id`, so it never loads every advisory.
- **Contract and sibling parity**: the handler signature and error mapping match `get.rs`. The service method signature matches `fetch`/`list`. Only reads are done (no writes to shared entities). The caller-site pattern for `AdvisoryService` matches existing handlers.

## Step 10 – Commit and push
```
git add <in-scope files>
git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add SBOM advisory severity summary endpoint

Add AdvisoryService::severity_summary and GET /api/v2/sbom/{id}/advisory-summary
returning deduplicated counts per severity level.

Implements TC-9201"
git push -u origin TC-9201
```
- Fork detection: `git remote get-url upstream`. If there is an upstream, run `gh pr create -R <upstream> --head <fork-owner>:TC-9201 --base main`. Otherwise run `gh pr create --base main`.
- The PR body has the line `Implements [TC-9201](<webUrl>)`, plus `Closes <owner>/<repo>#<n>` if the GitHub Issue field is set.

## Step 11 – Update Jira
- Set `customfield_10875` to the PR URL as an ADF `inlineCard`.
- Add a comment with the PR link, a summary of the changes and any deviations from the plan (for example a docs file approved outside the original scope). It ends with the footnote from `shared/comment-footnote.md` with skill name `implement-task`.
- Move TC-9201 to **In Review**.
