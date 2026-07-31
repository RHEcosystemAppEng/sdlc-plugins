# Step 8 -- Remediation

## Triage Outcome: Case B -- Affected versions exist, create remediation task

The version impact analysis shows that versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream ship a vulnerable version of openssl-libs (< 3.0.7-28.el9_4). Remediation is required.

## Ecosystem Classification

openssl-libs is an RPM system package. Per the ecosystem classification table:

| Category | Ecosystems | Remediation tasks per stream |
|----------|------------|------------------------------|
| System package | RPM | 1 -- Konflux release repo fix only |

A **single** remediation task is created for the Konflux release repo. The two-task upstream backport + downstream propagation flow is NOT used because RPM is a system package ecosystem -- the fix happens directly in the Konflux release repo.

## Remediation Task Description

The following task description follows `task-description-template.md` format. "Files to Modify" is intentionally omitted per `remediation-templates.md` -- `implement-task` discovers the relevant files via code analysis.

### Task: Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)

**Proposed Jira issue creation** (requires engineer confirmation):

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)",
  description: <task-description-below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)
```

#### Task Description Content

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

The vulnerable RPM package openssl-libs (versions before 3.0.7-28.el9_4) is
present in rpms.lock.yaml for versions 2.2.0 through 2.2.2. A buffer
over-read in X.509 certificate chain verification allows a remote attacker
to craft a certificate with a malformed extension that triggers an
out-of-bounds read.

Affected versions: RHTPA 2.2.0 (openssl-libs 3.0.7-25.el9_3),
RHTPA 2.2.1 (openssl-libs 3.0.7-27.el9_4),
RHTPA 2.2.2 (retag of 2.2.1, openssl-libs 3.0.7-27.el9_4)

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Package origin: explicit install (openssl-libs is present in rpms.lock.yaml)
- Update the openssl-libs package spec in rpms.in.yaml or rpms.lock.yaml
  to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml after updating the package spec
- Verify the Konflux build pipeline triggers successfully with the
  updated package version

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

## Post-creation Steps

### 1. Description Digest Comment

After creating the remediation task, post a description digest comment per `shared/description-digest-protocol.md`. The digest comment is posted BEFORE creating issue links or other comments.

Procedure:
1. Re-fetch the task description from Jira after `create_issue` (the Jira API normalizes content during storage):
   ```
   task_desc = jira.get_issue(<task-key>, fields=["description"])
   ```
2. Write the re-fetched description to a temp file and compute the SHA-256 digest using `scripts/sha256-digest.py`:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the input format and outputs a format-tagged digest (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`).
3. Post the digest comment on the newly created task:
   ```
   jira.add_comment(<task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py`.

### 2. Issue Linkage

After the digest comment, link the remediation task to the Vulnerability issue:

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: <task-key>,
  type: "Depend"
)
```

Note: For RPM system package ecosystems, there is no second task (no upstream backport), so no "Blocks" link is needed. Only the single "Depend" link from the Vulnerability issue to the remediation task.

### 3. Transition to In Progress

```
jira.transition_issue("TC-8005", <in-progress-transition-id>)
```

### 4. Add ai-cve-triaged label

```
jira.edit_issue("TC-8005", fields={
  "labels": ["CVE-2026-40215", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 5. Post-Triage Summary Comment

Post a summary comment on TC-8005 documenting the triage outcome. The comment includes an @mention of the vulnerability issue's reporter using an ADF mention node.

```
Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 3.0.7-25.el9_3 | YES |
| 2.2.1 | 3.0.7-27.el9_4 | YES |
| 2.2.2 | -- | YES (retag of 2.2.1) |
| 2.2.3 | 3.0.7-28.el9_4 | NO |
| 2.2.4 | 3.0.7-28.el9_4 | NO |

Affects Versions corrected: [RHTPA 2.0.0] --> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
Ecosystem: RPM (system package)
Package origin: explicit install (present in rpms.lock.yaml)

Remediation task created: <task-key> (Konflux release repo fix)

@reporter-mention (ADF mention node: {"type": "mention", "attrs": {"id": "<reporter-account-id>", "text": "@<reporter-name>"}})

---
This comment was AI-generated by sdlc-workflow/triage-security v0.13.7.
```

## Pre-creation Checklist

- [x] **Task count per stream**: 1 task (RPM system package -- matches ecosystem classification table)
- [x] **Cross-stream coverage**: issue is scoped to 2.2.x; the 2.1.x stream is not analyzed in this scoped triage (would be handled by Case A cross-stream check if 2.1.x is also affected)
- [x] **Link types**: "Depend" for the task linked to its CVE Jira TC-8005
- [x] **Preemptive labels**: not applicable (no streams without their own CVE Jira identified in this scoped triage)
- [x] **Coordination guidance**: omitted (no Deployment Context column in Source Repositories table -- backward compatibility default to upstream)
