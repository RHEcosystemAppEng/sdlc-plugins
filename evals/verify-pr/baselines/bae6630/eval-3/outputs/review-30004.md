## Review Comment Classification: #30004

**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Comment**: Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

### Classification: Question

**Reasoning**: The reviewer is asking for clarification, not requesting a change. The language is interrogative throughout: "Have you considered...?", "Is that intentional?" The reviewer observes a behavior (GET by ID returns soft-deleted SBOMs without requiring `include_deleted=true`) and asks whether this is by design. Notably, the task description explicitly states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." The task's `get.rs` modifications include adding `include_deleted` parameter support, and the current behavior of returning deleted SBOMs on direct GET without the flag may indeed be intentional as an intermediate state. The reviewer is seeking understanding, not demanding a change.

**Action**: No sub-task created.
