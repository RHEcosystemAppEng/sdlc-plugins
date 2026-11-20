**Summary:** Add configurable license policy and loader
**Epic:** TC-9004: License compliance report API
**Labels:** ai-generated-jira | **Priority:** Major | **Fix Versions:** RHTPA 1.5.0

## Repository
trustify-backend

## Target Branch
main

## Description
Introduce a configurable license compliance policy for TC-9004 (license compliance report). The policy is stored as a JSON config file in the repository and declares which licenses are allowed (and optionally which are explicitly denied). A typed loader parses and validates the policy so that the license report service (Task 2) can evaluate each license group as compliant or non-compliant. Organizations have different policies, so the policy file path must be overridable via configuration.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — export the new license policy model module
- `modules/fundamental/src/sbom/service/mod.rs` — export the license policy loader
- `common/src/error.rs` — add an `AppError` variant (or reuse an existing internal-error variant) for policy load/validation failures

## Files to Create
- `config/license-policy.json` — default license policy (e.g., allowed: SPDX IDs such as `MIT`, `Apache-2.0`, `BSD-3-Clause`; denied: e.g., `GPL-3.0-only`, `AGPL-3.0-only`)
- `modules/fundamental/src/sbom/model/license_policy.rs` — `LicensePolicy` struct (serde `Deserialize`) with `allowed`/`denied` SPDX identifier lists and an `is_compliant(license: &str) -> bool` method
- `modules/fundamental/src/sbom/service/license_policy.rs` — loader that reads the policy from the configured path (default `config/license-policy.json`), validates it, and returns `Result<LicensePolicy, AppError>`

## Implementation Notes
- Follow the module pattern `model/ + service/ + endpoints/` used by `modules/fundamental/src/sbom/` — models live in `sbom/model/`, logic in `sbom/service/`.
- Policy semantics: a license is compliant only if it is in `allowed` and not in `denied`. Licenses not listed in either are **non-compliant** (default-deny). License matching should be on SPDX identifiers, case-insensitive.
- **Fail-closed behavior (protects the UC-2 CI gate):** if the policy file is missing, unreadable, is invalid JSON, or has an empty `allowed` list, the loader MUST return an error (`AppError`) — it must never fall back to an empty/permissive policy that would mark every group compliant. The guard belongs in the loader function in `modules/fundamental/src/sbom/service/license_policy.rs`.
- Make the policy path configurable (e.g., an env var / CLI config value wired where `server/src/main.rs` builds application state), defaulting to `config/license-policy.json`.
- Load the policy once at startup or cache it in service state; do not re-read the file per request (p95 < 500ms NFR).
- Per CONVENTIONS.md §Module pattern: place the policy model in `sbom/model/` and the loader in `sbom/service/`, mirroring `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/service/sbom.rs`.
  Applies: task modifies modules/fundamental/src/sbom/model/license_policy.rs matching the convention's domain module (`.rs` model/service) scope.
- Per CONVENTIONS.md §Error handling: return `Result<LicensePolicy, AppError>` and wrap I/O and parse errors with `.context()`; see `common/src/error.rs` for the `AppError` enum.
  Applies: task modifies common/src/error.rs matching the convention's Rust error-handling (`.rs`) scope.
- Applicable constraints (docs/constraints.md): §2 commit rules (Conventional Commits, Jira ID footer `Implements <task-key>`, `Assisted-by:` trailer); §3 PR rules (`gh pr create --base main`, post PR link to Jira); §5 code change rules (scope changes to the listed files, inspect before modifying, no duplication of existing functionality, add doc comments to every new test function, given-when-then comments for non-trivial tests); §1.4/1.5 implement-task scope rules.

## Reuse Candidates
- `common/src/error.rs::AppError` — existing error enum implementing `IntoResponse`; extend rather than introduce a new error type
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — already carries a `license` field; use its license value format to decide how policy identifiers are matched

## Acceptance Criteria
- [ ] `config/license-policy.json` exists with a documented schema (`allowed`, `denied` SPDX ID lists)
- [ ] `LicensePolicy::is_compliant` returns true only for licenses in `allowed` and not in `denied`; unlisted licenses are non-compliant
- [ ] The policy file path is configurable and defaults to `config/license-policy.json`
- [ ] Loading a missing, unreadable, malformed, or empty-allowlist policy returns an error — it never yields a permissive/empty policy (fail-closed)
- [ ] The policy is loaded once and reused, not read from disk per request

## Test Requirements
- [ ] Unit test: valid policy file parses into the expected `LicensePolicy`
- [ ] Unit test: `is_compliant` for allowed, denied, unlisted, and case-variant license IDs
- [ ] Unit test (fail-closed): missing policy file → loader returns error
- [ ] Unit test (fail-closed): malformed JSON → loader returns error
- [ ] Unit test (fail-closed): policy with empty `allowed` list → loader returns error

## Verification Commands
- `cargo test -p trustify-module-fundamental license_policy` — all license policy tests pass
- `cargo build` — workspace builds

## Dependencies
- None
