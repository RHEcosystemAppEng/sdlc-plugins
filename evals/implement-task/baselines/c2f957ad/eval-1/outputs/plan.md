# Implementation Plan — TC-9201: Add advisory severity aggregation service and endpoint

Skill: `/sdlc-workflow:implement-task` (executed in plan-only mode; no repo edits, no Jira/git/Serena calls).

## Step 0 — Project Configuration validation
`claude-md-mock.md` contains Repository Registry (trustify-backend -> `serena_backend`, path `./`),
Jira Configuration (Project key TC, Cloud ID, Feature issue type ID 10142, PR field
`customfield_10875`, GitHub Issue field `customfield_10747`) and Code Intelligence. **PASS.**

## Step 1 — Parsed task
- Repository: trustify-backend; **Target Branch: `main`**; no Target PR; no Bookend Type -> default flow.
- All required sections present (Repository, Target Branch, Description, Files to Modify/Create,
  API Changes, Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies).
- GitHub Issue field `customfield_10747`: would be read from the issue; if set, add
  `Closes <owner>/<repo>#<n>` to the PR body only.
- webUrl: `https://redhat.atlassian.net/browse/TC-9201` (captured from the issue response).

## Step 1.5 — Description digest
Would fetch comments, find latest `[sdlc-workflow] Description digest:` comment, compute digest with
`scripts/sha256-digest.py` and compare. (Not executed — mock data, no comments available -> would log
"No description digest found — skipping integrity check.")

## Step 2 — Dependencies
"Depends on: None" -> nothing to verify.

## Step 3 — Jira
`jira.user_info()` -> assign TC-9201 to current user -> transition to **In Progress**.

## Step 4 — Code understanding (serena_backend)
- `get_symbols_overview` on `advisory/service/advisory.rs`, `advisory/endpoints/mod.rs`,
  `advisory/endpoints/get.rs`, `advisory/model/mod.rs`, `advisory/model/summary.rs`,
  `entity/src/sbom_advisory.rs`, `entity/src/sbom.rs`, `common/src/error.rs`.
- `find_symbol(include_body=true)` for `AdvisoryService::fetch`, `AdvisoryService::list`,
  `AdvisorySummary`, and the advisory `get` handler; `find_referencing_symbols` on `AdvisoryService`
  (only additive change — no existing signatures modified, so backward compatible).
- Reuse search: `search_for_pattern` for `severity`, `count`, `group_by`, `SeveritySummary`,
  `advisory-summary` to avoid duplicating an existing aggregation helper or symbol. Plan assumes none found.
- `CONVENTIONS.md` at repo root: read and follow; extract CI check commands (expected: `cargo fmt --check`,
  `cargo clippy --all-targets -- -D warnings`, `cargo check`) and any OpenAPI generation command
  (if present, run it in Step 9 and commit the regenerated spec).
- Documentation identified: `README.md`, `docs/api.md` (REST API reference), `CONVENTIONS.md`.
- Conventions: see `conventions.md`.

## Step 5 — Branch
```
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 — Changes

### Files to Create
| # | File | Purpose | Detail |
|---|---|---|---|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | `SeveritySummary` response struct | `file-1-severity-summary-model.md` |
| 2 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for `/api/v2/sbom/{id}/advisory-summary` | `file-2-severity-summary-endpoint.md` |
| 3 | `tests/api/advisory_summary.rs` | Integration tests | `file-3-advisory-summary-tests.md` |

### Files to Modify
| # | File | Change | Detail |
|---|---|---|---|
| 4 | `modules/fundamental/src/advisory/model/mod.rs` | add `pub mod severity_summary;` | `file-4-model-mod.md` |
| 5 | `modules/fundamental/src/advisory/service/advisory.rs` | add `AdvisoryService::severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>)` | `file-5-advisory-service.md` |
| 6 | `modules/fundamental/src/advisory/endpoints/mod.rs` | declare `mod severity_summary;` and register `.route("/api/v2/sbom/{id}/advisory-summary", get(severity_summary::get))` | `file-6-endpoints-mod.md` |
| — | `server/src/main.rs` | **No change** — task states routes auto-mount via module registration. Verified (would verify) that the advisory router is already mounted. | n/a |

### Summary of behavior
1. Handler extracts `Path<Id>`, calls `AdvisoryService::severity_summary(id, Transactional::None)`.
2. Service checks that the SBOM exists (`sbom::Entity::find_by_id`); if not -> returns `Ok(None)`;
   handler maps to `AppError::NotFound` (404) consistent with `GET /api/v2/sbom/{id}`.
3. Service selects **distinct** advisory IDs + severity via `sbom_advisory` join -> `advisory`
   (`SELECT DISTINCT advisory.id, advisory.severity ... WHERE sbom_advisory.sbom_id = $1`), so duplicate
   links are counted once. Single aggregated query, indexed on `sbom_advisory.sbom_id` -> meets the
   <200ms target for 500 advisories (no N+1).
4. Counts bucketed case-insensitively into critical/high/medium/low; all start at 0 (`Default`).
5. `total` = number of unique advisories counted in the four buckets (critical+high+medium+low).
   Advisories with missing/unrecognized severity are excluded from all counts — see "Open points".
6. Returns `Json(SeveritySummary)`; errors wrapped with `.context(...)` -> `AppError`.

### Code quality
- `///` doc comments on `SeveritySummary`, each field, `severity_summary` service method, and the handler.
- Defensive handling: `severity` is `Option` on the entity — `None` handled explicitly, no `unwrap()`.
- No new constants duplicating existing severity enums: if a `Severity` enum exists in `advisory/model`
  or `entity`, reuse it for bucketing instead of string matching (symbol-dedup search in Step 4).

