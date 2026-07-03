# Task Creation Log

Documents all Jira operations that would be performed in Step 6.

## Step 2.5 — Issue Type Discovery

Type-to-role mapping (simulated for eval):
- Feature: Feature (ID: 10142, level: 2)
- Epic: Epic (ID: 10000, level: 1)
- Task: Task (ID: 10003, level: 0)

## Step 6a.0 — Create Epics

### Epic 1: TC-9004: License compliance engine

```
jira.create_issue(
  projectKey="TC",
  issueTypeName="Epic",
  summary="TC-9004: License compliance engine",
  description="Core model structs, policy configuration, and service logic for license aggregation and compliance checking against configurable policy.",
  parent="TC-9004",
  additional_fields={
    "labels": ["ai-generated-jira"],
    "priority": {"name": "Major"},
    "fixVersions": [{"name": "RHTPA 1.5.0"}]
  }
)
```

### Epic 2: TC-9004: License report API

```
jira.create_issue(
  projectKey="TC",
  issueTypeName="Epic",
  summary="TC-9004: License report API",
  description="REST endpoint, integration tests, and API documentation for the license compliance report feature.",
  parent="TC-9004",
  additional_fields={
    "labels": ["ai-generated-jira"],
    "priority": {"name": "Major"},
    "fixVersions": [{"name": "RHTPA 1.5.0"}]
  }
)
```

## Step 6a — Create Tasks

All tasks use the following additional_fields:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

Field propagation rationale:
- **labels**: "ai-generated-jira" — always included per constraint 4.8
- **priority**: "Major" — inherited from Feature TC-9004 (priority is set and not "Undefined")
- **fixVersions**: "RHTPA 1.5.0" — inherited from Feature TC-9004 (Feature has fixVersions set; no fixVersion scope setting in Jira Field Defaults, defaulting to "both" which includes tasks)

### Task 1 — Add license report model and policy configuration
- Parent: Epic 1 (TC-9004: License compliance engine)
- Type: Task
- additional_fields as above

### Task 2 — Add license compliance service for SBOM packages
- Parent: Epic 1 (TC-9004: License compliance engine)
- Type: Task
- additional_fields as above

### Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint
- Parent: Epic 2 (TC-9004: License report API)
- Type: Task
- additional_fields as above

### Task 4 — Add integration tests for license report endpoint
- Parent: Epic 2 (TC-9004: License report API)
- Type: Task
- additional_fields as above

### Task 5 — Document license report endpoint and policy configuration
- Parent: Epic 2 (TC-9004: License report API)
- Type: Task
- additional_fields as above

## Step 6a — Digest Comments

After each task creation, a description digest comment would be posted per the description-digest-protocol.md. See task-N-digest.md files for details.

## Step 6b — Issue Links

### Feature "Incorporates" links (Feature -> Epics, since Epics are available)

```
jira.create_issue_link(type="Incorporates", inward="TC-9004", outward=<epic-1-key>)
jira.create_issue_link(type="Incorporates", inward="TC-9004", outward=<epic-2-key>)
```

### Task "Depends on" links

```
jira.create_issue_link(type="Depend", inward=<task-2-key>, outward=<task-1-key>)
  # Task 2 depends on Task 1

jira.create_issue_link(type="Depend", inward=<task-3-key>, outward=<task-2-key>)
  # Task 3 depends on Task 2

jira.create_issue_link(type="Depend", inward=<task-4-key>, outward=<task-3-key>)
  # Task 4 depends on Task 3

jira.create_issue_link(type="Depend", inward=<task-5-key>, outward=<task-3-key>)
  # Task 5 depends on Task 3

jira.create_issue_link(type="Depend", inward=<task-5-key>, outward=<task-4-key>)
  # Task 5 depends on Task 4
```

## Step 6c — Summary Comment

See summary-comment.md for the feature summary comment posted on TC-9004.
