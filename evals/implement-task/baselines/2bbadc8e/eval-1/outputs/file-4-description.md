# File 4: server/src/main.rs

**Action**: No changes needed

## Purpose

The task description explicitly states: "no changes needed (routes auto-mount via module registration)."

## Changes

None. The Axum server in `main.rs` mounts all module routers automatically. Adding the route in `modules/fundamental/src/advisory/endpoints/mod.rs` is sufficient for the new endpoint to be available.

## Rationale

The project's endpoint registration convention composes module-level routers into the main application router. When a new route is added to a module's `endpoints/mod.rs`, it becomes part of that module's router, which is already mounted by `main.rs`. No additional wiring is required.
