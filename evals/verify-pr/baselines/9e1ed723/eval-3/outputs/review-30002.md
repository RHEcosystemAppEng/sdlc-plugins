# Review Comment 30002 — Classification

- **Comment ID:** 30002
- **Author:** reviewer-a
- **Review:** 20001 (CHANGES_REQUESTED)
- **File/Line:** `migration/src/m0042_sbom_soft_delete/mod.rs:14`
- **Thread:** top-level (`in_reply_to_id: null`), no replies. No existing classification reply, so it is **unclassified**.

## Comment text

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

## Initial classification (Step 4c): **suggestion**

## Reasoning

- The comment proposes a performance improvement, not a fix for a defect. The reviewer justifies it with "a partial index **would help**" and offers the SQL as "Something like". That is an optional alternative, not a requirement.
- Nothing in TC-9103 calls for an index. The acceptance criterion only requires "Migration adds `deleted_at` column with NULL default to `sbom` table", and the PR does that. Without the index the PR is still correct. The only effect is on query performance as the table grows.
- The comment uses "should", but the only reason given is expected performance, so it reads as a recommendation.

## Convention upgrade check (Style/Conventions sub-agent, Check 1): **not upgraded**

The index is a performance suggestion, so it got the extra scrutiny that Check 1c requires.

- **1a CONVENTIONS.md:** the repository has a `CONVENTIONS.md`, but its content was not supplied in the fixture data, so no documented convention could be matched. The documented Key Conventions in `repo-backend.md` cover framework, module pattern, error handling, endpoint registration, response types, query helpers, testing and caching. None of them mention indexes, migrations or soft-delete columns.
- **1b Codebase patterns:** the PR diff has 0 occurrences of `Index::create`, `create_index` or `CREATE INDEX`. There is no counted pattern of index creation in migrations.
- **1c Performance scrutiny:** the diff has no retroactive index migrations or documented index conventions. The only performance convention is `tower-http` HTTP caching, which is unrelated to DB indexing.
- **1d Decision:** the only basis for an upgrade would be general database best practice, and the skill forbids upgrading on that basis. The comment **stays a suggestion**.

## Final classification: **suggestion**

## Outcome

- **Sub-task:** none.
- **Planned reply (not posted, fixture eval):**
  `[sdlc-workflow/verify-pr] Classified as **suggestion** — proposes a performance optimization (partial index on deleted_at) that the task's acceptance criteria do not require; not documented in the available project conventions and no established index-creation pattern found in the codebase/diff (0 occurrences). No sub-task created.`
