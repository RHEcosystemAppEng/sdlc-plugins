# Task Creation Log — TC-9001 (simulated; no Jira calls made)

## Type-to-role mapping (Step 2.5, assumed)
- Feature: Feature (ID: 10142, level: 2) — from CLAUDE.md
- Epic: not discovered (assumed unavailable offline) → no Epics created; Feature → Task hierarchy
- Task: Task (level: 0)

## additional_fields applied to every created task
```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```
- priority: inherited from the Feature ("Major", not "Undefined") → propagated
- fixVersions: the Feature has ["RHTPA 1.5.0"] and CLAUDE.md `fixVersion scope: both` → propagated
- parent: omitted (no Epics)

## Issues to create (summary → placeholder key → digest)
| # | Summary | Key | Digest |
|---|---|---|---|
| 1 | Add advisory severity aggregation model and service method | TC-NEW-1 | sha256-md:a89188ceea048131bd3d06bc8f677c3b3c3a4d65c443107cb3a225c8b4e0eee1 |
| 2 | Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching | TC-NEW-2 | sha256-md:2e064ebcb1c28a7aaf9e8d3a06070606d1e740682382cdb43d69ae362d0338c3 |
| 3 | Invalidate cached advisory summaries on advisory ingestion | TC-NEW-3 | sha256-md:c0448f72121ccd79c509a9df46c3c150cbda58e29b063c228def9118f7998e57 |
| 4 | Add optional threshold query parameter to advisory-summary endpoint | TC-NEW-4 | sha256-md:ac15f7bbc3077d2d7ae5bf96215ba91e6e31e30b692f2f88b08f3d30dd8071c7 |
| 5 | Document advisory-summary endpoint in REST API reference | TC-NEW-5 | sha256-md:6518a43337e4d29f093d623f96197c043991f5487e83f6b5231b774140f82349 |
| 6 | Smoke Tests for advisory severity aggregation endpoint | TC-NEW-6 | sha256-md:86843c89b5fedb4813c14e40b86e863474bc6ef82113d1ed194ed5f8608552e7 |
| 7 | Performance Benchmarks for advisory severity aggregation endpoint | TC-NEW-7 | sha256-md:368fbe33979ded63290046e07392cf5f090f651e55ed19df258768342d3300c4 |

Digests were computed with `scripts/sha256-digest.py` over the markdown description files (`sha256-md`). In a live run they are computed over the description re-fetched from Jira after creation. Each digest comment is in `task-N-digest.md`.

## Links (Step 6b)
- Incorporates: TC-9001 → TC-NEW-1 … TC-NEW-7
- Depend: 2→1; 3→2; 4→2; 5→2,3,4; 6→1,2,3,4; 7→1,2,3,4
