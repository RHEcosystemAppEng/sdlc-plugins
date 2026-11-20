# Implementation Plan — TC-9201

**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend (Serena: `serena_backend`)
**Target Branch**: main -> task branch `TC-9201`

## Pre-flight (Steps 0–3)

- Step 0: Project Configuration in claude-md-mock.md is valid (Repository Registry, Jira Configuration with project key/cloud ID/feature type ID, Code Intelligence present).
- Step 1: All required sections present (Repository, Target Branch, Description, Files to Modify/Create, API Changes, Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies). No Target PR, no Bookend Type -> default flow. GitHub Issue field `customfield_10747` would be read (skip if empty).
- Step 1.5: Would fetch comments and verify `[sdlc-workflow] Description digest:` (warn and continue if absent).
- Step 2: Dependencies: None.
- Step 3: Would assign to current user and transition to In Progress (not executed in eval).
- Step 5: `git checkout main && git pull && git checkout -b TC-9201` (not executed).

## Step 4 — Code understanding (summary)

- Sibling conventions: see `conventions.md`.
- `CONVENTIONS.md` exists at repo root — would be read; its CI check commands (e.g. `cargo fmt --check`, `cargo clippy`, `cargo check`, plus any OpenAPI generation) used in Step 9.
- Reuse: `AdvisorySummary.severity` field, `sbom_advisory` join entity, `AppError` + `.context()`, existing SBOM lookup (`SbomService::fetch` or `entity::sbom::Entity::find_by_id`) for the 404 check.
- Symbol dedup: grep the `fundamental` crate for `SeveritySummary`, `severity_summary`, `Severity` enum before declaring anything. If a `Severity` enum already exists (likely the type of `AdvisorySummary.severity`), match on it instead of string comparisons.
- Docs identified: `docs/api.md` (REST API reference), `README.md`.

## Files

| # | File | Action | Detail file |
|---|------|--------|-------------|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | Create | `file-1-model-severity-summary.md` |
| 2 | `modules/fundamental/src/advisory/model/mod.rs` | Modify | `file-2-model-mod.md` |
| 3 | `modules/fundamental/src/advisory/service/advisory.rs` | Modify | `file-3-service-advisory.md` |
| 4 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | Create | `file-4-endpoint-severity-summary.md` |
| 5 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Modify | `file-5-endpoints-mod.md` |
| 6 | `tests/api/advisory_summary.rs` | Create | `file-6-tests-advisory-summary.md` |
| — | `server/src/main.rs` | **No change** | Listed in Files to Modify but task states routes auto-mount via module registration. Verified intent; left untouched. |

### Change overview

1. **Model** — new `SeveritySummary { critical, high, medium, low, total }` (all `u64`, `Default` derive so every level defaults to 0), with `Serialize/Deserialize/ToSchema`.
2. **Model mod** — `pub mod severity_summary;` (+ re-export if `mod.rs` re-exports siblings).
3. **Service** — `AdvisoryService::severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, Error>`:
   - verifies SBOM exists, returns NotFound otherwise;
   - queries `sbom_advisory` joined to `advisory` filtered by `sbom_id`, selecting **DISTINCT advisory id + severity** (dedup in SQL; single round trip, satisfies <200ms for 500 advisories);
   - folds rows into counts per level; `total` = number of unique advisories counted.
4. **Endpoint** — `severity_summary` handler: `Path<Id>` -> service call -> `Ok(Json(summary))`, `Result<_, AppError>` with `.context()`. utoipa `#[utoipa::path]` annotation matching `get.rs`.
5. **Route** — `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))` in advisory `endpoints/mod.rs` (path form chosen to match how existing routes in that file are written; flagged in conventions.md re: router prefix).
6. **Tests** — four integration tests (valid counts, 404, all zeros, dedup) with doc comments, Given/When/Then, value-based `assert_eq!` on the full struct.

## Acceptance criteria mapping (Step 8)

| Criterion | How satisfied |
|---|---|
| Returns `{critical, high, medium, low, total}` | `SeveritySummary` serialized via Json; test 1 asserts full struct |
| 404 for missing SBOM | Service checks SBOM existence -> `Error::NotFound` -> `AppError` 404; test 2 |
| Unique advisories only | `SELECT DISTINCT` on advisory id in join query; test 4 |
| Levels default to 0 | `#[derive(Default)]` and fold starting from `SeveritySummary::default()`; test 3 |
| < 200ms for 500 advisories | Single indexed join query on `sbom_advisory.sbom_id`, aggregation of ≤500 small rows in memory; no N+1 |

## Step 9 — Self-verification plan

- Scope containment: `git diff --name-only` must list only files 1–6. Possible out-of-scope needs to flag (not planned):
  - `tests/Cargo.toml` — only if test targets are declared explicitly (`[[test]]`) rather than auto-discovered; would ask user.
  - `docs/api.md` — documents REST endpoints; new endpoint arguably needs an entry. Not in Files to Modify, so flagged to user rather than edited.
  - OpenAPI spec file — if CONVENTIONS.md lists an OpenAPI generation command, its output is staged as part of the deliverable.
- Sensitive-pattern check on staged diff.
- CI checks from CONVENTIONS.md (hard stop on any non-zero exit).
- Rust module tests: `cargo test -p trustify-module-fundamental` (crate name resolved via `cargo metadata`) and the tests crate package.
- Data-flow trace: HTTP GET -> `Path<Id>` -> `AdvisoryService::severity_summary` -> SBOM existence check -> join query (`sbom_advisory` x `advisory`) -> fold -> `SeveritySummary` -> Json 200 / AppError 404. Complete.
- Query scope: query filtered by `sbom_advisory.sbom_id = $1` — matches target scope.
- Contract & sibling parity: handler signature/ error handling matches `get.rs`; service method signature matches `fetch`; read-only query so no cross-module write concerns; caller-site matches how other handlers call services with `Transactional::None`.

## Commit message (Step 10)

```
feat(advisory): add SBOM advisory severity summary endpoint

Add AdvisoryService::severity_summary, which counts unique advisories
linked to an SBOM (via sbom_advisory) per severity level, and expose it
as GET /api/v2/sbom/{id}/advisory-summary returning
{ critical, high, medium, low, total }. Returns 404 for unknown SBOMs
and defaults all levels to 0.

Implements TC-9201
```

Committed with: `git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" ...`

## PR (Step 10) and Jira (Step 11) — not executed

- Fork detection via `git remote get-url upstream`; `gh pr create --base main` (or `-R <upstream> --head <fork>:TC-9201`).
- PR body: summary, `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)`, plus `Closes <owner>/<repo>#<n>` if GitHub Issue field set.
- Jira: set `customfield_10875` (ADF inlineCard with PR URL), add comment (PR link, summary, deviations: server/main.rs untouched, docs/api.md flagged) ending with the shared comment footnote, transition to In Review.
