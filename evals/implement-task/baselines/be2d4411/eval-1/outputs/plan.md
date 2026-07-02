# Implementation Plan for TC-9201

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Status**: To Do
**Parent**: is incorporated by TC-9001

## Step-by-Step Execution

### Step 0 -- Validate Project Configuration

Verified CLAUDE.md contains all required sections:
1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key (TC), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present, tool naming convention documented (`mcp__<serena-instance>__<tool>`), Serena instance `serena_backend` with `rust-analyzer`

All sections valid. Proceeding.

### Step 1 -- Fetch and Parse Jira Task

Parsed structured description sections:
- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM
- **Files to Modify**: 3 files (advisory service, endpoints mod, model mod)
- **Files to Create**: 3 files (severity_summary model, severity_summary endpoint, integration tests)
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes**: Present with detailed patterns
- **Acceptance Criteria**: 5 criteria
- **Test Requirements**: 4 test cases
- **Target PR**: Not present (default flow)
- **Bookend Type**: Not present (default flow)
- **Dependencies**: None
- **GitHub Issue custom field**: `customfield_10747` configured in Jira Configuration; would check the field value on the fetched issue. Not available in this eval context -- skipped.

### Step 1.5 -- Verify Description Integrity

No digest comment was found -- skipping integrity check. This task may have been created before digest tracking was introduced.

> Warning: No description digest found -- skipping integrity check (backward compatibility).

### Step 2 -- Verify Dependencies

Task has no dependencies. Proceeding.

### Step 3 -- Transition to In Progress and Assign

Would execute:
1. `jira.user_info()` to get current user account ID
2. `jira.edit_issue("TC-9201", assignee=<current-user-account-id>)` to assign
3. `jira.transition_issue("TC-9201")` to "In Progress"

### Step 4 -- Understand the Code

#### Serena Instance
Using `serena_backend` (from Repository Registry) for code intelligence. Tools called as `mcp__serena_backend__<tool>`.

#### Files to Inspect

**Files to Modify:**
1. `modules/fundamental/src/advisory/service/advisory.rs` -- Would use `mcp__serena_backend__get_symbols_overview` to see existing methods (`fetch`, `list`, `search`), then `mcp__serena_backend__find_symbol` with `include_body=true` on the `list` method to understand the pattern for the new `severity_summary` method.
2. `modules/fundamental/src/advisory/endpoints/mod.rs` -- Would inspect route registration patterns via `get_symbols_overview`.
3. `modules/fundamental/src/advisory/model/mod.rs` -- Would read to see existing module declarations (`pub mod summary;`, `pub mod details;`).

**Sibling files for convention analysis:**
- `modules/fundamental/src/advisory/endpoints/get.rs` -- GET handler pattern (Path extraction, service call, JSON response)
- `modules/fundamental/src/advisory/endpoints/list.rs` -- list handler pattern
- `modules/fundamental/src/advisory/model/summary.rs` -- AdvisorySummary struct (has `severity` field used for counting)
- `modules/fundamental/src/advisory/model/details.rs` -- AdvisoryDetails struct
- `modules/fundamental/src/sbom/endpoints/get.rs` -- sibling module GET handler for cross-module pattern comparison
- `modules/fundamental/src/sbom/service/sbom.rs` -- SbomService for cross-module service pattern comparison

**Entity files:**
- `entity/src/sbom_advisory.rs` -- join table linking SBOMs to advisories (needed for the query)
- `entity/src/advisory.rs` -- advisory entity

**Backward compatibility check:**
- Would use `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to identify all callers and ensure the new method does not break existing behavior (it is purely additive).

**Test sibling files:**
- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

#### CONVENTIONS.md Lookup
Would read `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). Would extract any CI check commands for use in Step 9. Since file contents are not available in this eval, no specific CI commands extracted.

#### Documentation Files Identified
- `docs/api.md` -- REST API reference, likely needs updating for the new endpoint
- `CONVENTIONS.md` -- project conventions
- `README.md` -- may reference API surface

