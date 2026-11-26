# Implementation Plan — TC-9201: Add advisory severity aggregation service and endpoint

Skill: `/sdlc-workflow:implement-task` (SKILL.md followed step by step; external calls are
simulated and described rather than executed).

---

## Step 0 – Project Configuration validation

From `claude-md-mock.md` under `# Project Configuration`:

| Section | Status |
|---|---|
| Repository Registry | Present — `trustify-backend`, Serena instance `serena_backend`, path `./` |
| Jira Configuration | Present — Project key `TC`, Cloud ID `2b9e35e3-...`, Feature issue type ID `10142`, Git PR field `customfield_10875`, GitHub Issue field `customfield_10747` |
| Code Intelligence | Present — naming convention `mcp__<serena-instance>__<tool>`; limitation: rust-analyzer takes 30-60 s to index on first use |

Result: validation passes, so execution continues.

## Step 0.5 – Jira access

Would try the Atlassian MCP first and fall back to the REST API (`scripts/jira-client.py`) only
if the user agreed. **Not called in this eval.**

## Step 1 – Fetch and parse the task (`jira.get_issue("TC-9201")`, simulated from task-standard.md)

| Section | Parsed value |
|---|---|
| Repository | `trustify-backend` |
| **Target Branch** | **`main`**. This is the base for the new branch and the PR's `--base` |
| Description | Add a service method and a REST endpoint that count advisory severities (Critical/High/Medium/Low/total) for one SBOM |
| Files to Modify | `advisory/service/advisory.rs`, `advisory/endpoints/mod.rs`, `advisory/model/mod.rs` (`server/src/main.rs` is listed as "no changes needed", so it is **not** modified) |
| Files to Create | `advisory/model/severity_summary.rs`, `advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs` |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary`. NEW endpoint, returns `{critical, high, medium, low, total}` |
| Implementation Notes | Follow `endpoints/get.rs`; service method signature `(&self, sbom_id: Id, tx: &Transactional<'_>)`; use the `sbom_advisory` join table; count on `AdvisorySummary.severity`; `Router::new().route(...)`; `AppError` + `.context()` |
| Acceptance Criteria | 5 items (see Step 8) |
| Test Requirements | 4 tests |
| Target PR | absent. Default flow (new branch + new PR) |
| Review Context | absent |
| Bookend Type | absent. Normal implementation flow |
| Dependencies | None |

- `webUrl` would come from the API response, e.g. `https://redhat.atlassian.net/browse/TC-9201`, for the PR "Implements" link.
- GitHub Issue field `customfield_10747`: would read the field and parse `owner/repo#number` for a `Closes` line in the PR body. The mock has no value, so this is skipped silently.
- All required sections are present, so there is no need to stop for clarification.

## Step 1.5 – Description integrity (digest check)

- Would call `jira.get_issue_comments("TC-9201")` and look for comments starting with
  `[sdlc-workflow] Description digest:`, using the most recent one if several exist.
- **No digest comment is available in the mock data.** Per `shared/description-digest-protocol.md`
  (backward compatibility), log this warning and **proceed without blocking**:
  > "No description digest found — skipping integrity check. This task may have been created before digest tracking was introduced."
- If a digest existed, the plan would be: compute it with `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`,
  compare the format tags, then compare the hex digests. On a mismatch, ask the user whether to proceed or stop.

## Step 2 – Dependencies

"Depends on: None", so there is nothing to check.

## Step 3 – Assign and transition (simulated)

`jira.user_info()` → `jira.edit_issue(TC-9201, assignee=<me>)` → `jira.transition_issue → In Progress`. **Not called.**

## Step 4 – Understand the code (Serena `serena_backend`; fallback Read/Grep/Glob)

Code I would inspect **before** changing anything:

| File | Tool calls | Purpose |
|---|---|---|
| `modules/fundamental/src/advisory/endpoints/get.rs` | `get_symbols_overview`, `find_symbol(include_body=true)` on the handler | Reference pattern: `Path<Id>` extraction, how the service is injected (`State`/`web::Data`), `Result<Json<T>, AppError>` return |
| `modules/fundamental/src/advisory/endpoints/mod.rs` | `get_symbols_overview`, `find_symbol` on the router fn | How routes are composed (`Router::new().route(...)`), caching layer setup |
| `modules/fundamental/src/advisory/service/advisory.rs` | `get_symbols_overview`, `find_symbol("AdvisoryService/fetch", include_body=true)`, `find_symbol("AdvisoryService/list", ...)` | Method signature (`&self, ..., tx: &Transactional<'_>`), connection acquisition, `.context()` usage |
| `modules/fundamental/src/advisory/model/summary.rs` | `find_symbol("AdvisorySummary", include_body=true)` | Type of the `severity` field (enum vs string vs `Option`) |
| `modules/fundamental/src/advisory/model/mod.rs` | `get_symbols_overview` | Existing `pub mod summary; pub mod details;` registration style and re-exports |
| `entity/src/sbom_advisory.rs` | `find_symbol("Model"/"Relation", include_body=true)` | Join-table columns (`sbom_id`, `advisory_id`) and relations to `advisory` |
| `entity/src/advisory.rs` | `find_symbol` | Where severity is stored in the DB (column for the aggregation query) |
| `common/src/error.rs` | `find_symbol("AppError", include_body=true)` | `NotFound` variant and `.context()` extension trait |
| `modules/fundamental/src/sbom/service/sbom.rs` + `sbom/endpoints/get.rs` | `find_symbol("SbomService/fetch")` | How a missing SBOM becomes a 404, so the new endpoint matches it (AC #2) |
| `tests/api/advisory.rs`, `tests/api/sbom.rs` | Read | Test harness, fixture setup, assertion style |
| `tests/Cargo.toml` | Read | Whether test files need `[[test]]` registration |

- `find_referencing_symbols` on `AdvisoryService` and the advisory router function. The changes are additive (a new method and a new route), so existing callers are unaffected.
- `search_for_pattern("advisory-summary|severity_summary|SeveritySummary|SeverityCount")` across the workspace. This is the symbol deduplication check, so an existing struct or helper gets reused rather than redeclared.
- `search_for_pattern("Severity")` in `modules/fundamental` and `common`. If a `Severity` enum already exists (likely the type of `AdvisorySummary.severity`), match on it instead of comparing strings.
- **CONVENTIONS.md lookup**: the Registry path is `./`, so read `./CONVENTIONS.md` (it is listed in repo-backend.md). Extract its CI check commands, e.g. `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo check`, plus any OpenAPI or code generation commands, for use in Step 9.
- **Documentation files identified**: `README.md`, `CONVENTIONS.md`, `docs/api.md` (REST API reference, per the project CLAUDE.md), `docs/architecture.md`.
- **Convention conformance analysis**: see `conventions.md`.

Convention conflict check: none found. The task notes agree with the sibling conventions. One point to note: the route path lives under `/api/v2/sbom/...` but is registered in the advisory module's `endpoints/mod.rs`. The task explicitly asks for this, so I follow it.

## Step 5 – Create branch

The task has a Target Branch of `main`, no Target PR, and no Bookend Type, so the default flow applies:

```
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 – Implementation (file list)

| # | File | Action | Detail doc |
|---|---|---|---|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | CREATE | `file-1-model-severity-summary.md` |
| 2 | `modules/fundamental/src/advisory/model/mod.rs` | MODIFY | `file-2-model-mod-registration.md` |
| 3 | `modules/fundamental/src/advisory/service/advisory.rs` | MODIFY | `file-3-service-severity-summary-method.md` |
| 4 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | CREATE | `file-4-endpoint-severity-summary-handler.md` |
| 5 | `modules/fundamental/src/advisory/endpoints/mod.rs` | MODIFY | `file-5-endpoints-mod-route-registration.md` |
| 6 | `tests/api/advisory_summary.rs` | CREATE | `file-6-integration-tests.md` |

`server/src/main.rs` is **not** modified. The task says routes auto-mount through module registration.

Summary of changes:
1. **Model**: `SeveritySummary { critical: u64, high: u64, medium: u64, low: u64, total: u64 }` deriving
   `Serialize, Deserialize, Debug, Clone, Default, PartialEq, Eq, ToSchema`. `Default` gives zeros (AC #4). Each item gets a doc comment.
2. **Model registration**: `pub mod severity_summary;` (plus a `pub use` re-export if siblings re-export).
3. **Service**: `AdvisoryService::severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>`:
   - check the SBOM exists with `sbom::Entity::find_by_id` and return `AppError::NotFound` if it does not (AC #2, same behaviour as `SbomService::fetch`)
   - run one DB query: join `sbom_advisory` to `advisory`, filter on `sbom_id`, `GROUP BY advisory.severity` with `COUNT(DISTINCT advisory.id)`. This deduplicates by advisory ID (AC #3) and does the counting in Postgres, which keeps it fast for 500 or more advisories (AC #5)
   - put each row into the matching struct field. Unknown or NULL severities are not counted in any bucket. `total` is the sum of the four buckets, so the response is internally consistent
   - wrap errors with `.context("...")`.
4. **Handler**: `pub async fn get_severity_summary(State(service), Path(id): Path<Id>) -> Result<Json<SeveritySummary>, AppError>`, a copy of the `get.rs` pattern.
5. **Route**: `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))`, using the same path parameter syntax as the existing registrations, plus `mod severity_summary;`. If siblings register utoipa OpenAPI paths, add the handler to the `#[openapi(paths(...))]` list as well.
6. **Tests**: 4 integration tests covering every Test Requirement (detail in file-6).

