# Implementation Plan for TC-9201

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Branch Name**: TC-9201
**Parent Feature**: TC-9001 (this task is incorporated by TC-9001)
**Labels**: ai-generated-jira

## Pre-Implementation Steps

### Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains:
- Repository Registry with trustify-backend entry (Serena instance: serena_backend, Path: ./)
- Jira Configuration with Project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence section with serena_backend instance using rust-analyzer

### Step 0.5 -- Jira Access Initialization

Attempt MCP-based Jira access. If MCP fails, prompt user for REST API fallback.

### Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue(TC-9201)`. Parse all structured sections:
- Repository: trustify-backend
- Target Branch: main
- Description: Add severity aggregation service and REST endpoint
- Files to Modify (3 files)
- Files to Create (3 files)
- API Changes: GET /api/v2/sbom/{id}/advisory-summary
- Implementation Notes: follow existing endpoint and service patterns
- Acceptance Criteria (5 items)
- Test Requirements (4 items)
- Dependencies: None
- No Target PR (this is a new implementation, not a review feedback fix)
- No Bookend Type (this is a standard implementation task)

Extract the issue's webUrl for use in PR description (e.g., `https://redhat.atlassian.net/browse/TC-9201`).

Check for GitHub Issue custom field (customfield_10747) -- extract if present, skip if empty.

### Step 1.5 -- Verify Description Integrity

1. Fetch comments on TC-9201 via `jira.get_issue_comments(TC-9201)`
2. Search for digest comment starting with `[sdlc-workflow] Description digest:`
3. If found: extract tagged digest, compute current digest via `python3 scripts/sha256-digest.py`, compare format tags and hex values
4. If no digest comment found: log warning and proceed (backward compatibility)
5. If mismatch: alert user and stop until they choose to proceed or re-run plan-feature

### Step 2 -- Verify Dependencies

Dependencies: None. Proceed without blocking.

### Step 3 -- Transition to In Progress and Assign

1. Get current user via `jira.user_info()`
2. Assign TC-9201 to current user via `jira.edit_issue(TC-9201, assignee=<account-id>)`
3. Transition TC-9201 to "In Progress" via `jira.transition_issue`

### Step 4 -- Understand the Code (Inspection Before Modification)

Use Serena instance `serena_backend` (from Repository Registry) for code intelligence.

#### 4a. Inspect files to modify

1. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` -- understand AdvisoryService structure, existing methods (fetch, list, search)
2. `mcp__serena_backend__find_symbol` with `include_body=true` on the `fetch` and `list` methods to understand patterns for the new `severity_summary` method
3. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern
4. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` -- understand module registration

#### 4b. Inspect reference files

1. Read `modules/fundamental/src/advisory/endpoints/get.rs` -- understand existing endpoint handler pattern (Path<Id> extraction, service call, JSON response)
2. Read `modules/fundamental/src/advisory/model/summary.rs` -- understand AdvisorySummary struct and its `severity` field
3. Read `entity/src/sbom_advisory.rs` -- understand the join table for SBOM-Advisory relationships
4. Read `common/src/error.rs` -- understand AppError enum and `.context()` wrapping pattern

#### 4c. Check backward compatibility

1. `mcp__serena_backend__find_referencing_symbols` on AdvisoryService to identify all callers
2. `mcp__serena_backend__find_referencing_symbols` on the advisory endpoints/mod.rs route registration

#### 4d. Convention conformance analysis (sibling analysis)

Inspect sibling files to discover implicit conventions:
- Compare `advisory/endpoints/get.rs` and `advisory/endpoints/list.rs` for endpoint patterns
- Compare `sbom/endpoints/get.rs` and `sbom/endpoints/list.rs` for cross-module endpoint patterns
- Compare `sbom/model/summary.rs` and `advisory/model/summary.rs` for model struct patterns
- Compare `sbom/service/sbom.rs` and `advisory/service/advisory.rs` for service method patterns

#### 4e. Test convention analysis

Inspect sibling test files:
- Read `tests/api/advisory.rs` -- understand advisory endpoint test patterns
- Read `tests/api/sbom.rs` -- understand SBOM endpoint test patterns
- Read `tests/api/search.rs` -- understand general API test patterns

#### 4f. CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at repository root (found in repo structure). Read it for:
- CI check commands (for Step 9 verification)
- Code generation commands
- Naming and structure conventions

#### 4g. Documentation file identification

Identify documentation files:
- `docs/api.md` -- REST API reference (may need updating with new endpoint)
- `docs/architecture.md` -- architecture overview
- `README.md` -- project readme

### Step 5 -- Create Branch

