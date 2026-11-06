## Repository
trustify-backend

## Target Branch
main

## Description
Add a configurable license policy, stored as a JSON config file in the repository, and a Rust model and loader that read and evaluate it. The policy says which SPDX license identifiers are allowed or denied. It also says how to treat packages with no license data or an unrecognized license. The license compliance report (TC-9004) uses this policy to set the `compliant` flag on each license group. This task covers the policy format, the loader, and the per-license compliance check. It does not add the report service or the endpoint.

## Files to Create
- `license-policy.json` — default license policy config at the repository root (e.g., `{ "allowed": ["MIT", "Apache-2.0", "BSD-3-Clause", ...], "denied": ["GPL-3.0-only", "AGPL-3.0-only", ...], "unknown_license": "non-compliant" }`)
- `modules/fundamental/src/sbom/model/license_policy.rs` — `LicensePolicy` struct (serde `Deserialize`), loader that reads the policy file from a configurable path, and `LicensePolicy::is_compliant(&self, license: &str) -> bool`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — declare and re-export the new `license_policy` module
- `common/src/error.rs` — add an `AppError` variant (or reuse an existing one) for an invalid or unreadable policy config, mapped through the existing `IntoResponse` impl

## Implementation Notes
- Follow the module pattern from the repository's Key Conventions (`model/ + service/ + endpoints/`). The policy model goes in `modules/fundamental/src/sbom/model/`, next to `summary.rs` (`SbomSummary`) and `details.rs` (`SbomDetails`).
- Error handling: loader functions return `Result<LicensePolicy, AppError>` and wrap I/O and JSON parse failures with `.context()`, as the rest of the codebase does (`common/src/error.rs::AppError`).
- Make the policy file path configurable (e.g., a server config or env value read in `server/src/main.rs` in Task 3). Default to `license-policy.json` at the repository root. Customers may have different compliance policies (see Customer Considerations).
- Fail closed: if the policy file is missing, unreadable, or not valid JSON, the loader must return an error. It must never fall back to an empty or permissive policy that marks every license compliant.
- Compare license identifiers case-insensitively after trimming. Treat licenses that are neither allowed nor denied according to the policy's `unknown_license` setting. The default is `non-compliant`.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` and wrap errors with `.context()`.
  Applies: task modifies `modules/fundamental/src/sbom/model/license_policy.rs` matching the convention's Rust source (`.rs`) scope.
- Constraints (docs/constraints.md): commits must follow Conventional Commits (§2.2), reference the Jira task in the footer (§2.1), and include an `Assisted-by:` trailer (§2.3). The PR must use `--base main` (§3.3). Changes must stay within the files listed here and must not duplicate existing utilities (§5.1, §5.4).

## Reuse Candidates
- `common/src/error.rs::AppError` — existing error enum with `IntoResponse`. Extend it rather than adding a new error type.
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — already has a `license` field. Match its license string format so policy matching lines up with stored data.

## Acceptance Criteria
- [ ] `license-policy.json` exists at the repository root with a documented default allow/deny list and an `unknown_license` setting
- [ ] `LicensePolicy` deserializes from the JSON file and is exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] `LicensePolicy::is_compliant` returns `true` for allowed licenses and `false` for denied licenses
- [ ] Licenses not in either list, and missing or empty licenses, are evaluated according to `unknown_license` (default: non-compliant)
- [ ] A missing or malformed policy file returns an `AppError`. The loader never falls back to an allow-all policy (fail closed).

## Test Requirements
- [ ] Unit test: an allowed license (e.g., `MIT`) is compliant
- [ ] Unit test: a denied license (e.g., `GPL-3.0-only`) is non-compliant
- [ ] Unit test: unknown and empty license strings are non-compliant under the default policy
- [ ] Unit test: license matching is case-insensitive
- [ ] Unit test: loading a malformed JSON policy returns an error rather than a permissive default
- [ ] Unit test: loading from a non-existent path returns an error

## Verification Commands
- `cargo test -p fundamental license_policy` — all license policy unit tests pass

## Dependencies
- None
