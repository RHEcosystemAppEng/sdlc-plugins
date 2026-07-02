# Implementation Plan for TC-9201

**Task**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Parent Feature**: TC-9001

---

## Step 1 -- Fetch and Parse Jira Task

Parsed the structured description from TC-9201. The following sections were extracted:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add the aggregation service method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new endpoint route
  - `modules/fundamental/src/advisory/model/mod.rs` -- register the new severity summary model module
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- severity summary response model
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- endpoint handler for severity aggregation
  - `tests/api/advisory_summary.rs` -- API integration tests
- **No Target PR** -- this is a standard implementation, not a review feedback fix.
- **No Bookend Type** -- this is a standard implementation task.

All required sections are present. No clarification needed.

## Step 1.5 -- Verify Description Integrity

Description digest verification completed successfully. The stored digest comment matches the current description digest (format tag `sha256-md`, identical hex hashes). The comment was not edited after posting (`created` and `updated` timestamps are identical). Proceeding silently without user prompt. (See `digest-match.md` for full details.)

## Step 2 -- Verify Dependencies

Check all tasks listed in the Dependencies section (if any). For each dependency, fetch its status via `jira.get_issue(<dependency-id>)` and verify the status is Done or equivalent. If no dependencies are listed, proceed immediately.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve the current user's Jira account ID via `jira.user_info()`.
2. Assign TC-9201 to the current user via `jira.edit_issue(TC-9201, assignee=<account-id>)`.
3. Transition TC-9201 to In Progress via `jira.transition_issue`.

## Step 4 -- Understand the Code

### 4a. Inspect files to modify

Inspect the following existing files using Serena (or Read/Grep/Glob as fallback) for the trustify-backend repository:

1. **`modules/fundamental/src/advisory/service/advisory.rs`**
   - Use `get_symbols_overview` to see the structure of the advisory service (existing methods, imports, types).
   - Use `find_symbol` on key service methods to understand patterns for querying advisories.
   - Identify how the service interacts with the database (connection handling, query patterns, result types).

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`**
   - Inspect how existing endpoints are registered (router configuration, path patterns).
   - Identify the endpoint handler signature pattern (request extractors, response types, error handling).
   - Note how sub-modules for endpoint handlers are declared and imported.

3. **`modules/fundamental/src/advisory/model/mod.rs`**
   - Inspect existing model module declarations to understand the pattern for registering new sub-modules.
   - Identify existing model types and their structure (derive macros, serde attributes, field patterns).

### 4b. Inspect file creation locations

For each file to create, inspect sibling files in the same directory:

1. **`modules/fundamental/src/advisory/model/`** -- inspect existing model files for struct patterns, derive macros, and serialization conventions.
2. **`modules/fundamental/src/advisory/endpoints/`** -- inspect existing endpoint handler files for handler function signatures, response wrapping, and error handling.
3. **`tests/api/`** -- inspect existing API test files for test setup patterns, assertion styles, and test organization.

### 4c. CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root of trustify-backend. If present, read it and extract:
- CI check commands for Step 9
- Code generation commands
- Naming, error handling, and testing conventions

### 4d. Convention conformance analysis

Analyze sibling files to discover implicit conventions:
- **Service methods**: naming pattern (e.g., `get_*`, `list_*`), return types, error handling
- **Endpoint handlers**: function signature pattern, response wrapping, path parameter extraction
- **Models**: derive macros, serde configuration, documentation style
- **Tests**: assertion patterns, test naming, setup/teardown patterns

### 4e. Test convention analysis

Inspect sibling test files in `tests/api/` to discover:
- Assertion style (e.g., status code checks, body deserialization patterns)
- Response validation patterns (field checks, count validation)
- Error case coverage patterns (404, 400, etc.)
- Test naming convention
- Parameterized test usage (if any)

### 4f. Documentation file identification

Identify documentation files related to the advisory module:
- README files in `modules/fundamental/` or parent directories
- API documentation or OpenAPI spec files
- Architecture docs describing the advisory module

## Step 5 -- Create Branch

Standard flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6a. Create severity summary model

**File**: `modules/fundamental/src/advisory/model/severity_summary.rs`

Create a new struct representing the severity aggregation response. Based on sibling model analysis, include:
- A response struct (e.g., `SeveritySummary`) with fields for each severity level count (critical, high, medium, low, none/unknown)
- Appropriate derive macros matching sibling models (e.g., `Serialize`, `Deserialize`, `Debug`, `Clone`, `utoipa::ToSchema`)
- Documentation comments on the struct and its fields

### 6b. Register model module

**File**: `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` declaration following the existing module registration pattern.

### 6c. Add service method

**File**: `modules/fundamental/src/advisory/service/advisory.rs`

Add a new method to the advisory service that:
- Accepts an SBOM identifier as input
- Queries the database for all advisories related to the given SBOM
- Aggregates severity counts across those advisories
- Returns a `SeveritySummary` struct
- Follows the error handling patterns of sibling service methods
- Includes a documentation comment explaining the method's purpose

### 6d. Create endpoint handler

**File**: `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create a new endpoint handler that:
- Extracts the SBOM identifier from the request path
- Calls the service method to get the severity aggregation
- Returns the result as a JSON response
- Follows the endpoint handler patterns from sibling endpoints (extractors, response wrapping, error handling)
- Includes OpenAPI annotations matching sibling endpoint patterns

