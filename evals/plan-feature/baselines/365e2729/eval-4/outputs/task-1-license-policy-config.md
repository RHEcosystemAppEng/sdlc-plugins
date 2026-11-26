## Repository
trustify-backend

## Target Branch
main

## Description
Introduce a configurable license compliance policy for TC-9004. The policy is stored as a JSON configuration file in the repository and declares which SPDX license identifiers are allowed (and optionally which are explicitly denied). This task adds the policy file, the Rust model for it, a loader that parses and validates it, and a pure evaluation function that classifies a license identifier as compliant or non-compliant. The license report service (Task 2) consumes this evaluator.

## Files to Create
- `license-policy.json` — default license policy (repository root), e.g. `{ "allowed": ["MIT", "Apache-2.0", "BSD-3-Clause", ...], "denied": ["GPL-3.0-only", "AGPL-3.0-only"], "treat_unknown_as": "non-compliant" }`
- `modules/fundamental/src/sbom/model/license_policy.rs` — `LicensePolicy` struct (serde `Deserialize`), plus `LicensePolicy::evaluate(&self, license: Option<&str>) -> bool`
- `modules/fundamental/src/sbom/service/license_policy.rs` — policy loader: reads the JSON file from a configurable path (default `license-policy.json`), validates it, and returns `Result<LicensePolicy, AppError>`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — declare and re-export the `license_policy` model module
- `modules/fundamental/src/sbom/service/mod.rs` — declare the `license_policy` loader module

## Implementation Notes
- Follow the existing module layout in `modules/fundamental/src/sbom/` (`model/` + `service/` + `endpoints/`). Place the policy struct beside `SbomSummary` (`modules/fundamental/src/sbom/model/summary.rs`) and `SbomDetails` (`modules/fundamental/src/sbom/model/details.rs`).
- Error handling: the loader returns `Result<LicensePolicy, AppError>` using the `AppError` enum from `common/src/error.rs`, wrapping I/O and parse failures with `.context()`.
- **Fail-closed policy loading (gate site: `modules/fundamental/src/sbom/service/license_policy.rs`, loader function).** A missing, unreadable, empty, or malformed policy file must produce an error, never a default "allow everything" policy. An empty `allowed` list must be rejected as invalid. Otherwise the CI compliance gate (UC-2) could silently pass every build.
- **Fail-closed evaluation (gate site: `LicensePolicy::evaluate` in `modules/fundamental/src/sbom/model/license_policy.rs`).** A package with no license, an empty string, or `NOASSERTION` is classified per `treat_unknown_as`, which defaults to non-compliant. A license that is in neither `allowed` nor `denied` is non-compliant. `denied` takes precedence over `allowed`.
- Normalize SPDX identifiers before comparing (trim whitespace, compare case-insensitively). Leave full SPDX expression parsing (`MIT OR Apache-2.0`) out of scope unless a crate is already in `Cargo.toml`. For a compound expression, treat it as compliant only when every component identifier is allowed (conservative), and document this.
- Per CONVENTIONS.md §Error handling: all fallible functions return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/sbom/service/license_policy.rs` matching the convention's Rust handler/service (`.rs`) scope. See `modules/fundamental/src/sbom/service/sbom.rs` for the established pattern.
- Per CONVENTIONS.md §Module pattern: new domain code goes under the module's `model/` and `service/` subdirectories. Applies: task modifies `modules/fundamental/src/sbom/model/license_policy.rs` matching the convention's domain module (`modules/*/src/<domain>/`) scope. See `modules/fundamental/src/sbom/model/summary.rs`.
- Constraints (docs/constraints.md): §5.1 keep changes to the files listed above; §5.2 inspect existing code before modifying it; §5.4 reuse existing utilities and do not duplicate them; §2.1–2.3 Conventional Commits with a `TC-9004`-traceable task ID footer and an `Assisted-by:` trailer; §3.1–3.3 branch named after the task ID, PR link posted to Jira, `gh pr create --base main`.

## Reuse Candidates
- `common/src/error.rs::AppError` — standard error type, for loader failures
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — carries the `license` field whose value format the evaluator must accept

## Acceptance Criteria
- [ ] `license-policy.json` exists at the repository root with a documented default allow/deny list
- [ ] `LicensePolicy` deserializes from the JSON file and exposes `evaluate`
- [ ] Licenses in `allowed` evaluate as compliant; licenses in `denied` or in neither list evaluate as non-compliant
- [ ] A missing, unknown, empty, or `NOASSERTION` license evaluates as non-compliant by default (fail-closed)
- [ ] The loader returns an `AppError` (it does not fall back to a permissive default) when the policy file is missing, unreadable, malformed, or has an empty `allowed` list
- [ ] The policy file path can be configured (for example via an environment variable or server config), with `license-policy.json` as the default

## Test Requirements
- [ ] Unit tests for `LicensePolicy::evaluate` covering allowed, denied, unlisted, missing/`NOASSERTION`, case and whitespace normalization, and the denied-overrides-allowed rule
- [ ] Unit test: loading a missing policy file returns an error (fail-closed)
- [ ] Unit test: loading a malformed JSON policy file returns an error (fail-closed)
- [ ] Unit test: a policy with an empty `allowed` list is rejected
- [ ] Unit test: the default `license-policy.json` parses successfully

## Verification Commands
- `cargo test -p fundamental license_policy` — all policy tests pass

## Dependencies
- None
