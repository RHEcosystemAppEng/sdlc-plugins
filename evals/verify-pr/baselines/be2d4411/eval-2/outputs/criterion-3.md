# Criterion 3: Invalid threshold returns 400 Bad Request

## Verdict: FAIL

## Criterion Text
`GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Evidence from Diff

The threshold value is looked up in the filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs`:

```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

## Detailed Reasoning

When an invalid threshold value is provided (e.g., `?threshold=invalid`), the `.position()` call returns `None` because "invalid" does not match any element in `["critical", "high", "medium", "low"]`. The code then calls `.unwrap_or(0)`, which silently defaults to index 0 (the position of "critical").

This means that **any** invalid threshold value (e.g., "foobar", "none", "xyz") is silently treated as `threshold=critical`. No validation error is raised, and no 400 status code is returned.

The task's implementation notes explicitly state:
> Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)

The correct implementation should:
1. Check whether the provided threshold matches a valid severity value
2. If not, return an `AppError` variant that maps to HTTP 400 Bad Request
3. The `AppError` enum is available in `common/src/error.rs` (already imported in the file)

Instead, the code silently swallows the invalid input, which is a usability and correctness issue -- callers who misspell a threshold value (e.g., "hig" instead of "high") will get results filtered to critical-only with no indication that their input was ignored.

## Conclusion

The criterion fails because invalid threshold values are silently accepted via `unwrap_or(0)` instead of producing a 400 Bad Request response. No validation or error handling exists for unrecognized threshold values.