Reuse: `AppError` / `.context()` from `common/src/error.rs`, `Id` and `Transactional` as already used in `AdvisoryService`, the existing `sbom` / `sbom_advisory` / `advisory` SeaORM entities, and the existing `Severity` enum if one is found. No new crate dependencies: `fundamental` already depends on `entity` and `common`.

Documentation impact: the endpoint is new and public, so `docs/api.md` would normally need an entry. **It is not in Files to Modify**, so per the scope rules it is flagged in Step 9 for user approval and not edited unilaterally.

## Step 7 – Tests

Tests are in `tests/api/advisory_summary.rs` (see file-6). Every test has a `///` doc comment and `// Given / // When / // Then` sections, and the assertions compare the full `SeveritySummary` value rather than only checking that fields exist. Run:

```
cargo test -p <tests crate>          # resolved via cargo metadata (Step 9)
```

## Step 8 – Acceptance criteria verification

| AC | How it is satisfied |
|---|---|
| GET returns `{critical, high, medium, low, total}` | Serde field names on `SeveritySummary` (lowercase); tested in `test_severity_summary_returns_correct_counts` |
| 404 for an unknown SBOM | Existence check returns `AppError::NotFound`, which `IntoResponse` maps to 404; tested in `test_severity_summary_nonexistent_sbom_returns_404` |
| Unique advisories only | `COUNT(DISTINCT advisory.id)`; tested in `test_severity_summary_deduplicates_advisories` |
| Levels default to 0 | `SeveritySummary::default()` is the starting point; tested in `test_severity_summary_no_advisories_returns_zeros` |
| Under 200 ms for 500 advisories | One aggregate SQL query (plus a PK lookup), no N+1 and no rows loaded into memory. Relies on indexes on `sbom_advisory.sbom_id` (verify these in the migration; if one is missing, flag it, since migration is out of scope) |

