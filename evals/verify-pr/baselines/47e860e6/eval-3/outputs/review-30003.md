# Review Comment 30003 — Classification

- **Comment ID:** 30003
- **Author:** reviewer-a
- **Review:** 20001 (CHANGES_REQUESTED)
- **File/Line:** `modules/fundamental/src/sbom/endpoints/mod.rs`, line 18 (RIGHT)
- **Thread:** top-level (no `in_reply_to_id`), no replies
- **Prior classification reply:** none, so the comment is unclassified and goes through classification

## Original comment

> Nit: `context("SBOM not found")` is misleading here because `.context()` wraps the error message for the anyhow chain — it doesn't mean the SBOM wasn't found. The actual 404 is handled by `ok_or(AppError::NotFound(...))` on the next line. Consider changing the context message to something like `"Failed to fetch SBOM"` to avoid confusion in error logs.

## Classification: **nit**

## Reasoning

- **The reviewer labels it a nit.** The comment starts with "Nit:" and uses soft wording: "**Consider** changing the context message to something like...".
- **It is minor wording feedback.** It asks to change the text of an error-context string. The control flow and HTTP behaviour stay the same.
- **Correctness is not affected.** The reviewer notes, and the diff confirms, that the 404 is already returned by `.ok_or(AppError::NotFound("SBOM not found".into()))`. Acceptance criterion 3 (returns 404 for a non-existent SBOM) is met, and `test_delete_nonexistent_sbom_returns_404` covers it. Only the error-log text for database failures would change.
- **No convention requires different text.** The repo's error-handling convention ("All handlers return `Result<T, AppError>` with `.context()` wrapping") is followed. The PR does use `.context()`, and the comment only concerns the wording of the message.

## Outcome

- **Sub-task created:** no. Nits do not trigger sub-task creation.
- **Reply that would be posted to the thread** (eval mode, so not posted):

  ```
  gh api repos/trustify/trustify-backend/pulls/744/comments/30003/replies -f body="[sdlc-workflow/verify-pr] Classified as **nit** — minor wording of the .context() error message; the 404 path is already handled by ok_or(AppError::NotFound(...)), so this does not affect correctness. No sub-task created."
  ```
