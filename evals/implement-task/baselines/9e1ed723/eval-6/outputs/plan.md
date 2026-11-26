# Implementation Plan: TC-9201 – Add advisory severity aggregation service and endpoint

These are the steps `/sdlc-workflow:implement-task` would take for TC-9201 in eval mode. Nothing was actually run against the repository, git, Jira or Serena.

---

## Step 0 – Validate Project Configuration

All required sections are present in the project CLAUDE.md (`claude-md-mock.md`):

| Section | Status |
|---|---|
| Repository Registry | Present. `trustify-backend`, Serena instance `serena_backend`, path `./` |
| Jira Configuration | Present. Project key `TC`, Cloud ID `2b9e35e3-…`, Feature issue type ID `10142`, Git PR field `customfield_10875`, GitHub Issue field `customfield_10747` |
| Code Intelligence | Present. Naming convention `mcp__<serena-instance>__<tool>`. Limitation: rust-analyzer can take 30-60 s to index |

Validation passes, so execution continues.

## Step 0.5 – Jira Access

Every Jira call goes through Atlassian MCP first. If MCP fails, the user is asked: (1) use the REST fallback, (2) skip the operation, or (3) retry. Because MCP is the path used here, the description comes back as markdown, and the digest tag is `sha256-md`.

## Step 1 – Fetch and Parse the Task

`jira.get_issue(TC-9201)` returns the structured description. Every required section is present, so there is nothing to ask the user.

| Field | Value |
|---|---|
| Repository | `trustify-backend` |
| Target Branch | `main` |
| Target PR | Not present, so the default flow applies (new branch, new PR) |
| Bookend Type | Not present, so this is a normal implementation task |
| Review Context | Not present |
| Dependencies | None |
| webUrl | `https://redhat.atlassian.net/browse/TC-9201`, used for the "Implements" link in the PR |
| GitHub Issue (`customfield_10747`) | Read from the issue fields. If it holds a URL, parse it as `<owner>/<repo>#<n>` for a `Closes` line in the PR. If it is empty, skip silently |

**Scope taken from the task:**
- Files to Modify:
  - `modules/fundamental/src/advisory/service/advisory.rs`
  - `modules/fundamental/src/advisory/endpoints/mod.rs`
  - `modules/fundamental/src/advisory/model/mod.rs`
  - `server/src/main.rs` (the task itself says "no changes needed", so this file is listed but will not be edited)
- Files to Create:
  - `modules/fundamental/src/advisory/model/severity_summary.rs`
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
  - `tests/api/advisory_summary.rs`
- API change: `GET /api/v2/sbom/{id}/advisory-summary` returns `{ critical, high, medium, low, total }`

## Step 1.5 – Verify Description Integrity

`digest-match.md` has the full reasoning. In short:
- There is one digest comment, `sha256-md:a1b2c3d4…67890`.
- Its `created` and `updated` timestamps are equal, so there is no edit warning.
- The tag is not legacy, and the tags match (`sha256-md` stored and computed).
- The hex digests match.
- The check passes silently: no prompt, no warning. Execution continues to Step 2.

## Step 2 – Verify Dependencies

The task says "Depends on: None", so there is nothing to check.

## Step 3 – Transition to In Progress and Assign

1. `jira.user_info()` returns the current user's accountId.
2. `jira.edit_issue(TC-9201, assignee=<accountId>)`
3. `jira.transition_issue(TC-9201 → In Progress)`

## Step 4 – Understand the Code (Serena instance `serena_backend`)

The first call may be slow while rust-analyzer indexes (30-60 s).

1. **Symbol overviews** (`mcp__serena_backend__get_symbols_overview`):
   - `modules/fundamental/src/advisory/service/advisory.rs`: `AdvisoryService` with `fetch`, `list`, `search`
   - `modules/fundamental/src/advisory/endpoints/mod.rs`: the router builder
   - `modules/fundamental/src/advisory/model/mod.rs`: module declarations
