# Planning Summary: TC-9006 — Vulnerability Remediation Tracking Dashboard

## Epic Hierarchy

This feature uses **Epic hierarchy** with **by-repository** grouping:

- **Feature**: TC-9006 (parent)
- **Epic 1**: TC-9006: trustify-backend (4 tasks)
- **Epic 2**: TC-9006: trustify-ui (4 tasks)

Links: TC-9006 incorporates both Epics. Tasks are children of their respective Epics, not linked directly to the Feature.

## Tasks

| # | Task | Repository | Epic | Dependencies |
|---|---|---|---|---|
| 1 | Add remediation models and aggregation service | trustify-backend | TC-9006: trustify-backend | None |
| 2 | Add remediation REST endpoints | trustify-backend | TC-9006: trustify-backend | Task 1 |
| 3 | Add integration tests for remediation endpoints | trustify-backend | TC-9006: trustify-backend | Task 2 |
| 4 | Add remediation API types, client functions, and React Query hooks | trustify-ui | TC-9006: trustify-ui | None |
| 5 | Create remediation dashboard page with summary cards and progress chart | trustify-ui | TC-9006: trustify-ui | Task 4 |
| 6 | Add filterable vulnerability table to remediation dashboard | trustify-ui | TC-9006: trustify-ui | Task 5 |
| 7 | Add tests for remediation dashboard | trustify-ui | TC-9006: trustify-ui | Task 6 |
| 8 | Add API reference documentation for remediation endpoints | trustify-backend | TC-9006: trustify-backend | Task 2 |

**Total**: 8 tasks across 2 repositories, grouped into 2 Epics.

## Architecture

**Backend** (trustify-backend): New `remediation` module under `modules/fundamental/` following the established `model/ + service/ + endpoints/` structure. Two REST endpoints aggregate remediation data from existing entity tables (no new database tables): `GET /api/v2/remediation/summary` for portfolio-wide severity/status counts and `GET /api/v2/remediation/by-product` for per-product breakdowns with pagination.

**Frontend** (trustify-ui): New `RemediationDashboardPage` under `src/pages/` following the established page directory structure. Uses React Query hooks for data fetching, PatternFly 5 components for UI, and includes summary cards, a progress chart, and a filterable vulnerability table with server-side pagination.

## Workflow Mode

**Direct-to-main** — all tasks target `main` branch. Cross-repo feature with independent deployment pipelines; backend endpoints can be deployed before the frontend consumes them.

## Propagated Fields

- **Priority**: Major (propagated from TC-9006 to all Epics and Tasks)
- **Fix Versions**: RHTPA 1.5.0 (propagated from TC-9006 to all Epics and Tasks)
- **Labels**: ai-generated-jira
- **Additional fields**: `{ "labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }`

## Convention Enrichment

Both repositories have CONVENTIONS.md. Convention applicability was evaluated per convention-applicability-rules.md:

- **trustify-backend**: Module Pattern, Error Handling, Response Types, Query Helpers, Endpoint Registration, Caching, and Testing conventions applied to relevant tasks based on .rs file scope matching.
- **trustify-ui**: API Layer, State Management, Component Library, Page Structure, Routing, Testing, and Naming conventions applied to relevant tasks based on .ts/.tsx file scope matching.

## Documentation

Task 8 addresses the "New Content" documentation consideration from TC-9006, adding API reference documentation for the two new remediation endpoints.
