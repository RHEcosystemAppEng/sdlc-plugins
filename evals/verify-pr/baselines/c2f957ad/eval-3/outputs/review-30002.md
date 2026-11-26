# Review Comment 30002 — Classification

- **Author:** reviewer-a
- **Review:** 20001 (CHANGES_REQUESTED)
- **File/line:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14 (RIGHT)
- **Thread:** top-level, no prior classification reply, so it is **unclassified**.

## Comment text

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`

## Initial classification: **suggestion**

## Reasoning

- The comment proposes a performance improvement ("would help"). It is not a functional defect. No acceptance criterion or Implementation Note in TC-9103 asks for an index. The migration as written meets "Migration adds `deleted_at` column with NULL default to `sbom` table".
- The word "should" appears, but the justification is a performance best practice, not a correctness gap. That makes it an optional alternative.

## Convention upgrade check (Style/Conventions Check 1)

- **1a — CONVENTIONS.md:** The repository structure lists `CONVENTIONS.md` at the root, but its content is not in the fixtures. The documented Key Conventions in `repo-backend.md` cover the Axum/SeaORM framework, the module pattern, error handling, endpoint registration, response types, query helpers, testing and caching. None covers index creation or partial indexes for soft-delete or filter columns. No convention matches.
- **1b — Codebase patterns:** The PR diff has 0 occurrences of `Index::create` or any index creation in migrations. The only other migration in the repo structure is `m0001_initial`, and no index pattern from it is shown. There is no counted codebase pattern.
- **1c — Performance scrutiny:** This is a performance suggestion (index), so it gets extra scrutiny. There are no retroactive index migrations, no documented performance conventions, and no index patterns in the supplied data.
- **1d — Decision:** **Not upgraded.** The only support is general database best practice ("indexes help frequent filters"). The skill explicitly forbids that as upgrade evidence.

## Final classification: **suggestion** (not upgraded)

## Outcome

- No sub-task created.
- Planned reply (not posted, eval mode):
  `[sdlc-workflow/verify-pr] Classified as **suggestion** — performance optimization not required by the task's acceptance criteria; not documented in CONVENTIONS.md and no established codebase pattern of index creation in migrations. No sub-task created.`
