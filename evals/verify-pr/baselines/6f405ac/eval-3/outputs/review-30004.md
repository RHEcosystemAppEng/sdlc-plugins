# Review Comment Classification: 30004

## Comment

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

**File:** `modules/fundamental/src/sbom/endpoints/get.rs` line 1
**Author:** reviewer-a

## Classification: QUESTION

## Reasoning

The reviewer asks two explicit questions: "Have you considered what happens when..." and "Is that intentional?" This is a request for clarification about the design decision, not a request for a code change. The reviewer observes that `get.rs` does not filter by `deleted_at`, meaning direct GET requests still return soft-deleted SBOMs, and asks whether this behavior is deliberate.

Notably, the task description explicitly states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." The task's acceptance criteria include "`GET /api/v2/sbom?include_deleted=true` includes soft-deleted SBOMs" for the list endpoint but do not require the individual GET endpoint to filter by default. This suggests the current behavior (GET by ID returns deleted SBOMs without filtering) may be intentional per the task spec, though the reviewer is reasonably asking for confirmation.

This is a question because:
1. The language is interrogative ("Have you considered...", "Is that intentional?")
2. The reviewer is asking for clarification about design intent, not requesting a change
3. No code modification is demanded or suggested

No sub-task is created for questions.
