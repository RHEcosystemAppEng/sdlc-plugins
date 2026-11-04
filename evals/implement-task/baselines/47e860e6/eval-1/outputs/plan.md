# Implementation Plan — TC-9201

**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend (Serena: `serena_backend`)
**Target Branch**: `main`
**Branch**: `TC-9201` (created from latest `main`)
**Target PR / Bookend**: none — default flow

## Pre-flight (Steps 0–3, simulated)

- Step 0: Project Configuration in `claude-md-mock.md` is valid (Repository Registry, Jira Configuration with project key/Cloud ID/feature type ID, Code Intelligence present).
- Step 1: All required sections present (Repository, Target Branch, Description, Files to Modify/Create, API Changes, Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies). GitHub Issue field `customfield_10747` configured — would read it and add `Closes owner/repo#N` to the PR body if populated.
- Step 1.5: Would fetch comments, locate `[sdlc-workflow] Description digest:` and compare with `scripts/sha256-digest.py`; proceed if matching / absent.
- Step 2: Dependencies = None — nothing to verify.
- Step 3: Would assign to current user and transition to In Progress.
- Step 4: Code inspection via `mcp__serena_backend__*`; conventions recorded in `conventions.md`. `CONVENTIONS.md` exists at repo root — read it and extract CI check commands for Step 9.

## Files

| # | File | Action | Detail file |
|---|------|--------|-------------|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | Create | `file-1-model-severity-summary.md` |
| 2 | `modules/fundamental/src/advisory/model/mod.rs` | Modify | `file-2-model-mod-registration.md` |
| 3 | `modules/fundamental/src/advisory/service/advisory.rs` | Modify | `file-3-service-severity-summary.md` |
| 4 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | Create | `file-4-endpoint-handler.md` |
| 5 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Modify | `file-5-endpoints-mod-route.md` |
| 6 | `tests/api/advisory_summary.rs` | Create | `file-6-integration-tests.md` |

**Not modified**: `server/src/main.rs` — listed in Files to Modify but explicitly "no changes needed"; routes auto-mount via the advisory module router.

## Change summary

1. **Model** — `SeveritySummary { critical, high, medium, low, total }` (all `u64`, `Default` derives zeros), serializable, documented.
2. **Model registration** — `pub mod severity_summary;` in `advisory/model/mod.rs`.
3. **Service** — `AdvisoryService::severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<Option<SeveritySummary>, Error>`:
   - Verify SBOM exists (`sbom::Entity::find_by_id`); return `Ok(None)` if not (-> 404).
   - Query `sbom_advisory` join (`entity/src/sbom_advisory.rs`) for the SBOM, join `advisory`, select **distinct advisory IDs** with their severity (dedup per AC).
   - Count per severity level into `SeveritySummary` (unknown/absent severity ignored for levels but noted; `total` = sum of the four levels — see note), starting from `SeveritySummary::default()` so all levels default to 0.
   - Single aggregated query (`SELECT severity, COUNT(DISTINCT advisory.id) ... GROUP BY severity`) to keep response < 200ms for 500 advisories.
   - Errors wrapped with `.context(...)`.
4. **Handler** — `get(State(service), Path(id): Path<Id>) -> Result<Json<SeveritySummary>, AppError>`; maps `None` -> `AppError::NotFound`, mirrors `advisory/endpoints/get.rs`.
5. **Route** — `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get))` plus `mod severity_summary;` in `advisory/endpoints/mod.rs`, using the same router builder/caching chain as siblings.
6. **Tests** — four integration tests (known counts, 404, all zeros, dedup) with value-based `assert_eq!` on the full struct, `///` docs and Given/When/Then.

## Reuse / deduplication checks

- Search for existing severity enum/constants (`Severity`, `SEVERITY_ORDER`, severity string mapping) in `modules/fundamental` and `entity` — reuse the type behind `AdvisorySummary.severity` rather than introducing new string constants.
- Reuse the SBOM-existence lookup pattern from `SbomService::fetch` (or call it if accessible) instead of writing a new one.
- `common/src/db/query.rs` checked — pagination/filter helpers not applicable to an aggregate.

## Verification (Steps 7–9)

- `cargo test -p trustify-fundamental` (package name resolved via `cargo metadata`) and the tests crate (`cargo test -p <tests-package> advisory_summary`).
- All CI commands extracted from `CONVENTIONS.md` (e.g. `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`) — hard stop on any non-zero exit. Run any OpenAPI-generation command listed there and commit the regenerated spec if it changes.
- Scope containment: `git diff --name-only` must equal the 6 files above.
- Data flow: HTTP GET -> `Path<Id>` -> `AdvisoryService::severity_summary` -> SBOM check -> distinct advisory/severity aggregation -> `SeveritySummary` -> `Json` response. Complete.
- Contract & sibling parity: handler signature/error mapping/caching identical to `get.rs`; service signature matches `fetch`/`list`.

## Acceptance criteria mapping

| AC | How satisfied |
|----|---------------|
| Returns `{critical, high, medium, low, total}` | `SeveritySummary` serialized via `Json` |
| 404 for unknown SBOM | SBOM existence check -> `None` -> `AppError::NotFound` |
| Unique advisories only | `COUNT(DISTINCT advisory.id)` / distinct select |
| Levels default to 0 | `SeveritySummary::default()` + fill from grouped rows |
| <200ms for 500 advisories | single grouped DB query, no N+1, uses indexed `sbom_advisory.sbom_id` |

## Items to flag to the user

- **Route prefix**: endpoint path is under `/api/v2/sbom/...` but registered in the advisory router (which serves `/api/v2/advisory`). Confirm the advisory router is not nested under a prefix; otherwise the absolute path must be adjusted.
- **`total` semantics**: defined as count of unique advisories linked to the SBOM. If advisories with unknown/none severity exist, `total` may exceed the sum of the four levels — plan uses unique-advisory count; confirm.
- **Out-of-scope candidates (not changed, flagged only)**: `tests/Cargo.toml` / test harness module list may need an entry for `advisory_summary.rs` if tests are not auto-discovered; `docs/api.md` (REST API reference) should document the new endpoint. Both require user approval per scope containment.

## Commit message

```
feat(advisory): add SBOM advisory severity summary endpoint

Add AdvisoryService::severity_summary that aggregates unique advisories
linked to an SBOM (via sbom_advisory) into per-severity counts, and expose
it as GET /api/v2/sbom/{id}/advisory-summary returning
{ critical, high, medium, low, total }. Returns 404 for unknown SBOMs;
all levels default to 0.

Implements TC-9201
```

Command: `git commit --trailer="Assisted-by: Claude Code" -m "<message above>"`

## PR (Step 10) and Jira (Step 11)

- `git remote get-url upstream` for fork detection; `gh pr create --base main` (or `-R <upstream> --head <fork-owner>:TC-9201 --base main` if fork).
- PR body includes `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)` and `Closes <owner>/<repo>#<n>` if the GitHub Issue field is set.
- Jira: set `customfield_10875` with ADF inlineCard of PR URL, add comment (PR link, summary, deviations — route-prefix note, untouched main.rs) ending with the implement-task footnote, transition to In Review.
