# Implementation Plan: TC-9201 – Add advisory severity aggregation service and endpoint

Simulated run of `/sdlc-workflow:implement-task TC-9201`. Nothing was changed in the
repository, and Jira, git, GitHub, and Serena were not called. Every action below is
what the skill would do.

---

## Step 0 – Validate Project Configuration: PASS

- Repository Registry: `trustify-backend` | Rust backend service | `serena_backend` | `./`
- Jira Configuration: Project key `TC`, Cloud ID `2b9e35e3-...`, Feature issue type ID `10142`,
  Git Pull Request field `customfield_10875`, GitHub Issue field `customfield_10747`
- Code Intelligence: naming convention `mcp__<serena-instance>__<tool>` is present. One
  limitation: rust-analyzer can take 30–60 s to index on first use.

## Step 0.5 – Jira Access

Use the Atlassian MCP first. If an MCP call fails, ask the user whether to fall back to
REST (`scripts/jira-client.py`), skip the operation, or retry.

## Step 1 – Fetch and Parse

`jira.get_issue("TC-9201")` returns:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Target PR | absent |
| Bookend Type | absent |
| Dependencies | None |
| Mode | **default** (steps 1–11; branch `TC-9201` from `main`; PR to `main`) |

- I record `webUrl` (for example `https://<jira-host>/browse/TC-9201`) for the PR body.
- GitHub Issue (`customfield_10747`): I read the field. If it holds a
  `https://github.com/<owner>/<repo>/issues/<n>` URL, I store `<owner>/<repo>#<n>` for a
  `Closes` line in the PR. If it is empty, I skip it silently.
- Every required section is present, so I have nothing to ask the user.

## Step 1.5 – Verify Description Integrity: MATCH, continue silently

There is one digest comment, `sha256-md:a1b2...7890`, and its `created` equals its
`updated`, so it was not edited. `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
produces the same tag and the same hex. I continue with no prompt. Details are in
`digest-match.md`.

## Step 2 – Verify Dependencies

Dependencies are "None", so there is nothing to check.
(The "is incorporated by TC-9001" link points to the parent feature, not a dependency.)

## Step 3 – Transition and Assign

1. `jira.user_info()` returns the current user's accountId.
2. `jira.edit_issue("TC-9201", assignee=<accountId>)`
3. `jira.transition_issue("TC-9201", "In Progress")`

## Step 4 – Understand the Code (Serena instance `serena_backend`)

### Files to inspect

| Tool call | Purpose |
|---|---|
| `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/service/advisory.rs")` | Structure of `AdvisoryService` (`fetch`, `list`, `search`) |
| `mcp__serena_backend__find_symbol("AdvisoryService/fetch", include_body=true)` | Signature pattern `(&self, id: Id, tx: &Transactional<'_>)`, how it gets a DB connection, and how errors are wrapped with `.context()` |
| `mcp__serena_backend__find_symbol("AdvisorySummary", include_body=true)` in `advisory/model/summary.rs` | Type of the `severity` field (enum or `String`/`Option<String>`) and its possible values |
| `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/endpoints/mod.rs")` and `find_symbol` for the router function | How routes are registered (`Router::new().route(...)`), including any caching layer |
| `mcp__serena_backend__find_symbol(..., include_body=true)` in `advisory/endpoints/get.rs` | Handler pattern: `Path<Id>`, service injection (`State`/`Extension`), return type `Result<Json<T>, AppError>` |
| `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/model/mod.rs")` | Existing `pub mod summary; pub mod details;` style |
| `mcp__serena_backend__find_symbol` in `entity/src/sbom_advisory.rs` | Join-table columns (`sbom_id`, `advisory_id`) and SeaORM `Relation`s to `advisory` and `sbom` |
| `mcp__serena_backend__find_symbol` in `entity/src/advisory.rs` | Where severity is stored in the DB (a column on `advisory` or derived) |
| `mcp__serena_backend__find_symbol("AppError", include_body=true)` in `common/src/error.rs` | `NotFound` variant and how `.context()` maps to responses |
| `mcp__serena_backend__find_symbol("SbomService/fetch", include_body=true)` in `sbom/service/sbom.rs` | How SBOM endpoints return 404 for a missing SBOM, so the 404 behavior matches them |
| `mcp__serena_backend__find_referencing_symbols("AdvisoryService")` | Callers and construction sites, so adding a method can't break them (additive, low risk) |
| `mcp__serena_backend__search_for_pattern("advisory-summary\|severity_summary\|SeveritySummary\|SEVERITY")` | Reuse check: an existing severity enum, ordering constant, or aggregation helper |
| `mcp__serena_backend__search_for_pattern("/api/v2/sbom/")` | Whether any route under `/api/v2/sbom/{id}/...` is already registered outside the sbom module, which tells me if a cross-module path is acceptable |
| `tests/api/advisory.rs`, `tests/api/sbom.rs`, `tests/Cargo.toml` | Test harness, fixtures and seeding helpers, assertion style, and how test files are registered (`[[test]]` entries or a `main.rs` with `mod` declarations) |

