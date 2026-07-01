## Repository
trustify-backend

## Target Branch
main

## Description
Add a default license policy configuration file and the logic to load it at application startup. The policy defines which licenses are compliant or non-compliant, supporting both allowlist and denylist approaches. This configuration is used by the license report service to flag non-compliant licenses.

## Files to Modify
- `server/src/main.rs` -- add license policy loading at application startup and inject it into the application state for endpoint access

## Files to Create
- `config/license-policy.json` -- default license policy configuration file defining compliant/non-compliant license SPDX identifiers

## Implementation Notes
- The license policy JSON file should follow a structure like: `{ "mode": "denylist", "licenses": ["GPL-3.0-only", "AGPL-3.0-only"] }` or `{ "mode": "allowlist", "licenses": ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause"] }`.
- Load the policy file path from environment variable or a default path (e.g., `config/license-policy.json`).
- In `server/src/main.rs`, load and parse the policy file during startup and add it to the Axum application state (likely via `Extension` or a similar shared state mechanism). Check how existing configuration is loaded and shared in `main.rs`.
- Handle missing policy file gracefully: if no policy file exists, use a default permissive policy (all licenses are compliant) and log a warning.
- Document the policy configuration format in the file itself or in a companion README section.
- Per CONVENTIONS.md (Key Conventions): Axum server setup and route mounting is in `server/main.rs`.
  Applies: task modifies `server/src/main.rs` matching the convention's `.rs` server file scope.

## Reuse Candidates
- `server/src/main.rs` -- existing application startup and state initialization patterns

## Acceptance Criteria
- [ ] A default `config/license-policy.json` exists with a reasonable default policy
- [ ] The license policy is loaded at application startup and available to endpoints
- [ ] Missing policy file results in a default permissive policy with a logged warning
- [ ] Policy supports both allowlist and denylist modes

## Test Requirements
- [ ] Unit test for loading a valid policy file
- [ ] Unit test for fallback behavior when policy file is missing
- [ ] Unit test for both allowlist and denylist policy modes

## Dependencies
- Depends on: Task 1 -- Add license compliance report model types

## Description Digest
sha256-md:275dce144d9ef56af10d5906cd0d4bc93b2236971c79ea9623f17185f5c78ee7
