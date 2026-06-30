# Review Comment Classification: 30004

## Comment
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Content:** Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: question

## Reasoning

The reviewer uses interrogative language throughout: "Have you considered", "Is that intentional?". The reviewer is asking for clarification about a design decision rather than directing a code change. The reviewer observes that `get.rs` does not filter by `deleted_at` and asks whether this is intentional behavior.

Notably, the task description explicitly states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." This suggests the current GET behavior (returning deleted SBOMs without the parameter) may be a discrepancy from the spec, but the reviewer is asking a question rather than directing a fix. The reviewer's intent is to seek clarification, not to mandate a change.

This meets the classification criteria for **question**: the reviewer asks for clarification, and no code change is directly requested.

## Sub-task required: No
