## Repository
trustify-backend

## Target Branch
main

## Description
Define the license policy configuration model that represents compliance rules loaded from a JSON config file. The policy specifies which licenses are allowed, denied, or flagged for review, enabling the license compliance report to check each package's license against the configured policy.

## Files to Create
- `modules/fundamental/src/license/mod.rs` — License module root, re-exports submodules
- `modules/fundamental/src/license/model/mod.rs` — Model submodule root
- `modules/fundamental/src/license/model/policy.rs` — `LicensePolicy` struct with `allowed`, `denied`, and `review` license lists; includes `load_from_file` deserialization from JSON

## Implementation Notes
Follow the established module pattern from existing domain modules (e.g., `modules/fundamental/src/sbom/model/`). The `LicensePolicy` struct should derive `Deserialize` for loading from JSON config files.

Use `serde_json::from_reader` for loading the policy file, wrapping errors with `.context()` per the error handling convention in `common/src/error.rs`.

Per CONVENTIONS.md §Module pattern: follow the `model/ + service/ + endpoints/` structure for the new license module.
Applies: task creates `modules/fundamental/src/license/model/policy.rs` matching the convention's Rust module scope.

Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping for the policy loading function.
Applies: task creates `modules/fundamental/src/license/model/policy.rs` matching the convention's Rust file scope.

## Acceptance Criteria
- [ ] `LicensePolicy` struct is defined with `allowed: Vec<String>`, `denied: Vec<String>`, and `review: Vec<String>` fields
- [ ] `LicensePolicy::load_from_file(path: &Path) -> Result<Self, AppError>` loads and deserializes a JSON policy file
- [ ] Invalid or missing policy files return descriptive `AppError` with context

## Test Requirements
- [ ] Unit test: valid JSON policy file deserializes correctly
- [ ] Unit test: missing policy file returns appropriate error
- [ ] Unit test: malformed JSON returns appropriate error

## Dependencies
- None (first task)
