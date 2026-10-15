# Review Comment Classification: 30004

## Comment Details

- **ID:** 30004
- **Author:** reviewer-a
- **File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
- **Body:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: QUESTION

## Reasoning

The reviewer asks a clarifying question about the design intent. Key indicators:

1. **"Have you considered"** -- this is an interrogative phrase that asks whether the author has thought about a scenario, not a directive to change code. It opens a discussion rather than demanding a fix.

2. **"Is that intentional?"** -- the comment ends with a direct question. The reviewer does not know whether the current behavior is a bug or a deliberate design choice. They are seeking clarification from the PR author before making any judgment.

3. **No imperative language** -- the comment contains no directives ("should," "must," "need to," "wrap," "add"). It describes an observation and asks for the author's perspective.

4. **Observation, not prescription** -- the reviewer observes that `get.rs` does not filter by `deleted_at`, then asks whether this is intentional. The task description says "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter," which implies `get.rs` should support `include_deleted`. However, the reviewer does not assert this -- they ask for clarification. The answer might be that direct GET intentionally returns deleted SBOMs (without requiring the parameter) as a design choice.

5. **Context awareness** -- notably, `get.rs` is listed in the task's Files to Modify but is absent from the PR diff. The reviewer's question highlights this gap, but framed as a question rather than a change request.

## Action

No sub-task created. Questions ask for clarification and do not require code changes. The PR author should respond to confirm whether the GET behavior for deleted SBOMs is intentional or an oversight.
