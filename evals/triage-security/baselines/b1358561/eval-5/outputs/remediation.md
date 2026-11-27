# Step 8 – Remediation: TC-8005 (CVE-2026-40215, openssl-libs)

## Decision path

- **Steps 4–6** were not executed against Jira. In a live run they would cover the sibling JQL for label `CVE-2026-40215`, a lifecycle check against the product pages URL, and resolved sibling issues. For this analysis: no known same-stream duplicate, 2.2.x versions assumed within lifecycle, no resolved sibling.
- **Step 7** (concurrent triage) was skipped because the Upstream Affected Component custom field is not configured.
- **Step 7.5** (release Jira) needs Jira, so it was not executed. A live run would find or create "RHTPA <next 2.2.z> Release Tasks" (Epic) and "RHTPA <next 2.2.z> CVE triage" (Task), each with individual confirmation. Step 7.5.3 cross-CVE dedup was skipped (Upstream Affected Component field not configured).
- **Supported versions affected?** Yes: 2.2.0, 2.2.1 and 2.2.2 (in scope), plus 2.1.0 and 2.1.1 (out of scope).
- **Scoped issue (2.2.x), other streams affected (2.1.x)**: **Case A** cross-stream comment, then **Case B** for 2.2.x.
- **Ecosystem RPM (system package)**: **1 task** for the 2.2.x stream, in the Konflux release repo. There is no upstream backport or downstream propagation task.
- **Origin**: explicit install (openssl-libs is in rpms.lock.yaml), so the "Explicit install origin" template applies.

Note for the engineer: the 2.2.x Konflux repo already pins 3.0.7-28.el9_4 from v0.4.11 (2.2.3) onward. The remediation task therefore mostly confirms that `main` and the next 2.2.z build stay at or above the fixed version. It keeps TC-8005 tracked to closure. The engineer may instead decide that 2.2.3 already delivered the fix.

## Remediation task (stream 2.2.x)

**Summary**: `Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)`
**Issue type**: Task
**Project**: TC
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-40215`
**Security level**: copied from TC-8005 (parent Vulnerability)
**Priority / fixVersion**: prompted (per Jira Field Defaults)

### Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

openssl-libs versions before 3.0.7-28.el9_4 contain a buffer over-read in
X509_verify_cert() (missing Subject Alternative Name extension length bounds check),
CVSS 7.1 (High).

Affected versions (stream 2.2.x, from rpms.lock.yaml at pinned tags):
- RHTPA 2.2.0 (v0.4.5): openssl-libs 3.0.7-25.el9_3
- RHTPA 2.2.1 (v0.4.8): openssl-libs 3.0.7-27.el9_4
- RHTPA 2.2.2 (retag of 2.2.1): openssl-libs 3.0.7-27.el9_4
Not affected: RHTPA 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) ship 3.0.7-28.el9_4.

Package origin: explicit install (openssl-libs is pinned in rpms.lock.yaml).
SBOM verification was skipped (cosign not available), so the classification is based on rpms.lock.yaml only.

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Update the package version in Dockerfile (dnf install command or package spec)
  / rpms.in.yaml so openssl-libs resolves to >= 3.0.7-28.el9_4
- If lock file exists: regenerate rpms.lock.yaml
- The released tags v0.4.11 and v0.4.12 already pin openssl-libs 3.0.7-28.el9_4;
  verify that main HEAD still pins >= 3.0.7-28.el9_4 and that no regression
  to an older release was introduced. If it already does, the change is limited
  to confirming the next 2.2.z build carries the fix
- Also check the openssl base package (openssl) for consistency with openssl-libs
  if both appear in rpms.lock.yaml

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

(No Coordination Guidance subsection: the Source Repositories table has no Deployment Context column.)

### Creation and linkage (proposed; each step needs confirmation, none executed)

1. `jira.create_issue(projectKey: "TC", issueTypeName: "Task", summary: <above>, description: <above>, labels: ["ai-generated-jira","Security","CVE-2026-40215"], security: <TC-8005 security level>)`
2. Post the description digest comment on the new task (`[sdlc-workflow] Description digest: <tagged-digest>`, computed with `scripts/sha256-digest.py`) before any links or other comments.
3. Link TC-8005 → task, type **Depend**.
4. If the Step 7.5 release Task exists: task → release Task (**Blocks**). Release Task → TC-8005 (**Related**).
5. Transition TC-8005 to In Progress, or skip if it is already Assigned or later.
6. Comment on TC-8005: "Remediation task created: <task-key>" (with the Comment Footnote).

## Case A – Cross-stream impact comment (proposed for TC-8005)

```
Cross-stream impact: openssl-libs < 3.0.7-28.el9_4 also affects stream(s) 2.1.x
(RHTPA 2.1.0, 2.1.1 ship openssl-libs 3.0.7-24.el9) based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

---
This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.
```

The Step 4 sibling search (`labels = CVE-2026-40215` with suffix `[rhtpa-2.1]`) decides what happens next for 2.1.x:
- **If a 2.1.x sibling exists**: link it as Related and create no task here.
- **If none exists**: create a **preemptive** system-package task for 2.1.x:
  - Summary: `Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.1.x)`
  - Repository: `rhtpa-release.0.3.z`, Target Branch: `main`
  - Same explicit-install template, with affected versions RHTPA 2.1.0 / 2.1.1 (openssl-libs 3.0.7-24.el9)
  - Labels: `ai-generated-jira`, `Security`, `CVE-2026-40215`, `security-preemptive`
  - Description prefix: "> **Preemptive remediation**: This task was created proactively from cross-stream impact analysis of TC-8005 (stream 2.2.x). No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one, this task will be linked and the `security-preemptive` label removed."
  - Link to TC-8005 as **Related** (not Depend). It is not linked to the 2.2.x release Task.
  - Then comment on TC-8005 listing the preemptive task.

## Pre-creation checklist

- [x] Task count per stream: RPM gives 1 task (2.2.x). A preemptive task for 2.1.x is created only if no sibling exists
- [x] Cross-stream coverage: 2.1.x is covered by a sibling or a preemptive task
- [x] Link types: Depend (2.2.x task → TC-8005), Related (preemptive 2.1.x task)
- [x] Preemptive label applied only to the 2.1.x task
- [x] Coordination guidance: omitted (no Deployment Context column)
- [x] Release Jira linking: the 2.2.x task is linked to the release Task if Step 7.5 created one
- [x] Dedup consistency: not applicable (Step 7.5.3 skipped)

## Post-triage (proposed)

- Add label `ai-cve-triaged` to TC-8005.
- Post a summary comment with the version impact table, the Affects Versions correction ([RHTPA 2.0.0] → [RHTPA 2.2.0, 2.2.1, 2.2.2]), the outcome (remediation task created plus a cross-stream notice), task and release Jira keys, an @mention of the TC-8005 reporter (ADF mention node), and the Comment Footnote.
