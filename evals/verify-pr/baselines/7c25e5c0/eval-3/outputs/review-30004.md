# Review Comment Classification: #30004

**Comment ID:** 30004
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Content:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` — so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: **Question**

### Reasoning

1. **"Have you considered"** — interrogative framing, asking for clarification rather than requesting a change.
2. **"Is that intentional?"** — explicitly asking whether the current behavior is by design. The reviewer is seeking information, not directing a modification.
3. The comment raises a valid observation (get.rs doesn't filter by `deleted_at`), but frames it as a question about intent rather than a directive to change the code. The reviewer acknowledges the possibility that this behavior might be intentional.

The observation is relevant: the task's "Files to Modify" includes get.rs with "add `include_deleted` parameter support", and get.rs is absent from the PR diff. However, the reviewer's language is interrogative, not prescriptive — they ask whether the omission is intentional rather than stating it must be fixed.

### Sub-task Required: No

No sub-task is created. Questions ask for clarification and do not trigger tracked work. The scope containment check separately flags get.rs as an unimplemented file from the task specification.
