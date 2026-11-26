# Review Comment 30002 — Classification

- **Author:** reviewer-a
- **Review:** 20001 (CHANGES_REQUESTED)
- **File/Line:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14 (RIGHT)
- **Prior classification reply:** none (unclassified, processed this run)

## Comment

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
> `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`

## Initial classification (Step 4c): **suggestion**

The reviewer proposes a performance improvement: "a partial index would help", "Something like ...". It is not needed for correctness. No acceptance criterion asks for an index, and the feature works without one. The justification is a general performance argument, not a defect.

## Convention upgrade check (Style/Conventions Check 1): **not upgraded**

- **1a CONVENTIONS.md:** `trustify-backend/CONVENTIONS.md` exists in the repository tree, but its content is not in the supplied fixtures. The documented Key Conventions in `repo-backend.md` cover the framework (Axum/SeaORM), the module layout, `.context()` error handling, endpoint registration, `PaginatedResults<T>`, shared query helpers, test assertion style and caching middleware. None of them covers index creation or soft-delete indexing. No matching convention, so there is no file-type applicability to evaluate.
- **1b Codebase patterns:** the only other migration is `migration/src/m0001_initial/mod.rs`. The PR diff and the repository fixture show no `Index::create` usage, no partial indexes and no retroactive index migrations. Counted occurrences of the pattern: 0.
- **1c Performance scrutiny:** this is a performance suggestion, so it gets extra scrutiny. No dedicated performance convention or index pattern is shown in the project. General database best practice ("indexes help frequent filters") is explicitly not enough to upgrade.
- **1d Decision:** the suggestion stays a **suggestion**.

## Outcome

- No sub-task created.
- Reply that would be posted (not posted, eval mode):
  `[sdlc-workflow/verify-pr] Classified as **suggestion** — performance improvement not documented in CONVENTIONS.md and no established codebase pattern (0 index-creation occurrences in migrations); not required by the task's acceptance criteria. No sub-task created.`
