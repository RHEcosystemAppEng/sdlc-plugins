# Review Comment 30002 — Classification

- **Author:** reviewer-a
- **Review:** 20001 (CHANGES_REQUESTED)
- **Location:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14 (RIGHT)
- **Thread:** top-level comment with no replies. No earlier classification reply exists, so the comment is **unclassified**.

## Comment

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
> `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`

## Classification: **Suggestion**. Checked for a convention upgrade and **not upgraded**.

## Reasoning

- **What the reviewer proposes is an optional optimization.** The justification is speculative performance ("will be frequent", "a partial index would help"). The SQL is offered loosely ("Something like:"). No functional defect is identified. Without the index, the soft-delete feature still behaves correctly.
- **The task does not require it.** TC-9103's acceptance criteria only ask the migration to add a nullable `deleted_at` column to `sbom`, and the PR does that. Nothing in the Description, Implementation Notes or Acceptance Criteria mentions indexes.
- **The convention-upgrade check found no backing.** The Style/Conventions sub-agent ran Check 1 with the extra scrutiny that performance suggestions get:
  - **CONVENTIONS.md (1a):** its content was not supplied. The documented "Key Conventions" for trustify-backend (in `repo-backend.md`) cover framework, module layout, error handling, routing, pagination, query helpers, testing and caching. None of them is about indexes.
  - **Codebase patterns (1b):** the PR contains 0 instances of `Index::create`, `CREATE INDEX` or partial-index creation. No index pattern can be counted in the code available.
  - **Performance scrutiny (1c):** there are no index migrations and no documented convention for indexes or query optimization.
  - **Decision (1d):** the only support for adding the index is general database best practice. The upgrade rule explicitly says that is not enough. The comment stays a suggestion.

## Outcome

- **Sub-task created:** no.
- **Planned reply (not posted):**
  `[sdlc-workflow/verify-pr] Classified as **suggestion** — proposes an optional performance optimization (partial index on sbom.deleted_at) that is not required by TC-9103's acceptance criteria; not documented in CONVENTIONS.md and no established index-creation pattern in the codebase. No sub-task created.`
