# Task 3 — Add GET /api/v2/remediation/by-product

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
Add `GET /api/v2/remediation/by-product`. It returns a paginated, per-product remediation breakdown, where each product entry has total, open, in-progress, and resolved counts. Large portfolios (more than 50 products) need pagination, per the Customer Considerations. The UI uses this endpoint for the product filter options and the product breakdown (UC-2).

## Files to Modify
- `modules/fundamental/src/remediation/model/mod.rs` — export the new `ProductRemediation` model
- `modules/fundamental/src/remediation/service/mod.rs` — add `RemediationService::by_product(paginated)` aggregation
- `modules/fundamental/src/remediation/endpoints/mod.rs` — register the `/by-product` route
- `tests/api/remediation.rs` — add by-product integration tests

## Files to Create
- `modules/fundamental/src/remediation/model/by_product.rs` — `ProductRemediation` struct
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — `GET /api/v2/remediation/by-product` handler

## API Changes
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}&sort={field}` — NEW. Returns `PaginatedResults<ProductRemediation>`:
  ```json
  {
    "items": [
      { "product_id": "string", "product_name": "string", "total": 0, "open": 0, "in_progress": 0, "resolved": 0 }
    ],
    "total": 0
  }
  ```

## Implementation Notes
- "Product" is modeled as the SBOM (`entity/src/sbom.rs`, `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` for name and identifier). Confirm this mapping (see the open question on TC-9006) before implementing. If products turn out to group several SBOMs, group by the product attribute rather than by the SBOM id.
- Aggregate in SQL: `GROUP BY sbom` over `entity/src/sbom_advisory.rs`, using conditional counts per status. Reuse the status column chosen in Task 2 through a shared helper in `RemediationService`, so status mapping logic is not duplicated.
- Use `common/src/db/query.rs` for offset, limit, and sorting, and wrap the results in `common/src/model/paginated.rs::PaginatedResults<T>`. Follow the existing list handler `modules/fundamental/src/sbom/endpoints/list.rs`.
- Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>`. Applies: task modifies `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's list endpoint scope. Example: `modules/fundamental/src/sbom/endpoints/list.rs`.
- Per CONVENTIONS.md §Query helpers: use the shared filtering, pagination, and sorting from `common/src/db/query.rs`. Applies: task modifies `modules/fundamental/src/remediation/service/mod.rs` matching the convention's query scope. Example: `modules/fundamental/src/sbom/service/sbom.rs::SbomService` list.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()`. Applies: task modifies `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's endpoint handler scope. Example: `modules/fundamental/src/advisory/endpoints/list.rs`.
- Per CONVENTIONS.md §Testing: use real-PostgreSQL integration tests with the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/remediation.rs` matching the convention's integration test scope. Example: `tests/api/sbom.rs`.
- Constraints (docs/constraints.md):
  - §2: Conventional Commits, a Jira ID footer, and an `Assisted-by:` trailer.
  - §3: the PR is created with `--base TC-9006`, and the PR link is posted to Jira.
  - §5: changes stay limited to the listed files, existing code is inspected first, and shared helpers are reused.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper
- `common/src/db/query.rs` — pagination and sorting helpers
- `modules/fundamental/src/sbom/endpoints/list.rs` — list handler pattern with pagination
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — product (SBOM) name and identifier fields
- `modules/fundamental/src/remediation/service/mod.rs::RemediationService` (Task 2) — status mapping and aggregation helper

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/by-product` returns 200 with `PaginatedResults<ProductRemediation>`
- [ ] Each item includes `total`, `open`, `in_progress`, and `resolved`, where `total == open + in_progress + resolved`
- [ ] `offset` and `limit` paginate correctly, and `total` reflects the full product count
- [ ] Products with no correlated vulnerabilities are excluded (or included with zero counts, matching the decision recorded in the struct doc comment)
- [ ] Fail-closed behavior: a database failure returns an error response, not an empty `items` list with 200

## Test Requirements
- [ ] Integration test: seed three products with known status mixes and assert the per-product counts
- [ ] Integration test: with more than `limit` products, assert that pagination (offset/limit) and `total` are correct
- [ ] Integration test: assert the per-item invariant `total == open + in_progress + resolved`
- [ ] Integration test: assert the sort order when `sort=open:desc` is supplied

## Verification Commands
- `cargo test -p tests remediation` — all remediation tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 2 — Add remediation module and GET /api/v2/remediation/summary
