# Implementation Plan — TC-9201: Add advisory severity aggregation service and endpoint

## Step 0 — Project Configuration validation
claude-md-mock.md contains Repository Registry (trustify-backend / serena_backend / `./`), Jira Configuration (Project key TC, Cloud ID, Feature issue type ID 10142, PR field customfield_10875, GitHub Issue field customfield_10747), and Code Intelligence. Validation passes.

## Steps 1–3 — Jira (simulated, no external calls)
- Parsed all required sections: Repository `trustify-backend`, Target Branch `main`, Description, Files to Modify/Create, API Changes, Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies (None). No Target PR, no Bookend Type -> default flow.
- Step 1.5: would fetch comments and verify the `[sdlc-workflow] Description digest:` comment; if absent, warn and continue.
- Step 2: no dependencies.
- Step 3: would assign to current user and transition to In Progress.
- GitHub Issue field (customfield_10747): would read it; if set, add `Closes <owner>/<repo>#<n>` to the PR body only.

## Step 4 — Code understanding (planned Serena calls)
- `mcp__serena_backend__get_symbols_overview` on `advisory/service/advisory.rs`, `advisory/endpoints/mod.rs`, `advisory/endpoints/get.rs`, `advisory/model/mod.rs`, `advisory/model/summary.rs`, `sbom/endpoints/get.rs`, `sbom/service/sbom.rs`.
- `find_symbol(include_body=true)` on `AdvisoryService/fetch`, `AdvisoryService/list`, the `get` handler, the router builder fn in `endpoints/mod.rs`, `AdvisorySummary`, `AppError`.
- Check `entity/src/sbom_advisory.rs` (columns `sbom_id`, `advisory_id`) and `entity/src/advisory.rs` (severity column).
- Symbol deduplication: `search_for_pattern` for `SeveritySummary|severity_summary|severity_count|Severity` across the repo — reuse an existing `Severity` enum if one exists rather than declaring a new one.
- Read `CONVENTIONS.md` at repo root; extract CI commands.
- Docs identified: `README.md`, `docs/api.md` (REST API reference), `docs/architecture.md`.
- Conventions: see `conventions.md`.

## Step 5 — Branch
```
git checkout main && git pull && git checkout -b TC-9201
```

## Step 6/7 — Files

| # | File | Action | Output detail |
|---|---|---|---|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | Create | `file-1-model-severity-summary.md` |
| 2 | `modules/fundamental/src/advisory/model/mod.rs` | Modify | `file-2-model-mod.md` |
| 3 | `modules/fundamental/src/advisory/service/advisory.rs` | Modify | `file-3-service-advisory.md` |
| 4 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | Create | `file-4-endpoint-severity-summary.md` |
| 5 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Modify | `file-5-endpoints-mod.md` |
| 6 | `tests/api/advisory_summary.rs` | Create | `file-6-integration-tests.md` |

Not modified: `server/src/main.rs` — listed in Files to Modify but explicitly "no changes needed"; routes auto-mount through the advisory module's router.

### Summary of changes
1. **SeveritySummary model**: `#[derive(Serialize, Deserialize, Debug, Clone, Default, PartialEq, Eq, ToSchema)] pub struct SeveritySummary { critical: u64, high: u64, medium: u64, low: u64, total: u64 }`. `Default` gives every level 0 when it has no advisories.
2. **model/mod.rs**: add `pub mod severity_summary;` (plus re-export if siblings re-export).
3. **AdvisoryService::severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>**:
   - Verify the SBOM exists (`sbom::Entity::find_by_id`); `None` -> `AppError::NotFound` (404, same as `GET /api/v2/sbom/{id}`).
   - Query `advisory` joined with `sbom_advisory` filtered by `sbom_id`, `SELECT DISTINCT advisory.id, advisory.severity` so duplicate links count once (dedup by advisory ID).
   - Fold the rows into `SeveritySummary`, matching severity case-insensitively; `total` = number of unique advisories. Unknown/None severities count toward `total` only.
   - Single indexed query keeps it well under 200ms for 500 advisories (no N+1).
   - All DB errors wrapped with `.context(...)`.
