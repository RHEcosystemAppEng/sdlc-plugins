# Implementation Plan: TC-9201 — Add advisory severity aggregation service and endpoint

Skill: `/sdlc-workflow:implement-task` (this is a simulated run, so no repository files are changed
and no Jira, git or Serena calls are made).

## Step 0 – Project Configuration validation
`claude-md-mock.md` contains all the required sections, so execution continues:
- Repository Registry: `trustify-backend` -> Serena instance `serena_backend`, path `./`
- Jira Configuration: project key TC, Cloud ID, Feature issue type ID 10142, Git PR field
  `customfield_10875`, GitHub Issue field `customfield_10747`
- Code Intelligence: naming convention `mcp__<instance>__<tool>`. Limitation: rust-analyzer can
  take 30–60 s to index on first use.

## Step 1 – Parsed task
| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Target PR / Bookend Type / Review Context | none (default flow) |
| Dependencies | None (Step 2 has nothing to check) |
| GitHub Issue (`customfield_10747`) | would be read from the issue. If set, the PR body gets `Closes <owner>/<repo>#<n>` |

All required sections are present, so there are no gaps to ask about.

## Steps 1.5 / 2 / 3 – Simulated Jira actions (not executed)
- Step 1.5: fetch comments, find the latest `[sdlc-workflow] Description digest:` comment, and
  compare it with `python3 scripts/sha256-digest.py`. If none is found, warn and continue.
- Step 2: no dependencies.
- Step 3: `jira.user_info()`, assign TC-9201 to the current user, and transition it to
  **In Progress**.

## Step 4 – Code understanding (simulated, via `serena_backend`)
- `get_symbols_overview` on `advisory/service/advisory.rs`, `advisory/endpoints/{mod,get}.rs` and
  `advisory/model/{mod,summary}.rs`.
- `find_symbol(include_body=true)` on `AdvisoryService::fetch`/`list`, the `get` handler,
  `AdvisorySummary`, `sbom_advisory::Model`/`Relation` and `AppError`.
- `search_for_pattern("severity")` and `search_for_pattern("SeveritySummary")` to deduplicate
  symbols and find helpers to reuse.
- Read `CONVENTIONS.md` at the repo root and extract its CI check commands for Step 9.
- Documentation files found: `README.md`, `docs/api.md` (REST API reference),
  `docs/architecture.md`.
- Sibling conventions: see `conventions.md`.

## Step 5 – Branch
```
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6/7 – Files

### Files to Create
| # | File | Change | Detail |
|---|---|---|---|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | `SeveritySummary { critical, high, medium, low, total }` (all `u64`, derives `Default`), plus a `record(Option<&str>)` helper that matches severity case-insensitively | `file-1-model-severity-summary.md` |
| 4 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | `get_severity_summary` handler: `Path<Id>` -> `service.severity_summary` -> `Json`. A `None` result becomes a 404 `AppError` with `.context()`. Has a `utoipa::path` annotation | `file-4-endpoint-severity-summary-handler.md` |
| 6 | `tests/api/advisory_summary.rs` | 4 integration tests: correct counts, 404 for an unknown SBOM, all zeros, dedup of duplicate links | `file-6-tests-advisory-summary.md` |

### Files to Modify
| # | File | Change | Detail |
|---|---|---|---|
| 2 | `modules/fundamental/src/advisory/model/mod.rs` | add `pub mod severity_summary;` | `file-2-model-mod-registration.md` |
| 3 | `modules/fundamental/src/advisory/service/advisory.rs` | add `AdvisoryService::severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<Option<SeveritySummary>, Error>`. It checks the SBOM exists, then runs a `DISTINCT (advisory.id, severity)` query over the `sbom_advisory` join and folds the rows into `SeveritySummary` | `file-3-service-severity-summary-method.md` |
| 5 | `modules/fundamental/src/advisory/endpoints/mod.rs` | add `mod severity_summary;` and `.route("/api/v2/sbom/{id}/advisory-summary", get(severity_summary::get_severity_summary))`, plus an OpenAPI path registration if the module has one | `file-5-endpoints-mod-route-registration.md` |
| — | `server/src/main.rs` | **No change.** The task says routes auto-mount through the module registration | — |

### API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` (NEW) returns
  `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`.

