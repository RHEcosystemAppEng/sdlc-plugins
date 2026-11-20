# Implementation Plan – TC-9201: Add advisory severity aggregation service and endpoint

- **Repository:** trustify-backend (Serena instance `serena_backend`, path `./`)
- **Target Branch:** `main`
- **Flow:** default. There is no Target PR and no Bookend Type.
- **Parent feature:** TC-9001 (via "is incorporated by")

---

## Step 0 – Validate Project Configuration

PASS. CLAUDE.md contains:
- Repository Registry with one entry
- Jira Configuration (Project key `TC`, Cloud ID, Feature issue type ID `10142`, Git PR field `customfield_10875`, GitHub Issue field `customfield_10747`)
- Code Intelligence with the `mcp__<serena-instance>__<tool>` naming convention

## Step 0.5 – Jira Access

Every Jira call tries Atlassian MCP first. If MCP fails, the user is offered three options: REST API v3 fallback via `scripts/jira-client.py`, skip, or retry.

## Step 1 – Fetch and Parse

`jira.get_issue(TC-9201)` returns a description with all required sections. Parsed values:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Files to Modify | `advisory/service/advisory.rs`, `advisory/endpoints/mod.rs`, `advisory/model/mod.rs`, `server/src/main.rs` (marked "no changes needed") |
| Files to Create | `advisory/model/severity_summary.rs`, `advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs` |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` (NEW) |
| Dependencies | None |
| Target PR / Bookend / Review Context | absent |

The skill also captures `webUrl`, e.g. `https://redhat.atlassian.net/browse/TC-9201`, and reads `customfield_10747` for a GitHub issue. If that field is set, the parsed `owner/repo#N` goes into the PR body as `Closes ...`. If it is empty, the skill skips it.

## Step 1.5 – Description Integrity

Digest comment found: `sha256-md:a1b2…7890`. Its created and updated timestamps are equal, so it was not edited. The computed digest from `scripts/sha256-digest.py` is `sha256-md` with the same hex value. **The digests match, so the skill proceeds silently with no user prompt.** See `digest-match.md` for the details.

## Step 2 – Verify Dependencies

"Depends on: None", so there is nothing to check.

## Step 3 – Transition and Assign

1. `jira.user_info()` returns the current user's accountId.
2. `jira.edit_issue(TC-9201, assignee=<accountId>)`
3. `jira.transition_issue(TC-9201 → In Progress)`

## Step 4 – Understand the Code (Serena: `serena_backend`)

rust-analyzer may need 30–60 s to index on first use.

| Action | Tool call |
|---|---|
| Service structure | `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/service/advisory.rs")` |
| Signature pattern for `fetch` and `list` (`&self, …, tx: &Transactional<'_>`) | `mcp__serena_backend__find_symbol("AdvisoryService/fetch", include_body=true)` and `AdvisoryService/list` |
| Endpoint pattern | `mcp__serena_backend__find_symbol` on the handler in `advisory/endpoints/get.rs` (`Path<Id>` extraction, service call, JSON return) |
| Route registration | `get_symbols_overview` and `find_symbol` on the router fn in `advisory/endpoints/mod.rs` (`Router::new().route(...)`) |
| Model registration | Read `advisory/model/mod.rs` to see how `pub mod summary; pub mod details;` are declared |
| Severity field | `find_symbol("AdvisorySummary", include_body=true)` in `advisory/model/summary.rs` to check whether `severity` is an enum, a string or an `Option` |
| Join table | `find_symbol` on `Model`, `Relation` and `Column` in `entity/src/sbom_advisory.rs` (columns `sbom_id`, `advisory_id`) |
| Errors | `find_symbol("AppError", include_body=true)` in `common/src/error.rs` to see the NotFound variant and how `.context()` is used |
| 404 consistency | `find_symbol` on `SbomService/fetch` and the `sbom/endpoints/get.rs` handler to see how a missing SBOM turns into 404 |
| Route prefix | Check how `/api/v2/sbom/{id}/…` routes can be registered from the advisory module, i.e. whether the router is nested under `/api/v2` or uses full paths |
| Reuse search | `search_for_pattern("severity")` and `search_for_pattern("count\|group_by")` across `modules/` and `common/src/db/query.rs` to find existing aggregation or severity helpers |
| Symbol dedup | Search for `SeveritySummary`, `severity_summary` and `SeverityCount` across the workspace to make sure none exist yet |
| Backward compat | `find_referencing_symbols` on the router fn in `advisory/endpoints/mod.rs` to find who mounts it (`server/src/main.rs`) |

