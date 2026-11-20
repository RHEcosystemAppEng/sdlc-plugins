# Task Creation Log — TC-9005 (simulated; no Jira calls made)

Jira keys below are placeholders (`<EPIC-A>`, `<TASK-1>`, ...) because no issues were actually created.

## Step 6a.0 — Epics

Every Epic is created with `issueTypeName="Epic"`, `parent=TC-9005` and this `additional_fields`:
`{"labels": ["ai-generated-jira"], "priority": {"name": "High"}, "fixVersions": [{"name": "RHTPA 2.0.0"}]}`

| Placeholder | Summary | Description (plain text) |
|---|---|---|
| `<EPIC-A>` | TC-9005: Advisory status schema and entity migration | Atomic migration replacing the advisory_status lookup table with the advisory_status_enum column (Task 2), and the SeaORM entity updates for the new schema (Task 3). |
| `<EPIC-B>` | TC-9005: Advisory query and ingestion updates | Removes the advisory_status join from advisory and search queries (Task 4). Makes the ingestion pipeline write enum values directly (Task 5). |
| `<EPIC-C>` | TC-9005: Feature branch lifecycle and documentation | Feature branch bookends: create TC-9005 (Task 1) and merge it to main (Task 7). Also covers the internal architecture documentation update (Task 6). |

## Step 6a — Tasks

Every Task is created with `issueTypeName="Task"`, project `TC` and this `additional_fields`:
`{"labels": ["ai-generated-jira"], "priority": {"name": "High"}, "fixVersions": [{"name": "RHTPA 2.0.0"}]}`

| # | Placeholder | Summary | Parent (Epic) | Target Branch | Description file | Digest file |
|---|---|---|---|---|---|---|
| 1 | `<TASK-1>` | Create feature branch TC-9005 from main | `<EPIC-C>` | main | task-1-create-feature-branch.md | task-1-digest.md |
| 2 | `<TASK-2>` | Add migration converting advisory_status lookup table to advisory_status_enum column | `<EPIC-A>` | TC-9005 | task-2-advisory-status-enum-migration.md | task-2-digest.md |
| 3 | `<TASK-3>` | Update SeaORM advisory entity to use AdvisoryStatus enum column | `<EPIC-A>` | TC-9005 | task-3-update-seaorm-advisory-entity.md | task-3-digest.md |
| 4 | `<TASK-4>` | Replace advisory_status joins with advisory.status column in advisory and search queries | `<EPIC-B>` | TC-9005 | task-4-update-advisory-queries.md | task-4-digest.md |
| 5 | `<TASK-5>` | Write advisory status enum directly in advisory ingestion pipeline | `<EPIC-B>` | TC-9005 | task-5-update-advisory-ingestion.md | task-5-digest.md |
| 6 | `<TASK-6>` | Update internal architecture documentation for advisory status enum migration | `<EPIC-C>` | TC-9005 | task-6-update-architecture-docs.md | task-6-digest.md |
| 7 | `<TASK-7>` | Merge feature branch TC-9005 to main | `<EPIC-C>` | main | task-7-merge-feature-branch.md | task-7-digest.md |

### Description digests

The Jira description is everything in each task file after the first `# Task N — ...` title line. Digests were computed with `python3 scripts/sha256-digest.py` on that text. In a real run the description would be fetched back from Jira first and hashed in its persisted form. Each digest is posted as a standalone comment, with no footnote, immediately after the task is created:

- Task 1: `[sdlc-workflow] Description digest: sha256-md:7e1649d1bc5f908764b159b3586da3661ba17dc3822c39814614f6d3636bad40`
- Task 2: `[sdlc-workflow] Description digest: sha256-md:f8bed44cfe41b6a880806ed0f6c2547f50375b40c25512d0304eeb27dff19078`
- Task 3: `[sdlc-workflow] Description digest: sha256-md:b1443859a4c5850fa93c8e9c23f4637d14595b1e98612826bc4f65249582b8f4`
- Task 4: `[sdlc-workflow] Description digest: sha256-md:ce1b3db7d27e81885b7c1843b7088a26c86dd7f9a4e37fe1dc014477c606b824`
- Task 5: `[sdlc-workflow] Description digest: sha256-md:cbe002121c01c0f85870bf7ec7c143951bb9b9b7b74fe27f6af7c415b474f93f`
- Task 6: `[sdlc-workflow] Description digest: sha256-md:f1005b8fd5267d6c05ce9a5a539a0a3a3c0785ff154f335baf814cd39dc2f9d8`
- Task 7: `[sdlc-workflow] Description digest: sha256-md:04f7728d19d31467553acb11ab81850b39b6bb7bdc2a7d5bbfc83237a690f29b`

### Feature label update

```
jira.edit_issue("TC-9005", fields={"labels": ["ai-generated-jira", "workflow:feature-branch"]})
```

## Step 6b — Issue links

**Incorporates** (Feature → Epic, because Epics are available):
- TC-9005 incorporates `<EPIC-A>`
- TC-9005 incorporates `<EPIC-B>`
- TC-9005 incorporates `<EPIC-C>`

**Depend** links (inward = dependent task, outward = the task it depends on):

| Dependent | Depends on |
|---|---|
| Task 2 | Task 1 |
| Task 3 | Task 1, Task 2 |
| Task 4 | Task 1, Task 3 |
| Task 5 | Task 1, Task 3 |
| Task 6 | Task 1, Task 2, Task 3, Task 4, Task 5 |
| Task 7 | Task 2, Task 3, Task 4, Task 5, Task 6 |
