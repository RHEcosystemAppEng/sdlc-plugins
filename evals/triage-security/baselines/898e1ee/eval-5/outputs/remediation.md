# Step 7 — Remediation

## Triage Outcome: Case A — Affected, create remediation task

Versions 2.2.0, 2.2.1, and 2.2.2 ship vulnerable openssl-libs (< 3.0.7-28.el9_4). Since the ecosystem is RPM (system package) and the package origin is **explicit install** (present in rpms.lock.yaml), a single remediation task is created for the Konflux release repo.

## Remediation Task Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

## Implementation Notes

- Update the package version in Dockerfile (dnf install command or package spec)
- If lock file exists: regenerate rpms.lock.yaml


## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

## Jira Issue Creation

```
task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)",
  description: <task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)
```

## Jira Linkage

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: <task-key>,
  type: "Depend"
)
```

## Post-Creation Actions

1. Post description digest comment on the new task
2. Transition TC-8005 to In Progress
3. Assign TC-8005 to current user
4. Add `ai-cve-triaged` label to TC-8005
5. Post summary comment on TC-8005 with version impact table and remediation task link