### Documentation impact
`docs/api.md` documents REST endpoints and would normally get the new endpoint, but it is **not** listed
in Files to Modify -> flagged in Step 9 scope containment for user approval rather than edited.

## Step 7 — Tests (`tests/api/advisory_summary.rs`)
1. `valid_sbom_returns_correct_severity_counts` — known advisories -> exact `SeveritySummary` value.
2. `nonexistent_sbom_returns_not_found` — 404.
3. `sbom_without_advisories_returns_all_zeros` — `SeveritySummary::default()`.
4. `duplicate_advisory_links_are_deduplicated` — same advisory linked twice counted once.
All with `///` docs, Given/When/Then comments, value-based `assert_eq!` on the whole struct.
Run `cargo test -p <tests crate>` (resolved via `cargo metadata`).

## Step 8 — Acceptance criteria mapping
| Criterion | Satisfied by |
|---|---|
| Returns `{critical, high, medium, low, total}` | `SeveritySummary` serde shape; test 1 |
| 404 for unknown SBOM | SBOM existence check -> `AppError::NotFound`; test 2 |
| Unique advisories only | `DISTINCT advisory.id` in query; test 4 |
| Levels default to 0 | `#[derive(Default)]` + bucketing; test 3 |
| <200ms for 500 advisories | single DISTINCT join query, no per-advisory loads, in-memory bucketing O(n) |

## Step 9 — Self-verification
- Scope containment: expected diff = files 1–6 only. **Flags for user approval (not done unilaterally):**
  - `tests/api/advisory_summary.rs` may need registration (e.g., `mod advisory_summary;` in a tests entry
    file or a `[[test]]` entry in `tests/Cargo.toml`) depending on how the tests crate discovers files.
  - `docs/api.md` update for the new endpoint.
  - OpenAPI spec file, if CONVENTIONS.md lists a generation command that regenerates it.
- Untracked file check, sensitive-pattern grep, dead-parameter check (none — purely additive).
- CI checks from CONVENTIONS.md (hard stop on any failure) + `cargo test -p trustify-module-fundamental`
  and the tests crate.
- Data-flow trace: HTTP `GET` -> `Path<Id>` -> service -> SBOM existence check -> DISTINCT join query
  -> bucketing -> `SeveritySummary` -> `Json` response. Complete.
- Query scope: query filtered by `sbom_id` at the DB (not loading all advisories). OK.
- Contract & sibling parity: no trait implemented; handler mirrors `advisory/endpoints/get.rs`
  (State + Path, `.context()`, NotFound mapping, caching layer, utoipa annotation if siblings use it);
  cross-module entity: read-only on `sbom_advisory`/`advisory`, no write concerns; caller-site: service
  called with `Transactional::None` like siblings.

## Step 10 — Commit and PR
Commit message:
```
feat(advisory): add SBOM advisory severity summary endpoint

Add AdvisoryService::severity_summary, which counts unique advisories
linked to an SBOM (via sbom_advisory) by severity level, and expose it
as GET /api/v2/sbom/{id}/advisory-summary returning
{ critical, high, medium, low, total }. Returns 404 when the SBOM does
not exist. Includes integration tests.

Implements TC-9201
```
Command:
```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "<message above>"
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add SBOM advisory severity summary endpoint" --body "..."
```
(If `git remote get-url upstream` succeeds -> `gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9201 --base main`.)
PR body includes `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)` and, if
`customfield_10747` is set, `Closes <owner>/<repo>#<n>`.

## Step 11 — Jira update
- Set `customfield_10875` to the PR URL using ADF `inlineCard`.
- Add comment: PR link, summary of changes, deviations (none; open points below), ending with the footnote
  rule + "This comment was AI-generated by sdlc-workflow/implement-task v0.14.0."
- Transition TC-9201 -> **In Review**.

## Open points / deviations to confirm
1. **`total` semantics**: implemented as sum of the four buckets; advisories with null/unknown severity
   are not counted. Alternative: `total` = all unique advisories. Would ask reviewer to confirm.
2. **Route ownership**: the path lives under `/api/v2/sbom/...` but is registered in the advisory
   module's router as the task instructs (Files to Modify lists `advisory/endpoints/mod.rs`).
3. `server/src/main.rs` listed in Files to Modify with "no changes needed" — left untouched.
