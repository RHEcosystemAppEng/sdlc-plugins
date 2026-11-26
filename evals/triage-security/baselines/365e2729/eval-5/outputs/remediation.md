# Step 8 – Remediation: TC-8005 (CVE-2026-40215, openssl-libs)

## Steps 4–7.5 summary (inputs to the Step 8 decision)

- **Step 4 (Duplicate/Sibling):** Needs JQL `project = TC AND issuetype = 10024 AND labels = CVE-2026-40215`, which was not executed (no Jira). No same-stream duplicate is known. Step 4.3 (cross-CVE overlap) is skipped because Upstream Affected Component is not configured.
- **Step 5 (Lifecycle):** The Product pages URL was not fetched (no external calls). 2.2.x is assumed to be in support, so engineer verification is needed.
- **Step 6 (Already Fixed):** No resolved sibling issues are known. Note: 2.2.3 and 2.2.4 already ship the fixed openssl-libs 3.0.7-28.el9_4.
- **Step 7 (Concurrent Triage):** Skipped because Upstream Affected Component is not configured.
- **Step 7.5 (Release Jira):** Would find or create `RHTPA <next 2.2.z> Release Tasks` (Epic) and `RHTPA <next 2.2.z> CVE triage` (Task). Not executed. The next 2.2.z version must be confirmed by the engineer and is not inferred here. Cross-CVE dedup (7.5.3) is skipped because Upstream Affected Component is not configured.

## Decision

- Supported versions in scope (2.2.x) are affected (2.2.0, 2.2.1, 2.2.2), so this is **Case B**: create remediation tasks.
- The issue is scoped and another stream (2.1.x: 2.1.0, 2.1.1) is also affected, so **Case A** also applies: post a cross-stream impact comment and, if no 2.1.x sibling CVE Jira exists, create a preemptive 2.1.x task.
- Ecosystem RPM (system package) means **1 task per stream**, a Konflux release repo fix.
- Origin is **explicit install** (openssl-libs is present in rpms.lock.yaml), so the explicit-install template is used.
- Important caveat for the engineer: the latest 2.2.x pin (2.2.4, `v0.4.12`) **already resolves openssl-libs 3.0.7-28.el9_4**. The 2.2.x task may reduce to verifying that `main` of rhtpa-release.0.4.z still pins >= 3.0.7-28.el9_4. Affected customers on 2.2.0–2.2.2 are remediated by upgrading to 2.2.3+. The engineer should confirm whether a task is still wanted (for verification and tracking) before creation.

---

## Remediation Task (stream 2.2.x), the primary task for TC-8005

**Summary:** `Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)`
**Project:** TC | **Issue type:** Task
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-40215`
**Security level:** copied from parent TC-8005 (`issue.security`). Leave it out only if the parent has none.
**Priority:** prompt engineer (CVSS 7.1 High, so dev-dependency handling does not apply)

### Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

openssl-libs versions before 3.0.7-28.el9_4 are vulnerable to a buffer over-read in
X.509 certificate chain verification (X509_verify_cert() does not validate the length
field of the Subject Alternative Name extension). CVSS 7.1 (High).

Affected versions (2.2.x stream, from rpms.lock.yaml at pinned tags):
- RHTPA 2.2.0 (v0.4.5): openssl-libs 3.0.7-25.el9_3
- RHTPA 2.2.1 (v0.4.8): openssl-libs 3.0.7-27.el9_4
- RHTPA 2.2.2 (retag of 2.2.1): openssl-libs 3.0.7-27.el9_4
Not affected: RHTPA 2.2.3 (v0.4.11) and RHTPA 2.2.4 (v0.4.12) ship 3.0.7-28.el9_4.

Package origin: explicit install (openssl-libs present in rpms.lock.yaml).
SBOM verification: skipped (cosign not available; matrix has no image reference/digest).
Using rpms.lock.yaml classification only.

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Update the openssl-libs package version/spec in rpms.in.yaml (or the Dockerfile
  dnf install / package spec) so it resolves to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml and confirm the openssl-libs entry is >= 3.0.7-28.el9_4
- The latest release tag v0.4.12 already resolves openssl-libs 3.0.7-28.el9_4; first
  verify the current main branch lock file. If main is already >= 3.0.7-28.el9_4, the
  change is limited to confirming the pin and ensuring no regression (no downgrade)
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml on main
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

(Coordination Guidance is left out because Source Repositories has no Deployment Context column.)

### Post-creation actions (each requires confirmation, none executed)

1. Post a description digest comment on the new task before any links: `[sdlc-workflow] Description digest: <sha256-md:...>` (via `scripts/sha256-digest.py`).
2. Link `TC-8005` (inward) → task (outward), type **Depend**.
3. If the 7.5 release Task exists: task (inward) → release Task (outward), **Blocks**. Release Task (inward) → `TC-8005` (outward), **Related**.
4. TC-8005 is already Assigned after Step 0.8, which is an indeterminate-category status, so no In Progress transition is needed.
5. Comment on TC-8005: "Remediation task created: <task-key>" plus the Comment Footnote.

---

## Case A – Cross-stream impact (2.1.x)

### Cross-stream comment on TC-8005 (proposed)

```
Cross-stream impact: openssl-libs < 3.0.7-28.el9_4 also affects stream(s) 2.1.x
(RHTPA 2.1.0, RHTPA 2.1.1 — openssl-libs 3.0.7-24.el9) based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

