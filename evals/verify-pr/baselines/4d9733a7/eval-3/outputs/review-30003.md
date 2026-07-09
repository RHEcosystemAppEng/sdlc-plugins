## Review Comment Classification: #30003

**Comment ID:** 30003
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/mod.rs` (line 18)
**Classification:** nit

### Reviewer Text

> Nit: `context("SBOM not found")` is misleading here because `.context()` wraps the error message for the anyhow chain -- it doesn't mean the SBOM wasn't found. The actual 404 is handled by `ok_or(AppError::NotFound(...))` on the next line. Consider changing the context message to something like `"Failed to fetch SBOM"` to avoid confusion in error logs.

### Reasoning

The reviewer explicitly labels this comment as "Nit:" at the start, self-classifying it as a minor feedback item. The content is about improving an error context string for clarity in logs -- it does not affect correctness, security, or functional behavior. The existing code works correctly: the `.context()` wrapping and the `.ok_or(AppError::NotFound(...))` handle the 404 case properly. The suggestion is to improve the wording of an internal error message to avoid confusion during debugging.

The use of "Consider changing" further confirms this is optional, minor style feedback.

### Action

No sub-task created. Nit-level feedback does not trigger sub-task creation.
