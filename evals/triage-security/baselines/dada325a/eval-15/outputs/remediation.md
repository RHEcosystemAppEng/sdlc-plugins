# Steps 4–8 and Post-Triage Summary: TC-8001

## Steps 4–7.5 (simulated, no Jira calls)

- **Step 4 – Siblings**: JQL `project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001` was not executed in this eval. No sibling data was supplied, so the eval assumes no same-stream duplicate and no 2.1.x companion issue. If a 2.1.x companion exists, link it as Related and skip the preemptive tasks below.
- **Step 4.3 – Cross-CVE overlap**: skipped because the Upstream Affected Component, PS Component and Stream fields are not configured.
- **Step 4.4 – Preemptive reconciliation**: no matching `security-preemptive` task was supplied (assumed none).
- **Step 5 – Lifecycle**: the product pages were not fetched in this eval. RHTPA 2.2.x is treated as supported. The engineer must confirm that 2.1.x is still supported before the preemptive tasks are created.
- **Step 6 – Already fixed**: no resolved siblings. Within the stream itself, the fix already shipped in RHTPA 2.2.3 (backend v0.4.11, quinn-proto 0.11.14).
- **Step 7 – Concurrent triage**: skipped because the Upstream Affected Component field is not configured.
- **Step 7.5 – Release Jira**: release Epic and Task lookup is needed only for streams that get new non-preemptive remediation. 2.2.x needs none, and the 2.1.x tasks are preemptive, so no release Epic or Task is created. 7.5.3 dedup is skipped because the field is not configured.

## Step 8 – Outcome

- **2.2.x (in scope)**: the affected releases are 2.2.0, 2.2.1 and 2.2.2. The fix is **already shipped** in RHTPA 2.2.3 and 2.2.4, so no new remediation Tasks are needed. Creating a bump or propagation task would duplicate work already released. Customers on 2.2.0 to 2.2.2 fix the issue by upgrading to 2.2.3 or later.
- **Case A, cross-stream (2.1.x)**: RHTPA 2.1.0 and 2.1.1 ship quinn-proto 0.11.9. The upstream fix on release/0.3.z is not confirmed. Because Cargo is a source dependency, two **preemptive** tasks are proposed, labelled `ai-generated-jira, Security, CVE-2026-31812, security-preemptive`:
  1. `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)`: upstream backport on rhtpa-backend, branch `release/0.3.z`.
  2. `Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`: downstream propagation, blocked by task 1. The pinning method is `artifacts.lock.yaml` (backend tag in the download URL).
  - Links: TC-8001 Related to each preemptive task, and task 1 Blocks task 2. Each task gets a description digest comment before any links are created.
- Labels: add `ai-cve-triaged` to TC-8001.
- All mutations require engineer confirmation (interactive mode).

---

## Post-triage summary comment (posted to TC-8001)

**Triage summary for CVE-2026-31812 (quinn-proto < 0.11.14, fixed in 0.11.14)**. Scope: stream 2.2.x `[rhtpa-2.2]`

**Version impact (lock file analysis at pinned commits from security-matrix.md)**

| Stream | Version | backend tag | quinn-proto | Affected? | Notes |
|--------|---------|-------------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | out of scope (cross-stream) |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | out of scope (cross-stream) |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.8 | — | YES | same as 2.2.1 (retag) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | fix shipped |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | fix shipped |

**Affects Versions correction**: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]. RHTPA 2.0.0 does not correspond to any supported stream.

**Outcome**: affected, and already remediated in-stream. RHTPA 2.2.3 and later ship quinn-proto 0.11.14, so no new 2.2.x remediation tasks were created. The recommended customer action is to upgrade to RHTPA 2.2.3 or later.

**Cross-stream impact**: quinn-proto < 0.11.14 also affects stream 2.1.x (RHTPA 2.1.0 and 2.1.1, quinn-proto 0.11.9) based on lock file analysis. That stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

**Remediation tasks**: the following preemptive tasks were created for stream 2.1.x, which has no CVE Jira:
- `<upstream-task-key>`: upstream backport, bump quinn-proto to 0.11.14 on rhtpa-backend `release/0.3.z` (security-preemptive)
- `<downstream-task-key>`: downstream propagation in rhtpa-release.0.3.z, blocked by `<upstream-task-key>` (security-preemptive)

These tasks use the "Related" link type. When PSIRT creates a 2.1.x CVE Jira, Step 4.4 reconciliation will link them and remove the label.

**Release Jira**: none. No non-preemptive remediation tasks were created.
**Dedup**: none. Dedup was skipped because the Upstream Affected Component field is not configured.

**Notes**: the security matrix is about 131 days old (Last-Updated 2026-06-28), so please refresh it. External CVE enrichment (MITRE/OSV) was unavailable. The due date of 2026-07-15 has passed.

@psirt-analyst: triage of TC-8001 is complete. Please review the corrected Affects Versions and the cross-stream finding for 2.1.x.

---
This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.

### ADF reporter mention node and footnote

```json
{ "type": "paragraph", "content": [
  { "type": "mention", "attrs": { "id": "557058:psirt-analyst-mock-id", "text": "@psirt-analyst" } },
  { "type": "text", "text": " triage of TC-8001 is complete. Please review the corrected Affects Versions and the cross-stream finding for 2.1.x." }
] },
{ "type": "rule" },
{ "type": "paragraph", "content": [
  { "type": "text", "text": "This comment was AI-generated by " },
  { "type": "text", "text": "sdlc-workflow/triage-security", "marks": [ { "type": "link", "attrs": { "href": "https://github.com/RHEcosystemAppEng/sdlc-plugins" } } ] },
  { "type": "text", "text": " v0.13.10." }
] }
```
