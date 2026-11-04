# Task 1 — Add license policy JSON config and loader

**Feature**: TC-9004 · **Labels**: ai-generated-jira · **Priority**: Major · **Fix Versions**: RHTPA 1.5.0

## Repository
trustify-backend

## Target Branch
main

## Description
Add a configurable license policy, stored as a JSON config file in the repository, plus a typed loader that the license compliance report (TC-9004) uses to decide whether each license is compliant. Different organizations have different compliance policies, so the policy must be editable data, not hard-coded logic. This task only adds the policy and its loader. The report aggregation (Task 2) and the endpoint (Task 3) use it.

## Files to Create
- `modules/fundamental/src/sbom/service/license_policy.rs` — `LicensePolicy` struct (serde `Deserialize`) and load/validate functions, plus `LicensePolicy::is_compliant(&self, license: &str) -> bool`
- `license-policy.json` — default license policy config at the repository root (for example, an allow-list of SPDX identifiers such as `MIT`, `Apache-2.0`, `BSD-3-Clause`, and a deny-list such as `GPL-3.0-only`, `AGPL-3.0-only`)

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — declare and re-export the `license_policy` module
- `modules/fundamental/Cargo.toml` — add `serde_json` if the crate does not already depend on it

## Implementation Notes
- Policy format suggestion: `{ "allowed": ["MIT", "Apache-2.0", ...], "denied": ["GPL-3.0-only", ...] }`. Licenses are matched by SPDX identifier, case-insensitively. Licenses on neither list are treated as **non-compliant** (fail closed), unless the policy explicitly sets a `"default": "allow"` field.
- Loading: read the path from configuration (environment variable or CLI arg, following however `server/src/main.rs` already wires configuration) and fall back to `license-policy.json`. Load and validate once at startup and share it via Axum state (`Arc<LicensePolicy>`), so it is not re-read per request (this keeps the p95 < 500ms NFR).
- **Fail-closed gate**: a missing, unreadable, or malformed policy file, or one containing a license on both `allowed` and `denied`, must return an `AppError` with context, for example `.context("failed to load license policy")`. It must never fall back to an empty policy that would mark everything compliant. The guard belongs in the load function in `modules/fundamental/src/sbom/service/license_policy.rs`.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` and wrap failures with `.context()`. Applies: task modifies `modules/fundamental/src/sbom/service/license_policy.rs` matching the convention's Rust service-code scope. Example: `common/src/error.rs` (`AppError`) and its use in `modules/fundamental/src/sbom/service/sbom.rs`.
- Per CONVENTIONS.md §Module pattern: put domain logic under the module's `service/` directory. Applies: task modifies `modules/fundamental/src/sbom/service/license_policy.rs` matching the convention's `model/ + service/ + endpoints/` module scope. Example: `modules/fundamental/src/sbom/service/sbom.rs`.
- Constraints (docs/constraints.md): §2.1–2.3 commits reference the Jira task ID in the footer, follow Conventional Commits, and carry the `Assisted-by: Claude Code` trailer. §3.1–3.3 branch is named after the task ID, PR link goes on the Jira task, and `gh pr create --base main`. §5.1–5.4 stay within the listed files, inspect code before modifying it, follow the referenced patterns, and do not duplicate existing utilities. §1.4–1.5 (implement-task scope) apply.

## Reuse Candidates
- `common/src/error.rs::AppError` — standard error type for load/validation failures
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — its `license` field holds the value format the policy must match against; check its representation (single SPDX id vs. expression) when designing matching

## Acceptance Criteria
- [ ] A default `license-policy.json` exists in the repository and is valid against the loader
- [ ] `LicensePolicy` loads from a configurable path and defaults to `license-policy.json`
- [ ] `is_compliant` returns `true` for allowed licenses, `false` for denied licenses, and `false` for licenses on neither list (fail closed by default)
- [ ] A missing, unreadable, or malformed policy file produces an `AppError`. It never yields an empty or permissive policy
- [ ] A policy listing the same license as both allowed and denied is rejected with a descriptive error
- [ ] No new database tables or migrations are added

## Test Requirements
- [ ] Unit test: valid policy JSON parses, and `is_compliant` returns the expected values for allowed, denied, and unlisted licenses
- [ ] Unit test: license matching is case-insensitive on SPDX identifiers
- [ ] Unit test (fail-closed): a missing file returns an error, not a default-allow policy
- [ ] Unit test (fail-closed): malformed JSON returns an error
- [ ] Unit test: a conflicting allow/deny entry returns an error
- [ ] Unit test: the shipped `license-policy.json` loads successfully

## Verification Commands
- `cargo test -p trustify-module-fundamental license_policy` — all license policy tests pass (adjust the package name to the crate name in `modules/fundamental/Cargo.toml`)

## Documentation Updates
- `README.md` — mention the license policy config file and how to point the server at a custom policy (full docs are in Task 4)