### Documentation impact
- `docs/api.md` (REST API reference) would normally get the new endpoint. The task has no
  Documentation Updates section and the file is not in Files to Modify, so it is **flagged for
  user approval** in Step 9 rather than edited.

## Step 8 – Acceptance criteria mapping
| Criterion | How it is satisfied |
|---|---|
| Returns `{critical, high, medium, low, total}` | `SeveritySummary` serialized via `Json`. Tested in test 1 |
| 404 for an unknown SBOM | the service returns `None`, which the handler turns into the not-found `AppError` (same as `GET /api/v2/sbom/{id}`). Tested in test 2 |
| Counts unique advisories only | `SELECT DISTINCT advisory.id, severity`. Tested in test 4 |
| Levels default to 0 | `#[derive(Default)]` on `SeveritySummary`. Tested in test 3 |
| < 200 ms for 500 advisories | one indexed existence lookup plus one filtered join query, deduplicated in SQL, with no N+1 queries. Would be checked by timing test 1 with a 500-advisory fixture locally |

## Step 9 – Self-verification plan
- **Scope containment:** the expected diff is files 1–6 only. Flagged for approval, not edited:
  `docs/api.md`, and `tests/Cargo.toml` or the test aggregator module if the new test file needs
  registering.
- **Convention conflicts flagged:** the `/api/v2/sbom/...` route is registered in the advisory
  router, as the task explicitly asks. The user would be asked to confirm.
- **Sensitive pattern check:** none expected.
- **CI checks:** run every command from `CONVENTIONS.md` (e.g. `cargo fmt --check`,
  `cargo clippy --all-targets -- -D warnings`, `cargo check`). Any non-zero exit is a hard stop.
  Also run any OpenAPI generation command and commit its output.
- **Rust module tests:** resolve packages via `cargo metadata --no-deps --format-version 1`, then
  `cargo test -p trustify-module-fundamental` and `cargo test -p <tests crate>`.
- **Data-flow trace:** HTTP `GET` -> `Path<Id>` -> `AdvisoryService::severity_summary` -> SBOM
  existence check -> `sbom_advisory` ⨝ `advisory` DISTINCT query -> fold into `SeveritySummary`
  -> `Json` response, or 404. Every stage connects.
- **Contract and sibling parity:** handler signature, `AppError`/`.context()` and caching layer
  match the `get.rs` siblings. The service signature matches `fetch`/`list`. The query is
  read-only, so there are no cross-module write concerns.
- **Duplication check:** grep for existing severity counting or aggregation before finalizing.

## Step 10 – Commit message

```
feat(advisory): add SBOM advisory severity summary endpoint

Add AdvisoryService::severity_summary, which counts the unique
advisories linked to an SBOM per severity level (critical, high,
medium, low) plus a total. Advisories are deduplicated by ID through the
sbom_advisory join table.

Expose it as GET /api/v2/sbom/{id}/advisory-summary, returning a
SeveritySummary response. It returns 404 when the SBOM does not exist,
and severity levels with no advisories default to 0.

Include integration tests for counts, an unknown SBOM, an SBOM with no
advisories, and duplicate advisory links.

Implements TC-9201
```

Command:
```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "<message above>"
```

PR (no fork assumed; `git remote get-url upstream` checked first):
`gh pr create --base main --title "feat(advisory): add SBOM advisory severity summary endpoint" ...`.
The body includes `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)` (the
`webUrl` from Step 1) and a `Closes <owner>/<repo>#<n>` line if the GitHub Issue field is set.

## Step 11 – Jira update (simulated)
- Set `customfield_10875` to the PR URL as an ADF `inlineCard`.
- Add a comment with the PR link, a summary of changes, and deviations: `server/src/main.rs` was
  left unchanged, and the flagged doc and test-registration items. The comment ends with the
  `implement-task` comment footnote.
- Transition TC-9201 to **In Review**.
