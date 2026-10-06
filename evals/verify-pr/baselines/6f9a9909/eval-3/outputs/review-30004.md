# Review Comment 30004 — Classification

## Comment

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` — so direct GET still returns deleted SBOMs. Is that intentional?

**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1

## Classification

**question**

## Reasoning

The reviewer asks two explicit questions: "Have you considered..." and "Is that intentional?" The comment does not request a change or suggest a specific fix. Instead, it seeks clarification about a design decision — whether the direct GET endpoint should also filter by `deleted_at` or whether returning soft-deleted SBOMs via direct access is intentional behavior.

Notably, the task description itself specifies that the SBOM "remains accessible via direct GET with a `?include_deleted=true` parameter," which implies `get.rs` should support the parameter. However, the reviewer is asking about the current behavior rather than directing a change. The comment is exploratory and informational in nature. Questions do not trigger sub-task creation.