**CONVENTIONS.md:** present at the repo root. Read it, and extract its CI check commands (likely `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo check`/`cargo test`) plus any OpenAPI or code-generation commands, for use in Step 9.

**Documentation files to track:** `README.md`, `docs/api.md` (REST API reference, which likely needs the new endpoint) and `docs/architecture.md`. These are noted for Step 6 doc impact and the Step 9 currency check.

**Siblings for convention analysis:**
- `advisory/endpoints/get.rs`, `advisory/endpoints/list.rs`, `sbom/endpoints/get.rs`
- `advisory/model/summary.rs`, `advisory/model/details.rs`
- `tests/api/advisory.rs`, `tests/api/sbom.rs`

**Expected conventions (to confirm in Step 4):**
- Naming: snake_case `verb_noun` fns; one file per handler, named after the endpoint
- Errors: `Result<T, AppError>` with `.context("…")`
- Structure: `model/ + service/ + endpoints/`, with model structs deriving `Serialize`, `Deserialize`, `utoipa::ToSchema` (if OpenAPI is used)
- Routes: `Router::new().route("/path", get(handler))` in `endpoints/mod.rs`
- Tests: integration tests against a real Postgres DB, asserting `assert_eq!(resp.status(), StatusCode::OK)`

**Override:** Skill guidance takes precedence over sibling tests. Assertions will be value-based (compare the whole `SeveritySummary`), and every test fn gets a `///` doc comment.

**Possible convention conflict to flag:** the new route sits under `/api/v2/sbom/{id}/…` but lives in the advisory module. If the advisory router nests under `/api/v2/advisory`, registering an SBOM-scoped path there may need a full path or a separate route. If that turns out to conflict with the module routing, I would ask the user before going further.

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
use utoipa::ToSchema;

/// Aggregated count of unique advisories per severity level for a single SBOM.
#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize, ToSchema)]
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

