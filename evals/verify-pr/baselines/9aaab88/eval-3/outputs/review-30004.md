# Review Comment Classification: 30004

**Comment ID:** 30004
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/get.rs, line 1
**Classification:** question

## Reasoning

The reviewer asks two explicit questions: "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`?" and "Is that intentional?" The language is interrogative throughout, seeking clarification about design intent rather than requesting a code change.

This is a **question** because:
- Both sentences are phrased as questions ("Have you considered...?", "Is that intentional?")
- The reviewer is asking whether the current behavior (GET returning deleted SBOMs without the include_deleted parameter) is by design
- The reviewer observes behavior but does not prescribe a fix or suggest a change
- Looking at the task description, it explicitly states "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter" -- the task description actually specifies `include_deleted=true` support for GET, suggesting the reviewer's observation about missing filter in get.rs may surface a gap, but the reviewer's language frames this as a question, not a directive

No sub-task created.
