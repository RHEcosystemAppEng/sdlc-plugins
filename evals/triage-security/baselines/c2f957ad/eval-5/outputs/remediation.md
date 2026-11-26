# Step 8 – Remediation: TC-8005 (CVE-2026-40215, openssl-libs, stream 2.2.x)

## Decision

- Supported versions in scope are affected (2.2.0, 2.2.1, 2.2.2), so this is **Case B**:
  create remediation tasks.
- The issue is scoped and stream 2.1.x is also affected (2.1.0, 2.1.1), so **Case A**
  applies: post a cross-stream impact comment. Then check for a sibling CVE-2026-40215 issue
  with suffix `[rhtpa-2.1]`. If none exists, create a preemptive RPM task for 2.1.x
  (labels include `security-preemptive`, Related link to TC-8005). Jira was not queried in
  this eval, so sibling status is unknown.
- Ecosystem RPM is a system package, so **one task** goes to the Konflux release repo.
- Origin is an explicit install (in rpms.lock.yaml), so the task uses the **Explicit install
  origin** template.
- Steps 4–7.5 (duplicates, lifecycle, already-fixed, concurrent triage, release Jira) need
  Jira/WebFetch and were not run in this eval. The Upstream Affected Component field is not
  configured, so Steps 4.3 and 7 are skipped.

## Remediation Task (to be created after engineer confirmation)

**Summary**: Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)

**Issue type**: Task
**Project**: TC
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-40215`
**Security level**: copied from parent TC-8005 (`security: <parent-issue-security-level>`), omitted only if the parent has none

### Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

openssl-libs versions before 3.0.7-28.el9_4 have a buffer over-read in
X.509 certificate chain verification (X509_verify_cert(): Subject Alternative
Name extension length not bounds-checked). CVSS 7.1 (High).

Affected versions: RHTPA 2.2.0 (openssl-libs 3.0.7-25.el9_3, tag v0.4.5),
RHTPA 2.2.1 (openssl-libs 3.0.7-27.el9_4, tag v0.4.8),
RHTPA 2.2.2 (retag of 2.2.1, tag v0.4.8)
Not affected: RHTPA 2.2.3 and 2.2.4 (openssl-libs 3.0.7-28.el9_4, tags v0.4.11 / v0.4.12)

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Package origin: explicit install. openssl-libs is pinned in rpms.lock.yaml
  (rpms.lock.yaml classification; SBOM verification was skipped because cosign
  was not available).
- Update the openssl-libs package spec (rpms.in.yaml / Dockerfile dnf install
  or package spec) to >= 3.0.7-28.el9_4
- If lock file exists: regenerate rpms.lock.yaml
- The latest released 2.2.x build (2.2.4, v0.4.12) already ships
  3.0.7-28.el9_4. Verify that main's rpms.lock.yaml is at >= 3.0.7-28.el9_4,
  and make sure any future 2.2.x z-stream build does not pin an older lock.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

Coordination Guidance was left out on purpose. The Source Repositories table has no
Deployment Context column, so it is omitted for backward compatibility.

## Creation and linkage sequence (interactive, after confirmation)

1. `jira.create_issue(projectKey: "TC", issueTypeName: "Task", summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)", description: <above>, labels: ["ai-generated-jira", "Security", "CVE-2026-40215"], security: <TC-8005 security level>)`
2. Post a description digest comment on the new task before any links or comments:
   `[sdlc-workflow] Description digest: <tagged-digest>`
3. Link: `jira.create_link(inwardIssue: "TC-8005", outwardIssue: <task-key>, type: "Depend")`
4. If Step 7.5 found or created a release Task (RHTPA 2.2.x release, e.g. "RHTPA 2.2.5 CVE
   triage"): link task -> release Task (Blocks) and release Task -> TC-8005 (Related).
5. Transition TC-8005 to In Progress (or the equivalent) if it is not already there, and assign it to the current user.
6. Comment on TC-8005: "Remediation task created: <task-key>" + Comment Footnote.

## Cross-stream impact comment (Case A, on TC-8005)

```
Cross-stream impact: openssl-libs < 3.0.7-28.el9_4 also affects stream(s)
2.1.x (RHTPA 2.1.0, 2.1.1 ship openssl-libs 3.0.7-24.el9) based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

---
<Comment Footnote, skill name: triage-security>
```

## Post-triage

- Add label `ai-cve-triaged` to TC-8005.
- Post a summary comment covering: the version impact table, the Affects Versions
  correction, the outcome (remediation created), task links, release Jira references,
  dedup results, an @mention of the reporter (ADF mention node), and the Comment Footnote.

## Pre-creation checklist

- [x] Task count: RPM gives 1 task for 2.2.x
- [x] Cross-stream coverage: 2.1.x needs a sibling CVE Jira or a preemptive task (pending the Step 4 search)
- [x] Link types: Depend (task to own CVE); Related for any 2.1.x preemptive task
- [x] Preemptive label applies only to a 2.1.x task if one is created
- [x] Coordination guidance: omitted (no Deployment Context column)
- [ ] Release Jira linking: pending Step 7.5 (not run in eval)
- [x] Dedup: Step 7.5.3 not applicable (Upstream Affected Component field not configured)
