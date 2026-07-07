# Implementation Plan — TC-9201

## Task Summary

**Key:** TC-9201
**Summary:** Add advisory severity aggregation service and endpoint
**Repository:** trustify-backend
**Target Branch:** main

## Overview

Implement a service and REST endpoint that aggregates advisory severity counts for
a given product or component. The endpoint accepts a query scope (product ID or
component ID) and returns a breakdown of advisory counts grouped by severity level
(critical, high, medium, low, none/unknown).

## Step-by-Step Plan

### Step 1: Define the Severity Aggregation Model

**File to create:** `entity/src/advisory_severity_summary.rs`

- Define a `SeverityAggregation` struct with fields for each severity level count:
  - `critical: i64`
  - `high: i64`
  - `medium: i64`
  - `low: i64`
  - `none: i64` (for advisories with no severity or unknown severity)
  - `total: i64`
- Derive `Serialize`, `Deserialize`, `Debug`, `Clone`, `Default`, `utoipa::ToSchema`.
- Register the module in `entity/src/lib.rs`.

### Step 2: Implement the Aggregation Service

**File to create:** `modules/advisory/src/service/severity_aggregation.rs`

- Add a method on the advisory service (or a new dedicated service struct) that:
  1. Accepts a scope parameter (product ID, component ID, or unscoped for global).
  2. Queries the database using a SQL aggregation:
     ```sql
     SELECT severity, COUNT(*) as count
     FROM advisory
     WHERE <scope_filter>
     GROUP BY severity
     ```
  3. Maps database rows to the `SeverityAggregation` struct, assigning counts to
     the appropriate severity fields.
  4. Computes the `total` as the sum of all severity buckets.
  5. Returns `Result<SeverityAggregation, Error>`.

- Handle the case where no advisories match the scope: return a default
  `SeverityAggregation` with all counts at zero.

- Register the new module in `modules/advisory/src/service/mod.rs`.

### Step 3: Add the REST Endpoint

**File to modify:** `modules/advisory/src/endpoints/mod.rs` (or a new file
`modules/advisory/src/endpoints/severity_aggregation.rs`)

- Define a new endpoint: `GET /api/v2/advisory/severity-summary`
- Query parameters:
  - `product` (optional): UUID of the product to scope the aggregation.
  - `component` (optional): UUID of the component to scope the aggregation.
  - If neither is provided, return global aggregation across all advisories.
  - If both are provided, return a 400 Bad Request error.
- Response: `200 OK` with `SeverityAggregation` as JSON body.
- Add OpenAPI annotations (`#[utoipa::path(...)]`) for schema documentation.
- Wire the endpoint into the router in the module's `configure` function.

### Step 4: Add Request Validation

- Validate that at most one scope parameter is provided.
- Validate that provided UUIDs are syntactically correct (handled by deserialization).
- Return appropriate error responses (400 for invalid input, 404 if the referenced
  product/component does not exist).

### Step 5: Write Tests

**File to create:** `modules/advisory/src/service/severity_aggregation_test.rs`
(or add to existing test module)

- **Test: aggregation with mixed severities**
  - Given: advisories exist with varying severity levels (2 critical, 3 high,
    1 medium, 0 low).
  - When: the aggregation service is called with no scope filter.
  - Then: the response contains `critical: 2, high: 3, medium: 1, low: 0,
    none: 0, total: 6`.

- **Test: aggregation scoped to a product**
  - Given: advisories exist across multiple products.
  - When: the aggregation service is called with a specific product ID.
  - Then: only advisories for that product are counted.

- **Test: aggregation with no matching advisories**
  - Given: no advisories match the given scope.
  - When: the aggregation service is called.
  - Then: all counts are zero and total is zero.

- **Test: endpoint returns 400 for conflicting scope parameters**
  - Given: both `product` and `component` query parameters are provided.
  - When: the endpoint is called.
  - Then: a 400 Bad Request response is returned.

**File to create:** `modules/advisory/tests/severity_aggregation.rs` (integration test)

- **Test: end-to-end severity aggregation via HTTP**
  - Given: test database is seeded with advisories of known severities.
  - When: `GET /api/v2/advisory/severity-summary` is called.
  - Then: the JSON response matches expected aggregation counts.

- **Test: scoped query via HTTP**
  - Given: test database is seeded with advisories across two products.
  - When: `GET /api/v2/advisory/severity-summary?product=<uuid>` is called.
  - Then: only the scoped product's advisories are counted.

### Step 6: Verify Acceptance Criteria

- The endpoint returns correct severity counts for global, product-scoped, and
  component-scoped queries.
- Zero-count severities are included in the response (not omitted).
- Invalid scope combinations return 400.
- The endpoint is documented in the OpenAPI schema.
- All tests pass.

### Step 7: Self-Verification

- Confirm scope containment: changes are limited to advisory module and entity
  crate.
- Run `cargo clippy` and `cargo fmt --check` to ensure code quality.
- Verify no untracked files are left behind.
- Check for sensitive patterns in the diff.
- Verify the new endpoint is consistent with existing endpoint conventions in the
  module.
- Run the full test suite: `cargo test`.

### Step 8: Commit and Push

- Create branch: `feat/TC-9201-advisory-severity-aggregation`
- Commit with Conventional Commits format:
  `feat(advisory): add severity aggregation service and endpoint`
- Push and create PR targeting `main` with Jira link to TC-9201.

### Step 9: Update Jira

- Update TC-9201's Git Pull Request custom field with the PR URL.
- Add a comment with the PR link and implementation summary.
- Transition TC-9201 to "In Review".

## Files Changed Summary

| File | Action | Purpose |
|---|---|---|
| `entity/src/advisory_severity_summary.rs` | Create | Aggregation response model |
| `entity/src/lib.rs` | Modify | Register new module |
| `modules/advisory/src/service/severity_aggregation.rs` | Create | Aggregation query logic |
| `modules/advisory/src/service/mod.rs` | Modify | Register service module |
| `modules/advisory/src/endpoints/severity_aggregation.rs` | Create | REST endpoint handler |
| `modules/advisory/src/endpoints/mod.rs` | Modify | Wire endpoint into router |
| `modules/advisory/src/service/severity_aggregation_test.rs` | Create | Unit tests |
| `modules/advisory/tests/severity_aggregation.rs` | Create | Integration tests |

## Dependencies

None identified. This is a new, additive feature with no blocking dependencies on
other tasks.
