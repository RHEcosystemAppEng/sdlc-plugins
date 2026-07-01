# Step 8 — Remediation for TC-8005

## Triage Outcome: Case A — Affected, Create Remediation Task

Versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream are affected by CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4). Remediation is required.

### Ecosystem: RPM (System Package)

Because openssl-libs is an RPM system package (not a source dependency ecosystem like Cargo or npm), remediation follows the **single-task** path. There is no upstream backport task — the fix happens directly in the Konflux release repo. The two-task upstream backport + downstream propagation flow is NOT used for RPM ecosystems.

### Remediation Task: Update openssl-libs in Konflux Release Repo

**Proposed Jira Task creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)",
  description: <task-description-below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)
```

**Task Description (following task-description-template.md format):**

---

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

openssl-libs versions before 3.0.7-28.el9_4 are vulnerable to a buffer over-read during X.509 certificate chain verification (CVE-2026-40215, CVSS 7.1 High). Versions 2.2.0 through 2.2.2 ship the vulnerable package. Versions 2.2.3+ already ship the patched version.

The package is classified as an explicit install (present in rpms.lock.yaml).

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Update the openssl-libs package version in rpms.in.yaml to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml to reflect the updated package version
- The package is an explicit install in rpms.lock.yaml — update the package spec directly
- Verify the Konflux build pipeline triggers successfully with the updated package

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] rpms.lock.yaml reflects the updated version
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated openssl-libs

## Dependencies

- Depends on: TC-8005 (parent tracking issue)

---

### Post-Creation Steps (Proposed)

After creating the remediation task, the following actions would be performed:

1. **Description Digest Comment**: Re-fetch the task description from Jira after `create_issue`, compute a SHA-256 digest using `scripts/sha256-digest.py`, and post a digest comment with marker `[sdlc-workflow] Description digest: <tagged-digest>`. This digest comment is posted BEFORE any issue links or other comments.

2. **Link to Vulnerability Issue**:
   ```
   jira.create_link(
     inwardIssue: "TC-8005",
     outwardIssue: "<task-key>",
     type: "Depend"
   )
   ```

3. **Transition** TC-8005 to In Progress.

4. **Assign** TC-8005 to the current user.

5. **Post summary comment** to TC-8005 documenting the remediation task created.

### Why Single Task (Not Two Tasks)

The RPM ecosystem uses a single remediation task because:
- openssl-libs is a system package, not a source code dependency
- The fix is applied directly in the Konflux release repo (rpms.in.yaml / rpms.lock.yaml)
- There is no "upstream source repo" to backport to — the package comes from the RPM ecosystem/distribution
- This contrasts with source dependency ecosystems (Cargo, npm, Go) which require two tasks: an upstream backport task in the source repo and a downstream propagation subtask in the Konflux release repo

### Note on Files to Modify

The Files to Modify section is intentionally omitted per remediation-templates.md. These depend on repository structure that the triage skill does not have context for — `/implement-task` discovers them via code analysis.

---

All actions above are **proposed** and require engineer confirmation before execution. No Jira mutations have been performed.
