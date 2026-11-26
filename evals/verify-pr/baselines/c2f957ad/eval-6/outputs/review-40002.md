# Review 40002 (review body): classification

- **Author:** reviewer-b
- **State:** CHANGES_REQUESTED
- **Body:** "The new Check 6 looks good overall, but I have a concern about the Markdown exclusion rule."

## Eval-review detection (Step 4a.1)
Not an eval result review. The author is a human (`reviewer-b`), not `github-actions[bot]`, and the body has neither the `## Eval Results` marker nor the `sdlc-workflow/run-evals` footer.

## Review-body extraction decision: not a separate classifiable item
Step 4a extracts review bodies only when they contain **substantive** feedback. This body is a summary line: general approval ("looks good overall") plus a pointer to a concern. It does not say what the concern is or ask for a change. The concern itself, and the change requested, are in inline comment 50001, which belongs to this review (`pull_request_review_id: 40002`).

Treating the body as a separate `review-body-40002` item would classify the same feedback twice and could create a duplicate sub-task. So:
- No synthetic `review-body-40002` item is classified.
- Its context (CHANGES_REQUESTED, "concern about the Markdown exclusion rule") is used as supporting evidence for classifying comment 50001 as a **code change request** (see review-50001.md).
- **No sub-task** comes from the review body itself, and no standalone `Re: @reviewer-b review` comment is needed. The reply on thread 50001 covers this review's feedback.
