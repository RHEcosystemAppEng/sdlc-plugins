# Implementation Plan: TC-9201 – Add advisory severity aggregation service and endpoint

## Step 0 – Validate Project Configuration

I checked CLAUDE.md (claude-md-mock.md). All required sections are present:

| Section | Status |
|---|---|
| Repository Registry | `trustify-backend`, Serena instance `serena_backend`, Path `./` |
| Jira Configuration | Project key TC, Cloud ID 2b9e35e3-..., Feature issue type ID 10142, Git PR field `customfield_10875`, GitHub Issue field `customfield_10747` |
| Code Intelligence | Naming convention `mcp__<serena-instance>__<tool>`. Limitation: rust-analyzer needs 30–60s to index on first use. |

Result: OK, proceed.

## Step 0.5 – Jira Access

All Jira calls try MCP first. If an MCP call fails, I ask the user before using the REST fallback (`scripts/jira-client.py`).

## Step 1 – Fetch and Parse TC-9201

`jira.get_issue("TC-9201")` returned a description with every required section:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Description | Service method plus REST endpoint that aggregates advisory severity counts for an SBOM |
| Files to Modify | `advisory/service/advisory.rs`, `advisory/endpoints/mod.rs`, `advisory/model/mod.rs`, `server/src/main.rs` (marked "no changes needed") |
| Files to Create | `advisory/model/severity_summary.rs`, `advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs` |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` (new) |
| Implementation Notes | Present |
| Acceptance Criteria | 5 items |
| Test Requirements | 4 items |
| Dependencies | None |
| Target PR | Absent, so default flow (new branch, new PR) |
| Review Context | Absent |
| Bookend Type | Absent, so this is a normal implementation task |

Other values captured:
- `webUrl`, for the PR "Implements" link.
- GitHub Issue field `customfield_10747`: if it holds a URL, I parse it to `<owner>/<repo>#<number>` for a `Closes` line. If it is empty, I skip it silently.

The description is complete, so there is no need to ask the user anything.

## Step 1.5 – Verify Description Integrity

Full details are in `digest-match.md`.
- Exactly one digest comment was found. Its `created` and `updated` timestamps are identical, so it has not been edited.
- Stored tag `sha256-md` equals the computed tag `sha256-md`.
- The hex digests match.
- Result: proceed silently, with no prompt and no warnings.

## Step 2 – Verify Dependencies

"Depends on: None", so there is nothing to check.

## Step 3 – Transition and Assign

1. `jira.user_info()` to get the current user's accountId.
2. `jira.edit_issue("TC-9201", assignee=<accountId>)`.
3. `jira.transition_issue("TC-9201", "In Progress")`.

## Step 4 – Understand the Code (Serena instance `serena_backend`)

Before starting I allow for the rust-analyzer indexing delay of up to 60s.

### Inspection

1. `mcp__serena_backend__get_symbols_overview` on:
   - `modules/fundamental/src/advisory/service/advisory.rs`
   - `modules/fundamental/src/advisory/endpoints/mod.rs`
   - `modules/fundamental/src/advisory/model/mod.rs`
2. `mcp__serena_backend__find_symbol` with `include_body=true` on:
   - `AdvisoryService/fetch` and `AdvisoryService/list`, for the signature `(&self, ..., tx: &Transactional<'_>)`, the query style and the error wrapping.
   - The handler in `advisory/endpoints/get.rs`, for the `Path<Id>` extraction, how the service is injected (`web::Data`/`State`) and how the JSON is returned.
   - The router function in `advisory/endpoints/mod.rs`, to see how `Router::new().route(...)` is chained and where caching middleware is configured.
   - `AdvisorySummary` in `advisory/model/summary.rs`, to find the type of the `severity` field (enum, `String` or `Option<...>`) and its exact variants or values.
   - The `sbom_advisory` entity in `entity/src/sbom_advisory.rs`: its columns (`sbom_id`, `advisory_id`) and its `Relation` to `advisory`.
   - `AppError` in `common/src/error.rs`: the `NotFound` variant and how `.context()` is used.
   - `SbomService::fetch` in `sbom/service/sbom.rs` and the SBOM `get.rs` handler, to see how the "SBOM not found leads to 404" behaviour is implemented, so I match it (AC 2).
3. `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` and on the advisory router function. I am only adding code, but I want to confirm nothing breaks.
4. `mcp__serena_backend__search_for_pattern`:
   - `advisory-summary` and `severity_summary`, to make sure the feature does not already exist.
   - `Severity`, `SEVERITY`, `severity_count` across `modules/` and `common/`, to look for an existing severity enum or counting helper before declaring a new one (symbol deduplication).
