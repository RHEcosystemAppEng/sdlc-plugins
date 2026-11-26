# Implementation Plan – TC-9201: Add advisory severity aggregation service and endpoint

- **Repository:** trustify-backend (Serena instance `serena_backend`, path `./`)
- **Target Branch:** `main`
- **Flow:** default (no Target PR, no Bookend Type)
- **GitHub Issue (customfield_10747):** read from the issue. If it holds a URL, parse it to `<owner>/<repo>#<number>` and add a `Closes ...` line to the PR body. If it is empty, skip it.

---

## Step 0 – Project Configuration validation
Passed. The Repository Registry, Jira Configuration (key TC, Cloud ID, Feature type 10142) and Code Intelligence sections are all present.

## Step 0.5 – Jira access
Use Atlassian MCP first. If MCP fails, prompt the user with the 1/2/3 REST fallback choice (`scripts/jira-client.py`).

## Step 1 – Fetch and parse
`jira.get_issue(TC-9201)`. All required sections are present, and the skill records `webUrl` for the PR link. Parsed scope:

| Section | Items |
|---|---|
| Files to Modify | `modules/fundamental/src/advisory/service/advisory.rs`, `modules/fundamental/src/advisory/endpoints/mod.rs`, `modules/fundamental/src/advisory/model/mod.rs`, `server/src/main.rs` (marked "no changes needed") |
| Files to Create | `modules/fundamental/src/advisory/model/severity_summary.rs`, `modules/fundamental/src/advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs` |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` -> `{ critical, high, medium, low, total }` |

## Step 1.5 – Description integrity
The digest **matches**: the tag is `sha256-md` on both sides, the hex is identical, and `created == updated`. The skill continues silently with no prompt. Details are in `digest-match.md`.

## Step 2 – Dependencies
"Depends on: None". Nothing to verify.

## Step 3 – Assign and transition
1. `jira.user_info()` to get the accountId.
2. `jira.edit_issue(TC-9201, assignee=<accountId>)`.
3. `jira.transition_issue(TC-9201 -> In Progress)`.

---

## Step 4 – Understand the code (Serena `serena_backend`)

Note: rust-analyzer may need 30–60 seconds to index on first use. Wait for indexing before trusting empty results.

1. `mcp__serena_backend__get_symbols_overview` on:
   - `modules/fundamental/src/advisory/service/advisory.rs`: confirm `AdvisoryService` with `fetch`, `list`, `search`, and the `(&self, ..., tx: &Transactional<'_>)` signature.
   - `modules/fundamental/src/advisory/endpoints/mod.rs`: see how routes are registered (`Router::new().route(...)`) and whether the router is nested under `/api/v2/advisory` or registers absolute paths.
   - `modules/fundamental/src/advisory/model/mod.rs`: existing `pub mod summary; pub mod details;`.
2. `mcp__serena_backend__find_symbol` with `include_body=true` for:
   - `AdvisoryService/fetch` and `AdvisoryService/list`: the query-building and error-wrapping pattern.
   - The handler in `advisory/endpoints/get.rs`: `Path<Id>` extraction, service call, return type, `Result<_, AppError>`.
   - `AdvisorySummary` in `advisory/model/summary.rs`: the type of the `severity` field (enum or string, optional or not).
   - `entity/src/sbom_advisory.rs`: the join-table columns (`sbom_id`, `advisory_id`) and relations.
   - `AppError` in `common/src/error.rs`: the NotFound variant and `.context()` usage.
   - `SbomService::fetch` in `sbom/service/sbom.rs` and the `sbom/endpoints/get.rs` handler: how a missing SBOM becomes a 404, which keeps AC #2 consistent with existing SBOM endpoints.
3. `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` and the advisory router function, to check that the additions do not break callers (both changes are additive).
4. `mcp__serena_backend__search_for_pattern` for:
   - Existing severity aggregation or count helpers (`severity`, `count`, `group_by`, `SeveritySummary`, `severity_summary`). This is a reuse and symbol-deduplication check.
   - Shared helpers in `common/src/db/query.rs` that could support the aggregation.
   - Caching configuration in the advisory/sbom route builders (`tower-http`), so the new route can match siblings.
5. **Convention analysis on siblings:** `advisory/endpoints/{get,list}.rs`, `sbom/endpoints/get.rs`, `advisory/model/summary.rs`, `sbom/model/summary.rs`, `tests/api/{advisory,sbom}.rs`.
6. **CONVENTIONS.md:** read `./CONVENTIONS.md`. Record its CI-check commands (e.g. `cargo fmt --check`, `cargo clippy ...`, `cargo check`) and any code-generation commands (e.g. OpenAPI generation) for Step 9.
7. **Documentation files:** `README.md`, `docs/api.md` (REST API reference), `docs/architecture.md`. Note that these are not in Files to Modify; see Step 6, Documentation impact.

### Expected conventions (to be confirmed in Step 4)
- **Errors:** handlers return `Result<T, AppError>`; service errors are wrapped with `.context("...")`.
- **Naming:** snake_case `verb_noun` service methods; one handler per file in `endpoints/`; model structs in `model/<name>.rs`.
- **Models:** derive `Serialize`, `Deserialize`, `Debug`, `Clone`, plus the `ToSchema` derive if siblings use utoipa.
- **Service signature:** `pub async fn x(&self, id: Id, tx: &Transactional<'_>) -> Result<T, Error>`.
- **Tests:** integration tests against a real PostgreSQL test database, using `assert_eq!(resp.status(), StatusCode::OK)`.
- **Skill overrides:** value-based assertions on the whole response struct, a `///` doc comment on every test, and given/when/then comments.

### Points to resolve in Step 4 (flag to the user if they conflict)
- **Route location.** The path is `/api/v2/sbom/{id}/advisory-summary`, but the task says to register it in `advisory/endpoints/mod.rs`. If the advisory router is nested under `/api/v2/advisory`, a relative route would produce the wrong URL. Plan: register the absolute path the way siblings do. If the advisory router can only register paths relative to `/api/v2/advisory`, raise a convention conflict with the user instead of editing `sbom/endpoints/mod.rs`, which is out of scope.
- **Severity representation.** The implementation notes say to count using `AdvisorySummary.severity`. If severity is stored on the `advisory` entity column, do the aggregation in SQL (join `sbom_advisory` -> `advisory`, `COUNT(DISTINCT advisory.id)` grouped by severity). That avoids loading every `AdvisorySummary` and keeps the response time under 200ms for 500 advisories. The mapping to Critical/High/Medium/Low uses the same severity type that `AdvisorySummary` uses.

---

## Step 5 – Branch
```
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 – Implement changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`
```rust
/// Aggregated count of unique advisories per severity level for a single SBOM.
#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize /*, ToSchema if siblings use it */)]
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
- `Default` makes every level 0 when there are no advisories (AC #4).
- Add a small documented constructor or helper that increments a level by severity. Treat unknown or `None` severities defensively: count them in `total` only, and document that choice in a comment.

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`
- Add `pub mod severity_summary;` (plus a `pub use` re-export if siblings re-export).

### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`
Add to `impl AdvisoryService`:
```rust
/// Returns per-severity counts of unique advisories linked to the given SBOM.
///
/// Returns `Ok(None)` when the SBOM does not exist so the endpoint can map it to 404.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<Option<SeveritySummary>, Error>
```
- Confirm the SBOM exists with `entity::sbom::Entity::find_by_id`, or reuse the lookup pattern from `SbomService::fetch`. Return `None` if it is missing.
- Query: `entity::sbom_advisory` filtered by `sbom_id`, joined to `entity::advisory`, selecting `DISTINCT advisory.id` with its severity. Better: group by severity with `COUNT(DISTINCT advisory.id)`. This de-duplicates repeated links (AC #3) and keeps aggregation in the database (AC #5).
- Fill `SeveritySummary` from the grouped rows. `total` is the sum of the distinct advisory count.
- Wrap errors with `.context("failed to compute advisory severity summary for SBOM")`, following the `fetch`/`list` pattern.
- Reuse first: use the existing `Transactional` connection helper and any `common/src/db/query.rs` helpers rather than raw SQL, unless siblings use raw SQL.

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
```rust
/// GET /api/v2/sbom/{id}/advisory-summary — returns advisory severity counts for an SBOM.
pub async fn severity_summary(
    State(service): State<AdvisoryService>, // match get.rs state extraction
    Path(id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    service
        .severity_summary(id, &Transactional::None)
        .await
        .context("...")?
        .map(Json)
        .ok_or_else(|| AppError::NotFound(...)) // same 404 mapping as sbom/endpoints/get.rs
}
```
- Mirror `get.rs` exactly: the state and `Path<Id>` extraction, the utoipa `#[utoipa::path]` annotation if siblings have one, and the 404 mapping.

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`
- Add `mod severity_summary;`.
- Register `.route("/api/v2/sbom/{id}/advisory-summary", get(severity_summary::severity_summary))`, following the existing `Router::new().route(...)` chain and any caching layer siblings apply. See the route-location note in Step 4.
- Add the handler to the OpenAPI path list if the module keeps one.

### 6.6 `server/src/main.rs`
- **No changes.** The task marks it "no changes needed": routes are mounted automatically through the module's router registration. Confirm in Step 4 that the advisory router is already mounted. Do not edit the file.

### 6.7 Code quality
- Doc comments on `SeveritySummary`, its fields, the service method, and the handler.
- Defensive handling of nullable severity values coming from the entity layer (`Option` -> `unwrap_or` or skip).
- Symbol deduplication: grep for an existing `SeveritySummary`, `severity_summary` or severity-order constant before declaring new ones.

### 6.8 Documentation impact
- No Documentation Updates section is present. `docs/api.md` documents REST endpoints, but it is **not** in Files to Modify. Do not edit it. Flag it in Step 9 as a candidate follow-up or ask the user. If OpenAPI is generated (per CONVENTIONS.md), regenerate it in Step 9 as an artifact.

---

## Step 7 – Tests: create `tests/api/advisory_summary.rs`
Follow the patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs` (test DB setup, HTTP client, `assert_eq!(resp.status(), StatusCode::...)`). Each test gets a `///` doc comment and `// Given / // When / // Then` sections. Assertions compare the whole deserialized `SeveritySummary`, not only individual fields or counts.

1. `test_advisory_summary_returns_counts_for_known_advisories`: ingest an SBOM linked to, for example, 2 Critical, 1 High, 3 Medium and 0 Low advisories. Assert status 200 and `SeveritySummary { critical: 2, high: 1, medium: 3, low: 0, total: 6 }`.
2. `test_advisory_summary_nonexistent_sbom_returns_404`: request a random or unknown ID and assert `StatusCode::NOT_FOUND`.
3. `test_advisory_summary_no_advisories_returns_zeros`: an SBOM with no advisory links. Assert 200 and `SeveritySummary::default()` (all zeros).
4. `test_advisory_summary_deduplicates_advisory_links`: link the same advisory to the SBOM more than once (duplicate `sbom_advisory` rows, or the same advisory reached through multiple paths). Assert it is counted once, e.g. `{ critical: 1, high: 0, medium: 0, low: 0, total: 1 }`.

- Parameterization: tests 1, 3 and 4 have different setups, so keep them as separate tests (Meszaros heuristic). Only introduce `rstest` if the siblings already use it.
- Registering the test file: if `tests/Cargo.toml` or an existing test `main.rs`/`mod.rs` must declare the new file (`[[test]]` or `mod advisory_summary;`), that file is out of scope. Flag it in Step 9 for user approval.
- AC #5 (<200ms at 500 advisories) is covered by the SQL-side aggregation design. Optionally add a timing assertion only if siblings have performance tests. Otherwise check it manually in Step 8.
- Before implementing, record the baseline `cargo clippy` / `cargo build` warnings. Then run `cargo test -p <tests crate>` and `cargo test -p <fundamental crate>`.

## Step 8 – Acceptance criteria check
| AC | How it is satisfied |
|---|---|
| Returns `{critical, high, medium, low, total}` | `SeveritySummary` serialized through `Json`; test 1 |
| 404 for unknown SBOM | Existence check, then the same NotFound mapping as `sbom/endpoints/get.rs`; test 2 |
| Unique advisories only | `COUNT(DISTINCT advisory.id)`; test 4 |
| Levels default to 0 | `#[derive(Default)]`; test 3 |
| <200ms for 500 advisories | A single grouped SQL query on the indexed join table; check by timing a seeded request |

## Step 9 – Self-verification
- **Scope containment:** `git diff --name-only` should list only the 3 modified and 3 created files. `server/src/main.rs` should not appear. Any test-harness registration file or `docs/api.md` change needs explicit user approval.
- **Untracked files:** `git status --short`. Check `??` entries in the touched directories.
- **Dead parameters:** none expected, since the change is additive.
- **Sensitive patterns:** `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`.
- **Documentation currency:** flag `docs/api.md` (new public endpoint) to the user.
- **Duplication check:** grep for other severity aggregation logic, for example in the search module.
- **Cross-section consistency:** paths for `AdvisoryService`, `AdvisorySummary` and `sbom_advisory` agree across Files to Modify and Implementation Notes and match `repo-backend.md`.
- **CI checks:** run every command from the CONVENTIONS.md CI section, then any code-generation commands (stage the regenerated OpenAPI output). **Any non-zero exit is a hard stop.**
- **Rust module tests:** use `cargo metadata --no-deps --format-version 1` to find the package for each modified file (fundamental module, tests crate). Run `cargo test -p <crate>` (or nextest) for each one. Stop on failure.
- **Data-flow trace:** HTTP GET -> `Path<Id>` -> `AdvisoryService::severity_summary` -> SBOM existence check -> grouped distinct query on `sbom_advisory` joined to `advisory` -> `SeveritySummary` -> `Json` response, or `AppError` NotFound -> 404. Every stage is connected.
- **Query scope:** the query is filtered by `sbom_id`. It is not a full scan.
- **Contract and sibling parity:** no trait is implemented. Parity with `get.rs` on extraction, errors, caching and OpenAPI annotation. Cross-module entity check: the endpoint only reads `sbom_advisory`. Caller-site check: `AdvisoryService` is invoked the same way as the existing handlers do.

## Step 10 – Commit and PR
```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(advisory): add SBOM advisory severity summary endpoint

Add AdvisoryService::severity_summary and GET /api/v2/sbom/{id}/advisory-summary
returning unique advisory counts per severity level.

Implements TC-9201"
```
- Fork detection: `git remote get-url upstream`. With a fork: `gh pr create -R <upstream> --head <fork-owner>:TC-9201 --base main`. Without one: `gh pr create --base main`.
- The PR body includes `Implements [TC-9201](<webUrl>)`, plus `Closes <owner>/<repo>#<n>` if the GitHub Issue field is set.

## Step 11 – Update Jira
- Set `customfield_10875` to an ADF `inlineCard` with the PR URL.
- Add a comment with the PR link, a summary of changes, and any deviations (for example the route-location resolution, the untouched `server/src/main.rs`, and the flagged `docs/api.md`). End it with the footnote rule plus "This comment was AI-generated by [sdlc-workflow/implement-task](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0."
- Transition TC-9201 to **In Review**.
