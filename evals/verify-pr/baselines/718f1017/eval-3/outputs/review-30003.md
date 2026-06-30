# Review Comment Classification: 30003

**Comment ID:** 30003
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/mod.rs
**Line:** 18
**Classification:** nit

## Reasoning

The reviewer explicitly labels this as "Nit:" at the beginning of the comment. The feedback concerns a misleading `.context("SBOM not found")` error message in the anyhow chain. The reviewer correctly notes that `.context()` wraps the error for the anyhow chain and the actual 404 is handled by `.ok_or(AppError::NotFound(...))` on the next line. They suggest changing the context message to "Failed to fetch SBOM" to avoid confusion in error logs.

This is minor style/clarity feedback that:
1. Does not affect correctness -- the 404 is correctly returned regardless of the context message.
2. Does not affect functionality -- the context message only appears in internal error logs/traces.
3. Is explicitly self-labeled as a "Nit" by the reviewer.

**Action:** No sub-task created. Minor style feedback that does not affect correctness.
