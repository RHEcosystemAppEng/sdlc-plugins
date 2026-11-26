# Review Comment 30003 — Classification

- **Author:** reviewer-a
- **Review:** 20001 (CHANGES_REQUESTED)
- **File/Line:** `modules/fundamental/src/sbom/endpoints/mod.rs`, line 18 (RIGHT)
- **Prior classification reply:** none (unclassified, processed this run)

## Comment

> Nit: `context("SBOM not found")` is misleading here because `.context()` wraps the error message for the anyhow chain — it doesn't mean the SBOM wasn't found. The actual 404 is handled by `ok_or(AppError::NotFound(...))` on the next line. Consider changing the context message to something like `"Failed to fetch SBOM"` to avoid confusion in error logs.

## Classification: **nit**

## Reasoning

- The reviewer labels it "Nit:" and phrases it softly ("Consider changing").
- It only affects the wording of an error-context string in logs. Behavior does not change: when the record is missing, the 404 still comes from `.ok_or(AppError::NotFound(...))`, and DB errors still propagate through `.context(...)`. Acceptance criterion "returns 404 for non-existent SBOM" is still met.
- This is minor wording and readability feedback. It does not affect correctness.

## Outcome

- No sub-task created.
- Reply that would be posted (not posted, eval mode):
  `[sdlc-workflow/verify-pr] Classified as **nit** — minor wording of an error-context message; does not affect correctness or behavior (404 is still produced by ok_or). No sub-task created.`
