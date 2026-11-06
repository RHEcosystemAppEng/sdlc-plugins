# Criterion 3 — FAIL

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## What was checked

How the handler deals with a threshold value that is not one of `critical`, `high`, `medium` or `low`.

## Findings

```rust
.position(|&s| s == threshold.to_lowercase())
.unwrap_or(0);
```

- An unknown value such as `invalid` makes `position` return `None`. `.unwrap_or(0)` then quietly treats it as index 0 (`critical`).
- No error is returned. The handler never builds an `AppError`, even though the Implementation Notes say to reuse `common/src/error.rs::AppError` and return 400.
- Because of the reversed comparison described in criterion 1, index 0 means every count is included. A request with `?threshold=invalid` therefore gets **200 OK** and the full unfiltered summary.
- `threshold` is typed as `Option<String>`, not as the `Severity` enum the Implementation Notes ask for. If it were the enum, serde would reject bad values during extraction.
- No test for an invalid threshold was added.

## Verdict

FAIL. Invalid values are accepted and return 200 instead of 400 Bad Request.
