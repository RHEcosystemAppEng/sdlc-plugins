# Review Comment Classification: 30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Text:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: question

## Reasoning

The reviewer asks two questions: "Have you considered..." and "Is that intentional?" This is a request for clarification about the design decision, not a directive to change code. The reviewer is raising a concern but framing it as a question to understand intent rather than prescribing a fix. The task description explicitly states "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter", which means the GET endpoint should support `include_deleted=true` but the task description says deleted SBOMs "remain accessible via direct GET" -- implying the current behavior (returning deleted SBOMs on direct GET) may be intentional by design. The reviewer is asking for confirmation of this design choice. No sub-task is created for question classifications.
