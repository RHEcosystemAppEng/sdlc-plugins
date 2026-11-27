# Review Comment 30002 — Classification

- **Author:** reviewer-a
- **Review:** 20001 (CHANGES_REQUESTED)
- **File/Line:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14 (RIGHT)
- **Thread:** top-level, no replies, no prior classification reply → **unclassified**, processed this run

## Comment text

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
> `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`

## Initial classification (Step 4c): **Suggestion**

## Reasoning

- The comment is about performance ("a partial index would help"). It proposes an optimisation ("Something like: ...") rather than pointing out something broken. The task does not ask for an index: the Acceptance Criteria only require the migration to add a nullable `deleted_at` column, and the PR does that.
- Even with the column unindexed, the endpoint behaves correctly. The index only affects query cost.

## Convention upgrade check (Style/Conventions Check 1)

- **1a, CONVENTIONS.md:** `CONVENTIONS.md` is listed at the repository root in `repo-backend.md`, but its contents are not in the fixture data, so there is no documented index convention I can cite. The "Key Conventions" summary in `repo-backend.md` (Axum/SeaORM, module layout, `AppError` + `.context()`, `PaginatedResults<T>`, `common/src/db/query.rs` helpers, integration tests, `tower-http` caching) says nothing about index creation, partial indexes, or soft-delete indexing. Convention match: **none**. Applicability and file-type overlap are therefore moot.
- **1b, codebase patterns:** the PR diff has 0 occurrences of `Index::create` or any index creation in migration files. The only other migration in the tree is `m0001_initial`, and its contents are not supplied. Counted pattern: **0 occurrences**. No consistent usage is demonstrated.
- **1c, performance scrutiny:** this is a performance suggestion, so it gets extra scrutiny. Neither the diff nor the documented conventions show any dedicated performance pattern, such as retroactive index migrations or a documented indexing policy.
- **1d, decision:** **not upgraded.** "Indexes help queries that filter on `deleted_at IS NULL`" is general database best practice. The skill forbids upgrading on that basis without a concrete CONVENTIONS.md section or a counted codebase pattern.

## Final classification: **Suggestion** (no sub-task)

## Reply that would be posted (inline thread reply)

`[sdlc-workflow/verify-pr] Classified as **suggestion** — performance optimisation (partial index on deleted_at) proposed as an improvement; not documented in CONVENTIONS.md and no established index-creation pattern found in the codebase/diff, and not required by the task's acceptance criteria. No sub-task created.`
