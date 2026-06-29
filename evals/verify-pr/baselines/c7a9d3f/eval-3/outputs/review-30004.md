# Review Comment Classification: 30004

**Comment ID:** 30004
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/get.rs
**Line:** 1
**Content:** Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: question

## Reasoning

The reviewer is asking for clarification about intentional design behavior, not requesting a specific code change. The language is interrogative ("Have you considered...?", "Is that intentional?") and the comment raises a design concern rather than prescribing a fix. The reviewer observes that `get.rs` does not filter by `deleted_at` and asks whether this is deliberate.

While this question identifies a legitimate gap -- the task specification lists `modules/fundamental/src/sbom/endpoints/get.rs` as a file to modify with `include_deleted` parameter support, and the PR does not include changes to this file -- the reviewer's comment is phrased as a question seeking clarification rather than a directive to change code. The scope containment analysis (Intent Alignment sub-agent) separately flags the missing `get.rs` modification as a FAIL verdict, which is the appropriate mechanism for tracking this gap.

Note: The missing `get.rs` implementation is captured in the Scope Containment check (FAIL verdict) and does not require a separate sub-task from this review comment classification. The question itself does not trigger sub-task creation because it asks for intent clarification, not a code change.

**Action:** No sub-task created.
