# TC-9003 — SBOM comparison view: Planning Record and Repository Impact Map

## Step 0 — Project Configuration validation
- `## Repository Registry` — present (1 entry). Note: the registry lists only `sdlc-plugins`; the target repositories `trustify-backend` and `trustify-ui` were supplied as eval fixtures (`repo-backend.md`, `repo-frontend.md`) and are treated as registered repositories without Serena instances.
- `## Jira Configuration` — present (Project key TC, Cloud ID 2b9e35e3-…, Feature issue type ID 10142).
- `## Code Intelligence` — present; no Serena instances → fallback to Read/Glob/Grep over the provided repository structure.

## Step 1 — Feature extraction
| Field | Value |
|---|---|
| Key | TC-9003 |
| Title | SBOM comparison view |
| Priority | Critical (set → propagate) |
| Fix Versions | RHTPA 1.5.0 (set → propagate; `fixVersion scope: both`) |
| Figma | https://www.figma.com/design/mock123/SBOMCompare (context from `figma-context.md`) |
| Documentation signals | Doc impact: **New Content** — endpoint reference (API consumers) + comparison UI guide (UI users); reference material: SBOM detail page docs, package/advisory data model docs |

## Step 1.5 — Parent link
No parent on TC-9003. Prompt would be shown; in this non-interactive eval the choice is **skip** (no parent linked).

## Step 2.5 — Issue types (simulated; no Jira access)
Documented assumption: TC uses a Jira hierarchy where Feature (ID 10142) is level 2, so an Epic exists at level 1.
```
Type-to-role mapping:
  Feature: Feature (ID: 10142, level: 2)
  Epic:    Epic    (ID: <discovered at runtime>, level: 1)
  Task:    Task    (ID: <discovered at runtime>, level: 0)
```
Hierarchy Configuration: `Default epic grouping strategy: by-sub-feature` → applied without prompting. Suggested groupings (auto-approved for the eval) are listed below.

## Step 3 — Repository analysis summary
- **CONVENTIONS.md**: present in both repositories (`trustify-backend/CONVENTIONS.md`, `trustify-ui/CONVENTIONS.md`). Their content is represented by the "Key Conventions" sections of the fixtures; section names used in tasks: Module pattern, Error handling, Endpoint registration, Testing (backend); API layer, Page structure, Component library, Routing, Naming, Shared components, Testing (frontend).
- **Documentation files**: `README.md` and `CONVENTIONS.md` in each repo. No `docs/` API reference directory exists in either repo.
- **Testing readiness template** (`docs/testing-readiness.md`): not present in either repository → no testing tasks generated.
- **Eval infrastructure**: no task modifies a skill `SKILL.md` → not applicable.
- **Shared-artifact analysis**: no acceptance criterion depends on a shared artifact's lifecycle. The diff only *reads* SBOM/package/advisory data populated by the ingestor (`modules/ingestor/src/graph/sbom/mod.rs`, `.../advisory/mod.rs`); no writer changes needed. Not applicable.
- **Cross-cutting call sites**: none — the change adds a new endpoint/route and a new page; no shared signatures change.
- **Backend API discovery (for manual frontend REST calls):**
  - `GET /api/v2/sbom` — existing; `PaginatedResults<SbomSummary>` = `{ items, total }` (`modules/fundamental/src/sbom/endpoints/list.rs`, `common/src/model/paginated.rs`)
  - `GET /api/v2/sbom/{id}` — existing; `SbomDetails` (`modules/fundamental/src/sbom/endpoints/get.rs`)
  - `GET /api/v2/sbom/compare?left&right` — **does not exist**; to be created (Tasks 1–2) with the Figma-specified response shape.
- **Reuse candidates found**: `SbomService` (sbom/service/sbom.rs), `PackageSummary` (license), `AdvisorySummary` (severity), `common/src/db/query.rs`, `AppError`; UI: `useSboms`, `useSbomById`, `SeverityBadge`, `severityUtils`, `EmptyStateCard`, `FilterToolbar`, `PackageTable`, `AdvisoryList`.

## Step 4 — Repository Impact Map

```
trustify-backend:
  changes:
    - Add SbomComparison response model (six diff categories) under modules/fundamental/src/sbom/model/
    - Add diff computation service over existing sbom_package / package_license / sbom_advisory data (no new tables)
    - Fail closed (404) when either SBOM does not exist instead of returning an empty diff
    - Add GET /api/v2/sbom/compare?left={id1}&right={id2} endpoint and route registration
    - Add integration tests for the compare endpoint in tests/api/sbom.rs
    - Document the comparison endpoint (API reference; README endpoint list)

trustify-ui:
  changes:
    - Add SbomComparison TypeScript types, fetchSbomComparison REST function and useSbomComparison hook with MSW mocks
    - Add /sbom/compare page with left/right SBOM selectors, Compare button, empty/loading/error states
    - Encode left/right SBOM IDs in the URL so comparisons are shareable and deep-linkable
    - Render six collapsible diff sections with colored count badges, sortable tables and virtualization for >100 rows
    - Highlight New Vulnerabilities rows with critical severity
    - Add row selection and "Compare selected" action on the SBOM list page
    - Add Export dropdown (JSON / CSV) for the loaded comparison (non-MVP)
    - Document the comparison UI workflow
```