5. Sibling conformance:
   - Production code: `get_symbols_overview` on `advisory/endpoints/get.rs`, `advisory/endpoints/list.rs`, `sbom/endpoints/get.rs`, `advisory/model/summary.rs` and `advisory/model/details.rs`.
   - Tests: `tests/api/advisory.rs` and `tests/api/sbom.rs`.

### CONVENTIONS.md lookup

`./CONVENTIONS.md` exists at the repository root. I read it in full for:
- naming, layout and test conventions to follow;
- **verification commands**: I record every command under its CI checks / lint section (expected to be something like `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo check`), for Step 9;
- **code generation commands**, for example OpenAPI spec regeneration. If any exist, I run them in Step 9 and commit their output.

### Documentation files to track

- `README.md`
- `docs/api.md`, the REST API reference. This is a candidate for documenting the new endpoint.
- `docs/architecture.md`
- `CONVENTIONS.md`

### Expected conventions (confirmed against siblings during Step 4)

- **Errors:** handlers return `Result<T, AppError>`. Fallible calls are wrapped with `.context("...")`. A missing entity becomes `AppError::NotFound`.
- **Naming:** files and functions in `snake_case`, using a `verb`/`noun` pattern. Model structs end in `...Summary` or `...Details`.
- **Module structure:** `model/ + service/ + endpoints/`. Each new file is registered with `pub mod` in the sibling `mod.rs`.
- **Models:** derive `Serialize, Deserialize, Debug, Clone, PartialEq, Eq` plus `utoipa::ToSchema` if siblings use it.
- **Service methods:** `pub async fn name(&self, <args>, tx: &Transactional<'_>) -> Result<T, Error>`.
- **Tests:** integration tests against a real Postgres database. Status assertions use `assert_eq!(resp.status(), StatusCode::OK)`.
- **Skill overrides that take precedence over siblings:** value-based assertions (compare the whole `SeveritySummary`, not just counts), a `///` doc comment on every test, and given/when/then comments in non-trivial tests.

Convention conflicts:
- None expected.
- One thing to confirm: the Implementation Notes say to "return the struct directly (Axum's `Json` handles serialization)". If `get.rs` actually returns `Json(value)`, I follow `get.rs`, because that is how the note's own intent plays out in practice.
- If the existing code really does differ from the task, I flag it to the user before going further.

## Step 5 – Create Branch

```
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 – Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

```rust
/// Aggregated count of unique advisories per severity level for a single SBOM.
#[derive(Serialize, Deserialize, Debug, Clone, Default, PartialEq, Eq, ToSchema)]
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