- `Default` gives all-zero counts, which covers the "levels default to 0" acceptance criterion.
- `ToSchema` is only added if siblings use utoipa.

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;`, following the existing `pub mod summary;` declarations. Add a `pub use` re-export only if siblings re-export.

### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add a method to `AdvisoryService` that follows the `fetch`/`list` signature pattern:

```rust
/// Returns per-severity counts of unique advisories linked to the given SBOM.
///
/// Returns `AppError::NotFound` if the SBOM does not exist. Advisories linked
/// more than once are counted once; advisories without a recognised severity
/// contribute to `total` only.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify the SBOM exists -> NotFound (404) consistent with SbomService::fetch
    // 2. Query advisories joined via entity::sbom_advisory filtered by sbom_id,
    //    SELECT DISTINCT advisory.id, advisory.severity
    //    (or GROUP BY severity with COUNT(DISTINCT advisory.id) in SQL for performance)
    // 3. Fold rows into SeveritySummary, matching severity case-insensitively
    //    against Critical/High/Medium/Low; total = number of distinct advisories
}
```

- **Deduplication:** done at the database level with `DISTINCT` on advisory id, or `COUNT(DISTINCT advisory.id) … GROUP BY severity`. This satisfies the unique-advisories criterion.
- **Performance (<200 ms for 500 advisories):** a single aggregate query keyed on the indexed `sbom_advisory.sbom_id`, plus one existence check. No N+1 queries and no loading of full advisory rows.
- **Query scope:** filtered to the given `sbom_id`. It never loads all advisories.
- **Defensive access:** if `severity` is `Option<…>`, a `None` value is counted only in `total`, using an `if let`/match rather than unwrap.
- **Reuse:** use the severity type and enum from `AdvisorySummary` and the existing query helpers in `common/src/db/query.rs` where they apply. Do not declare a new severity enum if one already exists.
- **Errors:** `.context("Failed to compute advisory severity summary")` on DB errors, matching `common/src/error.rs`.
- **Cross-module entity:** read-only on `sbom_advisory`, so no transaction or conflict-handling concerns. It reuses the provided `tx`.

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Modelled on `advisory/endpoints/get.rs`:

```rust
/// GET /api/v2/sbom/{id}/advisory-summary — returns severity counts of advisories linked to an SBOM.
#[utoipa::path(/* mirror get.rs: tag, params(id), responses(200 = SeveritySummary, 404) */)]
pub async fn severity_summary(
    State(service): State<AdvisoryService>,   // same extractor/state pattern as get.rs
    Path(id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &Transactional::None)
        .await
        .context("Failed to fetch advisory severity summary")?;
    Ok(Json(summary))
}
```

The state, DB and transaction plumbing will copy `get.rs` exactly.

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

- Add `mod severity_summary;`
- Register `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))`, using the path syntax and prefix convention the existing routes use (`:id` vs `{id}`, nested vs absolute).
- Add the handler and schema to the OpenAPI `paths(...)`/`components(...)` list if siblings register there.

### 6.6 `server/src/main.rs`

**No change.** The task says routes auto-mount through module registration. It is listed under Files to Modify only as a note. I would confirm this with `find_referencing_symbols` on the advisory router.

### 6.7 Documentation impact

There is no Documentation Updates section. A public endpoint is being added, so `docs/api.md` (the REST API reference) probably needs an entry. **That file is outside Files to Modify/Create**, so I would not edit it in Step 6. It gets flagged in Step 9 for user approval. If CONVENTIONS.md defines an OpenAPI generation command, the generated spec changes would be staged as part of the deliverable, also subject to scope approval.

## Step 7 – Write Tests: `tests/api/advisory_summary.rs`

Follow `tests/api/advisory.rs` for the test context, DB fixture and HTTP client setup. Rules applied: value-based assertions on the whole struct, a `///` doc comment on each test, and given/when/then comments. The four cases need different setup and assertions, so they are separate tests rather than parameterized.

```rust
/// Verifies that an SBOM with known advisories returns correct per-severity counts.
#[test_context(TrustifyContext)] #[tokio::test]
async fn advisory_summary_returns_correct_counts(ctx) {
    // Given an SBOM linked to 2 Critical, 1 High, 3 Medium, 0 Low advisories
    // When GET /api/v2/sbom/{id}/advisory-summary
    // Then status is 200 and body == SeveritySummary { critical: 2, high: 1, medium: 3, low: 0, total: 6 }
}

/// Verifies that a non-existent SBOM ID returns 404.
async fn advisory_summary_unknown_sbom_returns_404(ctx) {
    // Given a random, non-existent SBOM id
    // When requesting its advisory summary
    // Then assert_eq!(resp.status(), StatusCode::NOT_FOUND)
}

/// Verifies that an SBOM with no linked advisories returns all-zero counts.
async fn advisory_summary_no_advisories_returns_zeros(ctx) {
    // Given an SBOM with no advisories
    // When requesting its advisory summary
    // Then body == SeveritySummary::default()  (all zeros)
}

/// Verifies that an advisory linked multiple times to the same SBOM is counted once.
async fn advisory_summary_deduplicates_advisory_links(ctx) {
    // Given one High advisory linked twice to the SBOM via sbom_advisory, plus one Low advisory
    // When requesting its advisory summary
    // Then body == SeveritySummary { critical: 0, high: 1, medium: 0, low: 1, total: 2 }
}
```

If `tests/Cargo.toml` or a test harness file needs to register the new test module (e.g. `[[test]]` or `mod advisory_summary;`), that file is out of scope and gets flagged in Step 9.

Run `cargo test -p <tests-crate>` and `cargo test -p <fundamental-crate>`, resolving crate names via `cargo metadata --no-deps --format-version 1`. Failures are fixed before going on. The same test failing 3 times with the same error is a stop.

