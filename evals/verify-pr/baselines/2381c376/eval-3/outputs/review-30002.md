# Review Comment Classification: 30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Body:**
> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

## Classification: Suggestion

## Reasoning

The reviewer uses suggestive language rather than imperative directives:

1. **"should also"** -- the phrase "should also" indicates an additive recommendation, not a required fix. Compare with comment 30001's "should run...inside a single database transaction" which addresses a correctness bug; here "should also add an index" proposes a performance optimization that is not required for correctness.
2. **"would help"** -- "a partial index would help" is conditional and suggestive, indicating the reviewer believes this is beneficial but is not requiring it. The word "would" signals a recommendation, not a demand.
3. **"Something like:"** -- presenting the SQL example with "something like" further reinforces that this is a proposed approach, not a prescribed fix.

The reviewer proposes an alternative (adding an index for query performance) but does not require it. The absence of an index does not cause a functional defect -- it is a performance consideration. The language patterns ("should also", "would help", "something like") consistently indicate suggestion rather than requirement.

## Convention Upgrade Eligibility

The suggestion was evaluated for convention upgrade per the Style/Conventions Check 1 (Convention Upgrade) process:

### Step 1a -- Check CONVENTIONS.md

The fixture data includes a repository structure (repo-backend.md) that lists `CONVENTIONS.md` at the repository root. However, the content of CONVENTIONS.md is not provided in the fixture data. Without access to the actual CONVENTIONS.md content, we cannot verify whether the project documents index creation conventions for migration files.

**Result:** No CONVENTIONS.md content available to match against. Cannot verify a documented convention.

### Step 1b -- Check Codebase Patterns

The PR diff and fixture data do not include other migration files that would demonstrate a consistent codebase pattern of adding indexes on foreign key or filter columns. Only the single migration file `m0042_sbom_soft_delete/mod.rs` is visible in the diff. Without access to other migration files (e.g., `m0001_initial/mod.rs` or others), we cannot count occurrences of `Index::create` or similar patterns to establish a demonstrated convention.

**Result:** No codebase patterns verifiable from fixture data.

### Step 1c -- Performance-Related Scrutiny

This is a performance-related suggestion (index for query optimization). Extra scrutiny applies, but no performance-related conventions or patterns are documented or demonstrable from the available fixture data.

### Step 1d -- Upgrade Decision

The suggestion does NOT qualify for upgrade because:
- No CONVENTIONS.md content is available to verify a documented convention
- No codebase patterns can be counted from the fixture data to demonstrate established practice
- General database best practices ("indexes help queries") are insufficient for upgrade -- the evidence must cite a concrete CONVENTIONS.md section or a counted codebase pattern

**Result:** Suggestion remains classified as **suggestion**. No sub-task created.
