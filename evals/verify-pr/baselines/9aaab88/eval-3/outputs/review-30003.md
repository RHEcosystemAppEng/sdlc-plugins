# Review Comment Classification: 30003

**Comment ID:** 30003
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/mod.rs, line 18
**Classification:** nit

## Reasoning

The reviewer explicitly labels this comment as "Nit:" at the beginning of the message. The comment addresses a misleading error context message -- `.context("SBOM not found")` is confusing because `.context()` wraps the anyhow error chain, not the 404 logic. The reviewer suggests changing it to `"Failed to fetch SBOM"` to avoid confusion in error logs.

This is a **nit** because:
- The reviewer explicitly prefixes the comment with "Nit:" which is a clear self-classification signal
- The issue is about a misleading error message string, not a functional bug
- The actual 404 handling is correct (via `ok_or(AppError::NotFound(...))` on the next line)
- The suggested change improves clarity of error logs but does not affect correctness or behavior
- This is a minor style/readability concern

No sub-task created.
