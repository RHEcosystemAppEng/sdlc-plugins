# Review Comment 30003 — Classification

- **Author:** reviewer-a
- **Review:** 20001 (CHANGES_REQUESTED)
- **Location:** `modules/fundamental/src/sbom/endpoints/mod.rs`, line 18 (RIGHT)
- **Thread:** top-level comment with no replies. No earlier classification reply exists, so the comment is **unclassified**.

## Comment

> Nit: `context("SBOM not found")` is misleading here because `.context()` wraps the error message for the anyhow chain — it doesn't mean the SBOM wasn't found. The actual 404 is handled by `ok_or(AppError::NotFound(...))` on the next line. Consider changing the context message to something like `"Failed to fetch SBOM"` to avoid confusion in error logs.

## Classification: **Nit**

## Reasoning

- **The reviewer labels it a nit ("Nit:")** and words it softly ("Consider changing …").
- **It is about wording, not behavior.** The change is to the text of an error message in the anyhow context chain. The 404 is already handled correctly by `.ok_or(AppError::NotFound(...))`, and the DELETE handler's status codes (204/404/409) are unaffected.
- Changing the string would make the logs clearer, but it does not affect correctness, any acceptance criterion, or the API contract.

## Outcome

- **Sub-task created:** no.
- **Planned reply (not posted):**
  `[sdlc-workflow/verify-pr] Classified as **nit** — minor wording of an error-context message; the 404 path is correctly handled by ok_or(AppError::NotFound) and the change does not affect correctness. No sub-task created.`
