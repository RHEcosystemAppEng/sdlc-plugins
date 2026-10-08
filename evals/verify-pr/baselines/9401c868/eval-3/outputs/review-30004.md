## Review Comment 30004 — Classification

**Reviewer:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Comment:** Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

### Classification: Question

**Reasoning:** The reviewer asks two explicit questions: "Have you considered..." and "Is that intentional?" There is no directive or suggestive language requesting a code change. The reviewer is seeking clarification about the design intent -- whether it is deliberate that the GET-by-id endpoint does not filter out soft-deleted SBOMs. This aligns with the task description, which states "The SBOM ... remains accessible via direct GET with a `?include_deleted=true` parameter," so the current behavior may indeed be intentional per the task spec.

**Action:** No sub-task created.
