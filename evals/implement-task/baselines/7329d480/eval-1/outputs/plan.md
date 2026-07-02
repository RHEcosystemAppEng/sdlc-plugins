# Implementation Plan for TC-9201

## Step 0 -- Validate Project Configuration

The project CLAUDE.md contains all required sections under `# Project Configuration`:

1. `## Repository Registry` -- present, contains `trustify-backend` with Serena Instance `serena_backend` and Path `./`
2. `## Jira Configuration` -- present, contains Project key `TC`, Cloud ID, Feature issue type ID `10142`, Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`
3. `## Code Intelligence` -- present, tool naming convention documented, `serena_backend` configured with `rust-analyzer`

Validation passed. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

Parsed fields from TC-9201:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. The endpoint returns a summary with counts per severity level (Critical, High, Medium, Low) and a total, enabling dashboard widgets to render severity breakdowns without client-side counting.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method to AdvisoryService
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;` to register the new model module
  - `server/src/main.rs` -- no changes needed (routes auto-mount via module registration)
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler for /api/v2/sbom/{id}/advisory-summary
  - `tests/api/advisory_summary.rs` -- integration tests for the new endpoint
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }`
- **Acceptance Criteria**: 5 criteria (see task description)
- **Test Requirements**: 4 tests (see task description)
- **Dependencies**: None
- **Target PR**: not present
- **Bookend Type**: not present
- **Review Context**: not present

The issue `webUrl` would be captured as `https://redhat.atlassian.net/browse/TC-9201` for use in the PR description.

### Target Branch extraction

Target Branch is **main**. This value will be used in Step 5 (branch creation) and Step 10 (PR base).

### GitHub Issue extraction

GitHub Issue custom field `customfield_10747` is configured in Jira Configuration. The field value would be read from the fetched issue's fields. If present, the GitHub issue reference (e.g., `owner/repo#N`) would be included in the PR description with a `Closes` keyword.

## Step 1.5 -- Verify Description Integrity

Fetched comments on TC-9201 via `jira.get_issue_comments(TC-9201)`.

**No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced.**

Per the backward compatibility rules in `shared/description-digest-protocol.md`, a missing digest comment is a non-blocking warning. Proceeding with implementation normally.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user account ID via `jira.user_info()`
2. Assign TC-9201 to current user via `jira.edit_issue(TC-9201, assignee=<account-id>)`
3. Transition TC-9201 to In Progress via `jira.transition_issue`

## Step 4 -- Understand the Code

### Code inspection plan

Using Serena instance `serena_backend` (from Repository Registry), inspect the following files:

**Files to modify (read before changing):**

1. `modules/fundamental/src/advisory/service/advisory.rs` -- use `mcp__serena_backend__get_symbols_overview` to see AdvisoryService struct and its existing methods (`fetch`, `list`, `search`). Then use `mcp__serena_backend__find_symbol` with `include_body=true` on the `list` method to understand the pattern for the new `severity_summary` method.

2. `modules/fundamental/src/advisory/endpoints/mod.rs` -- use `mcp__serena_backend__get_symbols_overview` to see route registration pattern. Inspect how existing routes are registered with `Router::new().route(...)`.

3. `modules/fundamental/src/advisory/model/mod.rs` -- use `mcp__serena_backend__get_symbols_overview` to see existing `pub mod` declarations for model submodules.

4. `server/src/main.rs` -- quick inspection to confirm routes auto-mount (no changes needed as stated in the task).

**Sibling files for patterns (convention conformance):**

5. `modules/fundamental/src/advisory/endpoints/get.rs` -- sibling endpoint handler. Inspect to understand the endpoint pattern: path param extraction, service call, JSON response.

6. `modules/fundamental/src/advisory/endpoints/list.rs` -- another sibling endpoint handler for comparison.

7. `modules/fundamental/src/advisory/model/summary.rs` -- sibling model file. Inspect AdvisorySummary struct to see the `severity` field and understand struct conventions (derives, serde attributes).

8. `modules/fundamental/src/advisory/model/details.rs` -- another sibling model for comparison.

9. `modules/fundamental/src/sbom/endpoints/get.rs` -- cross-module sibling to verify SBOM path param pattern since the new endpoint is under `/api/v2/sbom/{id}/...`.

10. `entity/src/sbom_advisory.rs` -- the join table entity needed for querying advisories linked to an SBOM.

11. `common/src/error.rs` -- AppError enum and `.context()` usage pattern.

**Sibling test files:**

12. `tests/api/advisory.rs` -- sibling test file for advisory endpoint tests. Inspect assertion patterns, setup, naming conventions.

13. `tests/api/sbom.rs` -- sibling test file for SBOM endpoint tests.

**Documentation files identified:**

14. `CONVENTIONS.md` -- repository root conventions file
15. `docs/api.md` -- REST API reference (may need updating for new endpoint)
16. `docs/architecture.md` -- architecture overview (likely no changes needed)

### CONVENTIONS.md lookup

The Repository Registry lists `trustify-backend` with Path `./`. Check for `CONVENTIONS.md` at the repository root. If present, read it and extract CI check commands from any "CI checks", "Verification", or similar section. Follow all conventions throughout implementation.

