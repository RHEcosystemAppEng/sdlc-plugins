# Criterion 6: Existing package list endpoint tests continue to pass (backward compatible)

**Verdict: PASS**

## Reasoning
- The change only adds a field. No existing field of `PackageSummary` is removed or renamed, and the endpoint path and parameters (`/api/v2/package`, `offset`, `limit`) are unchanged.
- The `list.rs` change is comment-only.
- All CI checks pass, per the task context, so existing tests still compile and pass.
- No existing tests were modified or deleted. The only test change is the new file `tests/api/package_vuln_count.rs`.

## Evidence
- `list.rs` hunk: `.list(params.offset, params.limit)` is unchanged apart from the trailing comment.
- CI status: all checks passing.
