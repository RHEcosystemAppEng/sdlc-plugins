# Step 8 — Remediation (Case B: Affected versions exist)

## Triage Decision

Versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream are affected. Remediation tasks are required.

## Ecosystem Classification

openssl-libs is an **RPM** (system package) ecosystem. Per the ecosystem classification table:

| Category | Ecosystems | Remediation tasks per stream |
|---|---|---|
| System package | RPM | **1** — Konflux release repo fix only |

A **single remediation task** is created — not the two-task upstream backport + downstream propagation flow used for source dependency ecosystems (Cargo, npm).

## Remediation Task Description

### Task: Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

The vulnerable RPM package openssl-libs (versions before 3.0.7-28.el9_4) is an explicit install in the Konflux release repo. Versions 2.2.0 (3.0.7-25.el9_3), 2.2.1 (3.0.7-27.el9_4), and 2.2.2 (retag of 2.2.1) ship the vulnerable version.

Advisory: https://access.redhat.com/errata/RHSA-2026:4021

## Implementation Notes

- Package origin: explicit install (present in rpms.lock.yaml)
- Update the openssl-libs package spec in rpms.in.yaml / rpms.lock.yaml to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml if the project uses rpms.in.yaml as the input spec
- Verify the Konflux build pipeline triggers successfully after the update
- Note: versions 2.2.3 and 2.2.4 already ship 3.0.7-28.el9_4 — no action needed for those versions

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

### Proposed Jira API Call

```python
task = jira.create_issue(
  projectKey="TC",
  issueTypeName="Task",
  summary="Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)",
  description=<system-package-task-description>,
  labels=["ai-generated-jira", "Security", "CVE-2026-40215"]
)
```

### Post-Creation Steps

1. **Description digest**: Re-fetch the task description from Jira after `create_issue`, compute SHA-256 digest using `scripts/sha256-digest.py`, and post a digest comment with marker `[sdlc-workflow] Description digest: <tagged-digest>` before creating issue links.

2. **Jira linkage**:
   ```
   jira.create_link(inwardIssue=TC-8005, outwardIssue=<task-key>, type="Depend")
   ```

3. **Transition** TC-8005 to In Progress.

4. **Add ai-cve-triaged label** to TC-8005.

5. **Post-triage summary comment** on TC-8005 documenting the version impact table, Affects Versions correction, and remediation task created.

## Note on Task Count

This remediation creates exactly **1 task** for the RPM ecosystem — the Konflux release repo fix. Unlike source dependency ecosystems (Cargo, npm) which create 2 tasks (upstream backport + downstream propagation), RPM system packages are fixed directly in the Konflux release repo. There is no upstream source repository step for system packages.
