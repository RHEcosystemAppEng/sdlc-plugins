# Review Comment 30002 — Classification

- **Comment ID:** 30002
- **Author:** reviewer-a
- **Review:** 20001 (CHANGES_REQUESTED)
- **File/Line:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14 (RIGHT)
- **Thread:** top-level (no `in_reply_to_id`), no replies
- **Prior classification reply:** none, so the comment is unclassified and goes through classification

## Original comment

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

## Initial classification (Step 4c): **suggestion**

## Reasoning

- **The language is suggestive, not directive.** The reviewer proposes an extra improvement ("should **also** add an index"). The justification is a likely benefit, not a defect: "a partial index **would help**". The example is offered loosely ("**Something like:**"). Nothing in the comment says the current code is wrong.
- **There is no correctness impact.** Without the index, the migration and every acceptance criterion still work as specified. Criterion 8 ("Migration adds `deleted_at` column with NULL default to `sbom` table") is met. The comment is a performance improvement proposal, and the task specification does not require an index.
- **It proposes an alternative, optional approach.** That fits the skill's definition of a **suggestion**: "the reviewer proposes an alternative approach but does not require it".

## Convention upgrade check (Style/Conventions sub-agent, Check 1)

The comment is a suggestion, so it was checked for a possible upgrade to code change request. It did **not** qualify.

- **1a CONVENTIONS.md:** The fixture does not include the repository's CONVENTIONS.md content. The documented conventions available (the "Key Conventions" in `repo-backend.md`) cover:
  - framework
  - module pattern
  - error handling with `.context()`
  - endpoint registration
  - `PaginatedResults<T>`
  - shared query helpers
  - integration test patterns
  - `tower-http` caching

  None of them mention database indexes, partial indexes or index creation in migrations. Since no convention matched, there was no convention to run the file-type applicability check against.
- **1b Codebase patterns:** The PR diff and the repo structure contain **0** occurrences of `Index::create`, `create_index` or `CREATE INDEX`. The only other migration in the tree is `m0001_initial`, and nothing shows a pattern of adding indexes alongside new filter columns. No consistent usage is demonstrated.
- **1c Performance scrutiny:** This is a performance suggestion, so it got extra scrutiny. The only performance-related convention is HTTP caching middleware (`tower-http`), which has nothing to do with database indexing. There are no dedicated index migrations and no documented indexing guidance.
- **1d Decision:** **Not upgraded.** The only case for the index is general database best practice. The skill says that is insufficient: "general knowledge (e.g., 'indexes are a database best practice') is not sufficient."

## Final classification: **suggestion** (not upgraded)

## Outcome

- **Sub-task created:** no
- **Reply that would be posted to the thread** (eval mode, so not posted):

  ```
  gh api repos/trustify/trustify-backend/pulls/744/comments/30002/replies -f body="[sdlc-workflow/verify-pr] Classified as **suggestion** — proposes an optional performance improvement (a partial index on deleted_at) using suggestive language ('should also', 'would help', 'Something like'); not documented in CONVENTIONS.md and no established codebase pattern of index creation in migrations (0 occurrences found), so it was not upgraded to a code change request. No sub-task created."
  ```
