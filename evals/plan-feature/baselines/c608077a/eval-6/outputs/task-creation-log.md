# TC-9006 — Jira Creation Log (simulated; no external calls made)

Jira keys below are **placeholders** assigned in creation order. They stand in for the keys Jira would return.

Common `additional_fields` for every Epic and Task:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

- priority "Major" comes from the Feature. It is set (not "Undefined"), so it is propagated.
- fixVersions "RHTPA 1.5.0" comes from the Feature. The `fixVersion scope` is `both`, so it is propagated to Epics and Tasks.

## 6a.0 — Epics

| Order | Placeholder key | Call |
|---|---|---|
| 1 | TC-9007 | `jira.create_issue(projectKey="TC", issueTypeName="Epic", summary="TC-9006: trustify-backend", description=<plain-text backend epic description>, parent="TC-9006", additional_fields=<common>)` |
| 2 | TC-9008 | `jira.create_issue(projectKey="TC", issueTypeName="Epic", summary="TC-9006: trustify-ui", description=<plain-text frontend epic description>, parent="TC-9006", additional_fields=<common>)` |

Epic group mapping: `trustify-backend` → TC-9007, `trustify-ui` → TC-9008.

## 6a — Tasks

Each task is created with `issueTypeName="Task"`, `projectKey="TC"`, the description from its `task-N-*.md` file, `parent` set to its Epic, and `additional_fields=<common>`. The digest comment is posted right after each task is created, before any links.

| # | Placeholder key | Summary | Parent (Epic) | Description file | Digest comment file | Digest |
|---|---|---|---|---|---|---|
| 1 | TC-9009 | Add remediation model and aggregation service | TC-9007 | task-1-remediation-model-service.md | task-1-digest.md | sha256-md:3263f1218bfd65edbed2e6ec535773495af6172eb892aa493ed6925dd1750bcb |
| 2 | TC-9010 | Add remediation summary and by-product endpoints | TC-9007 | task-2-remediation-summary-by-product-endpoints.md | task-2-digest.md | sha256-md:38da99d45d9c0f7559dde15be03cdb9ff61f0feaeddd79492fc5fcb274993fd1 |
| 3 | TC-9011 | Add remediation vulnerabilities list and trend endpoints | TC-9007 | task-3-remediation-vulnerabilities-trend-endpoints.md | task-3-digest.md | sha256-md:1eb725f2cdfcd1b1d59f5e3a93eeae9f36e713353b8e69272f3312b214f795f0 |
| 4 | TC-9012 | Add remediation API client, types and React Query hooks | TC-9008 | task-4-remediation-api-client-hooks.md | task-4-digest.md | sha256-md:48ae47308385238afd8106f77e33b8da867fd76584e5c7928c42c20befffc657 |
| 5 | TC-9013 | Create remediation dashboard page with summary cards and trend chart | TC-9008 | task-5-remediation-dashboard-page.md | task-5-digest.md | sha256-md:e8b1a66074bbd227ff99b2cf9d68b788aace8aa6f44191a34f833033d0d2f3d4 |
| 6 | TC-9014 | Add filterable vulnerability table to the remediation dashboard | TC-9008 | task-6-remediation-vulnerability-table.md | task-6-digest.md | sha256-md:06addd1b1f0f0061525c5c8ff40cf643cd2413a32b0f27e5d9121458bb4f583c |
| 7 | TC-9015 | Document remediation dashboard and endpoints | TC-9007 | task-7-remediation-documentation.md | task-7-digest.md | sha256-md:5f05dd48e9a9be0bcbfe37760b282bc591b6a2484bfe58f0016c7dee5e08d9fe |

Digest note: normally the description is fetched back from Jira and hashed with `scripts/sha256-digest.py`. Jira is not available in this eval, so the script was run directly on each task markdown file, which produces the `sha256-md` tag.

The Feature labels are not changed, because the mode is direct-to-main and `workflow:feature-branch` is not needed.

## 6b — Links

Incorporates links (Feature → Epics only):
- `jira.create_issue_link(link_type="Incorporates", inward_issue_key="TC-9006", outward_issue_key="TC-9007")`
- `jira.create_issue_link(link_type="Incorporates", inward_issue_key="TC-9006", outward_issue_key="TC-9008")`

Depend links (dependent → dependency):
- TC-9010 → TC-9009
- TC-9011 → TC-9009, TC-9011 → TC-9010
- TC-9012 → TC-9010, TC-9012 → TC-9011
- TC-9013 → TC-9012
- TC-9014 → TC-9012, TC-9014 → TC-9013
- TC-9015 → TC-9010, TC-9015 → TC-9011, TC-9015 → TC-9013, TC-9015 → TC-9014

Each is `jira.create_issue_link(link_type="Depend", inward_issue_key=<dependent>, outward_issue_key=<dependency>)`.
