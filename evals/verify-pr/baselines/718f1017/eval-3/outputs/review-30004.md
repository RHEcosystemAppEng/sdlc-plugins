# Review Comment Classification: 30004

**Comment ID:** 30004
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/get.rs
**Line:** 1
**Classification:** question

## Reasoning

The reviewer uses interrogative language: "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`?" and "Is that intentional?" These are questions asking for clarification about the design decision, not requests for code changes.

The reviewer observes that `get.rs` does not appear in the PR diff and therefore does not filter by `deleted_at`. This means direct GET requests for a soft-deleted SBOM would still return the SBOM data. The reviewer is asking whether this is the intended behavior.

Notably, this question aligns with the Scope Containment finding: the task specification lists `modules/fundamental/src/sbom/endpoints/get.rs` under Files to Modify with the note "add `include_deleted` parameter support," but the file is absent from the PR. This is a genuine gap in the PR, but the reviewer's comment is phrased as a question, not a code change request.

The scope gap itself is captured by the Intent Alignment sub-agent's Scope Containment check (FAIL verdict), so it is tracked independently of this comment's classification.

**Action:** No sub-task created. This is a clarification question. The underlying scope gap is tracked by the Scope Containment FAIL verdict.