## Step 9 – Self-verification

- **Scope containment**: `git diff --name-only` must list only the 6 files above. Items flagged for user approval rather than changed:
  - `docs/api.md`: would need the new endpoint documented
  - `tests/Cargo.toml`: only if the tests crate needs a `[[test]]` / module entry for `advisory_summary.rs`
  - any OpenAPI spec file regenerated by a CONVENTIONS.md generation command: stage it only if the generation command produces it, as part of the deliverable
- **Untracked file check**: `git status --short`. Flag `??` files in the touched directories that the diff references.
- **Dead parameter detection**: no code removed, so not applicable. Confirm `tx` is actually used in the new method.
- **Sensitive-pattern check**: `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`. No matches expected.
- **Documentation currency**: `docs/api.md` (see scope flag above).
- **Duplication check**: grep for other severity-counting logic (for example in `search` or a dashboard module) and reuse it if found.
- **CI checks from CONVENTIONS.md**: run every extracted command in order. **Any non-zero exit is a hard stop**: report it to the user and do not commit.
- **Module-level Rust tests**: run `cargo metadata --no-deps --format-version 1` from the workspace root and resolve the package whose manifest or target source path contains each modified file. Do **not** use the nearest `Cargo.toml`, because the root `Cargo.toml` is a virtual workspace manifest. Expected result: `modules/fundamental/...` belongs to the `fundamental` package (actual name taken from the metadata, e.g. `trustify-module-fundamental`), and `tests/api/advisory_summary.rs` belongs to the `tests` package. Then:
  ```
  cargo test -p <fundamental-crate-name>
  cargo test -p <tests-crate-name>
  ```
  (or `cargo nextest run -p ...` if the project uses nextest). A non-zero exit is a hard stop.
