# Review Comment Classification: 30004

## Comment

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**PR:** #744

## Classification: Question

## Reasoning

The reviewer uses interrogative language throughout, asking for clarification rather than requesting a change:

- "Have you considered" -- asks whether the author has thought about a scenario, not directing a change
- "Is that intentional?" -- explicitly asking for clarification on design intent

The comment identifies that `get.rs` does not filter by `deleted_at`, meaning a direct GET by ID will still return soft-deleted SBOMs. However, the reviewer does not assert this is wrong -- they ask whether it is intentional. This is significant because the task description explicitly states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." The current behavior (GET by ID returns deleted SBOMs without filtering) may or may not align with the intended design, and the reviewer is seeking clarification.

The reviewer is not requesting a code change; they are asking the author to confirm the design decision. This is a **question** that should be answered by the PR author.

## Action

No sub-task created. Questions ask for clarification and do not require code changes.
