# Implementation Plan for TC-9201

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Branch Name**: TC-9201
**Status**: To Do
**Parent Feature**: TC-9001 (is incorporated by)
**Dependencies**: None

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains the required Project Configuration sections:
1. **Repository Registry** -- present, contains `trustify-backend` with Serena Instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key (TC), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` using `rust-analyzer`

All sections present and valid. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Parse the structured description from TC-9201:

- **Repository**: trustify-backend
- **Target Branch**: main (extracted; will be used as `--base` for PR creation)
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns summary with counts per severity level (Critical, High, Medium, Low) and total.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
  - `server/src/main.rs` -- no changes needed
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes**: Follow existing endpoint pattern, use `sbom_advisory` join table, reuse `AdvisorySummary.severity` field, return `AppError` with `.context()`
- **Acceptance Criteria**: 5 criteria (correct response shape, 404 for missing SBOM, deduplication, zero defaults, performance)
- **Test Requirements**: 4 test cases
- **Target PR**: not present (default flow)
- **Bookend Type**: not present (default flow)
- **Review Context**: not present
- **GitHub Issue custom field**: customfield_10747 -- would check the Jira issue's fields for a GitHub issue URL. If present, parse owner/repo/number for PR description `Closes` line. If absent, skip silently.
- **webUrl**: would be captured from Jira API response (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in PR description.

## Step 1.5 -- Verify Description Integrity

1. Fetch all comments on TC-9201 via `jira.get_issue_comments(TC-9201)`.
2. Search for comments starting with `[sdlc-workflow] Description digest:`.
3. **If no digest comment found**: log warning and proceed normally -- "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced." (backward compatibility)
4. **If digest comment found**: extract the tagged digest, compute current digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`, compare format tags and hex values. On mismatch, alert user and stop. On match, proceed silently.

## Step 2 -- Verify Dependencies

Task has no dependencies. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Get current user via `jira.user_info()`
2. Assign TC-9201 to current user via `jira.edit_issue(TC-9201, assignee=<accountId>)`
3. Transition TC-9201 to In Progress via `jira.transition_issue`

## Step 4 -- Understand the Code

### Files to inspect (using Serena instance `serena_backend`)

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- use `mcp__serena_backend__get_symbols_overview` to see AdvisoryService structure, then `mcp__serena_backend__find_symbol` with `include_body=true` on `fetch` and `list` methods to understand the existing pattern for service methods (parameter types, return types, transaction handling).

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- use `get_symbols_overview` to see route registration pattern, then read the route definitions to understand how handlers are mounted.

3. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- use `find_symbol` with `include_body=true` on the handler function to understand the endpoint pattern: Path extraction, service call, JSON return, error handling.

4. **`modules/fundamental/src/advisory/model/mod.rs`** -- read to see how sub-modules are registered (e.g., `pub mod summary;`, `pub mod details;`).

5. **`modules/fundamental/src/advisory/model/summary.rs`** -- use `find_symbol` on `AdvisorySummary` to confirm the `severity` field exists and understand its type.

6. **`entity/src/sbom_advisory.rs`** -- use `get_symbols_overview` to understand the join table structure (columns, relations) for querying advisories linked to an SBOM.

7. **`common/src/error.rs`** -- use `find_symbol` on `AppError` to understand error enum variants and `.context()` usage pattern.

### Sibling analysis for convention conformance

**Endpoint siblings** (in `modules/fundamental/src/advisory/endpoints/`):
- Read `list.rs` and `get.rs` to identify patterns: handler function signature, Path/Query extractors, service method invocation, return type, error wrapping.

**Model siblings** (in `modules/fundamental/src/advisory/model/`):
- Read `summary.rs` and `details.rs` to identify patterns: derive macros, field types, serde attributes, documentation style.

**Service siblings** (in `modules/fundamental/src/advisory/service/`):
- Read the `fetch` and `list` methods in `advisory.rs` to identify patterns: method signature, `&self` + params + `tx: &Transactional<'_>`, return type `Result<T, AppError>`, query building, error context.

**Cross-module siblings** (in `modules/fundamental/src/sbom/`):
- Read `sbom/endpoints/get.rs` to compare endpoint patterns across modules and confirm consistency.

### Test sibling analysis

