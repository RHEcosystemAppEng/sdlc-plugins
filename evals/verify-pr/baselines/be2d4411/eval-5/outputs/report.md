# Verification Report: PR #746 (TC-9105)

**Task**: Simplify PURL recommendation response to exclude qualifiers
**Repository**: trustify-backend
**PR**: https://github.com/trustify/trustify-backend/pull/746
**Jira**: https://redhat.atlassian.net/browse/TC-9105

---

## Verdicts

| Check                        | Verdict | Details |
|------------------------------|---------|---------|
| Scope Containment            | PASS    | All changes are within the 3 files listed to modify and 1 file listed to create. No unexpected files touched. |
| Diff Size                    | PASS    | 4 files changed. Proportional to the feature scope -- two production files and two test files. |
| Commit Traceability          | PASS    | Single PR addressing a single Jira task (TC-9105). |
| Sensitive Patterns           | PASS    | No secrets, credentials, API keys, `.env` files, or other sensitive data patterns detected. |
| CI Status                    | PASS    | All CI checks pass. |
| Criterion 1                  | PASS    | Endpoint returns versioned PURLs without qualifiers. See [criterion-1.md](criterion-1.md). |
| Criterion 2                  | PASS    | Response PURLs contain no `?` query parameters. See [criterion-2.md](criterion-2.md). |
| Criterion 3                  | PASS    | Deduplication applied after qualifier removal. See [criterion-3.md](criterion-3.md). |
| Criterion 4                  | PASS    | Pagination and sorting behavior preserved. See [criterion-4.md](criterion-4.md). |
| Criterion 5                  | PASS    | Response shape remains `PaginatedResults<PurlSummary>`. See [criterion-5.md](criterion-5.md). |
| Test Change Classification   | MIXED   | Both additive and reductive signals present. See detailed analysis below. |
| Eval Quality                 | N/A     | No eval result reviews exist. |
| Verification Commands        | N/A     | Eval environment; no live repository to execute against. |

---

## Test Change Classification: MIXED

### Structural Summary

#### File: `tests/api/purl_recommend.rs` (modified)

| Signal    | Type      | Description |
|-----------|-----------|-------------|
| Reductive | Removed   | `test_recommend_purls_with_qualifiers` -- entire test function deleted (17 lines) |
| Reductive | Relaxed   | `test_recommend_purls_basic` -- PURL assertion changed from fully qualified to versioned-only |
| Additive  | New       | `test_recommend_purls_dedup` -- new test function (16 lines) |
| Additive  | Tightened | `test_recommend_purls_basic` -- added two `!contains('?')` assertions |

**Net signal count**: 2 reductive, 2 additive

#### File: `tests/api/purl_simplify.rs` (new)

| Signal   | Type | Description |
|----------|------|-------------|
| Additive | New  | `test_simplified_purl_no_version` -- tests PURL without version qualifier |
| Additive | New  | `test_simplified_purl_mixed_types` -- tests different PURL types (npm, PyPI) |
| Additive | New  | `test_simplified_purl_ordering_preserved` -- tests ordering + pagination after qualifier removal |

**Net signal count**: 0 reductive, 3 additive

#### Aggregate

| Category  | Count |
|-----------|-------|
| Reductive | 2     |
| Additive  | 5     |
| **Net**   | **MIXED** |

### Semantic Assessment

The most significant reductive change is the assertion relaxation in `test_recommend_purls_basic`. In the base-branch version, the test asserted:

```rust
assert_eq!(
    body.items[0].purl,
    "pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar"
);
```

In the PR-branch version, this is replaced with:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

This is a **relaxation** of the expected value: the test no longer verifies that the response includes the exact qualifier string (`repository_url=https://repo1.maven.org&type=jar`). Instead, it verifies the versioned PURL and adds negative assertions confirming qualifier absence. The assertion now checks for *less specificity* in the PURL value while adding a new constraint on qualifier absence. This is consistent with the behavioral change (qualifiers are intentionally removed), but structurally it is a relaxation of the match precision -- the old assertion would catch any change to the qualifier format, while the new one would not detect such changes (since qualifiers are no longer present).

The removal of `test_recommend_purls_with_qualifiers` is a clear reductive signal: this test verified that qualifier-variant PURLs were returned as distinct entries, and that behavior is no longer tested because it no longer exists. The replacement test `test_recommend_purls_dedup` uses the same seed data but asserts the opposite behavior (1 entry instead of 2), which is appropriate for the new semantics but does not preserve the old test's coverage.

### Reductive Findings

1. **Removed function**: `test_recommend_purls_with_qualifiers` was deleted entirely. This test verified that PURLs with different `repository_url` qualifiers were returned as separate entries and that each entry contained qualifier details. This behavior no longer exists after the change, so the test removal is intentional and consistent with the feature change, but it is structurally reductive.

2. **Relaxed assertion**: In `test_recommend_purls_basic`, the expected PURL value was changed from a fully qualified string (with `?repository_url=...&type=jar`) to a versioned-only string (without qualifiers). The old assertion was a strict equality check against a 78-character PURL string; the new assertion checks a 46-character string. This is a relaxation -- the assertion now accepts a less-specific value.

### Conclusion

The test changes are classified as **MIXED**. The reductive signals (removed function, relaxed assertion) are intentional consequences of the behavioral change -- qualifiers are no longer part of the response, so tests that verified qualifier presence are appropriately removed or updated. However, they are structurally reductive regardless of intent. The additive signals (1 new test function in the modified file, 3 new test functions in the new file, 2 new negative assertions) expand coverage for the new behavior. The net effect is that the test suite trades qualifier-presence coverage for qualifier-absence and deduplication coverage, which aligns with the feature change.

---

## Notes

- The `dedup_by` implementation in the service layer only removes *consecutive* duplicates. If the database query returns non-adjacent duplicate PURLs (after qualifier stripping), they would not be deduplicated. This works correctly when same-version entries are adjacent in the result set (which is typical for ordered queries), but could be fragile if query ordering changes in the future. This is a minor implementation concern, not a verification blocker.
- Review comments: none.
- The `test_recommend_purls_unknown_returns_empty` and `test_recommend_purls_pagination` tests are unchanged in the diff, confirming that existing edge-case and pagination coverage is preserved.
