# Review Comment Classification: 30002

## Comment Details

- **ID:** 30002
- **Author:** reviewer-a
- **File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
- **Body:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:\n\n```sql\nCREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;\n```"

## Classification: SUGGESTION

## Reasoning

The reviewer's language uses suggestive, non-imperative phrasing. Key indicators:

1. **"should also"** -- the phrase "should also" is additive and suggestive. Unlike the bare imperative "should" (which demands), "should also" proposes an additional improvement beyond the current scope. It implies the current code is acceptable but could be enhanced.

2. **"would help"** -- "would help" is conditional and non-directive. It acknowledges a potential benefit without asserting a requirement. Compare this to comment 30001's "you'll have inconsistent state," which identifies a defect. Here, the reviewer says the index "would help" performance -- an optimization suggestion, not a correctness fix.

3. **"Something like:"** -- the phrase "something like" explicitly signals that the reviewer is offering one possible approach, not mandating a specific implementation. This hedging language is characteristic of suggestions.

4. **Performance optimization, not correctness** -- the comment proposes a performance improvement (indexing for query speed), not a correctness fix. The code works correctly without the index; it would simply be slower. This further supports classification as a suggestion rather than a required change.

## Convention Upgrade Eligibility

Per the Style/Conventions sub-agent's Check 1, suggestions are evaluated for convention upgrade when they match a documented project convention or a demonstrated codebase pattern.

- **CONVENTIONS.md check:** The repository structure (repo-backend.md) indicates a CONVENTIONS.md exists, but its content is not available in the fixture data. Without the actual CONVENTIONS.md content, no documented convention match can be established for index creation on nullable timestamp columns.

- **Codebase pattern check:** The PR diff does not contain other migration files that demonstrate a consistent pattern of adding indexes alongside new columns. The fixture data provides only the repository directory tree and the PR diff -- insufficient to count how many existing migrations create indexes for FK or filter columns.

- **Conclusion:** Without CONVENTIONS.md content documenting an index creation convention, and without codebase evidence of a consistent indexing pattern in migration files, there is no basis to upgrade this suggestion to a code change request. The suggestion remains classified as SUGGESTION.

## Action

No sub-task created. The suggestion is not backed by a documented project convention or a demonstrated codebase pattern.
