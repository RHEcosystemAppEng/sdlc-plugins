# Review Comment Classification: 30004

## Comment

- **ID:** 30004
- **Author:** reviewer-a
- **File:** modules/fundamental/src/sbom/endpoints/get.rs
- **Line:** 1
- **Body:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: question

## Reasoning

The reviewer asks for clarification about the intended behavior of the direct GET endpoint for soft-deleted SBOMs. The language is interrogative throughout:
- "Have you considered..." -- asks whether the author thought about this scenario
- "Is that intentional?" -- asks for confirmation of design intent

The reviewer does not request a code change or suggest an alternative implementation. Instead, they observe a potential gap and ask the author to confirm whether the current behavior is by design. The task description does mention modifying `get.rs` to add `include_deleted` parameter support, and the PR does not include changes to `get.rs`, but the reviewer frames this as a question rather than a code change request.

This observation is noted in the Scope Containment check (get.rs is listed in Files to Modify but not changed in the PR), which independently flags the gap.

## Action

No sub-task created. Questions ask for clarification and do not trigger sub-task creation. The scope gap with get.rs is tracked separately in the Scope Containment finding.
