# Task Creation Log — TC-9006 (simulated; no Jira calls made)

Jira keys are simulated placeholders. Every comment and digest that would be posted is also written as its own file in this directory.

## 6a.0 — Epics

| Order | Call | Result |
|---|---|---|
| 1 | `create_issue(projectKey="TC", issueTypeName="Epic", summary="TC-9006: trustify-backend", description="Backend work for TC-9006: new remediation module with summary, by-product and filterable vulnerability list endpoints (Tasks 1–3), plus feature documentation (Task 7).", parent="TC-9006", additional_fields={"labels":["ai-generated-jira"],"priority":{"name":"Major"},"fixVersions":[{"name":"RHTPA 1.5.0"}]})` | TC-9010 |
| 2 | `create_issue(projectKey="TC", issueTypeName="Epic", summary="TC-9006: trustify-ui", description="Frontend work for TC-9006: remediation API types/hooks, /remediation dashboard page with summary cards and progress chart, and filterable vulnerability table (Tasks 4–6).", parent="TC-9006", additional_fields={"labels":["ai-generated-jira"],"priority":{"name":"Major"},"fixVersions":[{"name":"RHTPA 1.5.0"}]})` | TC-9011 |

Epic group mapping: `trustify-backend` → TC-9010, `trustify-ui` → TC-9011

## 6a — Tasks

Every task uses `issueTypeName="Task"` and `additional_fields={"labels":["ai-generated-jira"],"priority":{"name":"Major"},"fixVersions":[{"name":"RHTPA 1.5.0"}]}`.

| Task | Summary | Description file | parent (Epic) | Key | Digest comment file |
|---|---|---|---|---|---|
| 1 | Add remediation module and summary endpoint | task-1-remediation-summary-endpoint.md | TC-9010 | TC-9012 | task-1-digest.md |
| 2 | Add remediation by-product endpoint | task-2-remediation-by-product-endpoint.md | TC-9010 | TC-9013 | task-2-digest.md |
| 3 | Add remediation vulnerability list endpoint | task-3-remediation-vulnerability-list-endpoint.md | TC-9010 | TC-9014 | task-3-digest.md |
| 4 | Add remediation API client types and React Query hooks | task-4-remediation-api-client-and-hooks.md | TC-9011 | TC-9015 | task-4-digest.md |
| 5 | Create remediation dashboard page with summary cards and progress chart | task-5-remediation-dashboard-page.md | TC-9011 | TC-9016 | task-5-digest.md |
| 6 | Add filterable remediation vulnerability table | task-6-remediation-vulnerability-table.md | TC-9011 | TC-9017 | task-6-digest.md |
| 7 | Document remediation dashboard and aggregation endpoints | task-7-remediation-documentation.md | TC-9010 | TC-9018 | task-7-digest.md |

Digest comments are posted right after each task is created, before any links. Each digest was computed with `scripts/sha256-digest.py` over the task description in markdown, which is what the MCP re-fetch returns. Format: `sha256-md:<64 hex>`.

## 6b — Links

**Incorporates (Feature → Epic):**
- `create_issue_link(link_type="Incorporates", inward_issue_key="TC-9006", outward_issue_key="TC-9010")`
- `create_issue_link(link_type="Incorporates", inward_issue_key="TC-9006", outward_issue_key="TC-9011")`

No Incorporates links go from the Feature to individual Tasks. Tasks belong to the hierarchy through their Epic `parent`.

**Depend (dependent → dependency):**
- TC-9013 → TC-9012
- TC-9014 → TC-9012, TC-9013
- TC-9015 → TC-9012, TC-9013, TC-9014
- TC-9016 → TC-9015
- TC-9017 → TC-9015, TC-9016
- TC-9018 → TC-9012, TC-9013, TC-9014, TC-9015, TC-9016, TC-9017

## Feature label

None. The mode is direct-to-main, so `workflow:feature-branch` is not added.
