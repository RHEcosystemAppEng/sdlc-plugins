## Repository
trustify-backend

## Target Branch
main

## Description
Introduce a configurable license compliance policy for the TC-9004 license compliance report. The policy is a JSON config file kept in the repository, plus a typed Rust model and loader that later tasks use to decide whether a license is compliant. Organizations can have different compliance policies, so the policy must be data-driven (allow list / deny list of SPDX license identifiers) rather than hard-coded.

This task delivers only the policy file, the policy model, the loader, and the evaluation function. It does not add the report service or the HTTP endpoint (Tasks 2 and 3).

## Files to Create
- `config/license-policy.json` — default license policy (SPDX identifiers grouped into `allowed` and `denied`, plus a `default` decision for licenses that appear in neither list)
- `modules/fundamental/src/sbom/model/license_policy.rs` — `LicensePolicy` struct (serde `Deserialize`), `LicensePolicy::load(path)` loader, and `LicensePolicy::evaluate(license: Option<&str>) -> bool` compliance check

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — declare and re-export the new `license_policy` module
- `common/src/error.rs` — add an `AppError` variant (or reuse an existing configuration variant if one exists) for an unreadable or invalid license policy, mapped to a 500 response by the existing `IntoResponse` impl

## Implementation Notes
- Follow the existing model layout in `modules/fundamental/src/sbom/model/` (`summary.rs` → `SbomSummary`, `details.rs` → `SbomDetails`): one struct per file, re-exported from `model/mod.rs`.
- Policy file shape (suggested):
  ```json
  {
    "allowed": ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC"],
    "denied": ["GPL-3.0-only", "AGPL-3.0-only"],
    "default": "non-compliant"
  }
  ```
- The policy path should be configurable (for example via the server's existing configuration or an environment variable read in `server/src/main.rs` in Task 3), defaulting to `config/license-policy.json`. Load the policy once at startup and share it as Axum state, not on every request (p95 < 500ms NFR).
- License values come from `PackageSummary.license` (`modules/fundamental/src/package/model/summary.rs`) and the `entity/src/package_license.rs` mapping. Match on SPDX identifiers; normalize case and surrounding whitespace before comparison.
- Fail-closed policy evaluation (this policy backs the CI compliance gate in UC-2, where a pipeline treats `compliant: true` as a pass):
  - A package with no license data, or a license that appears in neither list, must be evaluated as non-compliant unless the policy file sets `"default": "compliant"` explicitly. Gate site: `LicensePolicy::evaluate` in `modules/fundamental/src/sbom/model/license_policy.rs`.
  - A missing, unreadable, or malformed policy file must return an error from `LicensePolicy::load`. It must never fall back to an empty policy that treats everything as compliant.
- Error handling: return `Result<LicensePolicy, AppError>` and wrap I/O and serde errors with `.context()`, matching the convention used by handlers across the codebase.
- Per CONVENTIONS.md §Error handling: all fallible code returns `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/sbom/model/license_policy.rs` matching the convention's Rust source (`.rs`) scope. Example: `common/src/error.rs` (`AppError`, `IntoResponse`).
- Per CONVENTIONS.md §Module pattern: domain code lives in the `model/ + service/ + endpoints/` structure. Put the policy type under `model/`. Applies: task modifies `modules/fundamental/src/sbom/model/license_policy.rs` matching the convention's domain module (`modules/*/src/**.rs`) scope. Example: `modules/fundamental/src/sbom/model/summary.rs`.
- Constraints (docs/constraints.md): §5.1 change only the files listed above; §5.2 inspect code before modifying it; §5.4 do not duplicate existing helpers; §2.1–2.3 commits use Conventional Commits, reference the Jira task ID in the footer, and include an `Assisted-by:` trailer; §3.3 open the PR with `--base main`.

## Reuse Candidates
- `common/src/error.rs::AppError` — the shared error enum. Extend it instead of adding a new error type.
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — already carries the `license` field whose values the policy is evaluated against.
- `entity/src/package_license.rs` — package-to-license mapping entity. Use it to confirm the license identifier format (SPDX id vs. expression) the policy must match.

## Acceptance Criteria
- [ ] `config/license-policy.json` exists with `allowed`, `denied`, and `default` keys and a reasonable default set of SPDX identifiers
- [ ] `LicensePolicy::load` parses a valid policy file into a typed struct
- [ ] `LicensePolicy::load` returns an `AppError` (it does not panic and does not return an empty or permissive policy) when the file is missing or malformed
- [ ] `LicensePolicy::evaluate` returns `true` for allowed licenses and `false` for denied licenses
- [ ] Fail-closed: `LicensePolicy::evaluate` returns `false` for a missing (`None`) or unrecognized license unless the policy explicitly sets `"default": "compliant"`
- [ ] License matching ignores case and surrounding whitespace
- [ ] No new database tables or migrations are introduced

## Test Requirements
- [ ] Unit test: valid policy JSON loads, and allowed/denied licenses evaluate correctly
- [ ] Unit test: malformed JSON and a missing file each return an error from `LicensePolicy::load`
- [ ] Unit test (fail-closed): an unknown license and a `None` license each evaluate to non-compliant under the default policy
- [ ] Unit test: with `"default": "compliant"`, unknown licenses evaluate to compliant
- [ ] Unit test: case and whitespace differences (`"mit "`, `"Apache-2.0"`) are normalized

## Verification Commands
- `cargo test license_policy` — all policy tests pass
- `cargo clippy --all-targets -- -D warnings` — no warnings

## Dependencies
- None
