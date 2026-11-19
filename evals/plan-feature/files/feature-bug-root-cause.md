<!-- SYNTHETIC TEST DATA — mock Jira Feature with a linked Bug whose root cause lives in an unregistered repository; names, URLs, and identifiers are fictional -->

# Mock Jira Feature Issue

**Key**: TC-9009
**Summary**: Deterministic advisory ordering across API, exports, and UI
**Status**: New
**Priority**: Major
**Fix Versions**: None
**Labels**: ai-generated-jira
**Linked Issues**: TC-9050 (Bug) — Advisory list order changes between requests

---

## Feature Overview

Compliance exports and UI tables must show advisories in a stable, documented order. The order currently changes between requests, which makes exported reports and screenshots non-reproducible.

The requirement originates from Bug TC-9050: users reported that the advisory table reorders rows on refresh. Triage of TC-9050 traced the instability to the shared `advisories()` query builder in `acme-data-client`, which returns rows without an `ORDER BY`. `acme-backend`'s `get_advisories()` service consumes that builder unchanged, and the UI added an in-memory sort as a workaround while the Bug was open.

## Bug TC-9050 — triage findings

- **Observed symptom**: `AdvisoryTable` rows reorder on refresh; `AdvisoryTable.tsx` sorts the fetched list in memory as a workaround.
- **Root cause**: `advisories()` in `acme-data-client` — the shared query builder consumed by `acme-backend` — issues no `ORDER BY`, so the database returns rows in arbitrary order.
- **Fix location**: the shared query builder, so that every consumer (API clients, exports, UI) inherits the ordering there.
- **Registry status**: `acme-data-client` is a shared library and is not in this project's Repository Registry.

## Project Configuration (CLAUDE.md excerpt)

### Repository Registry

| Repository | Role | Path |
|---|---|---|
| acme-ui | React/TypeScript frontend | ${ACME_WS_DIR}/acme-ui |
| acme-backend | Java/Quarkus service | ${ACME_WS_DIR}/acme-backend |

`acme-data-client` (shared query builder library) is not registered.

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| Advisory lists return a stable, documented order from the API (advisory date descending, advisory ID as tiebreaker) | Requested after triage of TC-9050 | Yes |
| The UI advisory table renders rows in the order the API returns them | Removes the in-memory sort added as a workaround | Yes |
| Exported reports preserve the same order as the API | Compliance reproducibility | Yes |

## Acceptance Criteria

- Two consecutive `GET /api/v2/advisory` requests return the same row order.
- Advisory rows are ordered by advisory date descending, with advisory ID as the tiebreaker.
- The UI no longer sorts advisory rows in memory.
- Exported reports match the API order.

## Repository Structure: acme-ui

| Path | Existing behavior |
|---|---|
| `src/pages/advisories/AdvisoryTable.tsx` | Renders the advisory table; sorts the fetched list in memory as a workaround for TC-9050 |
| `src/api/advisories.ts` | Fetches advisory pages from `acme-backend` |
| `src/pages/advisories/__tests__/AdvisoryTable.test.tsx` | Component tests |

## Repository Structure: acme-backend

| Path | Existing behavior |
|---|---|
| `src/main/java/com/acme/advisory/AdvisoryResource.java` | `GET /api/v2/advisory` endpoint |
| `src/main/java/com/acme/advisory/AdvisoryService.java` | `get_advisories()` delegates to the shared `advisories()` query builder |
| `src/test/java/com/acme/advisory/AdvisoryResourceTest.java` | Endpoint tests |
