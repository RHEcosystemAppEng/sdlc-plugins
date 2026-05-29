# Implementation Plan: TC-9201 -- Add advisory severity aggregation service and endpoint

## Task Summary

Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. The endpoint `GET /api/v2/sbom/{id}/advisory-summary` returns a JSON summary with counts per severity level (Critical, High, Medium, Low) and a total.

**Target Branch:** main
**Working Branch:** TC-9201 (branched from main)

---

## Files Inspected / Analyzed Before Planning

The following files were analyzed (via repository structure and task description) to understand existing patterns and conventions before planning changes:

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- Studied to understand the endpoint handler pattern: `Path<Id>` extraction, service invocation, `Result<Json<T>, AppError>` return type, and transaction handling.
2. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Studied to understand `AdvisoryService` method signatures (`&self`, `id: Id`, `tx: &Transactional<'_>`), return types, and how the service interacts with entity/ORM layers.
3. **`modules/fundamental/src/advisory/model/summary.rs`** -- Studied to understand the `AdvisorySummary` struct and its `severity` field, which is the source data for counting by severity level.
4. **`modules/fundamental/src/advisory/model/mod.rs`** -- Studied to understand the `pub mod` re-export pattern for registering new model modules.
5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Studied to understand route registration pattern (`Router::new().route(...)` and how handlers are wired).
6. **`common/src/error.rs`** -- Studied to understand the `AppError` enum, its variants (including not-found), and the `.context()` wrapping pattern.
7. **`entity/src/sbom_advisory.rs`** -- Studied to understand the join table linking SBOMs to advisories, which is needed for the aggregation query.
8. **`entity/src/advisory.rs`** -- Studied to understand the advisory entity structure.
9. **`entity/src/sbom.rs`** -- Studied to understand SBOM entity for existence checks (404 handling).
10. **`tests/api/advisory.rs`** -- Studied to understand test harness patterns, HTTP client usage, and assertion style.
11. **`modules/fundamental/src/package/`** (full subtree) -- Studied as a sibling domain module to confirm the model/service/endpoints tri-layer pattern is consistent across domains.

---

## Files to Create

### 1. `modules/fundamental/src/advisory/model/severity_summary.rs`

**Purpose:** Define the `SeveritySummary` response struct.

**Details:** See `outputs/file-1-description.md`.

### 2. `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

**Purpose:** GET handler for `/api/v2/sbom/{id}/advisory-summary`.

**Details:** See `outputs/file-2-description.md`.

### 3. `tests/api/advisory_summary.rs`

**Purpose:** Integration tests for the new endpoint.

**Details:** See `outputs/file-3-description.md`.

---

## Files to Modify

### 4. `modules/fundamental/src/advisory/model/mod.rs`

**Purpose:** Register the new `severity_summary` model module.

**Details:** See `outputs/file-4-description.md`.

### 5. `modules/fundamental/src/advisory/endpoints/mod.rs`

**Purpose:** Register the new route for the severity summary endpoint.

**Details:** See `outputs/file-5-description.md`.

### 6. `modules/fundamental/src/advisory/service/advisory.rs`

**Purpose:** Add the `severity_summary` method to `AdvisoryService`.

**Details:** See `outputs/file-6-description.md`.

---

## Files NOT Modified

- **`server/src/main.rs`** -- No changes needed. Routes auto-mount via module registration as noted in the task description.

---

## Commit Strategy

Single commit encompassing all new and modified files.

### Commit Message

```
feat(advisory): add severity aggregation service and endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
advisory severity counts (critical, high, medium, low, total) for
a given SBOM. Includes SeveritySummary model, AdvisoryService method,
endpoint handler, and integration tests.

Refs: TC-9201
```

### Git Command

```bash
git checkout -b TC-9201 main
git add \
  modules/fundamental/src/advisory/model/severity_summary.rs \
  modules/fundamental/src/advisory/endpoints/severity_summary.rs \
  tests/api/advisory_summary.rs \
  modules/fundamental/src/advisory/model/mod.rs \
  modules/fundamental/src/advisory/endpoints/mod.rs \
  modules/fundamental/src/advisory/service/advisory.rs
git commit -m "feat(advisory): add severity aggregation service and endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
advisory severity counts (critical, high, medium, low, total) for
a given SBOM. Includes SeveritySummary model, AdvisoryService method,
endpoint handler, and integration tests.

Refs: TC-9201" --trailer='Assisted-by: Claude Code'
```

---

## Verification Steps

After implementation, verify:

1. `cargo check` passes with no errors.
2. `cargo test --test advisory_summary` passes all four test cases.
3. Manual curl to `GET /api/v2/sbom/{id}/advisory-summary` returns expected JSON shape.
4. 404 is returned for non-existent SBOM IDs.
5. Duplicate advisories are deduplicated in counts.
6. All severity fields default to 0 for SBOMs with no advisories.
