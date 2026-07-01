# Review Comment Classification: 30004

**Comment ID:** 30004
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/get.rs
**Line:** 1

## Comment Text

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: question

## Reasoning

The reviewer asks two direct questions: "Have you considered..." and "Is that intentional?" The reviewer is seeking clarification about whether the current behavior of the GET endpoint (returning soft-deleted SBOMs without requiring `include_deleted=true`) is by design. The task description states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." This suggests the GET endpoint should support the parameter, but the reviewer is asking whether it's intentional that GET returns deleted SBOMs even without the parameter. The reviewer does not request a specific code change -- they are asking the author to clarify intent. No code change is requested.

## Action

No sub-task created. This is a question asking for clarification about design intent; no code change is requested.