### Documentation files to check

- `README.md` at the repo root (API overview)
- `docs/api.md` (REST API reference, listed in CLAUDE.md). If it lists endpoints, it is
  affected by the new endpoint. It is not in Files to Modify, so it becomes a Step 9
  check 6 / check 1 **scope flag**, not an edit.
- `docs/architecture.md`, unlikely to be affected.
- `CONVENTIONS.md`

### CONVENTIONS.md lookup

Read `./CONVENTIONS.md`, at the root from the Registry Path. I would follow naming,
directory, and test conventions from it, and pull out:
- **CI check commands**. Expected: `cargo fmt --check`,
  `cargo clippy --all-targets -- -D warnings`, `cargo check`, possibly `cargo test`.
- **Code generation commands**. If an OpenAPI spec is generated (for example from
  `utoipa` annotations), I record the command so the regenerated spec is staged in Step 9.

### Conventions from siblings (binding for Steps 6 and 7)

From the repo summary, to be confirmed by Serena on `endpoints/get.rs`, `endpoints/list.rs`,
`sbom/endpoints/get.rs`, and `tests/api/advisory.rs`:

- **Module layout**: `model/` + `service/` + `endpoints/` per domain, with one file per
  model struct and one per handler.
- **Naming**: snake_case files and functions, `verb_noun` or noun handlers, PascalCase
  structs, and `*Summary` for response structs.
- **Errors**: handlers return `Result<T, AppError>` and wrap fallible calls with
  `.context("...")`.
- **Handlers**: `Path<Id>` extraction, call the service, return `Json(...)`.
- **Service methods**: `&self, <id>: Id, tx: &Transactional<'_>`.
- **Routes**: `Router::new().route("/path", get(handler))` in each module's
  `endpoints/mod.rs`. `server/main.rs` mounts modules, and caching middleware is set up
  in the route builders.
- **Tests**: integration tests against real PostgreSQL in `tests/api/`, using
  `assert_eq!(resp.status(), StatusCode::OK)`.

### Convention conflicts or ambiguities to raise before implementing

1. **Route path versus owning module**: the endpoint is `/api/v2/sbom/{id}/advisory-summary`
   but has to be registered in the **advisory** module's `endpoints/mod.rs`, whose
   prefix is `/api/v2/advisory`. If the advisory router is nested under
   `/api/v2/advisory`, I must register the route with an absolute path or merge a
   separate un-nested router. If neither works without touching `sbom/endpoints/mod.rs`
   or `server/main.rs`, I'll ask the user. The task says `server/src/main.rs` needs no
   changes, so I won't touch it.
2. **What `total` means**: is it the sum of the four levels, or all unique linked
   advisories, including ones with unknown or `None` severity? My default is the count
   of unique linked advisories, documented in the struct's doc comment. I'll confirm
   with the user if severity values outside the four levels show up in the data.

## Step 5 – Branch (default mode)

```
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 – Implement Changes

Working scope: the 3 files to modify and the 3 files to create. `server/src/main.rs` is
listed only to say it needs **no changes**, and it stays untouched.

### 6.1 `modules/fundamental/src/advisory/model/severity_summary.rs` (new)

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema; // only if siblings derive ToSchema

/// Counts of unique advisories linked to an SBOM, grouped by severity level.
///
/// Every level defaults to 0 when the SBOM has no advisories at that level.
/// `total` is the number of unique advisories linked to the SBOM.
#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    pub critical: u64,
    pub high: u64,
    pub medium: u64,
    pub low: u64,
    pub total: u64,
}
```

