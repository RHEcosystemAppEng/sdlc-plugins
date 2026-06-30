## Repository
trustify-backend

## Target Branch
main

## Description
Define the license policy model that represents an organization's allowed and denied license list. The policy is loaded from a JSON configuration file and used by the license report service to determine compliance. This task establishes the data structures and configuration loading logic without adding any endpoints.

## Files to Create
- `modules/fundamental/src/license/mod.rs` — license module root, re-exports submodules
- `modules/fundamental/src/license/model/mod.rs` — model submodule root
- `modules/fundamental/src/license/model/policy.rs` — LicensePolicy struct and deserialization logic
- `config/default-license-policy.json` — default license policy configuration file

## Implementation Notes
Follow the existing module pattern in `modules/fundamental/src/` where each domain has `model/`, `service/`, and `endpoints/` subdirectories. The LicensePolicy struct should be a simple Rust struct with serde Deserialize:

```rust
#[derive(Debug, Clone, Deserialize)]
pub struct LicensePolicy {
    pub allowed_licenses: Vec<String>,
    pub denied_licenses: Vec<String>,
    pub default_policy: PolicyDefault, // Allow or Deny
}

#[derive(Debug, Clone, Deserialize)]
pub enum PolicyDefault {
    Allow,
    Deny,
}
```

Load the policy from a configurable file path, with a built-in default. Reference the error handling pattern in `common/src/error.rs` using `AppError` for configuration loading failures.

Per CONVENTIONS.md §Module Pattern: follow model/ + service/ + endpoints/ structure.
Applies: task creates `modules/fundamental/src/license/model/policy.rs` matching the convention's `.rs` module scope.

## Acceptance Criteria
- [ ] LicensePolicy struct can be deserialized from a JSON file
- [ ] PolicyDefault enum supports Allow and Deny variants
- [ ] A default license policy JSON file exists with common permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) in the allowed list
- [ ] Policy loading function returns AppError on invalid configuration
- [ ] License module is registered in `modules/fundamental/src/lib.rs`

## Test Requirements
- [ ] Unit test: deserialize a valid license policy JSON into LicensePolicy struct
- [ ] Unit test: deserialize policy with missing fields returns appropriate error
- [ ] Unit test: PolicyDefault::Allow and PolicyDefault::Deny behave correctly in match expressions

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}
