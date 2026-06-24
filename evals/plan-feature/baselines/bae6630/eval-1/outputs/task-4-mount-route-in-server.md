## Repository
trustify-backend

## Target Branch
main

## Description
Ensure the new advisory summary route is mounted in the main Axum server. The route registration in `modules/fundamental/src/sbom/endpoints/mod.rs` (done in Task 3) connects it to the SBOM module router, but verify that `server/src/main.rs` correctly mounts the fundamental module's routes so the new endpoint is reachable.

## Files to Modify
- `server/src/main.rs` — Verify and, if needed, update the route mounting to include the new endpoint (likely no changes needed if the SBOM module router is already mounted wholesale)

## Implementation Notes
- In `server/src/main.rs`, the Axum server mounts all module routers. The SBOM endpoints module (`modules/fundamental/src/sbom/endpoints/mod.rs`) registers its routes internally, and the fundamental module is already mounted in `server/src/main.rs`.
- Since Task 3 adds the new route to the existing SBOM endpoints router in `modules/fundamental/src/sbom/endpoints/mod.rs`, the server should pick it up automatically without changes to `server/src/main.rs`.
- Verify this by inspecting how existing SBOM routes (e.g., `/api/v2/sbom/{id}` from `get.rs`) are mounted. If the fundamental module's router is merged into the main app router in `server/src/main.rs`, no change is needed here.
- If the server requires explicit per-endpoint registration, add the advisory-summary route following the existing pattern.

## Reuse Candidates
- `server/src/main.rs` — Existing route mounting logic; inspect how SBOM endpoints are included
- `modules/fundamental/src/sbom/endpoints/mod.rs` — The module-level router where the new route is already registered

## Acceptance Criteria
- [ ] The `GET /api/v2/sbom/{id}/advisory-summary` endpoint is reachable when the server starts
- [ ] No duplicate route registrations exist
- [ ] Server compiles and starts without errors

## Test Requirements
- [ ] Server starts successfully with the new route mounted
- [ ] A request to `/api/v2/sbom/{id}/advisory-summary` reaches the handler (not 404 from the router)

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint (route must be registered in the SBOM endpoints module first)

## Digest
[sdlc-workflow] Description digest: sha256-md:ef1bee61a43ca64ed532fc1a3a8d95eba550d6b9096f471d49fddc7141024a7c