- `Default` gives zeros for every level, which covers AC 4.
- I add a small doc-commented helper, `fn record(&mut self, severity: ...)`, that increments the matching bucket and `total`. It matches on the severity type found in `AdvisorySummary`.
- **Open question for Step 4:** how should `total` treat advisories whose severity is missing or outside the four levels? The AC defines `total` as the count of unique advisories. If unknown-severity advisories exist, `total` can be larger than the sum of the four buckets. I keep that behaviour, document it in the doc comment, and mention it in the PR. I do not invent a new bucket.

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` (plus a `pub use` re-export if siblings do that).

### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add this to `impl AdvisoryService`:

```rust
/// Returns per-severity counts of unique advisories linked to the given SBOM.
///
/// Returns `Ok(None)` when the SBOM does not exist so the endpoint can map it to 404.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<Option<SeveritySummary>, Error>
```

Logic:
1. **SBOM existence.** Look up `entity::sbom` by id using the same connection or transaction handling as `fetch`. If the SBOM is missing, return `Ok(None)`. I mirror whatever `SbomService::fetch` and the SBOM `get` endpoint use to produce a 404 (AC 2).
2. **Linked advisories, deduplicated.** Query `entity::advisory` inner-joined through `entity::sbom_advisory`, filtered on `sbom_advisory::Column::SbomId.eq(sbom_id)`. Select `advisory::Column::Id` and the severity column with `.distinct()` (one row per advisory id). This is done in SQL, so it covers AC 3 (deduplication) and keeps the query bounded for AC 5 (under 200ms with 500 advisories).
   - Preferred option: aggregate in SQL with `GROUP BY severity` and `COUNT(DISTINCT advisory.id)`.
   - Fallback: if the severity representation makes that awkward, fetch the distinct `(id, severity)` pairs and fold them in Rust. At 500 or fewer rows this is trivially fast.
3. **Fold** the rows into `SeveritySummary::default()` using `record`. The severity value is read defensively: `Option`/`NULL` goes only to `total`.
4. Wrap DB errors with `.context("failed to aggregate advisory severities for SBOM")`, in the same style as `fetch`/`list`.
5. Reuse what already exists: the `Transactional` and connection helper used by `fetch`/`list`, plus any filter helpers from `common/src/db/query.rs`. I add no new query utilities.
6. **Query scope:** the query is filtered on `sbom_id`, so it only touches the target subset and never loads all advisories.

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

```rust
/// GET /api/v2/sbom/{id}/advisory-summary — severity breakdown of advisories linked to an SBOM.
#[utoipa::path(...)] // only if sibling get.rs uses utoipa annotations
pub async fn get_severity_summary(
    service: <same injection as get.rs>,
    Path(id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    let tx = <same as get.rs>;
    service
        .severity_summary(id, &tx)
        .await
        .context("fetching advisory severity summary")?
        .map(Json)
        .ok_or_else(|| AppError::NotFound(format!("SBOM {id} not found")))
}
```

The exact `AppError` variant, handler naming and return wrapper are copied from `get.rs` and the SBOM `get.rs`.

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

- Add `mod severity_summary;`.
- Register `.route("/api/v2/sbom/{id}/advisory-summary", get(severity_summary::get_severity_summary))`. The path syntax (`{id}` or `:id`) and the prefix handling are copied from the existing registrations.
- Apply the same caching middleware configuration that sibling routes use, if any.
- **Note:** the route lives under the `/api/v2/sbom` prefix but is registered in the advisory module, as the task specifies. In Step 4 I check that no other route in the SBOM router conflicts with it.

### 6.6 `server/src/main.rs`

Listed in Files to Modify, but the description says "no changes needed (routes auto-mount via module registration)". In Step 4 I confirm that the advisory router is already mounted, and I make **no edits** to this file.

### 6.7 OpenAPI and documentation

- If the project generates an OpenAPI spec (code generation command from CONVENTIONS.md), I register the new path/schema in the existing `utoipa` `OpenApi` derive only if that derive lives in an in-scope file. If it lives elsewhere, I flag it in Step 9 rather than editing it silently.
- The task has no Documentation Updates section. `docs/api.md` describes the REST API, so it is a doc-impact candidate. It is not in Files to Modify, so I raise it in the Step 9 scope check for user approval instead of editing it on my own.

### 6.8 Code quality

- Every new struct, field, function and helper gets a `///` doc comment.
- Severity data coming from the joined advisory rows is accessed defensively: `Option` values are handled, nothing calls `unwrap()`.

## Step 7 – Write Tests: `tests/api/advisory_summary.rs`

Shared approach:
- Use the same fixtures and harness as `tests/api/advisory.rs`: a real Postgres test database and the same ingestion and setup helpers.
- Seed data with existing helpers where possible.
- Compare the full `SeveritySummary` value, not individual counts or lengths alone.
- Every test gets a `///` doc comment and `// Given / // When / // Then` sections.

| # | Test | Given | Then |
|---|---|---|---|
| 1 | `severity_summary_returns_counts_per_level` | SBOM linked to advisories with known severities, e.g. 2 Critical, 1 High, 3 Medium, 1 Low | Status 200, body equals `SeveritySummary { critical: 2, high: 1, medium: 3, low: 1, total: 7 }` |
| 2 | `severity_summary_unknown_sbom_returns_404` | A random or nonexistent SBOM id | `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` |
| 3 | `severity_summary_no_advisories_returns_zeros` | An SBOM with no advisory links | Status 200, body equals `SeveritySummary::default()` |
| 4 | `severity_summary_deduplicates_advisory_links` | One advisory linked to the SBOM more than once (duplicate `sbom_advisory` rows, or the same advisory reached through multiple links), plus one other advisory | Each advisory counts once, e.g. `{ critical: 1, high: 1, medium: 0, low: 0, total: 2 }` |

- Tests 1–4 differ in setup and expected status, so they are written as separate tests, not parameterized (Meszaros heuristic).
- Duplicate links: if a unique constraint on `sbom_advisory` makes them impossible to insert, I recreate the duplication through the closest realistic path (for example, multiple ingestions) and record that in the PR.
- **Test module registration:** `tests/api/` has no listed `main.rs`/`mod.rs`. If `tests/Cargo.toml` or a test entry file needs a `[[test]]` or `mod advisory_summary;` entry, that file is outside scope and I flag it in Step 9 for approval.
- I capture a baseline of `cargo build`/`clippy` warnings before the changes, then run `cargo test -p <tests crate>` and `cargo test -p <fundamental crate>`, and fix any failures.

## Step 8 – Verify Acceptance Criteria

| AC | How it is satisfied |
|---|---|
| Returns `{critical, high, medium, low, total}` | `SeveritySummary` serializes to exactly these fields; test 1 |
| 404 for missing SBOM, consistent with SBOM endpoints | Existence check plus the same `AppError` variant the SBOM `get` uses; test 2 |
| Unique advisories only | `DISTINCT` / `COUNT(DISTINCT advisory.id)` in SQL; test 4 |
| Levels default to 0 | `#[derive(Default)]`; test 3 |
| Under 200ms with 500 or fewer advisories | One filtered, indexed join on `sbom_advisory.sbom_id` plus an SBOM lookup, with no N+1 queries. I check the index on `sbom_id` exists (migration) and time the request for a 500-advisory fixture if feasible |

## Step 9 – Self-Verification

- **Scope containment:** `git diff --name-only` must list only these files.
  - Modified: `advisory/service/advisory.rs`, `advisory/endpoints/mod.rs`, `advisory/model/mod.rs`
  - Created: `advisory/model/severity_summary.rs`, `advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs`
  - `server/src/main.rs` should stay unchanged.
  - Candidates I may flag for approval: test-crate registration, `docs/api.md`, an OpenAPI aggregator file.
- **Untracked files:** run `git status --short` and check `??` entries in the touched directories.
- **Dead parameters:** none expected, since this change only adds code.
- **Validated-value override paths:** none. There are no merge or override paths after the counts are computed.
- **Sensitive patterns:** grep the staged diff for secrets.
- **Documentation currency:** check `docs/api.md` (see above).
- **Duplication:** search for existing severity enums or counters and reuse them if found.
- **Cross-section consistency:** every path in Files to Modify, Files to Create and Implementation Notes refers to the same `modules/fundamental/src/advisory/...` tree. These are consistent.
- **CI checks from CONVENTIONS.md:** run every extracted command, plus any code generation commands. Any non-zero exit is a **hard stop**: I report it and do not commit.
- **Rust module-level tests:** use `cargo metadata --no-deps --format-version 1` to find the packages that own the changed files (the fundamental module crate and the tests crate), then run `cargo test -p <crate>` for each. Non-zero exit is a hard stop.
- **Data-flow trace:** HTTP GET → `Path<Id>` → `AdvisoryService::severity_summary` → SBOM existence check → DISTINCT join on `sbom_advisory`→`advisory` → fold into `SeveritySummary` → `Json` response, or `AppError::NotFound` → 404. Every stage connects to the next.
- **Query scope:** filtered by `sbom_id`, not a full scan.
- **Contract and sibling parity:**
  - Contract: the handler signature is compatible with Axum `Handler`.
  - Sibling parity: same error wrapping, tracing/logging attributes and caching as `get.rs`.
  - Cross-module entity: read-only access to `sbom_advisory`, so there are no write conflicts.
  - Caller site: the service is called the same way `get.rs` calls `fetch`.

## Step 10 – Commit and Push

```
git add <in-scope files>
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(advisory): add SBOM advisory severity summary endpoint

Add AdvisoryService::severity_summary and GET /api/v2/sbom/{id}/advisory-summary
returning unique advisory counts per severity level (critical, high, medium,
low) and a total. Returns 404 for unknown SBOMs.

Implements TC-9201"
```

- **Fork detection:** run `git remote get-url upstream`.
  - If an upstream remote exists: `gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9201 --base main`.
  - Otherwise: `gh pr create --base main`.
- **PR body:** summary, list of changes, test plan, the `Implements [TC-9201](<webUrl>)` line, and `Closes <owner>/<repo>#<n>` only if the GitHub Issue field was populated.

## Step 11 – Update Jira

1. `jira.update_issue("TC-9201", {"customfield_10875": <ADF doc with inlineCard url=PR-URL>})`.
2. `jira.add_comment("TC-9201", ...)` containing the PR link, a summary of changes, and any deviations. Deviations include `server/src/main.rs` being left untouched as instructed, and any out-of-scope files the user approved. The comment ends with the footnote from `shared/comment-footnote.md` for skill `implement-task`.
3. `jira.transition_issue("TC-9201", "In Review")`.
