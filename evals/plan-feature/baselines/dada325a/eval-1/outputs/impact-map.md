# TC-9001 — Repository Impact Map and Planning Log

Feature: **TC-9001 — Add advisory severity aggregation endpoint**
Skill: sdlc-workflow/plan-feature v0.13.10 (eval run, offline: no Jira/Figma/Serena access; all Jira writes captured as files)

---

## Step 0 — Project Configuration validation

- Repository Registry: present (1+ entries). PASS
- Jira Configuration: Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`, Feature issue type ID `10142`. PASS
- Code Intelligence: present. No Serena instances are configured, so analysis uses the fallback path (Read/Glob/Grep over the supplied repository structure).

## Step 1 — Feature extraction

| Field | Value |
|---|---|
| Title | Add advisory severity aggregation endpoint |
| Priority | Major (set, so it is propagated) |
| fixVersions | `RHTPA 1.5.0` (non-empty) |
| Labels | ai-generated-jira |
| Figma links | None |
| Linked issues | None |
| Documentation signals | Doc impact type **Updates** — add the endpoint to the REST API reference. User purpose: API consumers need the endpoint path, parameters, and response shape. Reference: the existing SBOM advisory endpoints documentation. |

**Step 1.5 (parent link):** the Feature has no parent. This offline run cannot prompt the user, so the step was skipped. It is optional.

## Step 2 — Figma

No Figma URL was passed as an argument or found in the description, so the step was skipped. This is a backend-only feature.

## Step 2.5 — Issue type discovery

`jira.get_project_issue_types` could not be called (no external service access in this eval). CLAUDE.md `## Hierarchy Configuration` sets **Default epic grouping strategy: by-sub-feature**.

- **Applied (offline fallback):** no level-1 type could be confirmed, so the plan uses graceful degradation to Feature → Task (constraint §1.64/§1.80). Tasks get no `parent`, and "Incorporates" links go Feature → Task.
- **If a level-1 "Epic" type is discovered at creation time**, use the by-sub-feature grouping below (proposed, pending user approval):

| Epic summary | Tasks |
|---|---|
| `TC-9001: Advisory severity summary API` | Task 1, Task 2, Task 3 |
| `TC-9001: Documentation and feature validation` | Task 4, Task 5, Task 6 |

## Step 3 — Repository analysis (trustify-backend)

