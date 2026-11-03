# Review Comment 30002 — Classification

- **Comment ID:** 30002
- **Review ID:** 20001
- **Author:** reviewer-a
- **File/Line:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14 (RIGHT)
- **Thread:** top-level (`in_reply_to_id: null`), no replies, no prior classification reply → **unclassified**, processed this run

## Comment text

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

## Classification: **suggestion** (not upgraded)

## Reasoning

### Initial classification (Step 4c)

- This is a performance optimization ("a partial index would help", "Something like:"). The reviewer proposes an extra improvement and does not point out a defect. The migration in the diff is correct as written: it adds a nullable `deleted_at` column to `sbom`, which satisfies Acceptance Criterion 8.
- The task (TC-9103) does not ask for an index in its Description, Implementation Notes, or Acceptance Criteria. Without the index, the feature still works.
- The comment contains the word "should", but its justification is speculative performance ("will be frequent ... would help"). It does not identify a functional problem, so it reads as a proposed alternative or enhancement rather than a required change.

### Convention upgrade check (Style/Conventions Check 1, with performance scrutiny per 1c)

- **CONVENTIONS.md:** the repository tree in `repo-backend.md` lists a `CONVENTIONS.md` at the repo root, but the fixture does not include its contents. No documented index convention could be cited. Applicability is therefore "no": there is no convention section to match against the PR's changed `.rs` migration file.
- **Codebase patterns:** the PR diff contains no `Index::create` (or similar index-creation) pattern in any migration file, so the count of the suggested pattern in similar files is 0. The repository structure shows a single prior migration (`m0001_initial`) and lists no retroactive index migrations or documented performance conventions.
- **Decision:** Step 1d says not to upgrade on the basis of general best practice ("indexes are a database best practice"). An upgrade needs a concrete CONVENTIONS.md section or a counted codebase pattern, and neither is present. The comment **stays a suggestion**.

## Action

- No sub-task created.
- Planned reply (not posted; eval mode):
  `[sdlc-workflow/verify-pr] Classified as **suggestion** — performance optimization beyond the task's scope; not documented in CONVENTIONS.md and no established codebase pattern (0 index-creation occurrences in migrations). No sub-task created.`