2. **Read only the symbols needed** (`find_symbol`, `include_body=true`):
   - `AdvisoryService/fetch` and `AdvisoryService/list`, to get the signature pattern `(&self, …, tx: &Transactional<'_>) -> Result<…, AppError>` and how queries are built
   - the handler in `advisory/endpoints/get.rs`, to see how it uses `Path<Id>` extraction, the service call and the JSON return
   - the `AdvisorySummary` struct in `advisory/model/summary.rs`, to find the type of its `severity` field (enum or `String`/`Option<String>`) and its possible values
   - the `sbom_advisory` entity in `entity/src/sbom_advisory.rs`, to get its columns (`sbom_id`, `advisory_id`) and its `Relation` to `advisory`
   - the `AppError` type in `common/src/error.rs`, to find its variants (especially `NotFound`) and how `.context()` is used
   - the `SbomService::fetch` method in `sbom/service/sbom.rs`, to see how a missing SBOM is detected and how it is turned into a 404
3. **Callers that could break** (`find_referencing_symbols`): check `AdvisoryService` and the advisory router function. Adding a method and a route does not change existing signatures, so no callers should break. This step confirms that.
4. **Text search** (`search_for_pattern`):
   - Look for `"/api/v2/sbom"` and how the advisory router is mounted. The new route lives under the SBOM path but is registered in the advisory module, so I need the advisory router's mount prefix to choose the right relative path.
   - Look for `Severity`, `severity_summary`, `SeveritySummary` and `count_by_severity`, so nothing gets duplicated.
   - Look for the existing tower-http cache configuration in route builders.
5. **Siblings for conventions:**
   - Production code: `advisory/endpoints/get.rs`, `advisory/endpoints/list.rs`, `sbom/endpoints/get.rs`, `advisory/model/summary.rs`, `sbom/model/summary.rs`
   - Tests: `tests/api/advisory.rs`, `tests/api/sbom.rs`

### CONVENTIONS.md lookup
`CONVENTIONS.md` exists at the repository root (`./CONVENTIONS.md`). I would read it in full and use it as binding. I would also record two things from it:
- **CI check commands**, for example `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings` and `cargo check`. The real list comes from the file.
- **Code generation commands**, for example OpenAPI spec regeneration. A new endpoint probably changes the generated spec. If so, the regenerated artifact gets committed. If the artifact sits outside Files to Create/Modify, it is raised for approval in Step 9.

### Documentation files identified
- `README.md` at the repository root
- `CONVENTIONS.md`
- `docs/api.md` (REST API reference, listed in CLAUDE.md). The new endpoint probably belongs here, **but this file is not in Files to Modify**. See the Step 6 documentation impact note.
- `docs/architecture.md`, checked only for currency. No change is expected.

### Conventions found (binding for Steps 6–7)
- **Module layout:** `model/` + `service/` + `endpoints/` for each domain. Each new model file is declared with `pub mod` in `model/mod.rs`.
- **Naming:** snake_case files and functions in `verb_noun` / `noun_noun` style (`severity_summary`), PascalCase structs (`SeveritySummary`), with a `Summary` suffix for aggregate response types.
- **Errors:** handlers return `Result<T, AppError>`. Errors are wrapped with `.context("…")`. A missing entity becomes `AppError::NotFound`, the same way `SbomService::fetch` / `sbom/endpoints/get.rs` do it.
- **Service methods:** `pub async fn name(&self, <args>, tx: &Transactional<'_>) -> Result<T, Error>`, using the SeaORM query builder and the shared helpers in `common/src/db/query.rs` where they apply.
- **Endpoints:** take `Path<Id>`, get the service from state, call the method, return `Json(...)`. Routes go into `endpoints/mod.rs` with `Router::new().route("/path", get(handler))`.
- **Response models:** derive `Serialize`, `Deserialize`, `Debug`, `Clone`, `PartialEq`, `Eq` and `Default` where siblings do, plus `utoipa::ToSchema` if siblings derive it for OpenAPI.
- **Tests:** integration tests in `tests/api/` against a real PostgreSQL test DB, with status checks written as `assert_eq!(resp.status(), StatusCode::OK)`.
- **Caching:** tower-http caching is configured on route builders. If the advisory routes have a cache layer, the new route gets the same one.
- **Where the skill's rules override siblings:** every test function gets a doc comment. Assertions compare whole values rather than checking only length or a single field. Siblings that do otherwise are noted and not copied.

