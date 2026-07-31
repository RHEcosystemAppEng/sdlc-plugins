# Planning Summary: TC-9003 — SBOM Comparison View

## Plan Overview

Feature TC-9003 has been decomposed into 5 tasks across 2 repositories (trustify-backend and trustify-ui) using direct-to-main workflow mode.

## Task Summary

| Task | Title | Repository | Target Branch |
|---|---|---|---|
| 1 | SBOM comparison model and diff service | trustify-backend | main |
| 2 | SBOM comparison endpoint and integration tests | trustify-backend | main |
| 3 | SBOM comparison API types, client function, and React Query hook | trustify-ui | main |
| 4 | SBOM comparison page and components | trustify-ui | main |
| 5 | SBOM comparison documentation | trustify-backend | main |

## Inherited Field Propagation

- **Priority**: Critical — propagated from TC-9003 to all 5 created tasks. The feature's priority is set (not Undefined), so it is inherited by all tasks.
- **Fix Versions**: RHTPA 1.5.0 — propagated from TC-9003 to all 5 created tasks. The feature has a non-empty fixVersions array, and fixVersion scope config is absent (defaults to 'both'), so fixVersions are inherited by tasks.

## Workflow Mode Decision

**Mode**: direct-to-main

The backend comparison endpoint is additive (new GET endpoint) and can be merged independently. The frontend comparison page is also additive (new page and route). Cross-repo dependency ordering is enforced via explicit task dependencies. No atomicity risk from partial merges within either repository.

## Cross-Repository Dependencies

- Task 3 (trustify-ui) depends on Task 2 (trustify-backend): the frontend API client requires the backend comparison endpoint
- Task 5 (documentation) depends on Tasks 2 (trustify-backend) and 4 (trustify-ui): documentation requires both endpoint and UI to be complete

## Documentation Task

A documentation task (Task 5) was generated because the feature description includes Documentation Considerations with doc impact "New Content" — documenting the comparison endpoint and comparison UI.

## Figma Design Context

Frontend UI-facing tasks (Task 4) reference the Figma design context from figma-context.md, specifying PatternFly component mappings (Select, ExpandableSection, Badge, Table, EmptyState, Skeleton, Dropdown, Button) and visual specifications (badge colors, section ordering, empty/loading states). API-layer frontend tasks (Task 3) are exempt from Figma references as they handle data fetching only.

## Description Digests

| Task | Digest |
|---|---|
| 1 | sha256-md:0cff79731f06e5ff2914f1a12d639053bc31506f3c9098061c2ba2f256bedb57 |
| 2 | sha256-md:9f3883572d47ad6695e8705f80c9542679d45eaf11c9f2640c75095eb4f70678 |
| 3 | sha256-md:ae95aa31654a0ddbd4bf6c193594773edf74f01bbb05932c6dd2784b974fdf19 |
| 4 | sha256-md:5efc7cde6484628453fbd34f459e7dde5d16539dd47f616339e12f918abf2e69 |
| 5 | sha256-md:78a8d409124b9e580ac1f12c39b1cd1ff57d8d168f653a9ed5e8c4716929953e |