4. **Endpoint handler** `severity_summary` in `endpoints/severity_summary.rs`: `Path<Id>` extraction, call service inside a read transaction like `get.rs`, return `Json(summary)`. Add a `#[utoipa::path]` annotation if the sibling handlers have one.
5. **endpoints/mod.rs**: `mod severity_summary;` and `.route("/api/v2/sbom/{id}/advisory-summary", get(severity_summary::severity_summary))`, following the existing `Router::new().route(...)` chain and applying the same caching layer the sibling `get` route uses.
6. **Integration tests** (`tests/api/advisory_summary.rs`): four tests, one per Test Requirement, each with a `///` doc comment and Given/When/Then, asserting the full `SeveritySummary` value.

## Step 8 — Acceptance criteria mapping
| Criterion | How satisfied |
|---|---|
| Returns `{critical, high, medium, low, total}` | `SeveritySummary` fields serialized via `Json`; test 1 asserts the full body |
| 404 for unknown SBOM | explicit SBOM existence check -> `AppError::NotFound`; test 2 |
| Unique advisories only | `DISTINCT` on advisory ID in the query; test 4 |
| Levels default to 0 | `SeveritySummary::default()` as fold seed; test 3 |
| < 200ms for 500 advisories | one indexed join query, aggregation in memory over ≤500 rows; no N+1 lookups |

## Step 9 — Self-verification (planned)
- **Scope containment**: diff should contain exactly the 6 files above. All are in Files to Modify/Create.
- **Flag for user approval (out of scope, NOT planned)**:
  - The `tests` crate may need the new file registered (e.g. a `mod advisory_summary;` in a test harness root or a `[[test]]` entry in `tests/Cargo.toml`) depending on how `tests/api/*.rs` are compiled. Not in Files to Modify; would ask before touching.
  - `docs/api.md` documents the REST API; the new endpoint would ideally be added there. Not in scope; flag for the user instead of editing.
  - Generated OpenAPI spec (if CONVENTIONS.md lists a generation command) — generated artifacts would be committed with user approval.
- **Untracked file check**, **sensitive-pattern check** (`git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`), **dead parameter detection** (none — no code removed).
- **Duplication check**: grep for existing severity counting/grouping helpers; reuse if found.
- **CI checks**: run every command from CONVENTIONS.md; hard stop on any non-zero exit.
- **Rust module tests**: resolve crate names via `cargo metadata --no-deps --format-version 1`, then `cargo test -p <fundamental crate>` and `cargo test -p <tests crate>` (names from metadata, e.g. `trustify-module-fundamental`).
- **Data-flow trace**: HTTP GET `/api/v2/sbom/{id}/advisory-summary` -> `Path<Id>` -> `AdvisoryService::severity_summary` -> SBOM existence check -> `sbom_advisory` ⨝ `advisory` DISTINCT query -> fold into `SeveritySummary` -> `Json` response. All stages connected.
- **Query scope**: query filtered by `sbom_advisory.sbom_id = :id` — matches the target scope (single SBOM).
- **Contract & sibling parity**: Contract — new handler matches Axum `Handler` and returns `Result<_, AppError>`; Sibling parity — same transaction handling, `.context()` wrapping, caching layer and OpenAPI annotation as `get.rs`; Cross-module entity — read-only on `sbom_advisory`/`advisory`, no write concerns; Caller-site — service called the same way `get.rs` calls `fetch`.

## Step 10 — Commit message
```
feat(advisory): add SBOM advisory severity summary endpoint

Add AdvisoryService::severity_summary, which counts unique advisories
linked to an SBOM (via the sbom_advisory join table) by severity level,
and expose it as GET /api/v2/sbom/{id}/advisory-summary returning
{ critical, high, medium, low, total }. Unknown SBOM IDs return 404;
duplicate advisory links are counted once; levels with no advisories
default to 0.

Implements TC-9201
```
Command: `git commit --trailer="Assisted-by: Claude Code" -m "<message above>"`

PR: fork detection via `git remote get-url upstream`; then `gh pr create --base main` (or `-R <upstream> --head <fork-owner>:TC-9201 --base main` if fork). PR body includes `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)` (webUrl from the issue) and `Closes <owner>/<repo>#<n>` if the GitHub Issue field is set.

## Step 11 — Jira update (simulated)
- Set `customfield_10875` to the PR URL as an ADF inlineCard.
- Add a comment with PR link, change summary, deviations (none; note `server/src/main.rs` intentionally unchanged and flagged out-of-scope items), ending with the footnote from `shared/comment-footnote.md` (skill `implement-task`).
- Transition to In Review.