Possible convention conflict to check: the new route is `/api/v2/sbom/{id}/...` but it is registered in the **advisory** endpoints module, whose mount prefix is `/api/v2/advisory`. If the advisory router is nested under `/api/v2/advisory`, a relative path such as `/sbom/{id}/advisory-summary` would end up at the wrong URL. If inspection confirms the router is prefix-nested, I would ask the user whether to register the full path at the top level (as `server/src/main.rs` mounts modules) or to add the route to the SBOM router, which would be a scope change. If the advisory router registers absolute paths, as the task's `Router::new().route("/path", …)` wording suggests, there is no conflict and I use the absolute path `/api/v2/sbom/{id}/advisory-summary`.

## Step 5 – Create the Branch

```
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 – Implement the Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`
```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema; // only if sibling models derive ToSchema

/// Aggregated counts of unique advisories per severity level for a single SBOM.
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
- `Default` sets every count to 0, which covers the "default to 0" acceptance criterion.
- I would add a small helper such as `fn record(&mut self, severity: Option<&Severity>)` that increments the matching bucket and `total`, so the counting logic can be unit-tested. It needs a one-line doc comment.
- Open decision on `total`: should an advisory with no severity, or an unrecognised one (for example "None" or "Unknown"), count toward `total`? The spec says "counts per severity level … and a total". I would make `total` the number of unique advisories linked to the SBOM, write that down in the doc comment, and mention it in the PR as a deviation to confirm. If sibling code or the user says otherwise, `total` becomes the sum of the four buckets.
- Before declaring anything, I would search the package for an existing `Severity` enum or severity ordering (Symbol deduplication rule) and reuse whatever `AdvisorySummary.severity` already uses instead of adding a new enum.

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`
- Add `pub mod severity_summary;` next to `pub mod summary;` / `pub mod details;`, in the same order and style.

### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`: add `AdvisoryService::severity_summary`
```rust
/// Returns per-severity counts of unique advisories linked to the given SBOM.
///
/// Returns `Ok(None)` when the SBOM does not exist so the endpoint can map it to 404.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<Option<SeveritySummary>, Error> {
    // 1. Verify SBOM exists (sbom::Entity::find_by_id) — None => caller returns 404
    // 2. Query advisories joined through sbom_advisory filtered by sbom_id,
    //    selecting DISTINCT advisory.id + severity (dedup by advisory ID)
    // 3. Fold rows into SeveritySummary (default zeros)
}
```
- **Existence check:** follow whatever `SbomService::fetch` does to report "not found". It returns either `Option` or `AppError::NotFound`, and the new method copies it so the 404 behaviour matches the existing SBOM endpoints. Every DB call gets `.context("…")`.
- **Query:** `advisory::Entity::find().inner_join(sbom_advisory::Entity).filter(sbom_advisory::Column::SbomId.eq(sbom_id))`, selecting only `advisory::Column::Id` and the severity column, with `.distinct()` on advisory ID. This deduplicates in SQL, and the query is limited to the one SBOM, which keeps the response under 200 ms for 500 advisories. A further option is `GROUP BY severity` with `COUNT(DISTINCT advisory.id)` so only about 4 rows come back. I would pick the grouped form if the severity column can be grouped directly, and fold in Rust otherwise.
- **Defensive handling:** severity can be null or unrecognised. Use `Option` and match on it. Such advisories do not go into any bucket but are counted in `total` (see 6.1).
- **Reuse:** use the `Transactional` / connection pattern from `fetch` and `list`. Use helpers from `common/src/db/query.rs` only where they fit. There is no pagination or filtering here, so probably none apply.

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
```rust
/// GET /api/v2/sbom/{id}/advisory-summary — returns severity counts of unique advisories for an SBOM.
#[utoipa::path(...)] // only if siblings annotate for OpenAPI
pub async fn severity_summary(
    State(service): State<AdvisoryService>, // match get.rs extraction style
    Path(id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    let tx = Transactional::None; // match get.rs
    match service.severity_summary(id, &tx).await.context("fetching advisory severity summary")? {
        Some(summary) => Ok(Json(summary)),
        None => Err(AppError::NotFound(format!("SBOM {id} not found"))),
    }
}
```
- This mirrors `advisory/endpoints/get.rs` exactly: the same state/DB extractor, transaction setup and error mapping.

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`
- Add `mod severity_summary;`.
- Register `.route("/api/v2/sbom/{id}/advisory-summary", get(severity_summary::severity_summary))` in the existing `Router::new()` chain, using the path style of the existing routes (`{id}` vs `:id`, depending on the Axum version) and the same cache layer the sibling routes use.
- If OpenAPI is aggregated with `#[derive(OpenApi)] paths(...)`, add the new handler there as well.

