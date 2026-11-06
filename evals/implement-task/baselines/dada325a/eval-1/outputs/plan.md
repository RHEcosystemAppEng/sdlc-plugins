# Implementation Plan — TC-9201: Add advisory severity aggregation service and endpoint

## Step 0 — Project Configuration validation
`claude-md-mock.md` contains everything the skill requires:
- Repository Registry: `trustify-backend | Rust backend service | serena_backend | ./`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID 10142, Git PR field `customfield_10875`,
  GitHub Issue field `customfield_10747`
- Code Intelligence: `mcp__<serena-instance>__<tool>` naming, instance `serena_backend` (rust-analyzer)

Result: PASS, so execution continues.

## Step 1 — Parsed task
| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Target PR | none (default flow: new branch and new PR) |
| Bookend Type | none |
| Dependencies | None |
| GitHub Issue (customfield_10747) | not present in the mock, so skipped silently (no `Closes` line) |
| webUrl | `https://redhat.atlassian.net/browse/TC-9201` (assumed from the Jira response) |

All required sections are present. Nothing is missing, so there's no need to ask for clarification.

## Step 1.5 — Description integrity
In a live run I would fetch the comments and look for `[sdlc-workflow] Description digest:`. If one is found, I'd
compute the digest with `python3 scripts/sha256-digest.py` and compare. The mock has no comments, so the check is
skipped with a warning: "No description digest found — skipping integrity check."

## Step 2 — Dependencies
"Depends on: None", so there's nothing to verify.

## Step 3 — Jira (simulated, not executed)
`jira.user_info()`, then `jira.edit_issue(TC-9201, assignee=<me>)`, then `transition_issue -> In Progress`.

## Step 4 — Code understanding (planned Serena calls on `serena_backend`)
- `get_symbols_overview` on `advisory/service/advisory.rs`, `advisory/endpoints/mod.rs`, `advisory/endpoints/get.rs`,
  `advisory/model/mod.rs`, `advisory/model/summary.rs`
- `find_symbol AdvisoryService/fetch include_body=true` to copy the exact signature, connection and error idiom
- `find_symbol AdvisorySummary include_body=true` to learn the type of the `severity` field
- `find_symbol` on `entity/src/sbom_advisory.rs` (`Model`, `Relation`) and `entity/src/advisory.rs` (the severity column)
- `find_referencing_symbols AdvisoryService` to confirm that adding a method breaks no callers (it's additive)
- `search_for_pattern "severity"` / `"SeveritySummary"` / `"advisory-summary"` for symbol deduplication.
  The expected result is no existing aggregation, so a new struct is created.
- `SbomService::fetch` in `sbom/service/sbom.rs` can be reused for the SBOM-existence check that drives the 404
- Read `CONVENTIONS.md` and extract the CI check commands and any OpenAPI generation command
- Documentation candidates: `README.md`, `docs/api.md` (REST API reference). See "Documentation impact" below.
- Conventions: see `conventions.md`

## Step 5 — Branch (simulated)
```
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 — Changes

### Files to modify
| # | File | Change |
|---|---|---|
| 1 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `AdvisoryService::severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<Option<SeveritySummary>, Error>`: confirm the SBOM exists, then run one grouped `COUNT(DISTINCT advisory.id)` query over `sbom_advisory` joined to `advisory` |
| 2 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Add `mod severity_summary;` and `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get))` (path syntax matched to the existing routes) |
| 3 | `modules/fundamental/src/advisory/model/mod.rs` | Add `pub mod severity_summary;` (plus `pub use` if siblings re-export) |
| — | `server/src/main.rs` | **No change.** The task itself says routes auto-mount through module registration. It is listed in Files to Modify for reference only. |

### Files to create
| # | File | Purpose |
|---|---|---|
| 4 | `modules/fundamental/src/advisory/model/severity_summary.rs` | `SeveritySummary { critical, high, medium, low, total }` response struct, all `u64`, `Default` = zeros |
| 5 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | `GET /api/v2/sbom/{id}/advisory-summary` handler: `Path<Id>`, call service, `None` -> `AppError::NotFound`, return `Json` |
| 6 | `tests/api/advisory_summary.rs` | Integration tests for the four Test Requirements |

The detailed changes are in `file-1-...` through `file-6-...`.

### API change
`GET /api/v2/sbom/{id}/advisory-summary` → `200 {"critical":N,"high":N,"medium":N,"low":N,"total":N}`, or `404` if
the SBOM doesn't exist.

### Reuse / deduplication decisions
- 404 check: reuse the SBOM lookup (`entity::sbom::Entity::find_by_id`, the same query `SbomService::fetch` uses)
  instead of writing new existence logic. `SbomService` is in the same crate (`fundamental`), so no new dependency is needed.
- Severity values: reuse the severity type and column that back `AdvisorySummary.severity`, with no new severity enum.
  If the severity is a string, compare case-insensitively against `critical/high/medium/low` in one `match`.
  Unknown or missing severities count toward `total` but no bucket (documented in a code comment).
- Error idiom: `.context(...)` from `common/src/error.rs`, the same as the siblings.

### Documentation impact
- `docs/api.md` (REST API reference) would normally need the new endpoint. It is **not** in Files to Modify, so it is
  flagged for user approval at Step 9 instead of being edited.
- The OpenAPI spec: if `CONVENTIONS.md` lists an OpenAPI generation command, it is run in Step 9 and the generated
  file is staged as part of the deliverable. The handler gets a `#[utoipa::path(...)]` annotation if siblings use one.

