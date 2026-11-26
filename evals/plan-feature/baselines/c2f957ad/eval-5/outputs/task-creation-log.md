# TC-9005 — Task Creation Log (simulated Step 6)

Jira was not contacted (offline eval). Placeholder keys `TASK-1` … `TASK-7` stand for the keys Jira would return.

## 6a.0 — Epics

Skipped. No level-1 (Epic) issue type was discovered in Step 2.5, so the hierarchy degrades gracefully to Feature -> Task. Tasks are created without an Epic parent.

## 6a — Created tasks

Every task: `projectKey=TC`, `issueType=Task`, with:

```json
additional_fields = {
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

| # | Key | Summary | Description file | labels | priority | fixVersions | Digest comment |
|---|---|---|---|---|---|---|---|
| 1 | TASK-1 | Create feature branch TC-9005 from main | `task-1-create-feature-branch.md` | ai-generated-jira | High | RHTPA 2.0.0 | `task-1-digest.md` |
| 2 | TASK-2 | Add atomic migration replacing advisory_status table with advisory_status_enum column | `task-2-advisory-status-enum-migration.md` | ai-generated-jira | High | RHTPA 2.0.0 | `task-2-digest.md` |
| 3 | TASK-3 | Update SeaORM advisory entity to use AdvisoryStatus enum | `task-3-update-seaorm-advisory-entity.md` | ai-generated-jira | High | RHTPA 2.0.0 | `task-3-digest.md` |
| 4 | TASK-4 | Update advisory queries to use status enum column instead of join | `task-4-advisory-queries-use-status-column.md` | ai-generated-jira | High | RHTPA 2.0.0 | `task-4-digest.md` |
| 5 | TASK-5 | Update advisory ingestion to write status enum directly | `task-5-ingestion-write-status-enum.md` | ai-generated-jira | High | RHTPA 2.0.0 | `task-5-digest.md` |
| 6 | TASK-6 | Update internal architecture docs for advisory status enum | `task-6-update-architecture-docs.md` | ai-generated-jira | High | RHTPA 2.0.0 | `task-6-digest.md` |
| 7 | TASK-7 | Merge feature branch TC-9005 to main | `task-7-merge-feature-branch.md` | ai-generated-jira | High | RHTPA 2.0.0 | `task-7-digest.md` |

### Description digests

Each digest was computed with `python3 scripts/sha256-digest.py` over the task description file. This stands in for the description Jira would return on re-fetch. Each digest is posted as a standalone comment with no footnote.

| Task | Digest comment |
|---|---|
| TASK-1 | `[sdlc-workflow] Description digest: sha256-md:3870bd40b45a09478a4970273385a9c1652fd4035072216202d6b7621b59d829` |
| TASK-2 | `[sdlc-workflow] Description digest: sha256-md:d666f0c18de2e6e04d0441967b5ca4a56d024317148068dccd437a69565c4adc` |
| TASK-3 | `[sdlc-workflow] Description digest: sha256-md:f41058ab38ebd26db0713c4bc96c9a4227e505558811311d910ff124eb8198a0` |
| TASK-4 | `[sdlc-workflow] Description digest: sha256-md:b4d66ae6305f90ae1c3d9c4b613dcbbe337ca2a07b8e8c1adb548c810ce0b6e1` |
| TASK-5 | `[sdlc-workflow] Description digest: sha256-md:c6a2066dc1e15f4509b9f09edd04d7eaad9c9fb8359fa7c1ec4bbfc9caaabbd9` |
| TASK-6 | `[sdlc-workflow] Description digest: sha256-md:0962b8b8d55d08eb5874961fcdae29defdbe01dd6594f852f13fbc8d97234dc1` |
| TASK-7 | `[sdlc-workflow] Description digest: sha256-md:ec14fd911d4e3fda7844f313b23f5908cd6d090880b01c9abfa82e647ed2fa51` |

### Feature label update (feature-branch mode)

```
jira.edit_issue("TC-9005", fields={"labels": ["ai-generated-jira", "workflow:feature-branch"]})
```

The existing label `ai-generated-jira` is kept and `workflow:feature-branch` is appended.

## 6b — Issue links

**Feature incorporates Tasks** (no Epics): `link_type="Incorporates"`, inward `TC-9005`:
- TC-9005 -> TASK-1, TASK-2, TASK-3, TASK-4, TASK-5, TASK-6, TASK-7

**Depend links** (`link_type="Depend"`, inward = dependent, outward = dependency):

| Dependent | Depends on |
|---|---|
| TASK-2 | TASK-1 |
| TASK-3 | TASK-1, TASK-2 |
| TASK-4 | TASK-1, TASK-3 |
| TASK-5 | TASK-1, TASK-3 |
| TASK-6 | TASK-2, TASK-3, TASK-4, TASK-5 |
| TASK-7 | TASK-2, TASK-3, TASK-4, TASK-5, TASK-6 |

## 6c — Feature summary comment

See `summary-comment.md`.
