# Review Comment Classification: 30004

## Comment Details

- **ID:** 30004
- **Author:** reviewer-a
- **File:** modules/fundamental/src/sbom/endpoints/get.rs
- **Line:** 1
- **Body:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: QUESTION

## Reasoning

The reviewer is asking for clarification about a design decision, not requesting a code change. Key language indicators:

1. **"Have you considered"** -- opens with a question seeking the author's perspective.
2. **"Is that intentional?"** -- the closing question explicitly asks whether the current behavior is a deliberate design choice. The reviewer does not assert the behavior is wrong; they ask whether it was considered.
3. **No directive language** -- the comment contains no imperative statements ("should", "must", "add", "change"). It does not prescribe a fix or state what the code ought to do.

The reviewer observes that `get.rs` does not filter by `deleted_at`, meaning a direct GET by ID still returns soft-deleted SBOMs. Rather than declaring this a bug, they ask whether this is the intended behavior. This is a valid design question -- the task description does mention adding `include_deleted` parameter support to `get.rs`, but the acceptance criteria do not include a specific criterion for GET-by-ID filtering. The reviewer is seeking clarification, not demanding a change.

Note: While the task's "Files to Modify" section lists `get.rs` for `include_deleted` parameter support, the reviewer does not reference the task spec -- they are asking about intent from the PR author's perspective. The missing `get.rs` changes are captured separately in the Scope Containment check.

## Action

No sub-task created. Questions ask for clarification and do not require code changes.