### 6.6 `server/src/main.rs`
- **No edits.** The task says routes auto-mount through module registration. I would confirm in Step 4 that the advisory router is already mounted, and leave the file alone.

### Code quality checks
- Every new struct, function and helper has a `///` doc comment.
- Optional or null severity values from the entity layer are guarded with `Option` / `match` and never unwrapped.

### Documentation impact
- The task has no "Documentation Updates" section.
- `docs/api.md`, and possibly `README.md`, should probably list the new endpoint. These files are **outside Files to Modify**, so they are not changed. They are reported in the Step 9 scope check, and the user is asked whether to add the doc update or handle it in a follow-up.

## Step 7 – Write Tests

### Integration tests in `tests/api/advisory_summary.rs` (new)
The structure follows `tests/api/advisory.rs` and `tests/api/sbom.rs`: the same test DB bootstrap, HTTP client and fixture helpers. Each test has a `///` doc comment and `// Given / // When / // Then` sections.

1. `/// Verifies that an SBOM with known advisories returns the correct per-severity counts.`
   `test_advisory_summary_returns_severity_counts`. Seed an SBOM linked to, for example, 2 Critical, 1 High, 3 Medium and 1 Low advisories. Check `assert_eq!(resp.status(), StatusCode::OK)`, then `assert_eq!(body, SeveritySummary { critical: 2, high: 1, medium: 3, low: 1, total: 7 })`. This compares the whole value, not single fields.
2. `/// Verifies that requesting a summary for a non-existent SBOM returns 404.`
   `test_advisory_summary_unknown_sbom_returns_404`. Use a random or unused ID and check `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`. This test is trivial, so it has no given/when/then sections.
3. `/// Verifies that an SBOM with no linked advisories returns all-zero counts.`
   `test_advisory_summary_no_advisories_returns_zeros`. Seed an SBOM with no links and check `assert_eq!(body, SeveritySummary::default())`, with the zeros written out explicitly for clarity.
4. `/// Verifies that duplicate SBOM-advisory links are counted once per advisory.`
   `test_advisory_summary_deduplicates_advisories`. Link the same High advisory to the SBOM twice (or through two link rows), plus one Low advisory. Check `SeveritySummary { critical: 0, high: 1, medium: 0, low: 1, total: 2 }`.

The four tests differ in setup and in what they assert (status vs body), so they stay separate tests rather than being parameterised, per the Meszaros heuristic. If siblings use `rstest` and `SeveritySummary::record` gets unit tests, a parameterised `#[rstest]` table over severity inputs would fit in `severity_summary.rs`.

Possible scope issue: if the `tests` crate needs the new file declared (a `mod advisory_summary;` in a `tests/api/main.rs`/`mod.rs`, or a `[[test]]` entry in `tests/Cargo.toml`), that file is not in Files to Modify. It would be raised for approval in Step 9.

### Running the tests
- Record the `cargo clippy` / `cargo check` warning output before implementing.
- Run `cargo test -p <tests-crate>` and `cargo test -p <fundamental-crate>`. The crate names come from `cargo metadata --no-deps --format-version 1`.
- Fix any failures. If the same failure happens 3 times, stop and ask the user.

## Step 8 – Verify Acceptance Criteria

| Criterion | How it is met |
|---|---|
| GET returns `{critical, high, medium, low, total}` | The `SeveritySummary` struct serialises to exactly those fields. Covered by test 1 |
| 404 for a non-existent SBOM, same as the SBOM endpoints | The existence check copies `SbomService::fetch` and maps to `AppError::NotFound`. Covered by test 2 |
| Counts only unique advisories | `DISTINCT advisory.id` / `COUNT(DISTINCT …)` in SQL. Covered by test 4 |
| Levels default to 0 | `#[derive(Default)]` plus fold. Covered by test 3 |
| Under 200 ms for 500 advisories | One query, filtered to the SBOM and aggregated in the DB, using the indexed `sbom_advisory.sbom_id`. I would check timing with a 500-advisory fixture locally. If there is no index on `sbom_advisory.sbom_id`, I would flag that, since a migration is out of scope |

