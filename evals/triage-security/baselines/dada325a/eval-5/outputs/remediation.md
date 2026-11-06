# Step 8 – Remediation: TC-8005 (CVE-2026-40215, openssl-libs)

## Pre-remediation steps (4 – 7.5) summary

- **Step 4 – Siblings and duplicates:** proposed JQL `project = TC AND labels = 'CVE-2026-40215' AND issuetype = 10024 AND key != TC-8005`. It was not run (eval mode), so no siblings are known. Steps 4.3 (cross-CVE overlap) and 7 (concurrent triage) are **skipped**, because the Upstream Affected Component, PS Component, and Stream fields are not configured. Step 4.4 (preemptive reconciliation) needs a JQL search for `security-preemptive` tasks labeled CVE-2026-40215 with `(rhtpa-2.2)` in the summary. It was not run, so for this eval no such task is assumed.
- **Step 5 – Lifecycle:** the product pages URL (https://access.example.com/product-life-cycle/rhtpa) was not fetched. 2.2.x is the latest stream and is assumed supported, which the engineer must confirm.
- **Step 6 – Already fixed:** no resolved siblings are known. Note that **the 2.2.x stream already ships the fix from 2.2.3 onward** (3.0.7-28.el9_4 at `v0.4.11` and `v0.4.12`). Customers on 2.2.0 to 2.2.2 are remediated by upgrading to 2.2.3 or later.
- **Step 7.5 – Release Jira:** proposed search `project = TC AND issuetype = Epic AND summary ~ 'RHTPA 2.2' AND summary ~ 'Release Tasks'`. If nothing is found, the default proposal is to create **"RHTPA 2.2.5 Release Tasks"** (a patch bump from the latest matrix version 2.2.4) and the child Task **"RHTPA 2.2.5 CVE triage"**. Each creation needs individual confirmation. Step 7.5.3 dedup is skipped because the Upstream Affected Component field is not configured.

## Decision

- Scoped stream 2.2.x has affected versions (2.2.0, 2.2.1, 2.2.2), so **Case B** applies: create 1 remediation task, since RPM is a system package ecosystem.
- Another stream (2.1.x: 2.1.0, 2.1.1) is also affected, so **Case A** applies: post a cross-stream impact comment, plus a preemptive task for 2.1.x if no `[rhtpa-2.1]` sibling CVE Jira exists.
- Case C (close as Not a Bug) does **not** apply.

**Engineer attention:** the 2.2.x Konflux repo already pins the fixed openssl-libs as of `v0.4.11`. The 2.2.x task below is therefore mainly a verification and guard task: confirm that `main` of rhtpa-release.0.4.z still pins 3.0.7-28.el9_4 or later and that the next 2.2.x build ships it. The engineer may instead record "fixed in RHTPA 2.2.3" and skip the task.

---

## Task 1 (Case B): stream 2.2.x, explicit install origin

**Summary:** Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)
**Issue type:** Task
**Project:** TC
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-40215`
**Links:** TC-8005 → task (**Depend**); task → RHTPA 2.2.x CVE triage release Task (**Blocks**), if Step 7.5 is active; release Task → TC-8005 (**Related**)

### Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

openssl-libs versions before 3.0.7-28.el9_4 contain a buffer over-read in
X.509 certificate chain verification (X509_verify_cert(), missing length
validation of the Subject Alternative Name extension). CVSS 7.1 (High).

Affected versions (2.2.x stream, from rpms.lock.yaml at pinned commits):
- RHTPA 2.2.0 (build 0.4.5, tag v0.4.5): openssl-libs 3.0.7-25.el9_3
- RHTPA 2.2.1 (build 0.4.8, tag v0.4.8): openssl-libs 3.0.7-27.el9_4
- RHTPA 2.2.2 (build 0.4.9, retag of v0.4.8): same as 2.2.1

Not affected: RHTPA 2.2.3 (v0.4.11) and RHTPA 2.2.4 (v0.4.12) already ship
openssl-libs 3.0.7-28.el9_4.

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Package origin: explicit install. openssl-libs is pinned in rpms.lock.yaml
  (and its rpms.in.yaml input) in rhtpa-release.0.4.z. SBOM cross-verification
  was skipped (cosign not available), so classification relies on rpms.lock.yaml only.
- Verify the openssl-libs entry on main in rpms.lock.yaml is >= 3.0.7-28.el9_4
  (the fix landed between tags v0.4.8 and v0.4.11). If it has regressed or is
  lower, update the package spec in rpms.in.yaml and regenerate rpms.lock.yaml.
- Update the package version in Dockerfile (dnf install command or package spec)
  only if it is pinned there.
- If lock file exists: regenerate rpms.lock.yaml.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml on main
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

The Coordination Guidance subsection is omitted because the Source Repositories table has no Deployment Context column.
After creation, post a description digest comment (`[sdlc-workflow] Description digest: sha256-...`) before any links or comments.

---

## Case A: cross-stream impact (2.1.x)

### Cross-stream comment on TC-8005

```
Cross-stream impact: openssl-libs < 3.0.7-28.el9_4 also affects stream(s)
2.1.x (RHTPA 2.1.0, RHTPA 2.1.1 ship openssl-libs 3.0.7-24.el9) based on
lock file analysis (rpms.lock.yaml at v0.3.8 / v0.3.12).
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

