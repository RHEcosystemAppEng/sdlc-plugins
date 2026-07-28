# Review Comment Classification: 30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`
**Line:** 1
**Text:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: QUESTION

## Reasoning

The reviewer asks for clarification using explicit question language:

1. **"Have you considered"** -- this is an inquiry, not a directive. The reviewer is asking whether the author has thought about a specific scenario.
2. **"Is that intentional?"** -- the reviewer is asking about the author's intent, not asserting that the behavior is wrong. The reviewer acknowledges that the current behavior might be deliberate.

The comment does not request a code change. It raises a question about the design decision regarding `get.rs` behavior for soft-deleted SBOMs. The reviewer observes that direct GET does not filter by `deleted_at` and asks whether this is by design.

Notably, the task description itself states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." This suggests the task intends for GET by ID to support the `include_deleted` parameter, but the reviewer is asking whether the current implementation (which returns deleted SBOMs unconditionally on direct GET) matches the author's understanding. The question is seeking clarification, not demanding a change.

## Action

No sub-task created. Questions seek clarification and do not require code changes until the author responds and a code change request is explicitly made.