Standard flow (no Target PR, no Bookend Type):
```
git checkout main
git pull
git checkout -b TC-9201
```

### Step 6 -- Implement Changes

#### Files to Create

**File 1: `modules/fundamental/src/advisory/model/severity_summary.rs`**
- Create SeveritySummary response struct with fields: critical (u32), high (u32), medium (u32), low (u32), total (u32)
- Derive Serialize, Deserialize, Clone, Debug, Default
- Add doc comment explaining the struct purpose
- Follow patterns from sibling `summary.rs` and `details.rs`

**File 2: `modules/fundamental/src/advisory/endpoints/severity_summary.rs`**
- Create GET handler for `/api/v2/sbom/{id}/advisory-summary`
- Extract path params via `Path<Id>` (following `get.rs` pattern)
- Call `AdvisoryService::severity_summary` method
- Return `Json<SeveritySummary>` response
- Use `Result<T, AppError>` with `.context()` for error handling
- Add doc comment on handler function

**File 3: `tests/api/advisory_summary.rs`**
- Integration tests hitting real PostgreSQL test database
- Test functions with doc comments and given-when-then comments for non-trivial tests
- Follow `assert_eq!(resp.status(), StatusCode::OK)` pattern from siblings

#### Files to Modify

**File 4: `modules/fundamental/src/advisory/service/advisory.rs`**
- Add `severity_summary` method to AdvisoryService
- Method signature: `pub async fn severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>`
- Query `sbom_advisory` join table to find advisories linked to the SBOM
- Load AdvisorySummary for each linked advisory, extract severity field
- Count unique advisories by severity level (deduplicate by advisory ID)
- Return SeveritySummary struct with counts
- Handle 404 for non-existent SBOM IDs
- Add doc comment on new method

**File 5: `modules/fundamental/src/advisory/endpoints/mod.rs`**
- Add `pub mod severity_summary;` to register the new endpoint module
- Add route registration: `Router::new().route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::handler))` following existing pattern

**File 6: `modules/fundamental/src/advisory/model/mod.rs`**
- Add `pub mod severity_summary;` to register the new model module

### Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with four test functions:

1. `test_advisory_summary_valid_sbom` -- test valid SBOM with known advisories returns correct severity counts
2. `test_advisory_summary_nonexistent_sbom` -- test non-existent SBOM ID returns 404
3. `test_advisory_summary_empty_sbom` -- test SBOM with no advisories returns all zeros
4. `test_advisory_summary_deduplication` -- test duplicate advisory links are deduplicated

Each test function gets:
- A doc comment explaining what it verifies
- Given-when-then section comments (for non-trivial tests)
- Assertion style matching sibling tests: `assert_eq!(resp.status(), StatusCode::OK)` etc.

Run `cargo test` to verify all tests pass.

### Step 8 -- Verify Acceptance Criteria

1. GET /api/v2/sbom/{id}/advisory-summary returns correct JSON shape -- VERIFY via test
2. Returns 404 for non-existent SBOM -- VERIFY via test
3. Counts unique advisories (deduplication) -- VERIFY via test
4. All severity levels default to 0 -- VERIFY via test
5. Response time under 200ms for 500 advisories -- VERIFY via performance consideration in implementation

### Step 9 -- Self-Verification

1. **Scope containment**: `git diff --name-only` compared against Files to Modify and Files to Create
2. **Untracked file check**: `git status --short` for `??` entries in implementation directories
3. **Sensitive-pattern check**: scan staged diff for secrets/credentials
4. **Documentation currency**: check if `docs/api.md` needs updating with new endpoint
5. **Data-flow trace**: trace GET request -> Path extraction -> service call -> DB query -> severity counting -> JSON response (verify all stages connected)
6. **Contract & sibling parity**: verify SeveritySummary struct completeness, compare with sibling model/endpoint patterns
7. **Duplication check**: search for existing severity counting logic
8. **CI checks from CONVENTIONS.md**: run extracted CI commands
9. **Cross-section reference consistency**: verify file paths match across task sections

### Step 10 -- Commit and Push

**Commit message:**
```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add SeveritySummary model, AdvisoryService.severity_summary() method,
and GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM.

Implements TC-9201
```

With trailer: `--trailer="Assisted-by: Claude Code"`

**Push and create PR:**
```
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "..."
```

PR description includes:
- Summary bullets describing changes
- `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)` with clickable link
- Closes line for GitHub issue if customfield_10747 was populated

### Step 11 -- Update Jira

1. Update Git Pull Request custom field (customfield_10875) with PR URL in ADF format
2. Add comment to TC-9201 with PR link and summary of changes (with skill footer)
3. Transition TC-9201 to "In Review"