### 6e. Register endpoint route

**File**: `modules/fundamental/src/advisory/endpoints/mod.rs`

- Add `pub mod severity_summary;` declaration
- Register the new route in the router configuration, following the existing route registration pattern

## Step 7 -- Write Tests

**File**: `tests/api/advisory_summary.rs`

Write API integration tests following the test conventions discovered in Step 4e:

1. **Test: successful severity aggregation** -- verify that the endpoint returns correct severity counts for an SBOM with known advisories. Add a doc comment explaining what this test verifies. Include given-when-then comments for test structure.

2. **Test: empty result for SBOM with no advisories** -- verify that the endpoint returns zero counts when the SBOM has no associated advisories. Add a doc comment.

3. **Test: 404 for non-existent SBOM** -- verify that the endpoint returns a 404 status code when the SBOM ID does not exist. Add a doc comment.

All tests must:
- Follow sibling test assertion patterns (value-based assertions, not just length checks)
- Include documentation comments
- Include given-when-then section comments for non-trivial tests
- Use parameterized tests only if sibling tests use them

Run tests to verify:
```bash
cargo test
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

Go through each acceptance criterion from the task description and verify it is satisfied by the implementation. Confirm:
- The service method correctly aggregates severity counts
- The endpoint returns the expected response format
- Error cases are handled (non-existent SBOM returns 404)
- Tests pass and cover the specified scenarios

## Step 9 -- Self-Verification

### Scope containment
Run `git diff --name-only` and compare against the files listed in the task description. Verify no out-of-scope files were modified.

### Untracked file check
Run `git status --short` and check for untracked files in directories where implementation work occurred. Flag any referenced-by-code untracked files.

### Sensitive-pattern check
Search the staged diff for secrets, credentials, or environment file patterns.

### Documentation currency
Check if any documentation files need updating based on the new endpoint.

### Data-flow trace
Trace the complete data flow:
- Input: HTTP request with SBOM ID hits the severity summary endpoint
- Processing: endpoint handler extracts SBOM ID, calls service method, service queries database and aggregates severity counts
- Output: JSON response with severity summary returned to client

Verify all stages are connected.

### Contract and sibling parity
- Verify the new endpoint handler implements all required patterns from sibling endpoints
- Verify the service method follows the same error handling, return type, and database interaction patterns as sibling service methods
- Check cross-cutting concerns: logging, error wrapping, configuration

### Duplication check
Search for existing severity aggregation logic in the codebase to ensure no duplication.

### CI checks
Run any CI check commands extracted from CONVENTIONS.md. Hard stop on any failure.

## Step 10 -- Commit and Push

Commit following Conventional Commits:

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation service and endpoint

Add a service method that aggregates vulnerability advisory severity
counts for a given SBOM, along with a REST endpoint to expose this
aggregation. Includes API integration tests for success, empty, and
not-found scenarios.

Implements TC-9201"
```

Push and open a PR:

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation service and endpoint" --body "## Summary
- Add SeveritySummary model for severity count aggregation response
- Add service method to aggregate advisory severity counts per SBOM
- Add REST endpoint for severity summary retrieval
- Add API integration tests for success, empty, and 404 scenarios

## Jira
Implements [TC-9201](https://<jira-host>/browse/TC-9201)"
```

## Step 11 -- Update Jira

1. Update the Git Pull Request custom field (`customfield_10875`) on TC-9201 with the PR URL in ADF format.
2. Add a comment to TC-9201 with:
   - PR link
   - Summary of changes made (new model, service method, endpoint, and tests)
   - Confirmation that all acceptance criteria were met
   - The standard sdlc-workflow/implement-task footer
3. Transition TC-9201 to In Review.