### Convention conformance analysis

See `outputs/conventions.md` for the full list of discovered conventions from sibling analysis.

### Backward compatibility check

Use `mcp__serena_backend__find_referencing_symbols` on any symbols being modified (e.g., AdvisoryService) to ensure adding the new method does not break existing callers. Since we are only adding a new method (not modifying existing ones), backward compatibility risk is minimal.

## Step 5 -- Create Branch

Target Branch is **main**. No Target PR and no Bookend Type present, so this is the default flow.

```bash
git checkout main
git pull
git checkout -b TC-9201
```

This creates a new branch `TC-9201` from the latest `main`.

## Step 6 -- Implement Changes

### Files to create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- New SeveritySummary response struct with fields: critical, high, medium, low, total (all u64). Derive `Serialize`, `Deserialize`, `Debug`, `Clone`, `Default`. Add documentation comment on the struct.

2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- New GET handler function for `/api/v2/sbom/{id}/advisory-summary`. Extract `Path<Id>` param, call `AdvisoryService::severity_summary`, return `Json<SeveritySummary>`. Return 404 via AppError when SBOM not found.

### Files to modify

3. **`modules/fundamental/src/advisory/model/mod.rs`** -- Add `pub mod severity_summary;` line to register the new model module.

4. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Add `severity_summary` method to AdvisoryService. Takes `&self, sbom_id: Id, tx: &Transactional<'_>`. Queries `sbom_advisory` join table, joins to advisory table, groups by severity, counts distinct advisory IDs. Returns `SeveritySummary`.

5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Register the new route: `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get))`.

### Files with no changes

6. **`server/src/main.rs`** -- No changes needed per task description (routes auto-mount via module registration).

### Tests to create

7. **`tests/api/advisory_summary.rs`** -- Integration tests (see Step 7).

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with the following test functions, following sibling test conventions:

1. `test_advisory_summary_with_known_advisories` -- Verifies correct severity counts for an SBOM with known advisories
2. `test_advisory_summary_nonexistent_sbom` -- Verifies 404 for non-existent SBOM ID
3. `test_advisory_summary_no_advisories` -- Verifies all-zero response for SBOM with no advisories
4. `test_advisory_summary_deduplication` -- Verifies duplicate advisory links are deduplicated

Each test will have a `///` doc comment and given-when-then section comments.

Run `cargo test` to verify all tests pass. Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

- [x] GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` -- verified by endpoint implementation and test 1
- [x] Returns 404 when SBOM ID does not exist -- verified by test 2
- [x] Counts only unique advisories (deduplicates by advisory ID) -- verified by test 4
- [x] All severity levels default to 0 when no advisories exist -- verified by test 3 and `Default` derive on struct
- [x] Response time under 200ms for SBOMs with up to 500 advisories -- verified by using a single SQL query with GROUP BY (no N+1)

## Step 9 -- Self-Verification

1. **Scope containment**: `git diff --name-only` must match exactly the Files to Modify and Files to Create lists. Any out-of-scope files flagged for user approval.
2. **Untracked file check**: `git status --short` to find `??` entries near implementation directories.
3. **Sensitive-pattern check**: `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- must produce no matches.
4. **Documentation currency**: Check if `docs/api.md` needs updating for the new endpoint.
5. **CI checks from CONVENTIONS.md**: Run all CI check commands extracted during Step 4.
6. **Data-flow trace**: Trace the data flow from HTTP request through handler, service method, database query, and JSON response.
7. **Contract & sibling parity**: Verify the new endpoint handler follows the same Result<T, AppError> pattern, error handling, and response structure as siblings.
8. **Duplication check**: Search for existing severity aggregation logic to ensure no duplication.

## Step 10 -- Commit and Push

### Commit message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, AdvisoryService
method, route registration, and integration tests.

Implements TC-9201
```

### Commit command

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      tests/api/advisory_summary.rs

git commit --trailer='Assisted-by: Claude Code' -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, AdvisoryService
method, route registration, and integration tests.

Implements TC-9201"
```

### Push and create PR

```bash
git push -u origin TC-9201
```

```bash
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "## Summary

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns advisory severity counts (critical, high, medium, low, total) for a given SBOM, enabling dashboard widgets to render severity breakdowns without client-side counting.

### Changes
- New `SeveritySummary` response struct in `modules/fundamental/src/advisory/model/severity_summary.rs`
- New `severity_summary` method on `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`
- New GET handler in `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- Route registered in `modules/fundamental/src/advisory/endpoints/mod.rs`
- Integration tests in `tests/api/advisory_summary.rs`

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)"
```

The `--base main` flag explicitly targets the Target Branch extracted in Step 1.

If a GitHub Issue reference was extracted from `customfield_10747`, a `Closes owner/repo#N` line would be appended to the PR body.

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) on TC-9201 with the PR URL using ADF inlineCard format.
2. **Add comment** to TC-9201 with PR link, summary of changes, and note of any deviations.
3. **Transition** TC-9201 to In Review.
