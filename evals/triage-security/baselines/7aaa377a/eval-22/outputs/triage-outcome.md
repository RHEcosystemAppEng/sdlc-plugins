# Triage Outcome for TC-8021 (CVE-2026-31812)

## Version Impact Summary

The issue is scoped to the **2.2.x** stream (suffix `[rhtpa-2.2]`). Version impact analysis was performed across all streams to enable cross-stream impact detection.

### Version Impact Table

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | |
| 2.1.1 | 0.11.9 | YES | |
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | |
| 2.2.4 | 0.11.14 | NO | |

### In-Scope Versions (2.2.x stream)

- RHTPA 2.2.0: **affected** (quinn-proto 0.11.9 < 0.11.14)
- RHTPA 2.2.1: **affected** (quinn-proto 0.11.12 < 0.11.14)
- RHTPA 2.2.2: **affected** (retag of 2.2.1 -- same as 2.2.1)
- RHTPA 2.2.3: not affected (quinn-proto 0.11.14 >= 0.11.14)
- RHTPA 2.2.4: not affected (quinn-proto 0.11.14 >= 0.11.14)

## Step 7 -- Concurrent Triage Detection

No concurrent triages were detected for upstream component `quinn-proto`. The JQL search returned zero results. Proceeding directly to Case A/B/C branching.

## Case Determination

Since supported versions within the issue's scope are affected (2.2.0, 2.2.1, 2.2.2), this is **Case B (Affected -- create remediation tasks)**.

Additionally, since this is a scoped issue and the 2.1.x stream is also affected (2.1.0 and 2.1.1), **Case A (Cross-stream impact)** also applies. A cross-stream impact comment would be posted, and sibling CVE Jiras for stream 2.1.x would be checked before deciding whether to create preemptive remediation tasks for that stream.

### Proposed Actions (not executed -- eval mode)

1. **Affects Versions Correction** (Step 3): Propose correcting from `[RHTPA 2.0.0]` to `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`, scoped to the 2.2.x stream.

2. **Case A -- Cross-stream impact comment**: Post comment noting that stream 2.1.x is also affected (2.1.0 and 2.1.1 ship quinn-proto 0.11.9 < 0.11.14).

3. **Case B -- Remediation task creation** (for 2.2.x stream):
   - **Upstream backport task**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2), targeting `release/0.4.z` branch in `backend` repository.
   - **Downstream propagation subtask**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2), blocked by the upstream task.

4. **Post-triage summary**: Add `ai-cve-triaged` label, transition to In Progress, and post a summary comment with the version impact table and remediation task links.
