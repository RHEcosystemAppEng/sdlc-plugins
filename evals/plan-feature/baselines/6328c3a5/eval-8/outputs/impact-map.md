# Repository Impact Map -- TC-9007

## Shared-Artifact Analysis

**Shared artifact:** Service Catalog record (schema in `src/catalog/store.py`)

### Writers (producers)

| # | Path | Role | In Scope? |
|---|---|---|---|
| W1 | `src/workflows/registration.py` | Initial onboarding -- adds a service to the catalog | Yes |
| W2 | `src/workflows/scheduled_sync.py` | Scheduled provider synchronization | No -- stakeholder excluded |
| W3 | `src/workflows/fallback_import.py` | Fallback data import when sync unavailable | No -- stakeholder excluded |
| W4 | `src/api/on_demand_refresh.py` | Operator-requested refresh via POST /api/catalog/refresh | No -- stakeholder excluded |

### Consumers (readers)

| # | Path | Role | In Scope? |
|---|---|---|---|
| C1 | `src/api/catalog_summary.py` | Summary API -- reads catalog records | Yes |
| C2 | `src/reports/catalog_export.py` | Downloadable report -- reads catalog records | Yes |

---

## catalog-service

### In-scope changes

  changes:
    - Add `ownerGroup` field to the shared catalog record schema in `src/catalog/store.py`; ensure update semantics preserve the current value unless a new one is supplied
    - Update `src/workflows/registration.py` to collect and persist `ownerGroup` during initial service registration
    - Update `src/api/catalog_summary.py` to include `ownerGroup` in its response
    - Update `src/reports/catalog_export.py` to include `ownerGroup` in the downloadable report
    - Add or update tests for schema, registration, summary API, and export

### Unresolved scope -- stakeholder exclusion conflicts with acceptance criteria

**Conflict:** The acceptance criteria require that "every Service Catalog record has an `ownerGroup` value after creation or update" and that consumers display `ownerGroup` "regardless of how that record was populated." However, the stakeholder explicitly excludes the three alternate population paths (scheduled synchronization, fallback import, on-demand refresh). Records populated through these paths will NOT have an `ownerGroup` value, which means the universal criteria cannot be satisfied by registration and display changes alone.

**Excluded writer files and their tests:**

| Excluded writer | Matching test file |
|---|---|
| `src/workflows/scheduled_sync.py` | `tests/workflows/test_scheduled_sync.py` |
| `src/workflows/fallback_import.py` | `tests/workflows/test_fallback_import.py` |
| `src/api/on_demand_refresh.py` | `tests/api/test_on_demand_refresh.py` |

**Scope clarification needed:** Should the acceptance criteria be narrowed to apply only to the registration path (e.g., "every Service Catalog record created through registration has an `ownerGroup` value"), or should the excluded writers be brought into scope so that the universal criteria can be satisfied? Until clarified, the universal acceptance criteria remain unresolved -- the generated tasks cover only the registration path and display consumers and do not claim to satisfy the universal criteria.

---

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. All changes are within a single repository (catalog-service). The schema change adds a new field without breaking existing writers or consumers. Each task (schema, registration, summary API, report) can land independently on `main` without leaving the codebase in a broken state. No coordinated schema migrations, breaking API changes, cross-cutting refactors, or tightly coupled components were identified.

---

## Documentation

A documentation task is required. The feature's Documentation Considerations section specifies "Updates" impact type -- documenting that catalog records may be populated through registration, scheduled synchronization, fallback import, or on-demand refresh, and that all paths use the same catalog contract.