## Step 7 — Tests (`tests/api/advisory_summary.rs`)
1. `severity_summary_returns_counts_for_known_advisories`: 2 critical, 1 high, 3 medium, 0 low → exact struct equality
2. `severity_summary_returns_404_for_unknown_sbom`: random ID → `StatusCode::NOT_FOUND`
3. `severity_summary_returns_zeros_when_no_advisories`: SBOM without advisories → `SeveritySummary::default()`
4. `severity_summary_deduplicates_advisory_links`: the same advisory linked twice → counted once

Each test has a `///` doc comment and Given/When/Then sections, and asserts on the full deserialized body.
Run with `cargo test -p tests` (or `cargo nextest run -p <crate>`), resolving package names via `cargo metadata`.

## Step 8 — Acceptance criteria mapping
| AC | How it's satisfied |
|---|---|
| Returns `{critical, high, medium, low, total}` | `SeveritySummary` serialized via `Json`. Test 1. |
| 404 for missing SBOM | Service returns `None`, the handler maps it to `AppError::NotFound`. Test 2. |
| Unique advisories only | `COUNT(DISTINCT advisory.id)` grouped by severity. Test 4. |
| Levels default to 0 | `#[derive(Default)]`, and only matched buckets are set. Test 3. |
| < 200ms for 500 advisories | One aggregate query (`GROUP BY severity`) plus one PK lookup, with no N+1 and no loading of rows into memory. Relies on the indexes on `sbom_advisory.sbom_id` and `advisory.id` (to verify in the migration). |

## Step 9 — Self-verification plan
- **Scope containment:** the expected `git diff --name-only` is exactly files 1–6. `server/src/main.rs` is
  intentionally untouched.
  - Flag 1: `docs/api.md` would need the endpoint documented, but it's out of scope, so I'd ask the user.
  - Flag 2: `tests/Cargo.toml` (or a `tests/api/main.rs` / `mod` list) may need an entry for the new test file
    `advisory_summary.rs` so it compiles. That depends on how `sbom.rs` and `advisory.rs` are wired. It's out of
    scope, so I'd ask the user before touching it.
- **Untracked files:** check `git status --short` for `??` entries near the modified dirs. Only the three new files
  are expected.
- **Dead parameters:** not applicable, since no code is removed.
- **Sensitive patterns:** grep the staged diff. None expected.
- **CI checks:** run every command from the `CONVENTIONS.md` CI section (e.g. `cargo fmt --check`,
  `cargo clippy --all-targets -- -D warnings`) and any OpenAPI generation. Any non-zero exit is a hard stop.
- **Rust module tests:** `cargo test -p trustify-module-fundamental` and `cargo test -p <tests crate>`, with names
  resolved via `cargo metadata --no-deps --format-version 1`.
- **Data-flow trace:** HTTP `GET` → `Path<Id>` → `AdvisoryService::severity_summary` → SBOM lookup (None → 404) →
  grouped count query → fold into `SeveritySummary` → `Json` 200. Every stage connects (complete).
- **Query scope:** the aggregate is filtered by `sbom_advisory.sbom_id = $1`, never a full scan of all advisories.
- **Contract & sibling parity:**
  - Contract: no trait is implemented, so N/A. Serialize/ToSchema derives match the siblings.
  - Sibling parity: same `Transactional` parameter, `.context()` wrapping, `Json` return and caching layer as `get.rs`.
  - Cross-module entity: read-only, with no writes to shared entities.
  - Caller-site: the handler calls the service the same way `get.rs` calls `fetch`.
- **Duplication:** grep for `severity` aggregation or `COUNT(DISTINCT` in `modules/`. None expected.

## Step 10 — Commit (simulated)
```
git add modules/fundamental/src/advisory/service/advisory.rs \
        modules/fundamental/src/advisory/endpoints/mod.rs \
        modules/fundamental/src/advisory/model/mod.rs \
        modules/fundamental/src/advisory/model/severity_summary.rs \
        modules/fundamental/src/advisory/endpoints/severity_summary.rs \
        tests/api/advisory_summary.rs
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(advisory): add SBOM advisory severity summary endpoint

Add AdvisoryService::severity_summary and GET /api/v2/sbom/{id}/advisory-summary,
returning counts of unique advisories per severity level (critical, high,
medium, low) plus a total. Returns 404 when the SBOM does not exist.
Counting is done in a single grouped COUNT(DISTINCT) query.

Implements TC-9201"
git push -u origin TC-9201
```
Fork detection: run `git remote get-url upstream`. If it exists, use
`gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9201 --base main`. Otherwise use `gh pr create --base main`.

PR title: `feat(advisory): add SBOM advisory severity summary endpoint`
PR body:
```
## Summary
- Add `SeveritySummary` model and `AdvisoryService::severity_summary`
- Add `GET /api/v2/sbom/{id}/advisory-summary` (404 for unknown SBOM, deduplicated counts)
- Add integration tests in `tests/api/advisory_summary.rs`

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
```
(No `Closes` line, because the GitHub Issue field is empty.)

## Step 11 — Jira (simulated)
- `jira.update_issue(TC-9201, {"customfield_10875": {ADF doc with inlineCard <PR-URL>}})`
- `jira.add_comment`: the PR link, a summary of the changes, deviations (`server/src/main.rs` untouched as the task
  stated, plus any approved out-of-scope flags), and the footnote from `shared/comment-footnote.md` with skill name `implement-task`
- `jira.transition_issue -> In Review`
