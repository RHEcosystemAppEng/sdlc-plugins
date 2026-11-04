# Repository Impact Map — TC-9003: SBOM comparison view

> Posted as a Jira comment on TC-9003 (Step 4, after user approval of the map).

## Planning inputs

| Input | Source | Notes |
|---|---|---|
| Feature | TC-9003 (`feature-multi-repo.md`) | Priority: Critical; Fix Versions: RHTPA 1.5.0; Labels: ai-generated-jira |
| Figma | https://www.figma.com/design/mock123/SBOMCompare (`figma-context.md`) | Comparison View page: header toolbar, 6 collapsible diff sections, empty and loading states |
| Backend repo | `trustify-backend` (`repo-backend.md`) | Rust / Axum / SeaORM |
| Frontend repo | `trustify-ui` (`repo-frontend.md`) | React 18 / TypeScript / PatternFly 5 / React Query |
| Conventions | `CONVENTIONS.md` exists at the root of both repos. Its rules are summarized in each manifest's "Key Conventions" section | Applied to tasks with `Applies:` rationale |
| Testing readiness template | None found for either repo (`docs/testing-readiness.md` absent from both manifests) | No testing tasks generated |
| Documentation signals | "Documentation Considerations": **New Content** | Documentation task generated |

**Registry note:** `trustify-backend` and `trustify-ui` are not listed in this project's Repository Registry, which lists only `sdlc-plugins`. No Serena instances are configured. Repository analysis used the supplied repository manifests instead of live code inspection (the Glob/Grep/Read fallback). Before implementation, add both repos to the Registry, or confirm their paths.

## Discovered backend API contracts

- `GET /api/v2/sbom`: lists SBOMs and returns `PaginatedResults<SbomSummary>` (`{ items: SbomSummary[], total: number }`). Defined in `modules/fundamental/src/sbom/endpoints/list.rs`, with the wrapper in `common/src/model/paginated.rs`. Already consumed by `trustify-ui` via `src/api/rest.ts` and the `src/hooks/useSboms.ts` hook.
- `GET /api/v2/sbom/{id}` returns `SbomDetails` (`modules/fundamental/src/sbom/endpoints/get.rs`, `modules/fundamental/src/sbom/model/details.rs`).
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` is **NEW** (this feature). The response shape follows the Figma "Expected response shape":
  ```json
  {
    "added_packages":           [{ "name": "string", "version": "string", "license": "string", "advisory_count": 0 }],
    "removed_packages":         [{ "name": "string", "version": "string", "license": "string", "advisory_count": 0 }],
    "version_changes":          [{ "name": "string", "left_version": "string", "right_version": "string", "direction": "upgrade|downgrade" }],
    "new_vulnerabilities":      [{ "advisory_id": "string", "severity": "critical|high|medium|low", "title": "string", "affected_package": "string" }],
    "resolved_vulnerabilities": [{ "advisory_id": "string", "severity": "string", "title": "string", "previously_affected_package": "string" }],
    "license_changes":          [{ "name": "string", "left_license": "string", "right_license": "string" }]
  }
  ```
- Data sources for the diff (no new tables): `entity/src/sbom_package.rs` (SBOM to Package), `entity/src/package.rs`, `entity/src/package_license.rs` (license), `entity/src/sbom_advisory.rs` (SBOM to Advisory), `entity/src/advisory.rs`. Severity comes from `AdvisorySummary` (`modules/fundamental/src/advisory/model/summary.rs`).

## Shared-artifact analysis

Not applicable. The comparison is a read-only, on-the-fly computation over existing package and advisory data. It does not create, update, or populate any shared artifact. Its existing producers, the ingestion paths in `modules/ingestor/src/graph/sbom/mod.rs` and `modules/ingestor/src/graph/advisory/mod.rs`, are consumed as they are and not modified.

## Impact map

```
trustify-backend:
  changes:
    - Add SBOM comparison response model (added/removed packages, version changes, new/resolved vulnerabilities, license changes)
    - Add SBOM diff computation to the SBOM service, computed on-the-fly from existing sbom_package, package_license and sbom_advisory data (no new tables / no migration)
    - Add GET /api/v2/sbom/compare?left={id1}&right={id2} endpoint and register it in the SBOM route module
    - Return 404 for unknown SBOM IDs and 400 for missing/invalid query params (never an empty diff for a non-existent SBOM)
    - Add integration tests for the compare endpoint, including a 2000-package performance check

trustify-ui:
  changes:
    - Add TypeScript types for the comparison response, an API client function and a React Query hook for the compare endpoint, plus MSW mocks
    - Add diff section components (collapsible sections with colored count badge, per-category tables, critical-row highlight, virtualization for >100 rows, skeleton loading)
    - Add SBOM comparison page at /sbom/compare with left/right SBOM selectors, Compare button, URL-encoded state (left/right query params), empty state and loading state; register the route
    - Add multi-select checkboxes and a "Compare selected" action to the SBOM list page that navigates to /sbom/compare?left=..&right=..
    - Add client-side Export JSON / Export CSV of the loaded comparison (non-MVP)

