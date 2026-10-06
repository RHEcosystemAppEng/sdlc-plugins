## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration module that loads and validates a JSON configuration file defining which licenses are allowed, denied, or flagged for review. This policy is used by the license report service (Task 3) to determine compliance status for each license group in the report.

The policy file is stored in the repository and loaded at service initialization time. Organizations can customize the policy by editing the JSON configuration file.

## Files to Create
- `common/src/license_policy.rs` -- defines LicensePolicy struct, LicensePolicyEntry, policy loading from JSON file, and compliance checking logic

## Files to Modify
- `common/src/lib.rs` -- add `pub mod license_policy;` to expose the new module
- `common/Cargo.toml` -- add serde_json dependency if not already present (for JSON config file parsing)

## Implementation Notes
- The license policy JSON config file should support a structure like:
  ```json
  {
    "allowed": ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause"],
    "denied": ["GPL-3.0", "AGPL-3.0"],
    "review_required": ["LGPL-2.1", "MPL-2.0"]
  }
  ```
- Licenses not listed in any category should default to "review_required" (conservative default).
- The LicensePolicy struct should provide a method like `fn is_compliant(&self, license: &str) -> bool` that returns `true` only for licenses in the `allowed` list.
- Follow the error handling pattern in `common/src/error.rs` (AppError) for policy loading failures. Use `.context()` wrapping from anyhow for descriptive error messages.
- Per CONVENTIONS.md Error handling: all fallible operations return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `common/src/license_policy.rs` matching the convention's `.rs` file scope.

### Constraints (from docs/constraints.md)
- SS5.1: Keep changes scoped to the files listed in Files to Modify and Files to Create.
- SS5.2: Inspect existing common/ modules before writing to follow established patterns.
- SS2.1: Commit must reference Jira issue ID in footer.
- SS2.2: Use Conventional Commits format.

## Reuse Candidates
- `common/src/error.rs::AppError` -- reuse the existing error enum for policy loading failures
- `common/src/db/query.rs` -- reference for how common/ modules are structured and exported

## Acceptance Criteria
- [ ] `LicensePolicy` struct is defined with `allowed`, `denied`, and `review_required` license lists
- [ ] Policy can be loaded from a JSON configuration file path
- [ ] `is_compliant()` method correctly identifies allowed vs non-compliant licenses
- [ ] Licenses not in any category default to non-compliant (review_required)
- [ ] Policy loading errors return `AppError` with descriptive context messages
- [ ] Module is exported from `common/src/lib.rs`

## Test Requirements
- [ ] Unit test: loading a valid policy JSON file succeeds and produces correct LicensePolicy
- [ ] Unit test: `is_compliant()` returns true for allowed licenses, false for denied and review_required
- [ ] Unit test: unlisted licenses default to non-compliant
- [ ] Unit test: loading an invalid or missing policy file returns an appropriate error

## Dependencies
- None