### Requirement coverage
| Requirement | MVP | Covered by |
|---|---|---|
| `GET /api/v2/sbom/compare` returns structured diff | Yes | Task 1, Task 2 |
| Frontend comparison page at `/sbom/compare` | Yes | Task 3, Task 4, Task 5 |
| URL-shareable comparison | Yes | Task 4 |
| Export diff as JSON or CSV | No | Task 7 (scheduled after MVP) |
| Highlight packages with new critical vulnerabilities | Yes | Task 5 |
| UC-1 select two SBOMs on list page → "Compare selected" | — | Task 6 |
| NFR p95 < 1s @ 2000 packages | — | Task 1 (set-based queries), Task 2 (perf test) |
| NFR virtualized lists > 100 rows | — | Task 5 |
| NFR no new DB tables | — | Task 1 (AC) |
| Documentation (New Content) | — | Task 8 (API), Task 9 (UI) |

### Excluded requirements
| Requirement | Missing input preventing planning |
|---|---|
| "Add comparison endpoint to the API latency Grafana dashboard" (Customer Information/Supportability) | No target repository for dashboards/monitoring configuration is present in the Repository Registry or provided inputs. Task 2 adds a `tracing` span so data is available once a dashboard repo is identified. |
| "Monitor for timeouts on large SBOM comparisons (>2000 packages per SBOM)" — alerting part | Same as above: no monitoring/alerting repository provided. Instrumentation (span with timings) is in Task 2; alert rules are excluded. |
| "Both SBOMs must be from the same product/project" — enforcement | Specification is insufficient (no definition of product identity in the SBOM model, and no decision whether to block or warn). Planned as a non-blocking UI warning in Task 4; server-side enforcement excluded pending product-owner decision. |
| "Large SBOM diffs (>1000 package changes) may require pagination or filtering" | Figma explicitly specifies no pagination (virtualization instead) and no filter design exists. Virtualization is planned (Task 5); server-side pagination/filtering of the diff is excluded until a design/spec is provided. |

## Step 4.5 — Workflow mode
**Selected mode: `direct-to-main`.** See `workflow-mode-comment.md` for the full rationale.
- Coordinated schema migrations: none (NFR forbids new tables).
- Breaking API changes: none — the endpoint is new and additive; existing endpoints unchanged.
- Cross-cutting refactors: none.
- Tightly coupled components: the frontend consumes a new endpoint, but the coupling is one-directional and is enforced via Depend links (frontend tasks depend on Task 2), so each PR merged in dependency order leaves `main` of each repository working. The backend endpoint functions independently. The two sides live in separate repositories, so a single feature branch cannot span them.
→ All tasks target `main`; no bookend tasks generated; `workflow:feature-branch` label not applied.

## Step 5 — Epic grouping (by-sub-feature)
| Epic | Summary | Tasks |
|---|---|---|
| Epic 1 | TC-9003: SBOM comparison diff API | Task 1, Task 2 |
| Epic 2 | TC-9003: SBOM comparison UI | Task 3, Task 4, Task 5, Task 6 |
| Epic 3 | TC-9003: Comparison export | Task 7 |
| Epic 4 | TC-9003: Documentation | Task 8, Task 9 |

## Task list
| # | File | Repository | Summary | Depends on |
|---|---|---|---|---|
| 1 | task-1-sbom-diff-model-and-service.md | trustify-backend | Add SBOM comparison model and diff computation service | — |
| 2 | task-2-sbom-compare-endpoint.md | trustify-backend | Add GET /api/v2/sbom/compare endpoint | 1 |
| 3 | task-3-frontend-compare-api-client.md | trustify-ui | Add SBOM comparison API client and useSbomComparison hook | 2 |
| 4 | task-4-frontend-compare-page.md | trustify-ui | Add /sbom/compare page with SBOM selectors and URL-shareable state | 3 |
| 5 | task-5-frontend-diff-sections.md | trustify-ui | Render collapsible diff sections, count badges and critical highlighting | 4 |
| 6 | task-6-frontend-sbom-list-compare-selected.md | trustify-ui | Add SBOM multi-select and "Compare selected" action to SBOM list | 4 |
| 7 | task-7-frontend-export-diff.md | trustify-ui | Export SBOM comparison as JSON or CSV (non-MVP) | 5 |
| 8 | task-8-docs-compare-endpoint.md | trustify-backend | Document GET /api/v2/sbom/compare endpoint | 1, 2 |
| 9 | task-9-docs-comparison-ui-guide.md | trustify-ui | Document the SBOM comparison UI workflow | 4, 5, 6, 7 |

## Step 6 — `additional_fields` for every created issue (Epics and Tasks)
Feature priority = Critical (not "Undefined") → propagated. Feature fixVersions = [RHTPA 1.5.0], `fixVersion scope: both` → propagated.
```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```
Full per-issue creation calls, parents, digests and links: see `task-creation-log.md`.
