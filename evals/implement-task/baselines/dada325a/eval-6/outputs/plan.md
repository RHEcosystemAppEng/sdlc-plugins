# Implementation Plan – TC-9201: Add advisory severity aggregation service and endpoint

## Step 0 – Validate Project Configuration

The CLAUDE.md file (`claude-md-mock.md`) contains everything this step requires under `# Project Configuration`:

- `## Repository Registry`: `trustify-backend` (role: Rust backend service, Serena instance: `serena_backend`, path: `./`)
- `## Jira Configuration`: Project key `TC`, Cloud ID `2b9e35e3-...`, Feature issue type ID `10142`, Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`
- `## Code Intelligence`: naming convention `mcp__<serena-instance>__<tool>`. Instance `serena_backend` uses rust-analyzer, which may need 30–60 s to index on first use.

Result: PASS. Continue.

## Step 0.5 – Jira Access

Use Atlassian MCP first. If an MCP call fails, ask the user whether to use the REST API v3 fallback (`scripts/jira-client.py`), skip the operation, or retry.

## Step 1 – Fetch and Parse Task

Call `jira.get_issue(TC-9201)` and parse the sections:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Description | Service method plus REST endpoint that returns advisory severity counts (Critical/High/Medium/Low/total) for an SBOM |
| Files to Modify | `modules/fundamental/src/advisory/service/advisory.rs`, `modules/fundamental/src/advisory/endpoints/mod.rs`, `modules/fundamental/src/advisory/model/mod.rs`, `server/src/main.rs` (marked "no changes needed") |
| Files to Create | `modules/fundamental/src/advisory/model/severity_summary.rs`, `modules/fundamental/src/advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs` |
| API Changes | NEW `GET /api/v2/sbom/{id}/advisory-summary` returning `{ critical, high, medium, low, total }` |
| Implementation Notes | Present (patterns in get.rs, AdvisoryService, sbom_advisory, AdvisorySummary.severity, AppError) |
| Acceptance Criteria | 5 items |
| Test Requirements | 4 items |
| Target PR | absent, so default flow |
| Review Context | absent |
| Bookend Type | absent, so normal implementation |
| Dependencies | None |

- Capture `webUrl` (e.g. `https://<site>.atlassian.net/browse/TC-9201`) for the PR description.
- GitHub Issue extraction: read `customfield_10747`. If it holds a URL, parse it to `<owner>/<repo>#<n>` for a `Closes` line in the PR. If it is empty, skip silently.
- Every required section is present, so no clarification is needed.

## Step 1.5 – Verify Description Integrity

See `digest-match.md`. There is one digest comment (`created == updated`, so it was not edited). Its stored `sha256-md:a1b2…7890` matches the digest computed by `scripts/sha256-digest.py`: the tag and the hex both match. Proceed silently with no prompt.

## Step 2 – Verify Dependencies

"Depends on: None" means there is nothing to check. Continue.

## Step 3 – Transition and Assign

1. Call `jira.user_info()` to get the accountId.
2. Call `jira.edit_issue(TC-9201, assignee=<accountId>)`.
3. Call `jira.transition_issue(TC-9201 → In Progress)`.

## Step 4 – Understand the Code (Serena: `serena_backend`)

**Symbol inspection**
- `mcp__serena_backend__get_symbols_overview` on `advisory/service/advisory.rs`, then `find_symbol("AdvisoryService/fetch", include_body=true)` and `AdvisoryService/list`. Confirm the signature pattern `(&self, …, tx: &Transactional<'_>)`, the error-wrapping style, and how the DB connection is obtained.
- `get_symbols_overview` on `advisory/endpoints/mod.rs`. Confirm how `Router::new().route(...)` is built, how the service is injected (state or `Extension`), and whether caching middleware is applied there.
- `find_symbol` with body on `advisory/endpoints/get.rs`. This is the handler pattern: `Path<Id>`, the service call, the `Result<Json<T>, AppError>` return type, and the `.context()` call.
- `get_symbols_overview` on `advisory/model/mod.rs` and `model/summary.rs`. Inspect `AdvisorySummary.severity` and find out its type: an enum such as `Severity { Critical, High, Medium, Low, ... }`, an `Option<…>`, or a string. This decides how the counting works.
- `entity/src/sbom_advisory.rs`: find the column names (`sbom_id`, `advisory_id`) and the relations to `advisory`.
- `entity/src/advisory.rs`: find where severity is persisted (a column on advisory, or derived elsewhere).
- `sbom/service/sbom.rs` (`SbomService::fetch`) and `sbom/endpoints/get.rs`: see how a missing SBOM becomes a 404 (for example `Option` → `AppError::NotFound`). Mirror this for AC #2.
- `common/src/error.rs`: the `AppError` variants and the `.context()` usage.
- `find_referencing_symbols` on `AdvisoryService` and on the advisory router function. This confirms that adding a method and a route breaks no callers. The change is purely additive.
- `search_for_pattern` for an existing severity enum or ordering constant (`Severity`, `SEVERITY_`) and for existing count or group-by helpers in `common/src/db/query.rs`. Reuse them instead of redefining.

