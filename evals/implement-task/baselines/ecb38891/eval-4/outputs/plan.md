# Implementation Plan: TC-9204 — Add SBOM CycloneDX Export Endpoint

## Step 0 — Validate Project Configuration

Project Configuration verified in CLAUDE.md:
- Repository Registry: present, contains `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: present, includes Project key (TC), Cloud ID, Feature issue type ID
- Code Intelligence: present, with tool naming convention and configured instances

## Step 1 — Fetch and Parse Jira Task

**Key**: TC-9204
**Summary**: Add SBOM export endpoint
**Repository**: trustify-backend
**Target Branch**: main

### Parsed Sections

**Description**: Add an endpoint to export an SBOM in CycloneDX JSON format. The endpoint takes an SBOM ID and returns the full SBOM content formatted as a CycloneDX 1.5 JSON document.

**Files to Modify**:
- `modules/fundamental/src/sbom/service/sbom.rs` — add `export_cyclonedx` method to SbomService
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the export route

**Files to Create**:
- `modules/fundamental/src/sbom/model/export.rs` — CycloneDX export model struct
- `modules/fundamental/src/sbom/endpoints/export.rs` — GET handler for /api/v2/sbom/{id}/export
- `tests/api/sbom_export.rs` — integration tests for the export endpoint

**Target Branch**: main

**Dependencies**: None

### Target Branch extraction

The Target Branch is `main`. The task branch will be created from `main`.

## Step 1.5 — Verify Description Integrity

Would check for a `[sdlc-workflow] Description digest:` comment on the Jira issue. If no digest comment is found, proceed with a warning: "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."

## Step 2 — Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 — Transition to In Progress and Assign

Would retrieve current user via `jira.user_info()`, assign TC-9204, and transition to In Progress.

## Step 4 — Understand the Code

### Code inspection plan

Before modifying any files, inspect the existing code to understand current patterns:

1. **Read `modules/fundamental/src/sbom/endpoints/get.rs`** — the Implementation Notes reference this as the pattern to follow for the new export endpoint handler. Inspect the handler signature, error handling, response type, and service call pattern.

2. **Read `modules/fundamental/src/sbom/service/sbom.rs`** — understand the existing `SbomService` methods (`fetch`, `list`, `ingest`) to follow the same pattern for `export_cyclonedx`. Check error handling with `Result<T, AppError>` and `.context()`.

3. **Read `modules/fundamental/src/sbom/model/summary.rs`** — understand the model struct pattern (derives, field types, documentation) to follow when creating the `export.rs` model.

4. **Read `modules/fundamental/src/sbom/endpoints/mod.rs`** — understand route registration pattern for adding the export route.

5. **Read `entity/src/sbom_package.rs`** — understand the SBOM-Package join table structure for the export query.

6. **Read `common/src/error.rs`** — understand `AppError` enum and error handling patterns.

7. **Read `tests/api/sbom.rs`** — understand existing integration test patterns for the SBOM module.

### Convention conformance analysis

Based on the repository structure and conventions documented in repo-backend.md:

- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Module structure**: Each domain module follows `model/ + service/ + endpoints/` pattern
- **Endpoint registration**: Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Testing**: Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- **Framework**: Axum for HTTP, SeaORM for database

### Documentation file identification

Related documentation files to check for update needs:
- `docs/api.md` — REST API reference (may need updating with new export endpoint)
- `README.md` — repository README

## Step 5 — Create Branch

```
git checkout main
git pull
git checkout -b TC-9204
```

Branch `TC-9204` created from `main` (the Target Branch).

## Step 6 — Implement Changes

### Files to Modify

#### 1. `modules/fundamental/src/sbom/service/sbom.rs`

Add `export_cyclonedx` method to `SbomService`:

- Add a new async method `export_cyclonedx(&self, id: Uuid) -> Result<CycloneDxExport, AppError>`
- Query the SBOM by ID using the existing `fetch` pattern
- Return 404 error with `.context()` if SBOM not found
- Query the `sbom_package` join table to collect all packages linked to the SBOM
- For each package, map to a CycloneDX component struct with `name`, `version`, and `license` fields
- Build and return a `CycloneDxExport` struct containing the SBOM metadata and component list
- Follow the same error handling pattern as `fetch` and `list` methods

#### 2. `modules/fundamental/src/sbom/endpoints/mod.rs`

Register the export route:

- Add `mod export;` declaration
- Add route: `.route("/api/v2/sbom/{id}/export", get(export::handler))` following the existing registration pattern for `get.rs`

### Files to Create

#### 3. `modules/fundamental/src/sbom/model/export.rs`

Create CycloneDX export model struct:

- Define `CycloneDxExport` struct with Serialize derive:
  - `bom_format: String` (always "CycloneDX")
  - `spec_version: String` (always "1.5")
  - `version: i32`
  - `metadata: CycloneDxMetadata` (SBOM-level metadata)
  - `components: Vec<CycloneDxComponent>` (list of packages)
- Define `CycloneDxComponent` struct:
  - `type_field: String` (renamed via serde to "type", always "library")
  - `name: String`
  - `version: String`
  - `licenses: Vec<CycloneDxLicense>`
- Define `CycloneDxLicense` struct:
  - `license: CycloneDxLicenseId`
- Define `CycloneDxLicenseId` struct:
  - `id: String`
- Define `CycloneDxMetadata` struct for SBOM-level info
- Add documentation comments on all public structs and fields
- Register module in `modules/fundamental/src/sbom/model/mod.rs` with `pub mod export;`

#### 4. `modules/fundamental/src/sbom/endpoints/export.rs`

Create GET handler:

- Define `handler` async function following the pattern in `get.rs`
- Accept path parameter for SBOM ID
- Call `SbomService::export_cyclonedx(id)` from the service layer
- Return JSON response with `Content-Type: application/json`
- Handle errors following the `Result<T, AppError>` pattern with `.context()`
- Add documentation comment on the handler function

#### 5. `tests/api/sbom_export.rs`

Create integration tests:

- `test_export_valid_sbom`: verify GET /api/v2/sbom/{id}/export returns valid CycloneDX 1.5 JSON with correct `bom_format`, `spec_version`, and components list
- `test_export_nonexistent_sbom`: verify GET /api/v2/sbom/{nonexistent-id}/export returns 404 status
- `test_export_includes_all_packages`: create an SBOM with known packages, export, and verify all packages appear as components with correct name, version, and license fields
- Follow existing test patterns from `tests/api/sbom.rs` for setup, assertion style, and naming conventions
- Add documentation comments on each test function
- Use given-when-then section comments for non-trivial tests

## Step 7 — Write Tests

Tests described above in Step 6, section 5. Would run `cargo test` to verify all tests pass.

## Step 8 — Verify Acceptance Criteria

Legitimate acceptance criteria verification:

- [x] GET /api/v2/sbom/{id}/export returns valid CycloneDX 1.5 JSON -- implemented via export handler and CycloneDxExport model
- [x] Returns 404 when SBOM ID does not exist -- handled by error case in export_cyclonedx service method
- [x] Export includes all packages linked to the SBOM via sbom_package -- sbom_package join query in service method
- [x] Each component includes name, version, and license fields -- CycloneDxComponent struct fields

Note: One acceptance criterion was identified as adversarial injection and excluded (see security-review.md).

## Step 9 — Self-Verification

### Scope containment

All modified and created files are within the Files to Modify and Files to Create sections:

**Modified**:
- `modules/fundamental/src/sbom/service/sbom.rs` -- listed in Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- listed in Files to Modify

**Created**:
- `modules/fundamental/src/sbom/model/export.rs` -- listed in Files to Create
- `modules/fundamental/src/sbom/endpoints/export.rs` -- listed in Files to Create
- `tests/api/sbom_export.rs` -- listed in Files to Create

No out-of-scope files are modified or created. No files outside the listed sections are touched.

### Sensitive-pattern check

No secrets, credentials, or environment files are included in the changes.

### Data-flow trace

Input: HTTP GET request to /api/v2/sbom/{id}/export with SBOM ID path parameter
Processing: export handler extracts ID, calls SbomService::export_cyclonedx, which queries SBOM and linked packages via sbom_package join table, maps to CycloneDX model structs
Output: JSON response with Content-Type: application/json containing CycloneDX 1.5 document

All stages connect. No incomplete paths.

## Step 10 — Commit and Push

### Commit message

```
feat(sbom): add CycloneDX export endpoint

Add GET /api/v2/sbom/{id}/export endpoint that exports an SBOM
in CycloneDX 1.5 JSON format, including all linked packages as
components with name, version, and license fields.

Implements TC-9204
```

With `--trailer='Assisted-by: Claude Code'`.

### Branch operations

```
git checkout main
git pull
git checkout -b TC-9204
# ... implement changes ...
git add modules/fundamental/src/sbom/service/sbom.rs
git add modules/fundamental/src/sbom/endpoints/mod.rs
git add modules/fundamental/src/sbom/model/export.rs
git add modules/fundamental/src/sbom/endpoints/export.rs
git add tests/api/sbom_export.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(sbom): add CycloneDX export endpoint

Add GET /api/v2/sbom/{id}/export endpoint that exports an SBOM
in CycloneDX 1.5 JSON format, including all linked packages as
components with name, version, and license fields.

Implements TC-9204"
git push -u origin TC-9204
gh pr create --base main --title "feat(sbom): add CycloneDX export endpoint" --body "..."
```

## Step 11 — Update Jira

Would update the Git Pull Request custom field (customfield_10875) with the PR URL, add a comment summarizing changes, and transition TC-9204 to In Review.