---
This comment was AI-generated by sdlc-workflow/triage-security (https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.
```

### Task 2 (preemptive): stream 2.1.x, only if no `[rhtpa-2.1]` CVE-2026-40215 Vulnerability issue exists

**Summary:** Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.1)
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-40215`, `security-preemptive`
**Links:** TC-8005 → task (**Related**, not Depend). The task is not linked to the release Task because it is preemptive.

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

Affected versions (2.1.x stream, from rpms.lock.yaml at pinned commits):
- RHTPA 2.1.0 (build 0.3.8, tag v0.3.8): openssl-libs 3.0.7-24.el9
- RHTPA 2.1.1 (build 0.3.12, tag v0.3.12): openssl-libs 3.0.7-24.el9

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Package origin: explicit install. openssl-libs is pinned in rpms.lock.yaml of
  rhtpa-release.0.3.z. SBOM cross-verification was skipped (cosign not available).
- Update the openssl-libs package spec in rpms.in.yaml to >= 3.0.7-28.el9_4
  (or the equivalent fixed el9 errata build available to the 2.1.x base) and
  regenerate rpms.lock.yaml.
- Update the package version in Dockerfile (dnf install command or package spec)
  if pinned there.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

### Preemptive task-list comment on TC-8005 (if Task 2 is created)

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <task-2-key> (security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.

---
This comment was AI-generated by sdlc-workflow/triage-security (https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.
```

---

## Pre-creation checklist

- [x] Task count per stream: 1 per stream (RPM system package)
- [x] Cross-stream coverage: 2.1.x is covered by a preemptive task or by an existing sibling CVE Jira
- [x] Link types: Depend (Task 1 → TC-8005), Related (preemptive Task 2), no Blocks between tasks (single-task RPM flow)
- [x] Preemptive label on the 2.1.x task
- [x] Coordination guidance: omitted (no Deployment Context column)
- [x] Release Jira linking: Task 1 → release Task (Blocks), TC-8005 → release Task (Related), if Step 7.5 is active
- [x] Dedup consistency: dedup was skipped (field not configured)

## Post-triage (proposed)

- Add the `ai-cve-triaged` label to TC-8005.
- Post a summary comment containing the version impact table, the Affects Versions correction, the outcome (remediation created), the task keys, the release Jira keys, and an @mention of the TC-8005 reporter, ending with the Comment Footnote.
- Vulnerability status: already moved to Assigned in Step 0.8, so the In Progress transition is skipped.
