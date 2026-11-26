# Task 4 — Add GET /api/v2/remediation/vulnerabilities (filterable list)

**Parent Epic:** TC-9006: trustify-backend (<EPIC-BE>)
**Issue type:** Task
**Labels:** ai-generated-jira
**Priority:** Major
**fixVersions:** RHTPA 1.5.0

---

## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Add `GET /api/v2/remediation/vulnerabilities`, a paginated list of tracked vulnerabilities (SBOM × advisory pairs) that supports filtering by severity, product, and remediation status, and sorting by severity. This is the data source for the MVP requirement "Filterable vulnerability table on the dashboard" (UC-1 step 4 and UC-2 steps 2–4). The feature names no list endpoint, so this one is derived from that requirement. It must handle up to 10,000 tracked vulnerabilities, which means pagination happens server-side.

## Files to Modify
- `modules/fundamental/src/remediation/model/mod.rs` — export `RemediationVulnerability`
- `modules/fundamental/src/remediation/service/mod.rs` — add `RemediationService::list_vulnerabilities(filter, paginated)`
- `modules/fundamental/src/remediation/endpoints/mod.rs` — register the `/vulnerabilities` route
- `tests/api/remediation.rs` — add list and filter integration tests

## Files to Create
- `modules/fundamental/src/remediation/model/vulnerability.rs` — `RemediationVulnerability` struct
- `modules/fundamental/src/remediation/endpoints/vulnerabilities.rs` — list handler with filter query parameters

## API Changes
- `GET /api/v2/remediation/vulnerabilities?severity={critical|high|medium|low}&product={product_id}&status={open|in_progress|resolved}&offset={n}&limit={n}&sort={severity|status|product}:{asc|desc}` — NEW. Returns `PaginatedResults<RemediationVulnerability>`:
  ```json
  {
    "items": [
      {
        "advisory_id": "string",
        "advisory_title": "string",
        "severity": "critical",
        "status": "open",
        "product_id": "string",
        "product_name": "string"
      }
    ],
    "total": 0
  }
  ```
  `severity` and `status` accept more than one value as a comma-separated list (for example `severity=critical,high`).

## Implementation Notes
- Build the query over `entity/src/sbom_advisory.rs`, joined to `entity/src/advisory.rs` (title, severity) and `entity/src/sbom.rs` (product). Use the same status and severity mapping helpers that `RemediationService` introduced in Task 2.
- Apply filters, pagination, and sorting through `common/src/db/query.rs`, as `modules/fundamental/src/advisory/endpoints/list.rs` and `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` list/search do. Sort by severity rank (Critical > High > Medium > Low), not alphabetically.
- Reject unknown filter values (for example `severity=urgent`) with a 400 `AppError`. Do not silently ignore them. An ignored filter would return an unfiltered list that looks like a valid filtered result.
- Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>`. Applies: task modifies `modules/fundamental/src/remediation/endpoints/vulnerabilities.rs` matching the convention's list endpoint scope. Example: `modules/fundamental/src/advisory/endpoints/list.rs`.
- Per CONVENTIONS.md §Query helpers: use `common/src/db/query.rs` for filtering, pagination, and sorting. Applies: task modifies `modules/fundamental/src/remediation/service/mod.rs` matching the convention's query scope. Example: `modules/fundamental/src/advisory/service/advisory.rs`.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()`. Applies: task modifies `modules/fundamental/src/remediation/endpoints/vulnerabilities.rs` matching the convention's endpoint handler scope. Example: `modules/fundamental/src/advisory/endpoints/get.rs`.
- Per CONVENTIONS.md §Testing: use real-PostgreSQL integration tests with `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/remediation.rs` matching the convention's integration test scope. Example: `tests/api/advisory.rs`.
- Constraints (docs/constraints.md):
  - §2: Conventional Commits, a Jira ID footer, and an `Assisted-by:` trailer.
  - §3: the PR is created with `--base TC-9006`, and the PR link is posted to Jira.
  - §5: changes stay limited to the listed files, existing code is inspected first, and duplicated filter logic is avoided.

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering, pagination, and sorting
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper
- `modules/fundamental/src/advisory/endpoints/list.rs` — filterable list handler pattern
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — advisory title and severity fields
- `modules/fundamental/src/remediation/service/mod.rs::RemediationService` (Task 2) — status and severity mapping

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/vulnerabilities` returns 200 with `PaginatedResults<RemediationVulnerability>`
- [ ] The `severity` filter returns only matching items and supports more than one value
- [ ] The `product` filter returns only vulnerabilities that affect the given product
- [ ] The `status` filter returns only matching items and supports more than one value
- [ ] Filters combine with AND semantics
- [ ] `sort=severity:desc` orders Critical, High, Medium, Low
- [ ] Unknown filter values return 400. They are not silently ignored (fail-closed)
- [ ] Pagination is done server-side, and `total` reflects the filtered count

## Test Requirements
- [ ] Integration test: for each filter (severity, product, status) taken alone, assert that only matching items are returned and that `total` is correct
- [ ] Integration test: combined filters (`severity=critical&product=X&status=open`) return the intersection
- [ ] Integration test: `sort=severity:desc` returns items in severity-rank order
- [ ] Integration test: `severity=invalid` returns 400 and not an unfiltered 200 list
- [ ] Integration test: offset/limit pagination over more than one page

## Verification Commands
- `cargo test -p tests remediation` — all remediation tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 2 — Add remediation module and GET /api/v2/remediation/summary