## Step 9 – Self-Verification

- **Scope containment:** `git diff --name-only` should list only the 3 modified and 3 created files. `server/src/main.rs` should stay unchanged. Files that may need user approval:
  - `docs/api.md` (and `README.md`), for documenting the endpoint
  - the generated OpenAPI spec, if CONVENTIONS.md has a codegen step
  - `tests/api/main.rs` / `tests/Cargo.toml`, if the test module has to be registered
- **Untracked files:** run `git status --short`. New files are staged explicitly, and only the three in Files to Create.
- **Dead parameters:** nothing is removed, so this does not apply.
- **Sensitive patterns:** run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`. No matches are expected.
- **Documentation currency and scope preservation:** no existing docs are rewritten. The missing `docs/api.md` entry is reported as above.
- **Eval coverage currency:** no `skills/*/SKILL.md` file is touched, so this does not apply.
- **Cross-section consistency:** Files to Modify, Files to Create and Implementation Notes all use the same paths for `AdvisoryService`, `AdvisorySummary`, `sbom_advisory` and `AppError`. No conflicts.
- **Duplication check:** search for other severity counting or aggregation, for example in `search` or the SBOM module. Reuse anything found.
- **CI checks from CONVENTIONS.md:** run every recorded command (fmt, clippy, check, and so on) and any codegen. **Any non-zero exit is a hard stop and is reported to the user.**
- **Rust module tests:** run `cargo test -p <fundamental crate>` and `cargo test -p <tests crate>`, with crate names resolved through `cargo metadata`. A non-zero exit is a hard stop.
- **Data-flow trace:** HTTP GET → `Path<Id>` → `AdvisoryService::severity_summary` → SBOM existence check → `sbom_advisory` ⋈ `advisory` DISTINCT query → fold into `SeveritySummary` → `Json` response, with the 404 branch for a missing SBOM. Every stage connects to the next.
- **Query scope:** the query is filtered to `sbom_id` and is not a full-table scan, so this is fine.
- **Contract and sibling parity:**
  - Contract: no trait is implemented, but the handler signature must match Axum's `Handler` and the router's state type.
  - Sibling parity: same logging, tracing (`#[instrument]` if siblings use it), cache layer and OpenAPI annotation as `get.rs`.
  - Cross-module entity: the code only reads from `sbom_advisory` and writes nothing, so there are no transaction or conflict concerns.
  - Caller-site: `AdvisoryService` is called the same way other endpoints call it, with the same state extraction and `Transactional` usage.

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
returning unique-advisory counts per severity (critical/high/medium/low) and total.
Returns 404 for unknown SBOMs.

Implements TC-9201"
```
- **Fork detection:** run `git remote get-url upstream`.
  - If it succeeds: `gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9201 --base main …`
  - If it fails: `git push -u origin TC-9201`, then `gh pr create --base main …`
- **PR body:** a summary of the changes, the decisions made (how `total` is defined, the route registration path, any reused helpers), and the test plan. It includes `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)`, and also `Closes <owner>/<repo>#<n>` if `customfield_10747` had a GitHub issue. The `Closes` line goes in the PR body only, not the commit.

## Step 11 – Update Jira

1. Set `customfield_10875` (Git Pull Request) to the PR URL, in ADF format:
   `{"type":"doc","version":1,"content":[{"type":"paragraph","content":[{"type":"inlineCard","attrs":{"url":"<PR-URL>"}}]}]}`
2. `jira.add_comment(TC-9201, …)` with:
   - the PR link
   - a summary of the changes
   - deviations: the `total` semantics, `server/src/main.rs` left unchanged, and any out-of-scope doc or test-registration files the user approved or deferred
   - the required footnote: a horizontal rule, then "This comment was AI-generated by [sdlc-workflow/implement-task](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0."
3. `jira.transition_issue(TC-9201 → In Review)`