- `Default` gives the required zero values for every level.
- The derives copy whatever `AdvisorySummary` uses, such as `ToSchema` when siblings use it.

### 6.2 `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` next to `pub mod summary;` and `pub mod details;`,
plus a `pub use` re-export if siblings re-export.

### 6.3 `modules/fundamental/src/advisory/service/advisory.rs`: `AdvisoryService::severity_summary`

```rust
/// Aggregates severity counts of unique advisories linked to the given SBOM.
///
/// Returns `Ok(None)` when the SBOM does not exist so the endpoint can respond 404.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<Option<SeveritySummary>, Error>
```

Logic, following the connection and transaction handling in `fetch`:
1. **Check the SBOM exists**: look it up with `entity::sbom::Entity::find_by_id(...)`,
   the same lookup the SBOM endpoints use (I'll reuse a helper if one exists). If it
   is missing, return `Ok(None)`. If the sibling pattern returns an `Error::NotFound`
   instead, I follow that.
2. **Aggregate in a single query** through the `sbom_advisory` join table:
   `SELECT advisory.severity, COUNT(DISTINCT advisory.id) FROM sbom_advisory JOIN advisory ON ... WHERE sbom_advisory.sbom_id = $1 GROUP BY advisory.severity`,
   built with SeaORM (`select_only().column(..).column_as(Expr::col(advisory::Column::Id).count_distinct(), "count").group_by(..)`).
   - `COUNT(DISTINCT advisory.id)` satisfies "deduplicates by advisory ID".
   - Grouping in the database keeps the work at O(levels) rows instead of loading up
     to 500 advisories. That covers the under-200 ms requirement and makes sure the
     query filters on `sbom_id` (check 12).
3. **Map severities to fields**: match case-insensitively on the severity value from
   the `AdvisorySummary`/entity type (reusing an existing severity enum or constant
   if Step 4 finds one) and fill `critical`, `high`, `medium`, `low`. `total` comes
   from a `COUNT(DISTINCT advisory.id)` over the same join, so each advisory is counted
   once even if its severity is unknown.
4. Wrap DB errors with `.context("Failed to aggregate advisory severities for SBOM")`.
5. Treat a null severity as "not in any level", using defensive handling of the
   `Option` field.

### 6.4 `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (new)

```rust
/// Returns severity counts of unique advisories linked to an SBOM.
///
/// Responds 404 when the SBOM does not exist.
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,   // match get.rs injection style
    Path(id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    let tx = Transactional::None;              // match get.rs
    service
        .severity_summary(id, &tx)
        .await
        .context("Failed to compute advisory severity summary")?
        .map(Json)
        .ok_or_else(|| AppError::NotFound(format!("SBOM {id} not found")))
}
```

The 404 construction copies `sbom/endpoints/get.rs` exactly, so the 404 is
"consistent with existing SBOM endpoints". If siblings carry `#[utoipa::path(...)]`
annotations, I add one with responses 200 and 404.

### 6.5 `modules/fundamental/src/advisory/endpoints/mod.rs`

- Add `mod severity_summary;`
- Register `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))`.
  The path syntax (`:id` or `{id}`) follows the Axum version used by the existing routes,
  and the caching layer matches the existing routes. The nesting question is in Step 4,
  conflict 1.

### Reuse decisions

- Reuse `AppError` and `.context()` from `common/src/error.rs`, `Transactional`, `Id`,
  the entities `sbom_advisory`, `advisory`, `sbom`, and any existing severity enum or
  constant. I won't define a new `SEVERITY_*` constant if a variant already exists.
- Reuse the SBOM-existence lookup pattern from `SbomService::fetch`. Calling
  `SbomService` directly would only make sense if `fundamental::advisory` already
  depends on it. Both live in the same crate, so a direct call is fine. Otherwise I use
  the entity lookup inline and note that in the PR.

### Documentation impact

There is no Documentation Updates section and no doc file in scope. `docs/api.md` and
`README.md` endpoint lists are therefore **not edited**. They get flagged in Step 9.

## Step 7 – Write Tests: `tests/api/advisory_summary.rs` (new)

I follow the harness, fixtures, and `assert_eq!(resp.status(), StatusCode::OK)` style
in `tests/api/advisory.rs`. Every test gets a `///` doc comment. Non-trivial tests get
`// Given`, `// When`, `// Then` sections. Assertions compare whole values: the full
`SeveritySummary` struct, not single fields or lengths.

```rust
/// Verifies that an SBOM with known advisories returns correct per-severity counts.
#[tokio::test]
async fn advisory_summary_counts_by_severity() {
    // Given an SBOM linked to 2 critical, 1 high, 3 medium, 1 low advisories
    // When GET /api/v2/sbom/{id}/advisory-summary
    // Then 200 and body == SeveritySummary { critical: 2, high: 1, medium: 3, low: 1, total: 7 }
}

/// Verifies that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn advisory_summary_unknown_sbom_returns_404() { /* assert_eq!(resp.status(), StatusCode::NOT_FOUND) */ }

/// Verifies that an SBOM with no advisories returns all-zero counts.
#[tokio::test]
async fn advisory_summary_no_advisories_returns_zeros() {
    // Given an ingested SBOM with no advisory links
    // When requesting the summary
    // Then body == SeveritySummary::default()
}

/// Verifies that duplicate links to the same advisory are counted once.
#[tokio::test]
async fn advisory_summary_deduplicates_advisory_links() {
    // Given an SBOM linked twice to the same high advisory and once to a low advisory
    // When requesting the summary
    // Then body == SeveritySummary { critical: 0, high: 1, medium: 0, low: 1, total: 2 }
}
```

- **Parameterization**: the four tests differ in setup and expected status, so by the
  Meszaros heuristic they stay as separate tests. I won't add `rstest` unless the
  siblings already use it.
- **Duplicate-link fixture**: if `sbom_advisory` has a composite primary key that
  blocks duplicate rows, I build the duplicate the way ingestion can really produce it,
  for example the same advisory reached through two links or re-ingestion. If no such
  path exists, I tell the user the dedup test can only cover what the schema allows.
- **Test registration**: if `tests/Cargo.toml` uses `[[test]]` entries or a
  `tests/api/main.rs` needs `mod advisory_summary;`, that file is **outside the listed
  scope** and gets flagged for approval in Step 9 check 1 / check 2.

Run the tests (resolved in Step 9) and fix failures before continuing.

## Step 8 – Verify Acceptance Criteria

| Criterion | How it is satisfied |
|---|---|
| GET returns `{critical, high, medium, low, total}` | `SeveritySummary` serialized through `Json`, checked by test 1 |
| 404 for a missing SBOM, matching SBOM endpoints | Existence check plus the same `AppError::NotFound` path as `sbom/endpoints/get.rs`, checked by test 2 |
| Counts unique advisories only | `COUNT(DISTINCT advisory.id)`, checked by test 4 |
| Levels default to 0 | `#[derive(Default)]` and an initialized struct, checked by test 3 |
| Under 200 ms for up to 500 advisories | One indexed, grouped aggregate query returning at most about 5 rows. I'd confirm with a timed request against a 500-advisory fixture and confirm `sbom_advisory.sbom_id` is indexed. If it isn't, I'd raise that, since a migration is out of scope. |

## Step 9 – Self-Verification

Read `shared/self-verification.md`, then report each check that fires:

| # | Check | Expected result |
|---|---|---|
| 1 | Scope containment | Diff should be the 6 in-scope files. **Possible FLAGs**: `tests/Cargo.toml` or `tests/api/main.rs` (test registration), `docs/api.md` (new endpoint), any regenerated OpenAPI spec (staged without approval only if produced by a documented codegen command). `server/src/main.rs` should **not** appear. |
| 2 | Untracked files | Fires because there are new files in modified dirs. Make sure each new file is referenced (`mod severity_summary;` in both `mod.rs` files, test registered). |
| 3 | Sensitive patterns | Run `git diff HEAD` and `git diff --cached` greps. Expected PASS. |
| 4 | Dead parameters | Doesn't fire, since no code was removed. |
| 5 | Duplication | Fires. Search for existing severity aggregation or count helpers and severity enums. Expected PASS after the Step 6 reuse decisions. |
| 6 | Documentation currency | Fires because a public API was added. **FLAG** `docs/api.md` / `README.md` if they list endpoints, then ask the user before editing. |
| 7 | Doc scope preservation | Doesn't fire. |
| 8 | Eval coverage | Doesn't fire, since no SKILL.md was touched. |
| 9 | Example consistency | Doesn't fire. |
| 10 | Cross-section references | Fires. `advisory.rs`, `endpoints/mod.rs`, `model/mod.rs`, `model/summary.rs`, `endpoints/get.rs`, `entity/src/sbom_advisory.rs`, and `common/src/error.rs` match between Files to Modify/Create and Implementation Notes. Expected PASS. |
| 11 | Data-flow trace | Fires. Request `Path<Id>` goes to the handler, then `AdvisoryService::severity_summary`, then the SBOM existence check, then the grouped `sbom_advisory` JOIN `advisory` query, then the mapping into `SeveritySummary`, then `Json` 200 (or `AppError::NotFound` 404). The route is reachable through the advisory router, which `server/main.rs` mounts. |
| 12 | Query scope | Fires (aggregation over DB records). The query is filtered by `sbom_id` and aggregated in SQL. Expected PASS. |
| 13 | Contract & sibling parity | Contract: no trait involved. Sibling parity: handler and service method match `get.rs` / `fetch` for error wrapping, transaction handling, caching layer, and OpenAPI annotation. Cross-module entity: read only, nothing to compare. Caller-site: `AdvisoryService` and SBOM lookup used the same way existing handlers use them. |
| 14 | CI checks from CONVENTIONS.md | Run every recorded command (for example `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`). Run any codegen command and stage its output. **Any failure is a hard stop.** |
| 15 | Module tests (Rust) | Run `cargo metadata --no-deps --format-version 1` and map files to packages: the `advisory/...` files to the fundamental crate, `tests/api/advisory_summary.rs` to the tests crate. Then `cargo test -p <fundamental-crate>` and `cargo test -p <tests-crate>` (or nextest). Needs PostgreSQL. Try the run first. A failure is a hard stop. |
| 16 | Validated-value override paths | Doesn't fire, since there are no security-relevant or fail-closed values. |

## Step 10 – Commit and Push (default mode)

```
git add modules/fundamental/src/advisory/model/severity_summary.rs \
        modules/fundamental/src/advisory/model/mod.rs \
        modules/fundamental/src/advisory/service/advisory.rs \
        modules/fundamental/src/advisory/endpoints/severity_summary.rs \
        modules/fundamental/src/advisory/endpoints/mod.rs \
        tests/api/advisory_summary.rs   # plus any user-approved flagged files
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(advisory): add SBOM advisory severity summary endpoint

Add AdvisoryService::severity_summary, which aggregates unique advisories
linked to an SBOM by severity via the sbom_advisory join table, and expose it
as GET /api/v2/sbom/{id}/advisory-summary returning critical/high/medium/low/total
counts (404 for unknown SBOM).

Implements TC-9201"
```

Fork detection: `git remote get-url upstream`.

```
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add SBOM advisory severity summary endpoint" --body "..."
# fork: gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9201 --base main ...
```

PR body:
- `Implements [TC-9201](<webUrl>)`
- `Closes <owner>/<repo>#<n>`, only if `customfield_10747` had a GitHub issue
- A summary of changes, the reuse decisions, the test list, and how the route was
  registered under the advisory router

## Step 11 – Update Jira (default mode)

1. Set `customfield_10875` to the PR URL as ADF:
   `{"type":"doc","version":1,"content":[{"type":"paragraph","content":[{"type":"inlineCard","attrs":{"url":"<PR-URL>"}}]}]}`
2. Post a comment with the PR link, a summary of changes, and any deviations (for
   example user-approved test-registration or docs edits, and the `total` semantics
   decision). It ends with a rule and the footnote "This comment was AI-generated by
   [sdlc-workflow/implement-task](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0."
3. `jira.transition_issue("TC-9201", "In Review")`

## Stop Conditions

Hand the decision to the user if the same test fails 3 times with the same error, if one
file is edited more than 5 times for one change, or if a build error survives 2 fix
attempts.