**Routing check.** The new path is under `/api/v2/sbom/{id}/...` but is registered in the *advisory* endpoints module, as the task specifies. Use `search_for_pattern` on `server/src/main.rs` and both `endpoints/mod.rs` files to confirm that the advisory router is mounted at the root (paths fully qualified) rather than nested under `/api/v2/advisory`. If it is nested, the route would end up at the wrong URL. That would conflict with the task, so I would flag it to the user instead of editing `server/src/main.rs` on my own.

**CONVENTIONS.md.** It exists at the repo root (`./CONVENTIONS.md`). Read it, then extract the CI check commands (likely `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo check`, and similar) and any code generation commands (for example OpenAPI spec generation) for Step 9.

**Documentation files** to look at in Step 6/9: `README.md`, `CONVENTIONS.md`, and `docs/api.md` (REST API reference listed in CLAUDE.md).

**Convention conformance.** Siblings: `advisory/endpoints/get.rs`, `advisory/endpoints/list.rs`, `sbom/endpoints/get.rs`, `advisory/model/summary.rs`, `tests/api/advisory.rs`, `tests/api/sbom.rs`. Expected conventions, to be confirmed by inspection:
- *Structure*: `model/ + service/ + endpoints/` per domain. Each new model or endpoint file is registered with `pub mod` / `mod` in its `mod.rs`.
- *Naming*: snake_case `verb_noun` / noun handlers, structs named `<Thing>Summary`, file names that match the module.
- *Errors*: handlers return `Result<T, AppError>`, and errors are wrapped with `.context("...")`.
- *Responses*: single-object endpoints return `Json<T>`. Only list endpoints use `PaginatedResults<T>`, so this one does not.
- *Model derives*: whatever siblings use (likely `Serialize, Deserialize, Debug, Clone, PartialEq, Eq, Default` plus `utoipa::ToSchema` if the project uses OpenAPI).
- *Tests*: integration tests against a real PostgreSQL test DB, written as `assert_eq!(resp.status(), StatusCode::OK)`. Check the siblings for fixture and ingestion helpers.

Conflicts: none expected between the task and the conventions. If inspection finds one, ask the user before proceeding.

## Step 5 – Create Branch

