# Review Comment 30003 — Classification

- **Comment ID:** 30003
- **Author:** reviewer-a
- **Review:** 20001 (CHANGES_REQUESTED)
- **File/Line:** `modules/fundamental/src/sbom/endpoints/mod.rs:18`
- **Thread:** top-level (`in_reply_to_id: null`), no replies. No existing classification reply, so it is **unclassified**.

## Comment text

> Nit: `context("SBOM not found")` is misleading here because `.context()` wraps the error message for the anyhow chain — it doesn't mean the SBOM wasn't found. The actual 404 is handled by `ok_or(AppError::NotFound(...))` on the next line. Consider changing the context message to something like `"Failed to fetch SBOM"` to avoid confusion in error logs.

## Classification: **nit**

## Reasoning

- The reviewer labels it "Nit:" and phrases it as "Consider changing", which is soft and optional.
- It only asks to reword an error-context string. The behavior does not change. The Correctness sub-agent confirmed that the 404 path works: `.ok_or(AppError::NotFound(...))` turns `Ok(None)` into a 404. `.context(...)` only labels real database errors, and those still surface as errors with any wording.
- It affects how clear the logs are, not correctness, and no acceptance criterion depends on it.

## Outcome

- **Sub-task:** none.
- **Planned reply (not posted, fixture eval):**
  `[sdlc-workflow/verify-pr] Classified as **nit** — minor wording of an error-context message; the 404 path is handled correctly by ok_or(AppError::NotFound), so this does not affect correctness. No sub-task created.`
