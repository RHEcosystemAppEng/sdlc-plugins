# Review Comment 30004 — Classification

## Comment
> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

**File**: `modules/fundamental/src/sbom/endpoints/get.rs`, line 1

## Classification: Question

### Reasoning

The comment is framed entirely as questions, not directives:

- **"Have you considered..."** — an open-ended question asking the author to reflect on a design decision.
- **"Is that intentional?"** — explicitly asks for clarification about whether the current behavior is by design or an oversight.

The reviewer is not requesting a change. They are pointing out a potential inconsistency (GET by ID returns soft-deleted SBOMs without requiring `include_deleted=true`) and asking the author to confirm whether this is the intended behavior.

Notably, the task description states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." The current implementation does allow GET by ID to return deleted SBOMs (since `get.rs` has no `deleted_at` filter), which may or may not align with the intended design. But the reviewer is asking, not telling.

### Action
No sub-task is created. Questions do not trigger sub-task creation. The author should respond to the reviewer's question on the PR.
