# Step 8 – Remediation: TC-8005 (CVE-2026-40215, openssl-libs)

## Steps 4–7.5 (simulated, no Jira calls)

- **Step 4 Duplicates/siblings**: the skill would run JQL `project = TC AND labels = 'CVE-2026-40215' AND issuetype = 10024 AND key != TC-8005`. No sibling data is available in this eval, so no same-stream duplicate is assumed. Cross-stream companions for 2.1.x are unknown.
- **Step 4.3 Cross-CVE overlap**: skipped. The Upstream Affected Component, PS Component and Stream custom fields are not configured.
- **Step 4.4 Preemptive reconciliation**: no data on existing `security-preemptive` tasks.
- **Step 5 Lifecycle**: in a live run, check affected 2.2.x versions against https://access.example.com/product-life-cycle/rhtpa. Not fetched in this eval; all 2.2.x versions are assumed supported.
- **Step 6 Already fixed**: there are no resolved siblings. Note that 2.2.3 and later already ship the fixed RPM (3.0.7-28.el9_4). The fix exists in the latest release, but supported builds 2.2.0–2.2.2 shipped the vulnerable package.
- **Step 7 Concurrent triage**: skipped. The Upstream Affected Component field is not configured.
- **Step 7.5 Release Jira**: the skill would find or create an Epic "RHTPA 2.2.x Release Tasks" and a Task "RHTPA 2.2.x CVE triage" for the next 2.2.x release. Each needs individual confirmation, and the exact version comes from Jira. Step 7.5.3 dedup cannot run because the component field is not configured.

## Decision

- Issue scope 2.2.x has affected supported versions (2.2.0, 2.2.1, 2.2.2), so this is **Case B**: create remediation.
- Stream 2.1.x outside the scope is also affected (2.1.0 and 2.1.1 ship 3.0.7-24.el9), so **Case A** also applies: post a cross-stream impact comment, plus a preemptive task if no 2.1.x CVE Jira exists.
- Ecosystem is RPM, a system package, so **1 task per stream** (a Konflux release repo fix).
- Origin is **explicit install** (openssl-libs is in rpms.lock.yaml; SBOM verification was skipped because cosign is not available), so the **Explicit install origin** template is used.

---

## Remediation Task (Case B, stream 2.2.x)

**Summary**: Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)
**Project**: TC | **Issue type**: Task
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-40215`

### Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

openssl-libs versions before 3.0.7-28.el9_4 contain a buffer over-read in
X509_verify_cert() (Subject Alternative Name extension length not validated),
allowing a crafted certificate to leak memory or crash the process. CVSS 7.1 (High).

Affected versions (stream 2.2.x, from rpms.lock.yaml at pinned tags):
- RHTPA 2.2.0 (v0.4.5): openssl-libs 3.0.7-25.el9_3
- RHTPA 2.2.1 (v0.4.8): openssl-libs 3.0.7-27.el9_4
- RHTPA 2.2.2 (v0.4.9): retag of 2.2.1
Not affected: RHTPA 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) ship 3.0.7-28.el9_4.

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Package origin: explicit install — openssl-libs is pinned in rpms.lock.yaml
  (SBOM verification skipped — cosign not available; classification based on
  rpms.lock.yaml only).
- Update the openssl-libs package spec (rpms.in.yaml / Dockerfile dnf install)
  to require >= 3.0.7-28.el9_4.
- Regenerate rpms.lock.yaml and confirm openssl-libs (and its companion
  openssl package, if locked) resolves to >= 3.0.7-28.el9_4.
- The latest released build (2.2.4, v0.4.12) already ships 3.0.7-28.el9_4;
  verify main still pins >= 3.0.7-28.el9_4 and ensure any 2.2.x z-stream
  rebuild of the affected builds (2.2.0–2.2.2 lineage) picks up the fixed RPM.
- Verify the Konflux build pipeline triggers successfully.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml on main
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

### Post-creation steps (each needs engineer confirmation)

1. Post a description digest comment on the new task before any links:
   `[sdlc-workflow] Description digest: <sha256 tagged digest>`
2. Link `TC-8005` (inward) to the task (outward) with type **Depend**.
3. If the Step 7.5 release Task exists, link the task to the release Task with type **Blocks**, and link the release Task to TC-8005 with type **Related**.
4. Transition TC-8005 to In Progress, or skip if it is already Assigned or in a later status. Make sure it is assigned to the current user.
5. Comment on TC-8005: "Remediation task created: <task-key>" (with the Comment Footnote).

---

## Case A – Cross-stream impact (stream 2.1.x)

**Comment on TC-8005:**
```
Cross-stream impact: openssl-libs < 3.0.7-28.el9_4 also affects stream(s) 2.1.x
(RHTPA 2.1.0, 2.1.1 ship openssl-libs 3.0.7-24.el9) based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

---
This comment was AI-generated by sdlc-workflow/triage-security v0.13.10.
```

**If Step 4 finds no 2.1.x CVE Jira**, create a preemptive task.
- Summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.1.x)"
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-40215`, `security-preemptive`
- Repository: `rhtpa-release.0.3.z`. Target branch: `main`.
- Template: same explicit-install template as above, with this prefix:
  > **Preemptive remediation**: This task was created proactively from cross-stream impact analysis of TC-8005 (stream 2.2.x). No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one, this task will be linked and the `security-preemptive` label removed.
- Affected versions: 2.1.0 (v0.3.8) and 2.1.1 (v0.3.12), both shipping 3.0.7-24.el9.
- Link: TC-8005 to the preemptive task with type **Related**, not Depend. Do not link it to a release Task.

If a 2.1.x CVE Jira already exists, skip this task.

## Pre-creation Checklist

- [x] Task count per stream: 1, because RPM is a system package
- [x] Cross-stream coverage: 2.1.x gets either a preemptive task or an existing sibling
- [x] Link types: Depend for the 2.2.x task, Related for the 2.1.x preemptive task, no Blocks between upstream and downstream (single task)
- [x] Preemptive label applied to the 2.1.x task only
- [x] Coordination guidance omitted, because the Source Repositories table has no Deployment Context column
- [x] Release Jira linking applies to non-preemptive tasks only
- [x] Dedup: not applicable (component field not configured)

## Post-Triage

- Add the `ai-cve-triaged` label to TC-8005.
- Post a summary comment covering: the version impact table, the Affects Versions correction (RHTPA 2.0.0 → 2.2.0/2.2.1/2.2.2), outcome Case B plus Case A, task keys, release Jira keys, and an @mention of the reporter. End it with the Comment Footnote.