- **Data-flow trace**: HTTP GET with `{id}` → `Path<Id>` extraction → `AdvisoryService::severity_summary` → SBOM existence check (404 path) → aggregate query over `sbom_advisory` ⋈ `advisory` → mapping into `SeveritySummary` → `Json` → HTTP 200. Every stage connects to the next: **complete**.
- **Query-scope verification**: the query is scoped to `sbom_advisory.sbom_id = :id`. It is not a full-table scan, so it matches the task scope.
- **Contract & sibling parity**:
  - Contract: no traits are implemented. `SeveritySummary` derives the same traits as `AdvisorySummary` (Serialize/ToSchema) so it serializes and appears in the OpenAPI schema.
  - Sibling parity: the handler matches `get.rs` (same extractors, error type, and any caching or tracing attributes such as `#[utoipa::path]` / `#[instrument]`), and the service method matches `fetch`/`list` (same `tx` handling and `.context()`).
  - Cross-module entity: read-only access to `sbom_advisory`/`advisory`, so no transaction or conflict handling is needed.
  - Caller-site: the call is made the same way as existing handlers call `AdvisoryService` (`service.fetch(id, &Transactional::None)`-style).

## Step 10 – Commit and push

```
git add modules/fundamental/src/advisory/model/severity_summary.rs \
        modules/fundamental/src/advisory/model/mod.rs \
        modules/fundamental/src/advisory/service/advisory.rs \
        modules/fundamental/src/advisory/endpoints/severity_summary.rs \
        modules/fundamental/src/advisory/endpoints/mod.rs \
        tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(advisory): add SBOM advisory severity summary endpoint

Add AdvisoryService::severity_summary, which aggregates unique advisories
linked to an SBOM (via sbom_advisory) into per-severity counts, and expose
it as GET /api/v2/sbom/{id}/advisory-summary returning
{ critical, high, medium, low, total }. Returns 404 for unknown SBOMs and
zero counts for missing severity levels.

Implements TC-9201"
```

Fork detection: `git remote get-url upstream 2>/dev/null`.
- If it succeeds: `gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9201 --base main ...`
- If it fails: `git push -u origin TC-9201` then `gh pr create --base main ...`

PR body includes:
`Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)` (from `webUrl`). Add a `Closes <owner>/<repo>#<n>` line only if customfield_10747 has a value; it does not in the mock.

## Step 11 – Update Jira (simulated)

- `jira.update_issue(TC-9201, {"customfield_10875": <ADF doc with inlineCard PR URL>})`
- `jira.add_comment`: PR link, summary of changes, deviations (none; flagged scope items, if any), ending with the footnote from `shared/comment-footnote.md` (skill name `implement-task`).
- `jira.transition_issue → In Review`.
