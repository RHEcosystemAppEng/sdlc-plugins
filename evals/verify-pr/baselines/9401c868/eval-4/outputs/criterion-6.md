## Criterion 6: Existing package list endpoint tests continue to pass (backward compatible)

**Result: PASS**

### Analysis

The PR states that all CI checks pass, which implies existing tests are not broken by this change.

The change is additive in nature:
- A new field (`vulnerability_count`) is added to the `PackageSummary` struct. In JSON serialization, this adds a new key to the response object but does not remove or rename any existing keys.
- The endpoint handler logic in `list.rs` is unchanged (only a comment was added).
- The service method signature remains the same (`list(offset, limit)`).

Adding a new field to a response struct is a backward-compatible change for:
- API consumers: existing clients will ignore unknown fields (standard JSON practice).
- Existing tests: tests that deserialize the response into `PackageSummary` would need to account for the new field, but since CI passes, either the tests use partial matching or they have been updated accordingly.

The only new test file (`tests/api/package_vuln_count.rs`) is additive and does not modify existing test files.

This criterion is satisfied.
