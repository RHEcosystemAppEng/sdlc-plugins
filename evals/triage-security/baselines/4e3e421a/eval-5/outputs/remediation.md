# Step 8 – Remediation: TC-8005 (CVE-2026-40215, openssl-libs)

## Pre-remediation steps (simulated, no Jira calls)

- **Step 4 (duplicates / siblings):** would run JQL `project = TC AND issuetype = 10024 AND labels = CVE-2026-40215` to find same-stream duplicates (`[rhtpa-2.2]`) and cross-stream companions (`[rhtpa-2.1]`). Step 4.3 is skipped (Upstream Affected Component field not configured).
- **Step 5 (lifecycle):** check 2.2.0–2.2.2 against https://access.example.com/product-life-cycle/rhtpa. Assumed in support.
- **Step 6 (already fixed):** later 2.2.x builds (2.2.3+) ship the fix, but the released 2.2.0–2.2.2 do not. Not closed as already fixed.
- **Step 7 (concurrent triage):** skipped (Upstream Affected Component field not configured).
- **Step 7.5 (release Jira):** find or create the release Epic `RHTPA <next 2.2.z> Release Tasks` and Task `RHTPA <next 2.2.z> CVE triage`. Each needs individual confirmation. The 7.5.3 dedup check is skipped because the component field is not configured.

## Decision

- Stream 2.2.x (in scope) has affected versions -> **Case B**: create remediation tasks.
- Ecosystem RPM (system package) -> **1 task** for the 2.2.x stream (Konflux release repo fix). No upstream backport task.
- Origin (Step 2.3.5): **explicit install** (openssl-libs is in rpms.lock.yaml). SBOM verification was skipped, so this rests on the lock file classification only.
- Other streams affected (2.1.x: 2.1.0, 2.1.1 at 3.0.7-24.el9) -> **Case A**: post a cross-stream impact comment. Create a preemptive 2.1.x task only if no `[rhtpa-2.1]` sibling CVE Jira exists (see below).

## Remediation Task (2.2.x) — to be created

**Project:** TC | **Issue type:** Task
**Summary:** `CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 in rhtpa-release.0.4.z (2.2.x)`
**Labels:** `CVE-2026-40215`, `security`, `pscomponent:org/rhtpa-server`
**Priority / fixVersion:** prompt the engineer (CVSS 7.1 High; fixVersion = next 2.2.z release)
**Link:** Depend -> TC-8005; Blocks -> release Task `RHTPA <next 2.2.z> CVE triage` (if Step 7.5 is active). Also link TC-8005 -> release Task (Related).

### Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

openssl-libs versions before 3.0.7-28.el9_4 are vulnerable to a buffer over-read
in X.509 certificate chain verification (X509_verify_cert() Subject Alternative
Name extension length not validated). CVSS 7.1 (High).

Affected versions (2.2.x stream, from rpms.lock.yaml at pinned commits):
- RHTPA 2.2.0 (tag v0.4.5): openssl-libs 3.0.7-25.el9_3
- RHTPA 2.2.1 (tag v0.4.8): openssl-libs 3.0.7-27.el9_4
- RHTPA 2.2.2 (retag of 2.2.1, v0.4.8): openssl-libs 3.0.7-27.el9_4
Not affected: RHTPA 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) ship 3.0.7-28.el9_4.

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Package origin: explicit install. openssl-libs is pinned in rpms.lock.yaml
  (resolved from rpms.in.yaml). SBOM verification was skipped (cosign not
  available), so this classification comes from rpms.lock.yaml only.
- Update the openssl-libs package spec (rpms.in.yaml / Dockerfile dnf install
  spec, if pinned) so it resolves to >= 3.0.7-28.el9_4.
- Regenerate rpms.lock.yaml and verify openssl-libs >= 3.0.7-28.el9_4.
- Note: the lock file at v0.4.11 / v0.4.12 already contains 3.0.7-28.el9_4.
  First check whether main already has the fix. If it does, the remaining
  work is to make sure the next 2.2.z release is built from it and to confirm
  the shipped image (or SBOM) contains the fixed package.
- Verify the Konflux build pipeline triggers successfully.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

After creation, post a description digest comment per `shared/description-digest-protocol.md`. Post it before any links or other comments.

(Coordination Guidance is omitted: the Source Repositories table has no Deployment Context column.)

## Case A – Cross-stream impact comment (on TC-8005)

```
Cross-stream impact: openssl-libs < 3.0.7-28.el9_4 also affects stream(s)
2.1.x (RHTPA 2.1.0, 2.1.1 ship openssl-libs 3.0.7-24.el9) based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

---
_Comment Footnote per shared/comment-footnote.md (skill: triage-security)_
```

If no `[rhtpa-2.1]` sibling CVE Jira exists for CVE-2026-40215, also create a **preemptive** task for 2.1.x:
- Repository: rhtpa-release.0.3.z. Same explicit-install template, targeting openssl-libs >= 3.0.7-28.el9_4. The fixed build for 2.1.x (el9 vs el9_4 stream) still needs to be checked.
- Labels: standard labels plus `security-preemptive`.
- Link: **Related** to TC-8005, not Depend. Not linked to the release Task.
- Description prefix noting it originates from CVE-2026-40215 / TC-8005 (2.2.x).

## Post-triage

- Add label `ai-cve-triaged` to TC-8005.
- Post a summary comment covering: the impact table, the Affects Versions correction, outcome (1 remediation task for 2.2.x, plus a cross-stream notice and maybe a preemptive 2.1.x task), task keys, release Jira keys, and an @mention of the issue reporter. Include the Comment Footnote.
