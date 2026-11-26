**Summary:** TC-9004: Add configurable license compliance policy (JSON config + loader)

## Repository
trustify-backend

## Target Branch
main

## Description
Introduce a configurable license compliance policy for the license compliance report feature (TC-9004). The policy is stored as a JSON config file in the repository and defines which SPDX license identifiers are allowed (and/or denied) for a project. This task adds the policy file, a typed policy model, and a loader that validates the file at startup/first use. The policy is consumed by the license report service (Task 2) to flag non-compliant license groups.

Organizations may have different compliance policies, so the policy path must be configurable (with a sensible default pointing to the in-repo file).

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — export the new license policy model module
- `modules/fundamental/src/lib.rs` — expose the policy loader if needed by the server crate
- `common/src/error.rs` — add an `AppError` variant (or reuse an existing one) for invalid/missing policy configuration

## Files to Create
- `license-policy.json` — default license compliance policy (repo root), e.g. `{ "allowed": ["MIT", "Apache-2.0", "BSD-3-Clause", ...], "denied": ["GPL-3.0-only", "AGPL-3.0-only"] }`
- `modules/fundamental/src/sbom/model/license_policy.rs` — `LicensePolicy` struct (serde `Deserialize`), loader function, and `is_compliant(license: &str) -> bool` evaluation logic

## Implementation Notes
- Follow the module pattern `model/ + service/ + endpoints/` used under `modules/fundamental/src/sbom/` — the policy model belongs in `modules/fundamental/src/sbom/model/` alongside `summary.rs` and `details.rs`.
- Per CONVENTIONS.md §Error handling: all fallible functions return `Result<T, AppError>` with `.context()` wrapping; surface policy load/parse failures as `AppError` from `common/src/error.rs`.
  Applies: task modifies `modules/fundamental/src/sbom/model/license_policy.rs` matching the convention's Rust module (`.rs`) scope.
- **Fail-closed policy loading:** a missing, unreadable, empty, or malformed policy file MUST produce an error, never an "empty policy" that treats every license as compliant. Place the guard in the loader function in `modules/fundamental/src/sbom/model/license_policy.rs`.
- License evaluation semantics: license identifiers are compared case-insensitively against SPDX IDs; a license that is neither explicitly allowed nor present (unknown / `NOASSERTION` / missing) is treated as **non-compliant**, not compliant. Document this default in the policy file comment section of the docs task.
- Policy path: read from a configuration value (e.g., environment variable / CLI arg wired in `server/src/main.rs` in Task 3), defaulting to `license-policy.json`.
- Commit rules (docs/constraints.md §2): Conventional Commits format, Jira ID footer (`Implements <task-key>`), `Assisted-by:` trailer.
- PR rules (§3): `gh pr create --base main`; post the PR link on the Jira task.
- Code change rules (§5): keep changes scoped to the files listed above; inspect code before modifying; reuse existing helpers rather than duplicating.

## Reuse Candidates
- `common/src/error.rs::AppError` — existing error enum implementing `IntoResponse`; extend rather than introducing a new error type
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — already carries the `license` field; use the same license string representation for policy matching

## Acceptance Criteria
- [ ] A default `license-policy.json` exists in the repository and is valid JSON
- [ ] `LicensePolicy` deserializes from the JSON file and exposes an `is_compliant(license)` check
- [ ] Licenses on the allowed list evaluate as compliant; licenses on the denied list evaluate as non-compliant
- [ ] Unknown, missing, or `NOASSERTION` licenses evaluate as non-compliant (fail closed)
- [ ] A missing, empty, or malformed policy file returns an `AppError` instead of a permissive/empty policy

## Test Requirements
- [ ] Unit test: valid policy file loads and allowed/denied licenses evaluate correctly
- [ ] Unit test: license matching is case-insensitive for SPDX identifiers
- [ ] Unit test: unknown / empty / `NOASSERTION` license evaluates as non-compliant
- [ ] Unit test: missing policy file returns an error (not an empty policy)
- [ ] Unit test: malformed JSON and an empty JSON object (no rules) return an error

## Verification Commands
- `cargo test --workspace license_policy` — all policy tests pass

## Dependencies
- None
