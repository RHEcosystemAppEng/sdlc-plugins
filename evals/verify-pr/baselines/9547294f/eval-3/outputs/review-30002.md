# Review Comment Classification: 30002

## Comment

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**PR:** #744

## Classification: Suggestion

## Reasoning

The reviewer uses suggestive, advisory language rather than imperative directives:

- "should also add" -- while "should" can sometimes indicate a requirement, the combination with "also" positions this as an additional improvement beyond the core requirement, not a mandatory change
- "would help" -- explicitly conditional/suggestive phrasing, indicating the reviewer considers this beneficial but not strictly required
- "Something like:" -- offers an example implementation as a starting point, not a prescribed fix

The comment proposes adding a partial index on `deleted_at` for performance optimization. The reviewer frames this as a helpful addition ("would help") rather than identifying a bug or correctness issue. The tone is advisory: the reviewer is sharing a performance optimization idea, not flagging a defect that must be corrected.

This is classified as a **suggestion** because:
1. The language is suggestive ("should also", "would help", "something like")
2. No correctness defect is identified -- the code works without the index
3. The improvement is performance-related and optional

## Convention Upgrade Eligibility Analysis

Per Step 4c and the Style/Conventions sub-agent's Check 1 (Convention Upgrade), suggestions may be upgraded to code change requests if they match a documented or demonstrated project convention.

**CONVENTIONS.md check:** The repository contains a `CONVENTIONS.md` file (per `repo-backend.md`). However, the fixture data does not provide the contents of `CONVENTIONS.md`. Without access to the actual CONVENTIONS.md content, we cannot verify whether it documents an index creation pattern for migration files. The "Key Conventions" section in the repository structure file describes general patterns (Axum, SeaORM, module structure, error handling, etc.) but does not mention index creation conventions for migrations.

**Codebase pattern check:** The PR diff contains only one migration file (`m0042_sbom_soft_delete/mod.rs`), and the repository structure shows only one other migration (`m0001_initial/mod.rs`). There is no evidence in the fixture data of a widespread codebase pattern of adding indexes in migration files. We cannot count occurrences of `Index::create` or similar patterns across migration files because we only have the repository structure, not the actual file contents.

**Upgrade decision: NOT UPGRADED.** The suggestion does not qualify for upgrade because:
1. No CONVENTIONS.md content is available to verify a documented index convention
2. No codebase pattern evidence exists in the fixture data to demonstrate consistent index creation in migrations
3. General database best practices ("indexes improve query performance") are explicitly excluded as upgrade evidence per the Style/Conventions sub-agent rules ("Do NOT upgrade based on general industry best practices")

The suggestion remains classified as **suggestion**. No sub-task is created.

## Action

No sub-task created. This is a suggestion without convention backing.
