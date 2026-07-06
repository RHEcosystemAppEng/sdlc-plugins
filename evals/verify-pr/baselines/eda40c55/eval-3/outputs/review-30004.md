# Review Comment Classification: Comment 30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Text:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: QUESTION

## Reasoning

The reviewer asks two explicit questions: "Have you considered...?" and "Is that intentional?" This is seeking clarification about the design decision, not requesting a code change. The reviewer observes a behavior (GET by ID returns deleted SBOMs without requiring `include_deleted=true`) and asks whether this is by design or an oversight.

Key indicators supporting question classification:
1. **Explicit question marks**: two questions in the comment ("Have you considered...?" and "Is that intentional?")
2. **Seeks clarification, not code change**: the reviewer is asking whether the current behavior is intentional, not demanding it be changed
3. **No imperative language**: no "should", "must", "wrap", "add", or other directive verbs
4. **Acknowledges possible intentionality**: "Is that intentional?" indicates the reviewer recognizes the behavior might be by design (the task description says "remains accessible via direct GET with a `?include_deleted=true` parameter", which could be read as the GET endpoint should support the parameter but still return deleted SBOMs by default)

**Note**: This question does highlight a genuine gap -- the task's "Files to Modify" section lists `get.rs` with "add `include_deleted` parameter support", and the PR diff does not include changes to `get.rs`. However, the reviewer's comment is phrased as a question, not as a request to fix this. The scope containment check in the Intent Alignment analysis captures the missing `get.rs` modification separately.

**Conclusion**: This asks for clarification; no code change is requested. No sub-task created.
