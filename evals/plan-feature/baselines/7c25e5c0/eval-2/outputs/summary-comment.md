# Plan Summary — TC-9002: Improve search experience

## Tasks Created

| # | Task | Jira Key | Repository |
|---|------|----------|-----------|
| 1 | Add full-text search indexes | (pending creation) | trustify-backend |
| 2 | Improve search relevance scoring | (pending creation) | trustify-backend |
| 3 | Add search filter parameters | (pending creation) | trustify-backend |
| 4 | Search integration tests | (pending creation) | trustify-backend |

## Repositories Affected

- **trustify-backend** — search module (`modules/search/`), common query helpers (`common/src/db/`), migration, entity layer, integration tests

## Architecture Summary

The plan improves the search experience through three layers: a database migration adding PostgreSQL GIN full-text indexes (Task 1), a service-layer refactor using `ts_rank` for relevance scoring (Task 2), and endpoint-level filter parameters (Task 3), validated by comprehensive integration tests (Task 4). All changes target the existing `modules/search/` module and reuse established patterns from `common/src/db/query.rs`.

## Inherited Field Propagation

- **Priority:** `Normal` — inherited from Feature TC-9002. Propagated to all 4 created tasks via `additional_fields: { "priority": {"name": "Normal"} }`.
- **fixVersions:** `RHTPA 1.6.0` — inherited from Feature TC-9002. Propagated to all 4 created tasks via `additional_fields: { "fixVersions": [{"name": "RHTPA 1.6.0"}] }`. The fixVersion scope in Jira Field Defaults is absent, defaulting to `both`, so fixVersions are propagated to tasks.

## Workflow Mode

**Direct-to-main** — no atomicity constraints identified. Each task can land independently.

## Ambiguities Flagged

Five ambiguities were identified in the feature description and documented in the impact map and task descriptions as assumptions pending clarification. See impact-map.md for the full list.

## Excluded Requirements

- **"Better UI" (non-MVP):** excluded — no frontend repository available, no design mockups provided.