#### Convention Conformance Analysis Results
See `outputs/conventions.md` for the full list of discovered conventions from sibling analysis.

### Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type). Would execute:

```
git checkout main
git pull
git checkout -b TC-9201
```

Branch name: `TC-9201`, based off target branch `main`.

### Step 6-7 -- Implementation and Tests

#### Files to Create (3 files)

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- SeveritySummary response struct
   - See `outputs/file-1-description.md`

2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- GET handler
   - See `outputs/file-2-description.md`

3. **`tests/api/advisory_summary.rs`** -- Integration tests
   - See `outputs/file-3-description.md`

#### Files to Modify (3 files)

4. **`modules/fundamental/src/advisory/model/mod.rs`** -- Register new model module
   - See `outputs/file-4-description.md`

5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Register new route
   - See `outputs/file-5-description.md`

6. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Add severity_summary method
   - See `outputs/file-6-description.md`

#### Documentation Impact
- `docs/api.md` would be checked for API documentation. If it documents existing endpoints, the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint would be added following the existing documentation pattern.

### Step 8 -- Verify Acceptance Criteria

1. **GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }`** -- Satisfied by the SeveritySummary struct and endpoint implementation.
2. **Returns 404 when SBOM ID does not exist** -- Satisfied by checking SBOM existence before querying advisories, returning AppError with NOT_FOUND.
3. **Counts only unique advisories (deduplicates by advisory ID)** -- Satisfied by using `.distinct()` or collecting into a HashSet keyed by advisory ID in the service method.
4. **All severity levels default to 0 when no advisories exist** -- Satisfied by initializing SeveritySummary with all fields at 0 and only incrementing on matches.
5. **Response time under 200ms for SBOMs with up to 500 advisories** -- Satisfied by performing aggregation in a single SQL query with GROUP BY on severity, avoiding N+1 queries.

### Step 9 -- Self-Verification

#### Scope Containment
Would run `git diff --name-only` and compare against the declared files:

**Files to Modify (expected):**
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`

**Files to Create (expected):**
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

If `docs/api.md` was modified, it would be flagged as out-of-scope and the user would be asked to approve (documentation updates are justified by the new endpoint).

#### Untracked File Check
Would run `git status --short` and check for `??` entries in directories containing modified files. The three new files would be in tracked directories -- would verify they are staged.

#### Sensitive-Pattern Check
Would run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- no sensitive patterns expected in this implementation.

#### Documentation Currency
`docs/api.md` describes REST API endpoints -- if the new endpoint was not already documented in Step 6, it would be updated here.

#### Data-Flow Trace
- `GET /api/v2/sbom/{id}/advisory-summary` -> extract `sbom_id` from path (input) -> call `AdvisoryService::severity_summary(sbom_id, tx)` (processing) -> query `sbom_advisory` join table, aggregate by severity (processing) -> return `SeveritySummary` as JSON (output) -- **COMPLETE**

#### Contract & Sibling Parity
- `SeveritySummary` is a new struct, no trait/interface to implement beyond `Serialize` (Serde) -- satisfied.
- Sibling parity with `get.rs` endpoint: Path extraction pattern matches, error handling with `.context()` matches, return type pattern matches.
- No cross-module shared entity concerns -- the query reads from `sbom_advisory` (read-only, no inserts/updates).

#### Duplication Check
Would search for existing severity aggregation logic -- no existing aggregation expected based on the codebase structure.

### Step 10 -- Commit and Push

#### Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes AdvisoryService.severity_summary
method, SeveritySummary response model, and integration tests.

Implements TC-9201
```

With trailer: `--trailer='Assisted-by: Claude Code'`

#### Push and PR

```
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "..."
```

PR description would include:
- Summary of changes
- `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)` (clickable Jira link)
- If GitHub Issue custom field had a value, would append `Closes <owner>/<repo>#<number>`

### Step 11 -- Update Jira

Would execute:
1. Update Git Pull Request custom field (`customfield_10875`) with PR URL in ADF format
2. Add Jira comment with PR link, summary of changes, and note of no deviations from plan
3. Transition issue to "In Review"
