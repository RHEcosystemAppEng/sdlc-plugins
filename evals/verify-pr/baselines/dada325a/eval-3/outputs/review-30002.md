# Review Comment 30002 — Classification

- **Author:** reviewer-a
- **Review:** 20001 (CHANGES_REQUESTED)
- **File/Line:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14 (RIGHT)
- **Thread:** top-level (`in_reply_to_id: null`), no replies, no prior classification reply. Status: unclassified, so it is classified in this run.

## Comment text

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

## Initial classification: **Suggestion**

The comment opens with "should", but its justification is a performance improvement: "would help", "Something like". It does not point to a functional defect. The migration works as specified, and the acceptance criterion ("Migration adds `deleted_at` column with NULL default to `sbom` table") is met without an index. No acceptance criterion or implementation note in TC-9103 asks for an index. The comment proposes an optimization the task does not require, so it is a suggestion.

## Convention upgrade check (Style/Conventions Check 1)

- **1a, CONVENTIONS.md:** `repo-backend.md` lists `CONVENTIONS.md` at the repository root, but its content is not in the fixture data. The documented "Key Conventions" in `repo-backend.md` cover the framework (Axum/SeaORM), module layout, error handling, endpoint registration, response types, query helpers, testing, and caching. None of them mention index creation for migrations or for filter columns. No convention matches, so there is nothing to check for file-type applicability.
- **1b, codebase patterns:** The PR diff has 0 occurrences of `Index::create` or `create_index`. The repository structure shows only one other migration (`m0001_initial`), and nothing shows an index-on-filter-column pattern. Pattern count: 0.
- **1c, performance scrutiny:** This is a performance suggestion (indexes), so it gets extra scrutiny. There are no dedicated performance patterns: no retroactive index migrations and no documented index conventions. The only performance-related convention is `tower-http` caching middleware, which is unrelated.
- **1d, decision:** **Not upgraded.** Partial indexes for soft-delete columns are a general database best practice. The skill rules say general industry best practice is not enough evidence for an upgrade.

## Final classification: **Suggestion** (no sub-task)

## Outcome

- No sub-task created.
- Reply (would be posted to the thread):
  `[sdlc-workflow/verify-pr] Classified as **suggestion** — a partial index on deleted_at is a reasonable performance optimization, but it is not required by the task's acceptance criteria, not documented in CONVENTIONS.md, and not an established codebase pattern (0 index-creation occurrences found). No sub-task created.`