---
This comment was AI-generated by sdlc-workflow/triage-security v0.14.0.
```

### Preemptive task (only if Step 4 finds no 2.1.x sibling CVE Jira for CVE-2026-40215)

**Summary:** `Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.1.x)`
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-40215`, `security-preemptive`
**Link:** `TC-8005` → task, type **Related** (not Depend). Not linked to release Jira, because it is preemptive.

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8005 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

Affected versions (2.1.x stream, from rpms.lock.yaml at pinned tags):
- RHTPA 2.1.0 (v0.3.8): openssl-libs 3.0.7-24.el9
- RHTPA 2.1.1 (v0.3.12): openssl-libs 3.0.7-24.el9

Package origin: explicit install (openssl-libs present in rpms.lock.yaml).
SBOM verification: skipped (cosign not available). Using rpms.lock.yaml classification only.

Advisory: https://access.redhat.com/errata/RHSA-2026:4021

## Implementation Notes

- Update the openssl-libs package version/spec (rpms.in.yaml or Dockerfile dnf install)
  so it resolves to >= 3.0.7-28.el9_4 (or the el9 build carrying the fix available to
  this stream's base)
- Regenerate rpms.lock.yaml

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (originating CVE, stream 2.2.x)
```

Follow-up comment on TC-8005 (if created): "Preemptive remediation tasks created for streams without CVE Jiras: 2.1.x: <task-key> (security-preemptive) ..." plus the Comment Footnote.

## Pre-creation checklist

- [x] Task count per stream: 1 (RPM = system package)
- [x] Cross-stream coverage: 2.1.x is covered by a preemptive task or an existing sibling CVE Jira (pending Step 4 search)
- [x] Link types: Depend (2.2.x task to TC-8005), Related (2.1.x preemptive task to TC-8005). There is no Blocks link between tasks because RPM is a single task.
- [x] Preemptive label on the 2.1.x task
- [x] Coordination guidance: left out (no Deployment Context column)
- [x] Release Jira linking: the 2.2.x task gets Blocks to the release Task, and the CVE gets Related to the release Task, if 7.5 is active
- [x] Dedup consistency: not applicable (7.5.3 skipped)

## Post-triage

- Add label `ai-cve-triaged` to TC-8005.
- Post a summary comment with: the version impact table, the Affects Versions correction (RHTPA 2.0.0 → RHTPA 2.2.0/2.2.1/2.2.2), the outcome (remediation created), task links, release Jira refs, an @mention of the TC-8005 reporter (ADF mention node), and the Comment Footnote (`sdlc-workflow/triage-security v0.14.0`).
