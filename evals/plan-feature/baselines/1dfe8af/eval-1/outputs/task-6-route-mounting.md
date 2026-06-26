## Repository
trustify-backend

## Target Branch
main

## Description
Ensure the new advisory-summary endpoint is properly mounted in the main Axum server by verifying that the sbom module's route registration flows through to the server entrypoint. If the sbom endpoints/mod.rs route registration automatically propagates through the existing module mounting in server/main.rs, no changes are needed here. Otherwise, update server/main.rs to include the new route.

## Files to Modify
- `server/src/main.rs` — Verify and if needed update the server route mounting to include the advisory-summary endpoint

## Implementation Notes
The server entrypoint in `server/src/main.rs` sets up the Axum server and mounts all module routes. Per the existing convention, each module's `endpoints/mod.rs` registers its own routes, and `server/main.rs` mounts all modules.

Check whether the sbom module's route registration in `modules/fundamental/src/sbom/endpoints/mod.rs` is already mounted via a module-level router that `server/main.rs` merges. If so, the new route added in Task 3 will automatically be available. If the server mounts routes individually, add the advisory-summary route.

This task may result in no code changes if the existing architecture auto-discovers routes from module-level registration.

## Reuse Candidates
- `server/src/main.rs` — Existing route mounting pattern for all modules

## Acceptance Criteria
- [ ] GET /api/v2/sbom/{id}/advisory-summary is accessible when the server starts
- [ ] Server compiles and starts without errors
- [ ] No disruption to existing endpoint routing

## Verification Commands
- `cargo check -p trustify-server` — compiles without errors
- `cargo run -p trustify-server` — server starts and accepts requests on the new endpoint

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint

[sdlc-workflow] Description digest: sha256-md:f9b2c4d6e8a0513028d64f9a0c3e7a1b2f45b6c8d0e2534f6a8b0c2d4e5f7a9
