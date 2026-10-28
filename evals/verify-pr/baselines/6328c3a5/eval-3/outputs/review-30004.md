# Review Comment Classification: #30004

## Comment
"Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: QUESTION

## Reasoning
The reviewer asks two explicit questions: "Have you considered..." and "Is that intentional?" This is a request for clarification about a design decision, not a directive to change code. The reviewer observes that `get.rs` does not filter by `deleted_at` for direct GET requests, but frames this as an inquiry about intent rather than as a demand for a fix. Notably, the task description (TC-9103) specifies that "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter", which indicates that the current GET behavior may be intentionally lenient. The reviewer is seeking confirmation of the design intent. No sub-task is created because questions do not trigger code changes -- they require a human response from the PR author.