```
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 – Implement Changes (only files in scope)

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`
```rust
/// Aggregated count of unique advisories per severity level for a single SBOM.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize /*, ToSchema if used */)]
pub struct SeveritySummary {
    /// Number of unique Critical advisories.
    pub critical: u64,
    /// Number of unique High advisories.
    pub high: u64,
    /// Number of unique Medium advisories.
    pub medium: u64,
    /// Number of unique Low advisories.
    pub low: u64,
    /// Total number of unique advisories counted.
    pub total: u64,
}
```
`Default` gives all zeros, which covers AC #4. The plan may add a small helper such as `fn record(&mut self, severity)` that increments the right bucket and `total`. Open question: how should `total` treat advisories whose severity is unknown or None? It must still match the documented response contract. Plan: `total` = sum of the four buckets, so the response stays internally consistent. Record this decision in the PR description.

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`
Add `pub mod severity_summary;` and a re-export (`pub use severity_summary::*;`) only if siblings re-export.

### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`
Add a method to `AdvisoryService` that follows the `fetch`/`list` pattern:
```rust
/// Returns per-severity counts of unique advisories linked to the given SBOM.
/// Returns `Ok(None)` when the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<Option<SeveritySummary>, Error> { ... }
```
- First check that the SBOM exists, using `entity::sbom::Entity::find_by_id` or by reusing the existing lookup mechanism. If it is missing, return `None` so the handler maps it to 404 the same way existing SBOM endpoints do.
- Query `sbom_advisory` joined to `advisory`, filtered by `sbom_id`, selecting the advisory id and severity. **Deduplicate by advisory ID** in SQL with `SELECT DISTINCT advisory.id, advisory.severity` or `COUNT(DISTINCT advisory.id) ... GROUP BY severity` (AC #3). Aggregate in the DB with `GROUP BY severity` so the work stays a single indexed query, which keeps the response under 200 ms for 500 advisories (AC #5).
- Map each severity value to its bucket with the existing severity enum or type found in Step 4. Do not declare a new one (symbol deduplication). Guard defensively: treat a null or unknown severity with `unwrap_or_default` / a match fallback, and never panic.
- Wrap DB errors with `.context("Failed to compute advisory severity summary")`, matching `common/src/error.rs`.
- Query scope: the query is filtered by `sbom_id`, which is the target subset. It is not a broad scan.

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
Follow the pattern in `get.rs`:
```rust
/// GET /api/v2/sbom/{id}/advisory-summary — returns advisory severity counts for an SBOM.
pub async fn severity_summary(
    State(service): State<AdvisoryService>, // or the injection mechanism get.rs uses
    Path(id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &Transactional::None)
        .await
        .context("...")?
        .ok_or_else(|| AppError::NotFound(...))?; // the same 404 variant SBOM get uses
    Ok(Json(summary))
}
```
Add a `utoipa::path` annotation if siblings use one.

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`
- Add `mod severity_summary;`.
- Register the route with `.route("/api/v2/sbom/{id}/advisory-summary", get(severity_summary::severity_summary))`, using the same path-param syntax as existing routes (`{id}` vs `:id` depends on the Axum version). Apply the same caching middleware configuration as sibling routes if they have any.

### 6.6 `server/src/main.rs`
The task says this file needs no changes because routes auto-mount through module registration. Leave it untouched and only verify that the mounting is correct (see Step 4).

### Documentation impact
The task has no Documentation Updates section. `docs/api.md` (REST API reference) would normally document the new endpoint, but it is **not** in Files to Modify or Files to Create. Do not edit it. Flag it in the Step 9 scope check as a recommended follow-up or an out-of-scope change that needs user approval. If CONVENTIONS.md lists an OpenAPI generation command, run it in Step 9 and present the generated spec diff for approval, because it is also outside the listed files.

## Step 7 – Write Tests: `tests/api/advisory_summary.rs`

Register the new test module wherever sibling tests are registered (for example a `[[test]]` entry or a `mod` in the test crate). If that requires editing a file outside scope, flag it in Step 9.

Each test has a `///` doc comment and given/when/then section comments, and uses value-based assertions on the full struct:

1. `/// Verifies a valid SBOM with known advisories returns correct per-severity counts.` `test_advisory_summary_counts`. Given an SBOM linked to, for example, 2 Critical, 1 High, 3 Medium, and 0 Low advisories. When `GET /api/v2/sbom/{id}/advisory-summary` is called. Then `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(body, SeveritySummary { critical: 2, high: 1, medium: 3, low: 0, total: 6 })`.
2. `/// Verifies a non-existent SBOM ID returns 404.` `test_advisory_summary_sbom_not_found`. Assert `StatusCode::NOT_FOUND`.
3. `/// Verifies an SBOM with no advisories returns all zero counts.` `test_advisory_summary_no_advisories`. Assert OK and `body == SeveritySummary::default()`.
4. `/// Verifies duplicate advisory links are counted once.` `test_advisory_summary_deduplicates`. Given the same advisory linked twice to the SBOM (or ingested twice). Then its bucket is 1 and `total` is 1.

Parameterization: the four cases differ in setup and in the kind of assertion (status only vs body), so they stay as separate tests. Introduce `rstest` only if the siblings already use it.

Run `cargo test -p <tests-crate>` and `cargo test -p <fundamental-crate>`, resolving crate names with `cargo metadata --no-deps --format-version 1`. Fix any failures. Stop after 3 identical failures.

## Step 8 – Verify Acceptance Criteria

| AC | How satisfied |
|---|---|
| Endpoint returns `{critical, high, medium, low, total}` | `SeveritySummary` serialized via `Json`. Test 1 |
| 404 for unknown SBOM | SBOM existence check maps to the same `AppError` 404 variant as the SBOM get endpoint. Test 2 |
| Unique advisories only | `DISTINCT` / `COUNT(DISTINCT advisory.id)`. Test 4 |
| Levels default to 0 | `#[derive(Default)]` and buckets only incremented. Test 3 |
| < 200 ms for 500 advisories | Single aggregated `GROUP BY` query on the indexed `sbom_advisory.sbom_id`. No N+1. Check the timing manually or with a fixture of about 500 links if feasible |

## Step 9 – Self-Verification

- **Scope containment**: `git diff --name-only` should list only the 3 modified and 3 created files above. `server/src/main.rs` should show no diff. Anything else, such as `docs/api.md`, generated OpenAPI spec files, or test crate registration, gets listed with a reason, and the user must approve it before commit.
- **Untracked files**: run `git status --short` and check `??` files in the touched dirs. The new files must be staged on purpose. Flag anything else.
- **Dead parameters**: N/A (additive change). Confirm `tx` is actually used in `severity_summary`.
- **Sensitive patterns**: `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`. Expect no hits.
- **Documentation currency**: `docs/api.md` would be stale. Raise it as described above.
- **Duplication check**: grep for existing severity counting or aggregation code (for example in search or sbom modules) and reuse it if present.
- **CI checks**: run every command from the CONVENTIONS.md CI section, plus any code generation commands. Any non-zero exit is a hard stop: report it and do not commit.
- **Rust module tests**: run `cargo test -p` for the fundamental crate and the tests crate. Hard stop on failure.
- **Data-flow trace**: HTTP GET → `Path<Id>` extraction → `AdvisoryService::severity_summary` → SBOM existence check → `sbom_advisory ⋈ advisory` distinct/group-by query → bucket mapping into `SeveritySummary` → `Json` response (or `AppError` 404/500). Every stage is connected.
- **Query scope**: filtered by `sbom_id`, which matches the target scope.
- **Contract & sibling parity**:
  - Contract: no new trait impls. The handler signature satisfies Axum's `Handler`, and the struct implements `Serialize` (and `ToSchema` if required).
  - Sibling parity: same error wrapping, logging/tracing attributes (for example `#[instrument]`), caching, and OpenAPI annotations as `get.rs`.
  - Cross-module entity: read-only use of `sbom_advisory`/`advisory`, so no transaction or conflict handling is needed.
  - Caller-site: the service is invoked the same way other advisory handlers invoke it (same `Transactional` argument and the same error mapping).

## Step 10 – Commit and Push

```
git add <in-scope files>
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(advisory): add SBOM advisory severity summary endpoint

Add AdvisoryService::severity_summary and GET /api/v2/sbom/{id}/advisory-summary
returning unique advisory counts per severity level (critical, high, medium,
low) and a total. Returns 404 for unknown SBOMs.

Implements TC-9201"
git push -u origin TC-9201
```

Fork detection: run `git remote get-url upstream`. If an upstream remote exists, use `gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9201 --base main`. Otherwise use `gh pr create --base main`.

PR body: a summary of the changes, the decision on how `total` is computed, the test list, a note on `docs/api.md` if it was left out of scope, then `Implements [TC-9201](<webUrl>)`, plus `Closes <owner>/<repo>#<n>` if the GitHub Issue field was set.

## Step 11 – Update Jira

1. Call `jira.update_issue(TC-9201, fields={"customfield_10875": {ADF doc with inlineCard url=<PR-URL>}})`.
2. Call `jira.add_comment(TC-9201)` with the PR link, a summary of the changes, and any deviations (for example docs/api.md deferred, or `total` semantics). End the comment with the footnote: a rule, then "This comment was AI-generated by [sdlc-workflow/implement-task](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10."
3. Call `jira.transition_issue(TC-9201 → In Review)`.
