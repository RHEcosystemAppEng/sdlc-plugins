# Review Comment Classification: 30003

**Comment ID:** 30003
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/mod.rs
**Line:** 18
**Classification:** nit

## Reasoning

The reviewer flags a misleading `.context()` error message. The current code uses `.context("SBOM not found")` on the `fetch` call, but `.context()` wraps the anyhow error chain and does not determine the HTTP response -- the actual 404 is handled by the subsequent `.ok_or(AppError::NotFound(...))`. The reviewer suggests changing the context message to `"Failed to fetch SBOM"` to avoid confusion in error logs.

This is a minor error message wording improvement. The prefix "Nit:" used by the reviewer explicitly signals this is a nitpick. The current code functions correctly -- the right HTTP status codes are returned in all cases. The suggestion only improves the clarity of internal error log messages and does not affect API behavior, data integrity, or user-visible responses.

**Action:** No sub-task created. Minor style feedback that does not affect correctness.
