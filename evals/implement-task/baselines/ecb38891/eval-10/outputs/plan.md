# Implementation Plan: TC-9208 — Add Package License Summary Endpoint

## Task Overview

Add a REST endpoint `GET /api/v2/sbom/{id}/license-summary` that returns a summary of
license types (permissive, copyleft, unknown) for packages within an SBOM. Each category
includes a count and a list of specific license identifiers.

## Target Branch

**main** — extracted from the task description's Target Branch section.

## Branch Operations

```
git checkout main
git pull
git checkout -b TC-9208
```

## Step 4 — Code Inspection

Before making any changes, inspect the following existing files to understand current
patterns and confirm referenced code exists:

1. **`modules/fundamental/src/package/endpoints/list.rs`** — read to understand the
   existing endpoint handler pattern (route registration, request extraction, service
   call, response formatting). This is the primary sibling for the new endpoint handler.

2. **`modules/fundamental/src/package/model/summary.rs`** — read to understand the
   existing model struct pattern (derives, field types, serialization attributes). This
   is the sibling for the new LicenseSummary model.

3. **`modules/fundamental/src/package/endpoints/mod.rs`** — read to see how routes are
   currently registered and identify where to add the new route.

4. **`modules/fundamental/src/package/model/mod.rs`** — read to see how model
   sub-modules are currently exported and where to add the new module declaration.

5. **`entity/src/package_license.rs`** — read to understand the Package-License mapping
   entity structure for building the JOIN query.

6. **`common/src/error.rs`** — read to understand the AppError enum and how to return
   404 responses.

7. **`tests/api/advisory.rs`** and **`tests/api/sbom.rs`** — read to understand test
   conventions (setup, naming, assertion patterns). Note: sibling assertion style
   conflicts with skill guidance; see conventions.md for resolution.

8. **`CONVENTIONS.md`** — check the repository root for project-wide conventions and
   CI verification commands.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/mod.rs`

**Change:** Add route registration for the new license summary endpoint.

- Add `pub mod license_summary;` to import the new endpoint module.
- Register `GET /api/v2/sbom/{id}/license-summary` route pointing to the
  `license_summary::get_license_summary` handler.
- Follow the existing route registration pattern used for `list.rs`.

### 2. `modules/fundamental/src/package/model/mod.rs`

**Change:** Export the new LicenseSummary model module.

- Add `pub mod license_summary;` declaration alongside existing model modules
  (e.g., `pub mod summary;`).

## Files to Create

### 3. `modules/fundamental/src/package/model/license_summary.rs`

**Change:** Define the LicenseSummary response struct.

- Create a `LicenseCategoryDetail` struct with fields:
  - `count: usize` — number of unique licenses in this category
  - `licenses: Vec<String>` — deduplicated list of license identifiers
- Create a `LicenseSummary` struct with fields:
  - `permissive: LicenseCategoryDetail`
  - `copyleft: LicenseCategoryDetail`
  - `unknown: LicenseCategoryDetail`
- Derive `Serialize, Deserialize, Debug, Clone` on both structs.
- Add doc comments on both structs explaining their purpose.

### 4. `modules/fundamental/src/package/endpoints/license_summary.rs`

**Change:** Implement the GET handler for the license summary endpoint.

- Define `get_license_summary` async handler function accepting the SBOM ID path parameter.
- Return `Result<Json<LicenseSummary>, AppError>`.
- Query the database using the `package_license` entity from `entity/src/package_license.rs`:
  1. Verify the SBOM exists; return 404 AppError if not found.
  2. JOIN `sbom_package` with `package_license` to get all licenses for packages in the SBOM.
  3. Deduplicate licenses within each category.
  4. Categorize each license as permissive, copyleft, or unknown.
  5. Build the LicenseSummary response with counts and license identifier lists.
- Use `.context()` wrapping for all fallible operations.
- Follow the endpoint handler pattern from `list.rs`.
- Add a doc comment on the handler function.

### 5. `tests/api/package_license.rs`

**Change:** Write integration tests for the license summary endpoint.

- See `test-plan.md` for the detailed test assertion approach.
- Follow sibling test conventions for naming, setup, teardown, and organization.
- Use value-based assertions per skill guidance (overriding sibling `.any()`/`.count()` patterns).
- Four test functions covering all Test Requirements.

## Commit Message

```
feat(package): add license summary endpoint

Add GET /api/v2/sbom/{id}/license-summary that returns categorized
license counts (permissive, copyleft, unknown) with deduplicated
license identifier lists for packages within an SBOM.

Implements TC-9208
```

With flag: `--trailer='Assisted-by: Claude Code'`

## Acceptance Criteria Verification

- [x] GET /api/v2/sbom/{id}/license-summary returns categorized license counts — implemented in endpoint handler
- [x] Returns 404 when SBOM ID does not exist — handler checks SBOM existence first
- [x] Each category includes both a count and a list of license identifiers — LicenseSummary struct design
- [x] Licenses are deduplicated within each category — deduplication in query/handler logic
