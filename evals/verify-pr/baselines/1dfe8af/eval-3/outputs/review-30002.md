# Review Comment 30002 — Classification

## Comment
> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

**File**: `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14

## Classification: Suggestion

### Reasoning

Although the comment uses the word "should", it appears in the phrase "should also add" which is exploratory/additive rather than directive. The key linguistic signals are:

- **"should also"** — the word "also" signals an additive idea beyond the core requirement, not a correction of existing behavior. This is a common pattern for suggestions rather than demands.
- **"would help"** — explicitly suggestive language. The reviewer says the index "would help" performance, not that it is required or that the code is broken without it.
- **"Something like:"** — the reviewer presents a possible implementation as an example, not a prescribed fix. This phrasing indicates the reviewer is floating an idea.

The comment does not identify a correctness bug or a violation of existing behavior. It proposes a performance optimization (adding a partial index) that may or may not be necessary depending on table size and query patterns.

### Convention Upgrade Eligibility

For a suggestion to be upgraded to a code change request, there must be a documented or demonstrated project convention that supports the upgrade. Evaluating this:

- The repository's `CONVENTIONS.md` and `Key Conventions` section in the repo structure doc do not mention any convention requiring indexes on soft-delete columns or nullable filter columns.
- There is no demonstrated pattern in the existing migration (`m0001_initial`) that shows indexes being added alongside new columns.
- No other migration files are visible in the repository structure that would establish a convention of adding indexes for filter columns.

Since no documented or demonstrated project convention backs an upgrade from suggestion to code change request, this comment remains classified as a **suggestion**.

### Action
No sub-task is created. The suggestion may be worth considering in a follow-up optimization pass, but it is not a required change for this PR.