**Relevant modules and files (from the repository structure):**
- SBOM domain: `modules/fundamental/src/sbom/{model,service,endpoints}/`. The new endpoint lives under `/api/v2/sbom`. Route registration is in `endpoints/mod.rs`, and `SbomService` is in `service/sbom.rs`.
- Advisory domain: `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary` with a `severity` field)
- Data: `entity/src/sbom_advisory.rs` (SBOM-Advisory join table) and `entity/src/advisory.rs`. The "no new tables" NFR is met by aggregating over these.
- Ingestion (cache invalidation producers): `modules/ingestor/src/graph/advisory/mod.rs` (parse/store/**correlate**), `modules/ingestor/src/graph/sbom/mod.rs` (parse/store/link packages), `modules/ingestor/src/service/mod.rs` (`IngestorService`)
- Shared: `common/src/error.rs` (`AppError`), `common/src/db/query.rs` (query helpers), `common/src/model/paginated.rs` (not used: the summary is a single object, not a list)
- Server wiring: `server/src/main.rs`
- Tests: `tests/api/sbom.rs` (integration tests against PostgreSQL)

**CONVENTIONS.md:** present at the repository root. The conventions applied, taken from the repository's documented key conventions:
- §Module pattern
- §Error handling
- §Endpoint registration
- §Response types
- §Query helpers
- §Testing
- §Caching

All are scoped to Rust (`.rs`) sources. They are applied per task with `Applies:` rationales.

**Documentation files:** `README.md`, `CONVENTIONS.md`. No dedicated `docs/api/` or OpenAPI spec appears in the analyzed structure. The Documentation task (Task 4) leaves the choice of doc file to the implementer.

**Testing readiness template:** `docs/testing-readiness.md` was found. It defines 2 categories, **Smoke Tests** and **Performance Benchmarks**, which become Task 5 and Task 6.

**Eval infrastructure:** not applicable. No task modifies a `plugins/*/skills/*/SKILL.md` file.

**Reuse / duplication scan:**
- `SbomService` fetch: reused for the 404 existence check.
- `AdvisorySummary.severity`: its severity type is reused for bucketing and for threshold parsing.
- `sbom_advisory` entity: the aggregation source.
- `tower-http` cache configuration in route builders: reused for caching.
- `common/src/db/query.rs`: reused for filtering.
- The Feature names an existing `GET /api/v2/sbom/{id}/advisories` endpoint that **does not appear in the analyzed repository structure**. Task 1 tells the implementer to locate it and reuse its join logic if it exists.

### Shared-artifact producer/consumer trace — cached advisory summary

The MVP requirement "cached for 5 minutes" and the NFR "cache invalidation when new advisories are linked to an SBOM" make the cached summary a shared artifact. Its source data is the `sbom_advisory` rows.

| Role | Path | Kind | Coverage |
|---|---|---|---|
| Consumer | `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` (new) | Reads cache, then the aggregate query | Tasks 1, 2, 3; tests in `tests/api/sbom.rs` |
| Producer (primary) | `modules/ingestor/src/graph/advisory/mod.rs` | Advisory correlate writes `sbom_advisory` | Task 2: invalidation plus a test |
| Producer (verify) | `modules/ingestor/src/graph/sbom/mod.rs` | SBOM ingest or re-ingest. The structure says "link packages", so it may or may not write or delete `sbom_advisory`. | Task 2: verification step, conditional invalidation, and a conditional test |
| Entry points (scheduled, on-demand/API) | `modules/ingestor/src/service/mod.rs` (`IngestorService`) | Calls the graph producers | Task 2: wiring plus an on-demand-path test |
| Wiring | `server/src/main.rs` | Shares one cache instance between the fundamental and ingestor modules | Task 2 |

There is no scope exclusion conflicting with these paths. All of them are in Task 2.

## Repository Impact Map

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary response model ({critical, high, medium, low, total}) to the SBOM module
    - Add SbomService aggregation over sbom_advisory + advisory (single grouped query, COUNT DISTINCT advisory id) with SBOM existence check
    - Add and register GET /api/v2/sbom/{id}/advisory-summary returning 200 with counts, or 404 for unknown SBOM
    - Cache advisory-summary responses for 5 minutes using the existing cache infrastructure (keyed per SBOM; 404s not cached)
    - Invalidate an SBOM's cached summary from every ingestion path that links advisories to it (advisory correlate; SBOM ingest if it writes sbom_advisory; scheduled and on-demand IngestorService paths), wired through server/src/main.rs
    - Add optional ?threshold=<critical|high|medium|low> filter (non-MVP), included in the cache key, 400 on invalid values
    - Add integration tests in tests/api/sbom.rs for counts, dedup, 404, caching, invalidation, threshold
    - Update REST API reference documentation with the new endpoint
    - Feature-level validation: Smoke Tests and Performance Benchmarks per docs/testing-readiness.md
```

### Excluded requirements

| Requirement | Missing input that prevents planning |
|---|---|
| "Add the new endpoint to the API latency Grafana dashboard" (Customer Information/Supportability) | No monitoring or dashboard repository (Grafana dashboard definitions) is in the Repository Registry, and the analyzed `trustify-backend` structure contains no dashboard or alerting configuration. Provide the repository that owns the Grafana dashboards to plan this. |
| "Alert if p95 exceeds 500ms" (Customer Information/Supportability) | Same gap: no alerting-rules repository or configuration location is available. Task 6 measures against the 500ms threshold, but creating the alert rule cannot be planned without the target repository. |

### Open questions / assumptions (flagged for the engineer)

1. **`total` semantics:** the plan assumes `total` = the number of distinct advisories linked to the SBOM, including advisories with null or unrecognized severity, which count toward `total` only. Please confirm.
2. **Threshold semantics:** "filter counts above a severity" is read as *at or above*, because UC-2 expects `?threshold=critical` to return the critical count. Levels below the threshold are omitted, and `total` = the sum of the included levels. Please confirm.
3. **Cache infrastructure:** `tower-http` caching may be HTTP-header-only (client/proxy caching). If so, server-side invalidation cannot purge copies held by clients, and Task 2 needs a server-side keyed TTL cache. Task 2 requires user confirmation before adding any new crate dependency.
4. **Existing `GET /api/v2/sbom/{id}/advisories`:** this endpoint is referenced by the Feature but absent from the analyzed structure. Verify where it lives before implementing Task 1.

## Step 4.5 — Workflow mode decision

**Mode: `direct-to-main`**

Atomicity indicators evaluated:
1. Coordinated schema migrations: **none**. No new tables or migrations (NFR).
2. Breaking API changes: **none**. The endpoint is new and additive. Task 3 adds an optional parameter that is backward compatible.
3. Cross-cutting refactors: **none**.
4. Tightly coupled feature components: **none**. Backend only. The frontend widget is not part of this plan, and each task leaves `main` working: Task 1 serves correct uncached counts; Task 2 adds caching and invalidation together, so stale data is never served; Task 3 is an optional parameter.

Task dependencies (1 → 2 → 3) are ordering dependencies only. Merging any prefix leaves `main` correct. All tasks have Target Branch `main`. No bookend tasks are generated, and no `workflow:feature-branch` label is applied.

## Step 5 — Generated tasks

| # | File | Summary | Type | Depends on |
|---|---|---|---|---|
| 1 | `task-1-advisory-summary-endpoint.md` | Add GET /api/v2/sbom/{id}/advisory-summary endpoint | Implementation (MVP) | — |
| 2 | `task-2-summary-cache-and-invalidation.md` | Cache advisory summary for 5 minutes with ingestion-driven invalidation | Implementation (MVP) | 1 |
| 3 | `task-3-threshold-filter.md` | Add optional threshold filter to advisory summary endpoint | Implementation (non-MVP) | 1, 2 |
| 4 | `task-4-api-reference-docs.md` | Document advisory summary endpoint in REST API reference | Documentation | 1, 2, 3 |
| 5 | `task-5-smoke-tests.md` | Smoke tests for advisory severity summary feature | Testing (Smoke Tests) | 1, 2, 3 |
| 6 | `task-6-performance-benchmarks.md` | Performance benchmarks for advisory severity summary endpoint | Testing (Performance Benchmarks) | 1, 2, 3 |

Fail-open risk coverage applied:
- Task 1: an unknown SBOM must return 404, never 200 with all zeros.
- Task 2: invalidation must not be a silent no-op; ingestion fails if invalidation cannot run. 404s are not cached.
- Task 3: an invalid threshold returns 400, never unfiltered counts.

Each has an Acceptance Criterion, a Test Requirement, and an Implementation Note at the gate site.

## Step 6 — Task creation log (simulated; no Jira calls made)

### 6a.0 Epics
Skipped. No level-1 type was confirmed (see Step 2.5).

### 6a `additional_fields` for every created task (Tasks 1–6)

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

- `priority`: the Feature priority is "Major" (not "Undefined"), so it is **propagated**.
- `fixVersions`: the Feature has `RHTPA 1.5.0`, and CLAUDE.md `fixVersion scope: both` includes tasks, so it is **propagated**.
- `parent`: omitted (no Epics).
- Issue type: Task (level 0; resolved at creation time through issue type discovery).
- Project: `TC`.

| # | Summary | Placeholder key | Digest comment file | Digest |
|---|---|---|---|---|
| 1 | Add GET /api/v2/sbom/{id}/advisory-summary endpoint | TC-9001-T1 | `task-1-digest.md` | `sha256-md:63fecabb8647468956241980c8065c24282bd59cc64ee532833ef5a3adb61ddd` |
| 2 | Cache advisory summary for 5 minutes with ingestion-driven invalidation | TC-9001-T2 | `task-2-digest.md` | `sha256-md:bcd018209e86416ec42db6df772c3b4d44c9ac6fd6e19a6390f2b024a6cdac61` |
| 3 | Add optional threshold filter to advisory summary endpoint | TC-9001-T3 | `task-3-digest.md` | `sha256-md:032521851ad133078b14c942a4abbe6febe6c1c7a557002233c8fbd26766a969` |
| 4 | Document advisory summary endpoint in REST API reference | TC-9001-T4 | `task-4-digest.md` | `sha256-md:7d70699c882dcd3ba14070a6d21fc7eccea1d4b1b00e82374b459f3923e95dca` |
| 5 | Smoke tests for advisory severity summary feature | TC-9001-T5 | `task-5-digest.md` | `sha256-md:f2a4f5762afd37f9a8e39eddb639f236cc5e4208cd7c73d9fd5a0ffc0ee3d03a` |
| 6 | Performance benchmarks for advisory severity summary endpoint | TC-9001-T6 | `task-6-digest.md` | `sha256-md:0ee4ace6e63b26775ad66e79a96e73c1acd459298c1e12256365e23dfda1163d` |

These digests were computed with `scripts/sha256-digest.py` over the local task description files. Jira could not be reached to re-fetch the stored description. In a live run, re-fetch each task after creation and recompute the digest from the persisted description.

### 6b Issue links (to create after all tasks exist)

**Incorporates (Feature → Task):** TC-9001 → T1, T2, T3, T4, T5, T6

**Depend (dependent → dependency):**

| Dependent | Depends on |
|---|---|
| T2 | T1 |
| T3 | T1 |
| T3 | T2 |
| T4 | T1 |
| T4 | T2 |
| T4 | T3 |
| T5 | T1 |
| T5 | T2 |
| T5 | T3 |
| T6 | T1 |
| T6 | T2 |
| T6 | T3 |

### Jira comments written as files
- `impact-map-comment.md`: impact map plus workflow mode decision, posted on TC-9001 (Steps 4 and 4.5)
- `task-N-digest.md`: one standalone digest comment per task (Step 6a)
- `summary-comment.md`: plan summary, posted on TC-9001 (Step 6c)
