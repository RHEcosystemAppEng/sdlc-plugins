# Task 6: Mount advisory summary route in server and update API documentation

## Repository
trustify-backend

## Target Branch
main

## Description
Ensure the new advisory summary endpoint is mounted in the main Axum server entry point and update any API documentation references. While route registration happens in the SBOM endpoints module (Task 3), the server's `main.rs` mounts all modules and may need adjustment if the SBOM module's router is not already fully auto-discovered. Also verify that the endpoint appears correctly in any generated OpenAPI/Swagger documentation.

## Files to Modify
- `server/src/main.rs` — Verify SBOM module routes include the new advisory-summary endpoint (adjust if router mounting needs explicit addition)

## Implementation Notes
The `server/src/main.rs` file sets up the Axum server and mounts all module routers. Inspect how `modules/fundamental/src/sbom/endpoints/mod.rs` routes are mounted in `main.rs`. If the SBOM module router is mounted as a nested router (e.g., via `.nest("/api/v2/sbom", sbom_router())`), the new route added in Task 3 should be automatically included without changes to `main.rs`.

If `main.rs` explicitly lists individual route handlers rather than mounting a module router, add the advisory summary handler to the route list.

Verify that:
1. The SBOM module router mounting in `main.rs` picks up the new route
2. If the project uses `utoipa` or similar for OpenAPI generation, add the appropriate `#[utoipa::path]` annotation to the handler (reference existing endpoint annotations in `get.rs` or `list.rs`)

Per CONVENTIONS.md §Endpoint registration: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules.
Applies: task modifies `server/src/main.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `server/src/main.rs` — existing server setup and module mounting pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration that should expose the new endpoint to the server

## Acceptance Criteria
- [ ] The advisory summary endpoint is accessible at `GET /api/v2/sbom/{id}/advisory-summary` when the server starts
- [ ] Server compiles and starts without errors
- [ ] If OpenAPI documentation is generated, the new endpoint appears in the API spec

## Test Requirements
- [ ] Smoke test: start the server and verify `GET /api/v2/sbom/{id}/advisory-summary` returns a response (not 404 from missing route)

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint

## Verification Commands
- `cargo build -p trustify-server` — server compiles
- `cargo run -p trustify-server &; curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/api/v2/sbom/test-id/advisory-summary` — returns 404 (SBOM not found) not 405 (method not allowed) or connection error

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}

[sdlc-workflow] Description digest: sha256-md:879f010f78c5b932630947da5ec77db21d9586dde606e51d0033e52710bc7ebc
