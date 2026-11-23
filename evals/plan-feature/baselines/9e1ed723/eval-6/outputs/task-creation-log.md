# TC-9006 — Jira creation log (simulated; no external calls were made)

Keys are simulated placeholders, in creation order.

## 6a.0 — Epics
| Order | Call | Key | Summary | parent | additional_fields |
|---|---|---|---|---|---|
| 1 | `create_issue(projectKey=TC, issueTypeName=Epic)` | TC-9007 | TC-9006: trustify-backend | TC-9006 | labels=[ai-generated-jira], priority=Major, fixVersions=[RHTPA 1.5.0] |
| 2 | `create_issue(projectKey=TC, issueTypeName=Epic)` | TC-9008 | TC-9006: trustify-ui | TC-9006 | labels=[ai-generated-jira], priority=Major, fixVersions=[RHTPA 1.5.0] |

Epic group mapping: `trustify-backend → TC-9007`, `trustify-ui → TC-9008`.

## 6a — Tasks
Each task: `create_issue(projectKey=TC, issueTypeName=Task, summary, description=<task file body>, parent=<Epic>, additional_fields={"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]})`. Each creation is immediately followed by a re-fetch and a digest comment (see `task-N-digest.md`).

| Task | Key | parent (Epic) | Summary | Digest file |
|---|---|---|---|---|
| 1 | TC-9009 | TC-9007 | Create feature branch TC-9006 from main | task-1-digest.md |
| 2 | TC-9010 | TC-9007 | Add remediation module and GET /api/v2/remediation/summary aggregation endpoint | task-2-digest.md |
| 3 | TC-9011 | TC-9007 | Add GET /api/v2/remediation/by-product per-product remediation breakdown endpoint | task-3-digest.md |
| 4 | TC-9012 | TC-9007 | Add filterable GET /api/v2/remediation/vulnerabilities endpoint for outstanding vulnerabilities | task-4-digest.md |
| 5 | TC-9013 | TC-9008 | Add remediation API models, REST functions, and React Query hooks | task-5-digest.md |
| 6 | TC-9014 | TC-9008 | Add /remediation dashboard page with summary cards and remediation progress chart | task-6-digest.md |
| 7 | TC-9015 | TC-9008 | Add filterable outstanding-vulnerability table (severity, product, status) to /remediation | task-7-digest.md |
| 8 | TC-9016 | TC-9007 | Document the remediation tracking dashboard and remediation API endpoints | task-8-digest.md |
| 9 | TC-9017 | TC-9007 | Merge feature branch TC-9006 to main | task-9-digest.md |

Feature label update (feature-branch mode):
`edit_issue(TC-9006, fields={"labels": ["ai-generated-jira", "workflow:feature-branch"]})`

## 6b — Issue links
**Incorporates (Feature → Epics only, not Tasks):**
- `create_issue_link(link_type="Incorporates", inward=TC-9006, outward=TC-9007)`
- `create_issue_link(link_type="Incorporates", inward=TC-9006, outward=TC-9008)`

**Depend (dependent → dependency):**
| Dependent | Depends on |
|---|---|
| TC-9010 (T2) | TC-9009 (T1) |
| TC-9011 (T3) | TC-9009 (T1), TC-9010 (T2) |
| TC-9012 (T4) | TC-9009 (T1), TC-9010 (T2), TC-9011 (T3) |
| TC-9013 (T5) | TC-9009 (T1), TC-9010 (T2), TC-9011 (T3), TC-9012 (T4) |
| TC-9014 (T6) | TC-9009 (T1), TC-9013 (T5) |
| TC-9015 (T7) | TC-9009 (T1), TC-9013 (T5), TC-9014 (T6) |
| TC-9016 (T8) | TC-9010, TC-9011, TC-9012, TC-9013, TC-9014, TC-9015 (T2–T7) |
| TC-9017 (T9) | TC-9010, TC-9011, TC-9012, TC-9013, TC-9014, TC-9015, TC-9016 (T2–T8) |

## 6c — Summary comment
`add_comment(TC-9006, …)` — see `summary-comment.md`.
