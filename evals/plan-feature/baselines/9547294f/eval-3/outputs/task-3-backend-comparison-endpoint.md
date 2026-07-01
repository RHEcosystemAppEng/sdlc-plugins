# Task 3 — Add SBOM comparison REST endpoint

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Expose the SBOM comparison service as a REST endpoint at `GET /api/v2/sbom/compare` with query parameters `left` and `right` (SBOM IDs). This endpoint enables the frontend comparison UI and third-party API consumers to retrieve structured diffs between two SBOMs.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler function for GET /api/v2/sbom/compare that extracts query params, calls SbomService::compare, and returns the JSON response

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Add `pub mod compare;` and register the `/compare` route in the SBOM router

## API Changes
- `GET /api/v2/sbom/compare?left={id}&right={id}` — NEW: Returns SbomComparisonResult JSON with added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes

## Implementation Notes

### Endpoint handler pattern

Follow the existing endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `list.rs`:

```rust
#[derive(Deserialize)]
pub struct CompareQuery {
    pub left: String,
    pub right: String,
}

pub async fn compare(
    State(service): State<SbomService>,
    Query(params): Query<CompareQuery>,
) -> Result<Json<SbomComparisonResult>, AppError> {
    let result = service.compare(&params.left, &params.right).await.context("comparing SBOMs")?;
    Ok(Json(result))
}
```

### Route registration

In `modules/fundamental/src/sbom/endpoints/mod.rs`, add the compare route to the existing router:

```rust
.route("/compare", get(compare::compare))
```

This follows the pattern of `list.rs` and `get.rs` being registered in the same `mod.rs` file.

### Error handling

- Return 404 (via AppError) if either SBOM ID does not exist
- Return 400 if `left` or `right` query parameters are missing
- Use `.context()` wrapping on all service calls per the existing error handling convention

### Reuse candidates

- `modules/fundamental/src/sbom/endpoints/get.rs` — existing endpoint handler pattern to follow for request/response structure
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern
- `common/src/error.rs::AppError` — error type with IntoResponse implementation

Per CONVENTIONS.md: all handlers return `Result<T, AppError>` with `.context()` wrapping. Register the route in the module's `endpoints/mod.rs`.
Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's Rust endpoint file scope.

## Acceptance Criteria
- [ ] GET /api/v2/sbom/compare?left={id}&right={id} returns 200 with the structured diff JSON
- [ ] Missing query parameters return 400 Bad Request
- [ ] Non-existent SBOM IDs return 404 Not Found
- [ ] Response Content-Type is application/json
- [ ] Response shape matches the SbomComparisonResult struct

## Test Requirements
- [ ] Integration test: successful comparison of two SBOMs returns expected diff structure
- [ ] Integration test: missing `left` parameter returns 400
- [ ] Integration test: missing `right` parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: comparing an SBOM with itself returns empty diff sections

## Verification Commands
- `cargo build -p trustify-fundamental` — should compile without errors
- `cargo test -p trustify-tests -- api::sbom::compare` — should pass all comparison endpoint tests

## Documentation Updates
- API documentation should be updated to include the new `GET /api/v2/sbom/compare` endpoint with query parameters, request/response examples, and error codes

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison diff model and service

---
Priority: Critical
Fix Versions: RHTPA 1.5.0
Labels: ai-generated-jira

[sdlc-workflow] Description digest: sha256-md:c5f9b3a7d2e8461f0c6d9a3b5e7f1c4d8a2b6e0f3c5d9a1b7e4f8c2d6a0b3e5f
