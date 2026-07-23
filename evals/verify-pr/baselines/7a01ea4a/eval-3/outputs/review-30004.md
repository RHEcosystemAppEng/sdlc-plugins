# Review Comment Classification: 30004

## Comment
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Content:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: question

## Reasoning

The reviewer asks for clarification about the intended behavior of the GET-by-ID endpoint for soft-deleted SBOMs. The phrasing "Have you considered" and "Is that intentional?" are explicitly interrogative -- the reviewer is seeking clarification rather than directing a code change. The reviewer identifies a potential gap (get.rs does not filter by `deleted_at`) but frames it as a design question rather than a change request.

Notably, this question aligns with the Scope Containment finding: the task's "Files to Modify" section lists `modules/fundamental/src/sbom/endpoints/get.rs` with the note "add include_deleted parameter support," but `get.rs` has no changes in the PR diff. The scope containment check records this as a FAIL (unimplemented file). This gap is significant and is captured by the Scope Containment verdict rather than through review feedback sub-task creation.

## Action
No sub-task created. The underlying gap is captured by the Scope Containment FAIL verdict in the verification report.
