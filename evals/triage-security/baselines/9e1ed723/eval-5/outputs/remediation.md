# Step 8 – Remediation: TC-8005 (CVE-2026-40215, openssl-libs)

## Steps 4–7.5 context (simulated, no Jira calls)

- **Step 4 – Duplicates/siblings**: the JQL search for other Vulnerability issues labeled `CVE-2026-40215` was not run. No sibling data was supplied, so for this eval: no same-stream duplicate, and no known companion issue for 2.1.x. Step 4.3 (cross-CVE overlap) is skipped because the Upstream Affected Component field is not configured. Step 4.4: no preemptive tasks are known.
- **Step 5 – Lifecycle**: not queried (Product pages URL `https://access.example.com/product-life-cycle/rhtpa`). 2.2.x is assumed to be in support.
- **Step 6 – Already fixed**: no resolved siblings are known. Note that within scope, the latest releases 2.2.3 and 2.2.4 already ship `openssl-libs-3.0.7-28.el9_4`. The fix exists in shipped artifacts, but 2.2.0 to 2.2.2 are affected, so the issue is not closed as already fixed.
- **Step 7 – Concurrent triage**: skipped (Upstream Affected Component field not configured).
- **Step 7.5 – Release Jira**: find or create the Epic `RHTPA <next 2.2.z version> Release Tasks` and the Task `RHTPA <next 2.2.z version> CVE triage` (version to be confirmed by the engineer, for example 2.2.5). Step 7.5.3 dedup: no existing remediation is known.

## Decision

- Issue is **scoped** to 2.2.x, and 2.2.x versions (2.2.0, 2.2.1, 2.2.2) are affected, so this is **Case B**.
- Stream 2.1.x (outside scope) is also affected (3.0.7-24.el9), so **Case A** applies: post a cross-stream comment and, if no 2.1.x CVE Jira exists, create a preemptive task.
- Ecosystem **RPM** (system package): **1 task per stream**, Konflux release repo fix only. No upstream backport or downstream propagation split.
- Origin: **explicit install** (openssl-libs is in `rpms.lock.yaml`), so the explicit-install template is used.
- No Deployment Context column in Source Repositories, so the Coordination Guidance subsection is left out.

---

## Task 1 (Case B): stream 2.2.x

**Summary:** `Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)`
**Project:** TC | **Issue type:** Task
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-40215`
**Priority:** prompt engineer (no default configured) | **fixVersion:** prompt engineer (for example the next RHTPA 2.2.z)

### Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

openssl-libs before 3.0.7-28.el9_4 has a buffer over-read in X.509 certificate
chain verification (X509_verify_cert(): Subject Alternative Name extension
length not validated). CVSS 7.1 (High). Advisory: RHSA-2026:4021.

Version impact (rpms.lock.yaml at pinned tags, stream 2.2.x):

| Version | Tag     | openssl-libs     | Affected? |
|---------|---------|------------------|-----------|
| 2.2.0   | v0.4.5  | 3.0.7-25.el9_3   | YES       |
| 2.2.1   | v0.4.8  | 3.0.7-27.el9_4   | YES       |
| 2.2.2   | v0.4.8  | same as 2.2.1    | YES (retag) |
| 2.2.3   | v0.4.11 | 3.0.7-28.el9_4   | NO        |
| 2.2.4   | v0.4.12 | 3.0.7-28.el9_4   | NO        |

Dependency chain:
  rpms.lock.yaml: present → explicit install
  SBOM verification: skipped (cosign not available). Using rpms.lock.yaml classification only.
  Origin: explicit install (openssl-libs resolved in rpms.lock.yaml from rpms.in.yaml)

## Implementation Notes

- Update the package version in Dockerfile (dnf install command or package spec)
  / rpms.in.yaml so that openssl-libs resolves to >= 3.0.7-28.el9_4
- If lock file exists: regenerate rpms.lock.yaml
- The 2.2.x release repo already pins openssl-libs 3.0.7-28.el9_4 from tag v0.4.11
  (2.2.3) onward. Check rpms.lock.yaml on main first. If it already has
  >= 3.0.7-28.el9_4, the change is limited to confirming this and making sure the
  next 2.2.z build ships it. Do not regress to an older release.
- Affected released versions 2.2.0–2.2.2 are fixed by upgrading to 2.2.3 or later.
  No respin of older tags is expected unless requested by Product Security.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml on main
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

### Creation and linkage (after engineer confirmation)

1. `jira.create_issue(projectKey: "TC", issueTypeName: "Task", summary: <above>, description: <above>, labels: ["ai-generated-jira", "Security", "CVE-2026-40215"])`
2. Post the description digest comment on the new task (`[sdlc-workflow] Description digest: sha256-md:<hex>`) **before** any links or other comments.
3. Link: TC-8005 (inward) → task (outward), type **Depend**.
4. If the release Task exists (Step 7.5): task → release Task, type **Blocks**. Release Task → TC-8005, type **Related**.
5. Transition TC-8005 to In Progress (skip if already Assigned or later in an indeterminate-category status). Make sure it is assigned to the current user.
6. Comment on TC-8005: `Remediation task created: <task-key>` (with Comment Footnote).

---

## Case A: cross-stream impact on 2.1.x (outside issue scope)

### Cross-stream comment on TC-8005

```
Cross-stream impact: openssl-libs < 3.0.7-28.el9_4 also affects stream(s) 2.1.x
(RHTPA 2.1.0, 2.1.1 ship openssl-libs 3.0.7-24.el9) based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

---
This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.
```

### Preemptive task (only if no `CVE-2026-40215 ... [rhtpa-2.1]` Vulnerability issue exists)

**Summary:** `Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.1.x)`
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-40215`, `security-preemptive`
**Link:** TC-8005 → task, type **Related** (not Depend). Not linked to the release Task (preemptive).

The description uses the same explicit-install template as Task 1, with Repository `rhtpa-release.0.3.z`, a preemptive prefix noting the originating CVE Jira TC-8005 (stream 2.2.x), and version impact rows 2.1.0 (`v0.3.8`, 3.0.7-24.el9, YES) and 2.1.1 (`v0.3.12`, 3.0.7-24.el9, YES). The digest comment is posted before links. Then comment on TC-8005: `Preemptive remediation tasks created for streams without CVE Jiras: - 2.1.x: <task-key> (security-preemptive)`.

---

## Pre-creation checklist

- [x] Task count per stream: RPM system package → 1 task (2.2.x), plus 1 preemptive (2.1.x) if needed
- [x] Cross-stream coverage: 2.1.x covered by a preemptive task or an existing sibling CVE Jira
- [x] Link types: Depend (own CVE), Related (preemptive), no Blocks upstream→downstream (single RPM task)
- [x] Preemptive label on the 2.1.x task
- [x] Coordination guidance: left out (no Deployment Context column)
- [x] Release Jira linking: non-preemptive task Blocks release Task; CVE Related to release Task
- [x] Dedup consistency: no dedup'd streams

## Post-triage

- Add label `ai-cve-triaged` to TC-8005.
- Post a summary comment: version impact table, Affects Versions correction (`[RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`), outcome (remediation created), task keys, release Epic and Task keys, an @mention of the TC-8005 reporter (ADF mention node), and the Comment Footnote.