documentation (repository: trustify-backend — see open questions):
  changes:
    - Document the compare endpoint (API reference) and the comparison UI workflow (user guide)
```

## Requirement coverage

| Requirement | MVP | Covered by |
|---|---|---|
| `GET /api/v2/sbom/compare` returns structured diff | Yes | Task 2, Task 3 |
| Frontend comparison page at `/sbom/compare` | Yes | Task 4, Task 5, Task 6 |
| URL-shareable comparison | Yes | Task 6 (URL search params), Task 7 (list page navigation) |
| Export diff as JSON or CSV | No | Task 8 (client-side, built from the Figma Export dropdown) |
| Highlight packages with new critical vulnerabilities | Yes | Task 5 (critical row highlight in New Vulnerabilities) |
| NFR: p95 < 1s for 2000 packages each | | Task 2 (bulk queries + in-memory hash diff), Task 3 (performance test) |
| NFR: virtualized lists for >100 changed packages | | Task 5 |
| NFR: no new database tables | | Task 2 (no migration; acceptance criterion) |
| UC-1 (select two SBOMs on list page, then compare) | | Task 7, Task 6 |
| UC-2 (open shared URL to see the comparison directly) | | Task 6 (auto-run comparison when both params present on load) |
| Documentation (New Content) | | Task 9 |

## Excluded requirements

| Requirement | Reason it cannot be planned (missing input) |
|---|---|
| "Add comparison endpoint to the API latency Grafana dashboard" (Customer Information/Supportability) | No observability or dashboard repository is in the Repository Registry or the supplied inputs. The Grafana dashboard definitions have no target repo. Provide the dashboard repo (or confirm the dashboards are provisioned from `trustify-backend`) to plan this. |
| "Monitor for timeouts on large SBOM comparisons (>2000 packages per SBOM)" (Customer Information/Supportability) | Same gap. No alerting or monitoring repo or configuration is available. The backend task logs comparison duration and package counts (Task 2) so the data exists, but alert rules cannot be planned without a target repository. |

## Open questions (for reviewer)

1. **Same-product constraint:** "Both SBOMs must be from the same product/project". Should the backend reject cross-product comparisons with 400, or should the UI only warn? The current plan neither blocks nor warns. Confirm, and I will add an acceptance criterion to Task 3 or Task 6.
2. **Large diffs (>1000 changes):** the Figma specifies no pagination plus virtualization, so the endpoint returns the full diff unpaginated. Confirm that backend pagination or filtering is not needed for the MVP.
3. **Advisory-to-package correlation:** `affected_package` and `advisory_count` need an advisory-to-package relation. The entity list shows only `sbom_advisory` (SBOM-level). Task 2 must confirm where the ingestor stores this correlation (`modules/ingestor/src/graph/advisory/mod.rs`). If no persisted relation exists, this becomes a scope issue because no new tables are allowed.
4. **Cross-repo feature branch:** in feature-branch mode the bookend tasks target a single repository (`trustify-ui`, which has most tasks). Tasks 2 and 3 target `TC-9003` in `trustify-backend`, so a `TC-9003` branch must also be created and later merged there. Confirm whether to add backend bookend tasks or handle the backend branch manually.
5. **Documentation repository:** no docs repository is in the Registry. Task 9 targets `trustify-backend` by default. Redirect it if the product docs live elsewhere.

## Workflow mode

**feature-branch**. See `workflow-mode-comment.md`.

## Task list and Jira field values (`additional_fields`)

All tasks: `labels: ["ai-generated-jira"]`, `priority: {"name": "Critical"}` (inherited from the Feature), `fixVersions: [{"name": "RHTPA 1.5.0"}]` (inherited; `fixVersion scope: both`). Details are in `task-creation-log.md`.

| # | Summary | Repository | Target Branch | Depends on |
|---|---|---|---|---|
| 1 | Create feature branch TC-9003 from main | trustify-ui | main | — |
| 2 | Backend: SBOM comparison model and diff service | trustify-backend | TC-9003 | 1 |
| 3 | Backend: GET /api/v2/sbom/compare endpoint and integration tests | trustify-backend | TC-9003 | 1, 2 |
| 4 | Frontend: comparison API types, client function, React Query hook and mocks | trustify-ui | TC-9003 | 1, 3 |
| 5 | Frontend: comparison diff section components | trustify-ui | TC-9003 | 1, 4 |
| 6 | Frontend: SBOM comparison page and /sbom/compare route | trustify-ui | TC-9003 | 1, 4, 5 |
| 7 | Frontend: multi-select and "Compare selected" on SBOM list page | trustify-ui | TC-9003 | 1, 6 |
| 8 | Frontend: export comparison as JSON / CSV (non-MVP) | trustify-ui | TC-9003 | 1, 6 |
| 9 | Documentation: SBOM comparison endpoint and UI guide | trustify-backend | TC-9003 | 2–8 |
| 10 | Merge feature branch TC-9003 to main | trustify-ui | main | 2–9 |

---

This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.
