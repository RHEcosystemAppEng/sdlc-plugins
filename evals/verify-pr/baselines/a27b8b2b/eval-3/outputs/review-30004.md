# Review Comment 30004 — Classification Reasoning

**Comment ID:** 30004
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/get.rs (line 1)
**Classification:** question

## Reviewer Language Analysis

The reviewer uses interrogative language throughout:

- "Have you considered what happens when...?" — asks whether the author has thought about a scenario
- "Is that intentional?" — explicitly requests clarification of intent

No imperative or directive language is present. The reviewer does not instruct the author to make a change; they ask whether the current behavior is by design.

## Substance Analysis

The reviewer observes that `GET /api/v2/sbom/{id}` does not filter by `deleted_at`, meaning a direct GET on a soft-deleted SBOM will still return it even without `include_deleted=true`. The reviewer asks whether this is intentional.

This is a design clarification question. The task description states "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." The get.rs file is listed in Files to Modify, but the PR does not include changes to it. The reviewer is asking whether the omission is deliberate.

Note: The scope containment check separately flags get.rs as an unimplemented file from the task spec. The reviewer's question here is about design intent, not a code change directive.

## Classification Decision

**Question.** The reviewer asks for clarification about whether the current GET endpoint behavior for deleted SBOMs is intentional. The language is interrogative ("Have you considered?", "Is that intentional?") and requests information, not a code change.

## Action

No sub-task created.