## Step 8 – Verify Acceptance Criteria

| Criterion | How it is satisfied |
|---|---|
| GET returns `{critical, high, medium, low, total}` | `SeveritySummary` serialised via `Json`; test 1 |
| 404 for unknown SBOM, consistent with SBOM endpoints | Existence check that reuses SbomService/`AppError::NotFound` semantics; test 2 |
| Unique advisories only | `DISTINCT`/`COUNT(DISTINCT advisory.id)`; test 4 |
| Levels default to 0 | `Default` derive plus fold; test 3 |
| <200 ms for up to 500 advisories | Single aggregate query on the indexed join; verified by timing a seeded 500-advisory SBOM locally, and noted in the PR |

## Step 9 – Self-Verification

- **Scope containment:** `git diff --name-only` should list only the 3 modified and 3 created files. Flag for approval: `docs/api.md` (if an update is proposed), any generated OpenAPI spec, and any test harness registration file.
- **Untracked files:** `git status --short`. Check that the three new files are explicitly staged and nothing else is.
- **Dead parameters:** none expected, since no code is removed.
- **Sensitive patterns:** `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`
- **Doc currency and scope preservation:** check `docs/api.md` and `README.md`. No docs are replaced.
- **Eval coverage:** not applicable (no SKILL.md changes).
- **Cross-section consistency:** paths for `AdvisoryService`, `AdvisorySummary` and `sbom_advisory` agree across Files to Modify and Implementation Notes. ✔
- **Duplication check:** grep for other severity counting or aggregation logic and reuse it if found.
- **CI checks:** run every command from CONVENTIONS.md, plus codegen if defined. Any non-zero exit is a **hard stop** before commit.
- **Rust module tests:** `cargo test -p <fundamental-crate>` and `cargo test -p <tests-crate>`, with the same hard stop.
- **Data-flow trace:** HTTP GET → `Path<Id>` → `AdvisoryService::severity_summary` → SBOM existence check → aggregate query on `sbom_advisory ⋈ advisory` → fold into `SeveritySummary` → `Json` 200, or `AppError` 404/500. Every stage connects to the next.
- **Query scope:** filtered by `sbom_id`. ✔
- **Contract and sibling parity:** handler signature and error type match `get.rs`. Logging and caching middleware match the sibling route builders (apply `tower-http` cache config if siblings do). Read-only cross-module entity access. Callers of `AdvisoryService` follow the same `tx` pattern.

## Step 10 – Commit and Push

```
git add modules/fundamental/src/advisory/model/severity_summary.rs \
        modules/fundamental/src/advisory/model/mod.rs \
        modules/fundamental/src/advisory/service/advisory.rs \
        modules/fundamental/src/advisory/endpoints/severity_summary.rs \
        modules/fundamental/src/advisory/endpoints/mod.rs \
        tests/api/advisory_summary.rs
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(advisory): add SBOM advisory severity summary endpoint

Add AdvisoryService::severity_summary and GET /api/v2/sbom/{id}/advisory-summary
returning deduplicated advisory counts per severity level (critical, high,
medium, low) plus total.

Implements TC-9201"
```

- **Fork detection:** `git remote get-url upstream`.
  - Fork: `gh pr create -R <upstream> --head <fork-owner>:TC-9201 --base main`
  - Not a fork: `gh pr create --base main`
- **PR body:** summary, changes, and test notes, followed by:
  - `Implements [TC-9201](<webUrl>)`
  - `Closes <owner>/<repo>#<n>`, only if the GitHub Issue field was populated

## Step 11 – Update Jira

1. `jira.update_issue(TC-9201, {"customfield_10875": {ADF doc with inlineCard url=<PR-URL>}})`
2. `jira.add_comment(TC-9201, …)` containing the PR link, a summary of changes, and any deviations (e.g. no change to `server/src/main.rs`, and any approved out-of-scope doc or OpenAPI updates). It ends with a rule plus the footnote: "This comment was AI-generated by [sdlc-workflow/implement-task](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0."
3. `jira.transition_issue(TC-9201 → In Review)`
