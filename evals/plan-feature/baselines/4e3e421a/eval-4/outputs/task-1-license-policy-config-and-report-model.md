## Repository
trustify-backend

## Target Branch
main

## Description
Introduce the configurable license policy and the response model for the SBOM license compliance report (TC-9004). The policy is stored as a JSON configuration file in the repository and declares which SPDX license identifiers are allowed and which are denied. This task adds the policy file, a typed loader with a compliance-check function, and the serializable report structs (`LicenseReport`, `LicenseGroup`) that later tasks will populate and return from the new endpoint.

This task is purely additive: no existing behavior changes and no database tables are added (per the Feature's non-functional requirement "No new database tables").

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — declare and re-export the new `license_report` model module
- `modules/fundamental/src/sbom/service/mod.rs` — declare and re-export the new `license_policy` service module

## Files to Create
- `license-policy.json` — default license policy (JSON) checked into the repository root; contains `allowed` and `denied` arrays of SPDX license identifiers
- `modules/fundamental/src/sbom/model/license_report.rs` — `LicenseReport { groups: Vec<LicenseGroup> }` and `LicenseGroup { license: String, packages: Vec<PackageSummary>, compliant: bool }` structs (serde `Serialize`, utoipa/OpenAPI schema derive if used by sibling models)
- `modules/fundamental/src/sbom/service/license_policy.rs` — `LicensePolicy` struct, `LicensePolicy::load(path)` loader, and `LicensePolicy::is_compliant(license: &str) -> bool`

## Implementation Notes
- Follow the existing SBOM model layout: `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`) show the derive set and serialization style to copy for `LicenseReport` / `LicenseGroup`.
- Reuse `PackageSummary` from `modules/fundamental/src/package/model/summary.rs` as the element type of `LicenseGroup.packages` — it already carries the `license` field; do not define a parallel package struct.
- Response shape must match the Feature requirement exactly: `{ "groups": [ { "license": "MIT", "packages": [...], "compliant": true } ] }`.
- Policy loader errors must map into `AppError` (`common/src/error.rs`) with `.context()` wrapping, so the endpoint returns a server error instead of silently treating everything as compliant.
- **Fail-closed policy evaluation (CI gate, UC-2):** the report is consumed by CI pipelines that fail the build only when a group has `compliant: false`. Any degraded path that yields `compliant: true` by default would let non-compliant builds pass green. Therefore:
  - `LicensePolicy::load` MUST return an error (not an empty/permissive policy) when the file is missing, unreadable, or malformed JSON.
  - `LicensePolicy::is_compliant` MUST return `false` for licenses that are not in the `allowed` list (default-deny), including unknown/empty/`NOASSERTION` license values.
- Policy file location should be configurable (e.g., via a config/env value read at startup) with `license-policy.json` at the repo root as the default; document the chosen key in the doc task.
- Per CONVENTIONS.md §Module pattern: place new model and service code under the SBOM module's `model/` and `service/` directories. Applies: task modifies modules/fundamental/src/sbom/model/mod.rs matching the convention's `model/ + service/ + endpoints/` module directory scope. Example: `modules/fundamental/src/sbom/model/summary.rs`.
- Per CONVENTIONS.md §Error handling: policy loading and evaluation return `Result<T, AppError>` and wrap failures with `.context()`. Applies: task creates modules/fundamental/src/sbom/service/license_policy.rs matching the convention's Rust handler/service (`.rs`) scope. Example: `modules/fundamental/src/sbom/service/sbom.rs`.
- Constraints (docs/constraints.md): commits use Conventional Commits with a Jira footer (`Implements <task-key>`) and the `Assisted-by: Claude Code` trailer (§2.1–2.3); PR uses `--base main` and its link is posted to the Jira task (§3.2–3.3); changes stay within the files listed above, inspect code before modifying, and do not duplicate existing functionality (§5.1–5.4); compare against sibling implementations for error-handling parity (§5.8).

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — existing package DTO including `license`; reuse as `LicenseGroup.packages` element type
- `common/src/error.rs::AppError` — shared error enum implementing `IntoResponse`; use for policy load failures
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for derive/serde conventions on SBOM model structs

## Acceptance Criteria
- [ ] `license-policy.json` exists at the repository root with `allowed` and `denied` SPDX identifier arrays
- [ ] `LicenseReport` and `LicenseGroup` serialize to `{ "groups": [ { "license": ..., "packages": [...], "compliant": ... } ] }`
- [ ] `LicensePolicy::load` returns an `AppError` when the policy file is missing, unreadable, or not valid JSON (fail-closed — never a permissive default)
- [ ] `LicensePolicy::is_compliant` returns `true` only for licenses in `allowed`, and `false` for denied, unknown, empty, or `NOASSERTION` values
- [ ] No database migrations or new entities are added

## Test Requirements
- [ ] Unit test: valid policy JSON loads and `is_compliant("MIT")` returns `true` when MIT is allowed
- [ ] Unit test: a denied license (e.g., `GPL-3.0-only`) returns `false`
- [ ] Unit test: an unlisted/unknown license and an empty license string return `false` (default-deny)
- [ ] Unit test: missing policy file returns an error (fail-closed path)
- [ ] Unit test: malformed policy JSON returns an error (fail-closed path)
- [ ] Unit test: `LicenseReport` serializes to the documented JSON shape

## Verification Commands
- `cargo test -p trustify-module-fundamental license_policy` — all policy unit tests pass
- `cargo build` — workspace compiles with no new warnings

## Dependencies
- None
