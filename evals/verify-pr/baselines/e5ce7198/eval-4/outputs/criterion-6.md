## Criterion 6: Existing package list endpoint tests continue to pass (backward compatible)

### Result: PASS

### Evidence

Per the eval context, all CI checks pass for this PR. The change adds a new field to `PackageSummary` without modifying the behavior of existing fields (`id`, `name`, `version`, `license`). The endpoint handler in `list.rs` is functionally unchanged -- the only modification is an added comment.

The service layer in `service/mod.rs` adds a mapping step that preserves all existing field values (`id`, `name`, `version`, `license`) while adding the new `vulnerability_count` field. This is an additive change that does not alter the behavior of pre-existing fields.

Adding a new field to a JSON response is backward compatible for consumers that ignore unknown fields (standard practice in REST APIs). The existing test files in `tests/api/` (e.g., `sbom.rs`, `advisory.rs`, `search.rs`) would not be affected by a new field on `PackageSummary`.

### Conclusion

PASS -- CI passes, and the change is purely additive with no modifications to existing field behavior.
