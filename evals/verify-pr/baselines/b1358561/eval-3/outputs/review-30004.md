# Review Comment 30004 — Classification

- **Author:** reviewer-a
- **Review:** 20001 (CHANGES_REQUESTED)
- **File/Line:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1 (RIGHT)
- **Thread:** top-level, no replies, no prior classification reply → **unclassified**, processed this run

## Comment text

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` — so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: **Question**

## Reasoning

- The comment is phrased as questions ("Have you considered ...?", "Is that intentional?"). It asks the author to clarify intent and does not request a specific modification.
- No code change is requested in the comment itself, so under the classification rules it does not trigger a sub-task.

## Related verification finding (not a reclassification)

The question lines up with an independent finding from this verification run:

- The task lists `modules/fundamental/src/sbom/endpoints/get.rs` under **Files to Modify** ("add `include_deleted` parameter support"). The Description says a soft-deleted SBOM "remains accessible via direct GET with a `?include_deleted=true` parameter".
- The PR diff does not touch `get.rs`, so **Scope Containment is FAIL** (an unimplemented task file). The verification report records this; see `report.md`. The answer to the reviewer's question is that the behaviour is not intentional according to the task spec, because the task expected `get.rs` to change.
- The classification stays **Question**. The required work is tracked through the Scope Containment FAIL in the report rather than through a review-feedback sub-task.

## Outcome

- No sub-task created from this comment.
- Reply that would be posted (inline thread reply):
  `[sdlc-workflow/verify-pr] Classified as **question** — asks for clarification of intended behaviour; no code change requested in the comment. Note: the task's Files to Modify lists get.rs for include_deleted support, and the PR does not modify it (flagged as Scope Containment FAIL in the verification report). No sub-task created.`
