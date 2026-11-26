# Repository Impact Map — TC-9003: SBOM comparison view

> This is the content that would be posted as a comment on TC-9003 (Step 4), followed by the workflow-mode decision (Step 4.5).

## Inputs used

- Feature: TC-9003 "SBOM comparison view" (Priority: Critical, Fix Versions: RHTPA 1.5.0)
- Figma: https://www.figma.com/design/mock123/SBOMCompare — page "Comparison View" (from figma-context.md)
- Repositories: trustify-backend (repo-backend.md), trustify-ui (repo-frontend.md). No Serena instances configured — structures analysed from the repository manifests (Glob/Read fallback).
- Documentation signals: "Documentation Considerations" present — Doc Impact: **New Content** (endpoint reference + UI guide)
- Testing readiness template (`docs/testing-readiness.md`): not present in either repository manifest — no cross-cutting testing tasks generated.
- CONVENTIONS.md: present in both repository roots; conventions applied per task (Key Conventions sections of each manifest).

## Impact map

```
trustify-backend:
  changes:
    - Add SBOM diff domain model (SbomComparison + six entry types) under modules/fundamental/src/sbom/model/
    - Add diff computation service over existing sbom_package / package / package_license / sbom_advisory / advisory data (no new tables)
    - Add GET /api/v2/sbom/compare?left={id1}&right={id2} endpoint, registered in sbom/endpoints/mod.rs with existing caching config
    - Add integration tests for compare endpoint in tests/api/sbom.rs (diff categories, identical SBOMs, 400, 404, route ordering, perf)
    - Document compare endpoint (README API overview + endpoint reference)

trustify-ui:
  changes:
    - Add SbomComparison TypeScript types, compareSboms() REST client, useSbomComparison React Query hook, MSW handler + fixture
    - Add /sbom/compare page (lazy route) per Figma: toolbar with two typeahead Selects + Compare, six ExpandableSections with colored count badges and tables, empty/loading/error states, URL-encoded left/right params, critical-row highlight, virtualization >100 rows
    - Add row selection + "Compare selected" button on SBOM list page navigating to /sbom/compare?left=&right=
    - Add client-side JSON/CSV export from the comparison page Export dropdown (non-MVP)
    - Document the comparison UI workflow
```

## Requirement coverage

| Requirement | MVP | Covered by |
|---|---|---|
| `GET /api/v2/sbom/compare` structured diff | Yes | Task 1, Task 2 |
| Frontend comparison page at `/sbom/compare` | Yes | Task 3, Task 4 |
| URL-shareable comparison | Yes | Task 4 (URL is source of truth), Task 5 (navigation) |
| Export diff as JSON or CSV | No | Task 6 (client-side, Figma Export dropdown) |
| Highlight packages with new critical vulnerabilities | Yes | Task 4 (critical row highlight) |
| NFR: p95 < 1s at 2000 packages | — | Task 1 (bounded queries, in-memory diff), Task 2 (perf test) |
| NFR: virtualized lists >100 rows | — | Task 4 |
| NFR: no new DB tables | — | Task 1 (acceptance criterion) |
| UC-1 select two SBOMs on list page | — | Task 5 |
| Customer: same-product comparison | — | Task 5 (non-blocking warning) |
| Documentation (New Content) | — | Task 7 (API), Task 8 (UI) |

## Excluded requirements

- **"Add comparison endpoint to the API latency Grafana dashboard"** (Customer Information/Supportability) — no repository in the Repository Registry/inputs holds Grafana dashboard definitions. Missing input: the monitoring/dashboards repository (or dashboard JSON location). Task 2 adds handler tracing so metrics exist once the dashboard is updated.
- **"Monitor for timeouts on large SBOM comparisons (>2000 packages per SBOM)"** — alerting configuration lives outside both repositories. Missing input: the alerting/monitoring configuration repository.
- **"Large SBOM diffs (>1000 package changes) may require pagination or filtering"** (Customer Considerations) — only partially planned: the Figma design explicitly specifies "no pagination (virtualized for >100 rows)", so Task 4 uses virtualization. Server-side pagination/filtering of the diff is not planned. Missing input: a decision/spec on whether the API must paginate diff categories and the design for filtering controls.

## Shared-artifact analysis

No shared artifact (record/manifest/index/cache populated by multiple workflows) is created or changed: the diff is computed on-the-fly and read-only over existing SBOM/package/advisory data populated by `modules/ingestor/src/graph/sbom/mod.rs` and `modules/ingestor/src/graph/advisory/mod.rs`. Ingestion paths are unaffected. The only cache consideration is the `tower-http` response cache on the new route (Task 2).

## Cross-repo API contract

`GET /api/v2/sbom/compare?left={id1}&right={id2}` → 200 `SbomComparison`
(`added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`; snake_case field names; `direction` ∈ `upgrade|downgrade`; `severity` lowercase), 400 on missing params, 404 on unknown SBOM. Produced by Tasks 1–2 (trustify-backend), consumed by Tasks 3–6 (trustify-ui).

---

## Workflow mode decision (Step 4.5)

**Selected mode: `direct-to-main`**

Atomicity indicators evaluated:

1. **Coordinated schema migrations** — not present. No migrations; diff is computed from existing tables.
2. **Breaking API changes** — not present. The new endpoint is purely additive; no existing request/response contract changes.
3. **Cross-cutting refactors** — not present. No renames or shared-type changes.
4. **Tightly coupled feature components** — not present in the "neither side functions independently" sense: the backend endpoint is independently functional and mergeable (usable by API consumers on its own). The frontend depends on the backend, but this is a one-directional ordering dependency, not mutual coupling. Merging Task 1 → Task 2 (backend) before Tasks 3–6 (frontend) leaves `main` in both repositories working at every step; no frontend route is exposed before its endpoint exists.

Because no task PR leaves `main` broken when tasks merge in dependency order, all tasks target `main`. Cross-repo ordering is enforced via explicit `## Dependencies` entries (Task 3 and Task 4 depend on Task 2) and Jira "Depend" links. No bookend tasks are generated and the `workflow:feature-branch` label is not applied.

---

This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.
