# Implementation Plan — TC-9201: Add advisory severity aggregation service and endpoint

## Step 0 – Project Configuration validation
CLAUDE.md (claude-md-mock.md) has Repository Registry (trustify-backend, Serena `serena_backend`, path `./`),
Jira Configuration (key TC, Cloud ID, Feature type 10142, PR field customfield_10875,
GitHub Issue field customfield_10747) and Code Intelligence (`mcp__<instance>__<tool>`). PASS.

## Step 1 – Parsed task
- Repository: trustify-backend; Target Branch: `main`
- No Target PR, no Bookend Type -> **default mode** (steps 1–11; branch `TC-9201` from `main`; PR -> `main`).
- All required sections present. Dependencies: none.
- GitHub Issue field (customfield_10747): would be read; if set, `Closes <owner>/<repo>#<n>` goes in the PR body only.

## Steps 1.5 / 2 / 3 (simulated, no external calls)
- Fetch comments, look for `[sdlc-workflow] Description digest:`, compare with `scripts/sha256-digest.py`.
- No dependencies to verify.
- Assign to current user, transition to In Progress.

## Step 4 – Code understanding (via `mcp__serena_backend__*`)
- `get_symbols_overview` on `advisory/service/advisory.rs`, `advisory/endpoints/mod.rs`, `advisory/endpoints/get.rs`, `advisory/model/mod.rs`, `advisory/model/summary.rs`.
- `find_symbol` (body) on `AdvisoryService::fetch`, `get::get`, router fn, `AdvisorySummary`, `entity::sbom_advisory`, `entity::advisory`, `AppError` in `common/src/error.rs`.
- `find_referencing_symbols` on `AdvisoryService` (additive change only — no callers break).
- Read `CONVENTIONS.md` at repo root; extract CI commands for Step 9.
- Reuse search: existing `Severity` enum / severity ordering, aggregate helpers in `common/src/db/query.rs`.
- Docs identified: `README.md`, `docs/api.md` (REST API reference) — not in scope; see Step 9 flags.
- Conventions recorded in `conventions.md`.

## Step 5 – Branch
`git checkout main && git pull && git checkout -b TC-9201`

## Step 6/7 – Files

| # | Action | File | Change | Detail |
|---|---|---|---|---|
| 1 | Create | `modules/fundamental/src/advisory/model/severity_summary.rs` | `SeveritySummary { critical, high, medium, low, total: u64 }` with `Default`, serde, `record()` helper | file-1-model-severity-summary.md |
| 2 | Modify | `modules/fundamental/src/advisory/model/mod.rs` | `pub mod severity_summary;` | file-2-model-mod.md |
| 3 | Modify | `modules/fundamental/src/advisory/service/advisory.rs` | `severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<Option<SeveritySummary>, Error>`: SBOM existence check (None -> 404), single DISTINCT join query over `sbom_advisory`/`advisory`, count by severity | file-3-service-advisory.md |
| 4 | Create | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler: `Path<Id>` -> service -> `Json<SeveritySummary>`; `None` -> `AppError::NotFound`; `.context()` wrapping | file-4-endpoint-severity-summary.md |
| 5 | Modify | `modules/fundamental/src/advisory/endpoints/mod.rs` | `mod severity_summary;` + `.route("/api/v2/sbom/{id}/advisory-summary", get(severity_summary::severity_summary))` | file-5-endpoints-mod.md |
| 6 | Create | `tests/api/advisory_summary.rs` | 4 integration tests: correct counts, 404, all zeros, dedup | file-6-tests-advisory-summary.md |
| — | No change | `server/src/main.rs` | Listed in Files to Modify but explicitly "no changes needed" — routes auto-mount via advisory router | — |

## Step 8 – Acceptance criteria mapping
- Response shape `{critical, high, medium, low, total}` -> `SeveritySummary` serde (file 1); test 1.
- 404 for unknown SBOM -> service returns `None`, handler maps to `AppError::NotFound` like `sbom/endpoints/get.rs`; test 2.
- Unique advisories only -> `DISTINCT` on advisory id in query (file 3); test 4.
- Levels default to 0 -> `#[derive(Default)]`; test 3.
- <200ms for 500 advisories -> single filtered, indexed join query; aggregation in O(n) memory-light loop (or SQL `GROUP BY`). No dedicated perf test required by Test Requirements; would verify manually with a 500-advisory fixture.

## Step 9 – Self-verification (expected results)
1. Scope containment — PASS for files 1–6. Potential FLAGS for approval: `tests/Cargo.toml`/test harness registration of `advisory_summary.rs` if required; `docs/api.md` if it enumerates endpoints.
2. Untracked files — new files 1, 4, 6 are intended; nothing else.
3. Sensitive patterns — PASS (no secrets).
4. Dead parameters — not fired (no removals).
5. Duplication — check for existing severity enum/counting helpers; reuse if found.
6. Documentation currency — new public endpoint: FLAG `docs/api.md` (out of listed scope) for user approval; regenerate OpenAPI spec if CONVENTIONS.md lists a generator (staged automatically).
10. Cross-section references — paths consistent across sections; note `server/src/main.rs` listed under Files to Modify with "no changes" (not edited). Note route `/api/v2/sbom/...` registered in advisory router — verify absolute-path routing.
11. Data-flow trace — HTTP GET -> `Path<Id>` -> `AdvisoryService::severity_summary` -> SBOM lookup + `sbom_advisory` join -> `SeveritySummary` -> `Json` response. Complete.
12. Query scope — query filtered by `sbom_id` with DISTINCT at DB level. PASS.
13. Contract & sibling parity — handler/service signatures match `get`/`fetch`; error handling via `AppError` + `.context()`; read-only, no shared-entity writes.
14. CI checks — `cargo fmt --check`, `cargo clippy -D warnings`, plus CONVENTIONS.md commands.
15. Module tests (Rust) — resolve crates via `cargo metadata`: `cargo test -p trustify-module-fundamental` and the `tests` crate.

Open decisions/assumptions (would confirm with user if ambiguous):
- `total` = sum of the four levels; advisories with missing/unknown severity are excluded from all counts so `total` matches the breakdown.
- Severity strings matched case-insensitively (or by enum variant if `AdvisorySummary.severity` is an enum).

## Step 10 – Commit and PR

```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(advisory): add SBOM advisory severity summary endpoint

Add AdvisoryService::severity_summary and GET /api/v2/sbom/{id}/advisory-summary,
returning counts of unique advisories per severity level (critical, high,
medium, low) plus a total. Returns 404 when the SBOM does not exist and
deduplicates repeated sbom_advisory links by advisory ID.

Includes integration tests for counts, 404, empty SBOM, and deduplication.

Implements TC-9201"
```

- Fork detection via `git remote get-url upstream`; then `gh pr create --base main` (with `-R`/`--head` if fork).
- PR body: summary, `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)`, and `Closes <owner>/<repo>#<n>` only if the GitHub Issue field is set.

## Step 11 – Jira
- Set customfield_10875 to the PR URL (ADF inlineCard).
- Comment: PR link, summary of changes, deviations (none expected; note assumptions above), ending with the implement-task comment footnote.
- Transition to In Review.
