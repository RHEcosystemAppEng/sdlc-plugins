# Implementation Plan — TC-9208: Add package license summary endpoint with tests

## Pre-flight (Steps 0–3, simulated)

- **Step 0 – Project Configuration**: mock CLAUDE.md has Repository Registry (trustify-backend, Serena `serena_backend`, path `./`), Jira Configuration (project key, Cloud ID, Feature issue type ID), and Code Intelligence. Validation passes.
- **Step 1 – Parse task**: all required sections present (Repository, Target Branch=`main`, Description, Files to Modify/Create, API Changes, Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies). No Target PR and no Bookend Type, so this runs in **default mode** (direct to `main`).
- **Step 1.5 – Digest check**: would fetch comments and compare digests (not executed in eval).
- **Step 2 – Dependencies**: "None", nothing to verify.
- **Step 3**: would assign to current user and transition to In Progress (not executed).
- **Step 5 – Branch**: `git checkout main && git pull && git checkout -b TC-9208` (not executed).

## Step 4 – Code understanding (via `serena_backend`, simulated)

- `get_symbols_overview` on `modules/fundamental/src/package/endpoints/mod.rs`, `endpoints/list.rs`, `model/mod.rs`, `model/summary.rs`.
- `find_symbol include_body=true` on the list handler in `package/endpoints/list.rs` (the pattern named in Implementation Notes), and on `PackageService` in `package/service/mod.rs`.
- Inspect `entity/src/package_license.rs`, `entity/src/sbom_package.rs`, `entity/src/package.rs` for the JOIN path SBOM -> sbom_package -> package -> package_license.
- Check `common/src/error.rs` (`AppError`, incl. its NotFound variant) and `common/src/db/query.rs` for reusable helpers.
- Read sibling get-by-id handlers (`sbom/endpoints/get.rs`, `advisory/endpoints/get.rs`) for the 404 pattern.
- Read `CONVENTIONS.md` at repo root (exists per repo tree) for conventions and CI check commands (recorded for Step 9 check 14).
- Sibling tests `tests/api/sbom.rs`, `tests/api/advisory.rs` analysed — see `conventions.md`.

## Step 6 – Files to Modify

### 1. `modules/fundamental/src/package/model/mod.rs`
- Add `pub mod license_summary;` (and re-export `pub use license_summary::*;` only if sibling `summary` module is re-exported that way — mirror existing style).

### 2. `modules/fundamental/src/package/endpoints/mod.rs`
- Add `mod license_summary;`.
- Register the route `GET /api/v2/sbom/{id}/license-summary` -> `license_summary::get_license_summary` using the same router builder / caching middleware configuration as the existing `list` route registration.
- Note: the path lives under `/api/v2/sbom`, but the task explicitly scopes registration to the package endpoints module; follow the task. If the package router is nested under `/api/v2/package`, register at the router level that permits an absolute `/api/v2/sbom/{id}/license-summary` path; any edit needed in `sbom/endpoints/mod.rs` or `server/src/main.rs` would be out of scope and raised as a Step 9 scope flag for user approval rather than silently made.

## Step 6 – Files to Create

