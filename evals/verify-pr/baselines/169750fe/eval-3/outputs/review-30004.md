# Review Comment Classification: #30004

## Comment Details
- **Author:** reviewer-a
- **File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
- **Content:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` — so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: **Question**

## Reasoning

1. **"Have you considered"** — This is an interrogative, asking whether the author has thought about a scenario. It does not direct a change.
2. **"Is that intentional?"** — The reviewer is seeking clarification about design intent, not requesting a code change. They want to understand whether the current behavior is deliberate.
3. The comment identifies a potential gap but frames it entirely as a question. The reviewer has not concluded that this is a bug — they are asking the author to confirm or explain the behavior.
4. The task description (Acceptance Criteria item 6) only specifies that `GET /api/v2/sbom?include_deleted=true` includes soft-deleted SBOMs in the list endpoint. The direct GET by ID returning soft-deleted SBOMs could be intentional (the task says "remains accessible via direct GET with a `?include_deleted=true` parameter" in the description, but the acceptance criteria don't explicitly require filtering on the GET-by-ID endpoint).

## Action
- **Sub-task creation:** NO
- **Reason:** Questions ask for clarification and do not trigger sub-task creation. The answer is for the author to provide, not for automated tooling to resolve.
