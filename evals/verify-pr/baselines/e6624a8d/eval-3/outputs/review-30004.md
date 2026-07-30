# Review Comment Classification: 30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Text:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: question

## Reasoning

The reviewer asks for clarification using interrogative language: "Have you considered..." and "Is that intentional?" The comment does not request a code change or suggest a specific fix. Instead, it raises a question about the design intent of the current behavior. The reviewer observes that `get.rs` does not filter by `deleted_at` and asks whether this is by design or an oversight.

This is a clarification question -- the reviewer is seeking to understand the rationale rather than demanding a change. No code change is requested. No sub-task is created.

## Action

No sub-task created. This is a question asking for clarification; no code change is needed.