**Test siblings** (in `tests/api/`):
- Read `advisory.rs` and `sbom.rs` to identify patterns: test function naming, assertion style (`assert_eq!(resp.status(), StatusCode::OK)`), response deserialization, 404 test patterns, test setup/teardown, database seeding.

### CONVENTIONS.md lookup

- Check for `CONVENTIONS.md` at the repository root (path `./` from Repository Registry).
- If present, read it and extract: naming rules, directory structure conventions, code patterns, test conventions.
- Extract verification commands from CI checks section for use in Step 9.
- Extract code generation commands if any.

### Documentation file identification

- Check for `README.md` in `modules/fundamental/src/advisory/` and parent directories.
- Check `docs/api.md` and `docs/architecture.md` (referenced in CLAUDE.md) for API documentation that may need updating.

### Backward compatibility check

- Use `mcp__serena_backend__find_referencing_symbols` on any symbols being modified (e.g., if adding to AdvisoryService trait/impl) to confirm no callers are broken.

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9201
```

Target branch is `main` (extracted from Target Branch section in Step 1).

## Step 6 -- Implement Changes

### Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- new response struct
2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- new GET handler
3. **`tests/api/advisory_summary.rs`** -- integration tests (written in Step 7)

### Files to Modify

1. **`modules/fundamental/src/advisory/model/mod.rs`** -- add module registration
2. **`modules/fundamental/src/advisory/service/advisory.rs`** -- add service method
3. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- register route
4. **`server/src/main.rs`** -- no changes needed (routes auto-mount)

See `file-1-description.md` through `file-6-description.md` for detailed changes per file.

## Step 7 -- Write Tests

See `file-7-description.md` for detailed test implementation in `tests/api/advisory_summary.rs`.

Run tests: `cargo test`

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

1. GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- verified by response struct shape and test assertions.
2. Returns 404 when SBOM ID does not exist -- verified by service method checking SBOM existence and test for 404.
3. Counts only unique advisories (deduplicates by advisory ID) -- verified by using DISTINCT or HashSet in service method and deduplication test.
4. All severity levels default to 0 when no advisories exist -- verified by struct defaults and empty SBOM test.
5. Response time under 200ms for SBOMs with up to 500 advisories -- verified by efficient single SQL query with GROUP BY.

## Step 9 -- Self-Verification

### Scope containment
- Run `git diff --name-only` and compare against Files to Modify and Files to Create.
- Expected files: 6 files (3 created, 3 modified; `server/src/main.rs` has no changes).
- Flag any out-of-scope files for user approval.

### Untracked file check
- Run `git status --short` and check for `??` entries in directories where implementation occurred.
- Search for code references to any proximity-matched untracked files.

### Sensitive-pattern check
- Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`
- Flag any matches.

### Documentation currency
- Check `docs/api.md` for API documentation that should reference the new endpoint.
- Update if needed (new endpoint `GET /api/v2/sbom/{id}/advisory-summary`).

### CI checks from CONVENTIONS.md
- Run all verification commands extracted from CONVENTIONS.md in Step 4.
- Hard stop on any failure.

### Data-flow trace
- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param (Path<Id>) -> call `AdvisoryService::severity_summary(sbom_id, tx)` -> query `sbom_advisory` join table -> count by severity -> return `SeveritySummary` as JSON -- COMPLETE.

### Contract and sibling parity
- Verify `severity_summary` method follows the same signature pattern as `fetch` and `list` in AdvisoryService.
- Verify handler follows same pattern as `get.rs` and `list.rs`.
- Check cross-module entity usage of `sbom_advisory` table.

### Duplication check
- Search for existing severity aggregation logic in the codebase.
- Confirm no duplicate utility exists.

## Step 10 -- Commit and Push

### Commit message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total) for
advisories linked to a given SBOM. Includes SeveritySummary response
model, AdvisoryService.severity_summary() method, and integration tests.

Implements TC-9201
```

With trailer: `--trailer='Assisted-by: Claude Code'`

### Push and PR

```
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "..."
```

PR description would include:
- `Implements [TC-9201](<webUrl>)` with clickable Jira link
- Summary of changes
- If GitHub Issue custom field was populated: `Closes <owner>/<repo>#<number>`

## Step 11 -- Update Jira

1. Update Git Pull Request custom field (`customfield_10875`) on TC-9201 with PR URL in ADF format.
2. Add comment to TC-9201 with PR link, summary of changes, and any deviations.
3. Transition TC-9201 to In Review.