### 3. `modules/fundamental/src/package/model/license_summary.rs`
```rust
/// Licenses in one category with their deduplicated identifiers.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize, ToSchema)]
pub struct LicenseCategory {
    /// Number of distinct license identifiers in this category.
    pub count: usize,
    /// Sorted, deduplicated license identifiers.
    pub licenses: Vec<String>,
}

/// Summary of package licenses in an SBOM grouped by license type.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize, ToSchema)]
pub struct LicenseSummary {
    pub permissive: LicenseCategory,
    pub copyleft: LicenseCategory,
    pub unknown: LicenseCategory,
}
```
- Constructor/helper `LicenseSummary::from_licenses(impl IntoIterator<Item = Option<String>>)`: classify each identifier into permissive/copyleft/unknown, collect into `BTreeSet<String>` per category (dedup + deterministic order), then set `count = set.len()`. `None`/empty license -> `unknown` (defensive handling of DB data, per skill's defensive-access guidance) — whether a missing license contributes an identifier string (e.g. none) is decided by checking what the entity stores; default: skip missing values from the list, not invent a placeholder.
- Classification: a small `fn classify(id: &str) -> LicenseKind` with documented match on known SPDX ids (permissive: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, ...; copyleft: GPL-*, LGPL-*, AGPL-*, MPL-2.0, EPL-*, ...; else unknown). First search the codebase (`search_for_pattern` for "copyleft", "permissive", "SPDX") for an existing classifier to reuse per the Reuse rule.
- Count = number of deduplicated identifiers (AC: "Licenses are deduplicated within each category"; test requirement: "duplicate licenses within a category are counted only once").
- Doc comments on every new struct, field-level where meaning is not obvious, and public fn.

### 4. `modules/fundamental/src/package/endpoints/license_summary.rs`
- Handler modelled on `package/endpoints/list.rs`:
```rust
/// Returns license counts for an SBOM's packages, grouped by license type.
#[utoipa::path(get, path = "/api/v2/sbom/{id}/license-summary", ... responses((status = 200, body = LicenseSummary), (status = 404)))]
pub async fn get_license_summary(
    State(service): State<PackageService>,   // same extractor shape as list.rs
    Path(id): Path<Uuid>,                     // id type matches sbom get.rs
) -> Result<Json<LicenseSummary>, AppError> {
    let summary = service
        .license_summary(id, &db)
        .await
        .context("Failed to compute license summary")?
        .ok_or_else(|| AppError::NotFound(format!("SBOM {id} not found")))?;
    Ok(Json(summary))
}
```
- Service logic: add `license_summary(sbom_id)` to `PackageService` in `package/service/mod.rs`: first check SBOM existence (`entity::sbom::Entity::find_by_id`) -> `None` gives 404; then query `sbom_package` JOIN `package` JOIN `package_license` filtered by `sbom_id`, selecting license identifiers, and build `LicenseSummary::from_licenses`. SBOM with no packages yields `LicenseSummary::default()` (all zeros, empty lists).
- **Scope note**: `package/service/mod.rs` is not in Files to Modify. Preferred path is to place the query in the service to match the module pattern (`model/ + service/ + endpoints/`); this is an unlisted edit and would be raised as a Step 9 scope flag for user approval. If not approved, the query lives in the handler file (listed) using the shared DB connection, mirroring how list.rs obtains it.
- OpenAPI: add the `#[utoipa::path]` annotation and register the path/schema wherever siblings do; if an OpenAPI spec generation command exists in CONVENTIONS.md, run it in Step 9 and stage the generated artifact.

### 5. `tests/api/package_license.rs`
- Four integration tests (details in `test-plan.md`), following sibling structure/setup/naming from `tests/api/sbom.rs` and `advisory.rs`, but with value-based assertions (skill rule overrides sibling `.filter().any()` / `.count() > 0` style — see `conventions.md`).
- Register the test module if `tests/` uses a `mod` aggregator (e.g. `tests/api/main.rs`/`mod.rs`) — unlisted file -> Step 9 scope flag.

## Documentation impact
- New public endpoint: `docs/api.md` (referenced from mock CLAUDE.md) would ideally document `GET /api/v2/sbom/{id}/license-summary`. It is not in Files to Modify, so it is reported as a Step 9 scope/doc-currency flag rather than edited.

## Step 8 – Acceptance criteria mapping
| AC | Satisfied by |
|---|---|
| Returns categorized license counts | handler + `LicenseSummary::from_licenses`; test 1 |
| 404 for missing SBOM | existence check -> `AppError::NotFound`; test 2 |
| Each category has count + list | `LicenseCategory { count, licenses }`; tests 1, 3 |
| Deduplicated within category | `BTreeSet` collection; test 4 |

## Step 9 – Self-verification (planned checks)
- Scope containment: flag `package/service/mod.rs`, any test aggregator, `docs/api.md`, and any sbom router/server mount change as out-of-scope for approval.
- Duplication: confirm no existing license classifier/query helper.
- Data-flow trace: route -> handler -> service -> DB JOIN -> model -> JSON.
- Query scope: query filtered by `sbom_id`; no unbounded scans.
- Contract & sibling parity: error handling and router registration match list.rs/get.rs.
- CI checks from CONVENTIONS.md (or `cargo fmt --check`, `cargo clippy`, build fallback).
- Module tests (Rust): resolve crates via `cargo metadata` and run `cargo test -p <fundamental crate>` and the `tests` crate.
- Documentation currency: flag `docs/api.md`.

## Steps 10–11 (not executed)
Commit `feat(package): add SBOM license summary endpoint` referencing TC-9208, open PR against `main`, set Jira Git Pull Request field `customfield_10875`, comment on Jira with footnote.
