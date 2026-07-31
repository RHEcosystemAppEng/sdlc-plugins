# Plan Summary: TC-9006 — Add vulnerability remediation tracking dashboard

## Epic Hierarchy

Feature TC-9006 uses **by-repository** Epic grouping with the level-1 issue type "Epic".

| Epic | Summary | Parent | Tasks |
|---|---|---|---|
| TC-9007 (simulated) | TC-9006: trustify-backend | TC-9006 | Tasks 1, 2, 3, 7 |
| TC-9008 (simulated) | TC-9006: trustify-ui | TC-9006 | Tasks 4, 5, 6 |

**Incorporates links**: Feature TC-9006 Incorporates Epic TC-9007, Feature TC-9006 Incorporates Epic TC-9008.

## Inherited Field Propagation

- **Priority**: Major (propagated from Feature TC-9006 to all Epics and Tasks)
- **Fix Versions**: RHTPA 1.5.0 (propagated from Feature TC-9006 to all Epics and Tasks; fixVersion scope defaults to "both")

## Task Summary

| # | Task | Repository | Parent Epic | Dependencies |
|---|---|---|---|---|
| 1 | remediation-model-service | trustify-backend | TC-9007 | None |
| 2 | remediation-endpoints | trustify-backend | TC-9007 | Task 1 |
| 3 | remediation-integration-tests | trustify-backend | TC-9007 | Task 2 |
| 4 | remediation-api-client-hooks | trustify-ui | TC-9008 | Task 2 |
| 5 | remediation-dashboard-page | trustify-ui | TC-9008 | Task 4 |
| 6 | vulnerability-table | trustify-ui | TC-9008 | Task 5 |
| 7 | remediation-documentation (doc) | trustify-backend | TC-9007 | Task 3, Task 6 |

## Scope

**MVP requirements implemented** (4 of 5 requirements):
- GET /api/v2/remediation/summary (Tasks 1-2)
- GET /api/v2/remediation/by-product (Tasks 1-2)
- Dashboard page at /remediation with summary cards and progress chart (Task 5)
- Filterable vulnerability table (Task 6)

**Non-MVP excluded**:
- Export remediation report as CSV

## Documentation

Task 7 is a documentation task generated from the feature's Documentation Considerations (New Content). It covers REST API reference and dashboard user guide.

## Workflow

Direct-to-main workflow. No feature branch required.

**Total**: 2 Epics, 7 Tasks (3 backend implementation, 3 frontend implementation, 1 documentation)
