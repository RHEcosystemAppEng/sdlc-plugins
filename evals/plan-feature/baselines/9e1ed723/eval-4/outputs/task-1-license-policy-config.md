## Repository
trustify-backend

## Target Branch
main

## Description
Introduce a configurable license compliance policy for TC-9004 (Add license compliance report endpoint). The policy is stored as a JSON config file in the repository and declares which SPDX license identifiers are allowed (and optionally which are explicitly denied), plus how packages with no license data are treated. This task adds the policy file, a typed model for it, and a loader/evaluator that the license report service (Task 2) uses to flag non-compliant licenses. No new database tables are introduced.

## Files to Create
- `license-policy.json` — default license policy (allowed / denied SPDX identifiers, `unknown_license` handling) shipped in the repository
- `modules/fundamental/src/sbom/model/license_policy.rs` — `LicensePolicy` struct (serde-deserializable) and `LicensePolicy::evaluate(license: &str) -> bool` compliance check

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — declare and re-export the new `license_policy` module
- `server/src/main.rs` — load the policy at startup from a configurable path (default `license-policy.json`) and make it available to the fundamental module's route state

## Implementation Notes
- Follow the module pattern `model/ + service/ + endpoints/` used by `modules/fundamental/src/sbom/`; the policy type belongs in `modules/fundamental/src/sbom/model/` next to `summary.rs` (`SbomSummary`) and `details.rs` (`SbomDetails`).
- Policy loading errors must surface as `AppError` (`common/src/error.rs`) with `.context()` wrapping describing the policy path, matching the repository's error-handling pattern (`Result<T, AppError>` with `.context()`).
- **Fail-closed policy loading (gate site: policy loader in `modules/fundamental/src/sbom/model/license_policy.rs` and its call in `server/src/main.rs`)**: a missing, unreadable, or malformed policy file must cause startup (or report generation) to fail with an error. It must never fall back to an empty/permissive policy, because the CI gate in UC-2 treats "no `compliant: false` groups" as a pass — a silently empty policy would let every build pass without any check being performed.
- License identifier comparison should be case-insensitive on SPDX identifiers; compound expressions (e.g. `MIT OR Apache-2.0`) should be evaluated so that an `OR` expression is compliant if any operand is allowed and an `AND` expression only if all operands are allowed.
- Packages with no license data (empty / `NOASSERTION`) are evaluated according to the policy's `unknown_license` setting, defaulting to non-compliant.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` and wrap fallible operations with `.context()`. Applies: task modifies `modules/fundamental/src/sbom/model/license_policy.rs` matching the convention's Rust handler/service source scope.
- Per CONVENTIONS.md §Module pattern: place domain types under the module's `model/` directory. Applies: task modifies `modules/fundamental/src/sbom/model/license_policy.rs` matching the convention's `modules/*/src/*/model/` directory scope.
- Constraints (docs/constraints.md): commits must reference the Jira task in the footer, follow Conventional Commits, and include an `Assisted-by:` trailer (§2.1–2.3); PR must target `--base main` and its link must be posted on the Jira task (§3.2–3.3); changes must stay within Files to Modify / Files to Create, inspect code before modifying, and reuse existing utilities rather than duplicating (§5.1–5.4).

## Reuse Candidates
- `common/src/error.rs::AppError` — shared error enum implementing `IntoResponse`; use for policy load/parse failures
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — already carries the `license` field; the evaluator should accept the same license string representation

## Acceptance Criteria
- [ ] `license-policy.json` exists at the repository root and defines allowed licenses, denied licenses, and `unknown_license` handling
- [ ] `LicensePolicy` deserializes from the JSON file and exposes an evaluation method returning compliant / non-compliant for a license identifier or SPDX expression
- [ ] The policy file path is configurable at server startup, defaulting to `license-policy.json`
- [ ] A missing, unreadable, or malformed policy file produces an error (startup failure or `AppError`) — it never results in an empty or permissive policy that marks everything compliant
- [ ] Packages with no license data are classified non-compliant by default

## Test Requirements
- [ ] Unit tests for `LicensePolicy::evaluate` covering allowed, denied, unlisted, case-variant, `OR` and `AND` SPDX expressions
- [ ] Unit test: loading a non-existent policy path returns an error (fail-closed), not a default policy
- [ ] Unit test: loading a malformed JSON policy returns an error (fail-closed), not a default policy
- [ ] Unit test: empty / `NOASSERTION` license is non-compliant under the default policy

## Verification Commands
- `cargo test -p trustify-module-fundamental license_policy` — all policy tests pass

## Documentation Updates
- `README.md` — mention the `license-policy.json` file and the configuration option for its path
