# Triage Outcome for TC-8021

## Summary

**CVE**: CVE-2026-31812
**Library**: quinn-proto
**Fix threshold**: >= 0.11.14
**Issue scope**: Stream 2.2.x (from summary suffix `[rhtpa-2.2]`)
**Ecosystem**: Cargo (source dependency)

## Version Impact Table

| Stream | Version | quinn-proto | Affected? |
|--------|---------|-------------|-----------|
| 2.1.x | 2.1.0 | 0.11.9 | YES |
| 2.1.x | 2.1.1 | 0.11.9 | YES |
| **2.2.x** | **2.2.0** | **0.11.9** | **YES** |
| **2.2.x** | **2.2.1** | **0.11.12** | **YES** |
| **2.2.x** | **2.2.2** | **0.11.12** | **YES** (retag of 2.2.1) |
| 2.2.x | 2.2.3 | 0.11.14 | NO |
| 2.2.x | 2.2.4 | 0.11.14 | NO |

Bold rows indicate the issue's scoped stream (2.2.x).

## Triage Decision Path

### Step 7 -- Concurrent Triage Detection

No concurrent triages detected for the `quinn-proto` upstream component (JQL returned zero results). Proceeding to Case A/B/C.

### Case Determination

1. **Are any supported versions affected?** YES -- versions 2.2.0, 2.2.1, and 2.2.2 in stream 2.2.x are affected. This rules out Case C (close as Not a Bug).

2. **Is the issue scoped to a single stream?** YES -- the issue is scoped to stream 2.2.x via the `[rhtpa-2.2]` suffix.

3. **Are other streams also affected?** YES -- stream 2.1.x (versions 2.1.0 and 2.1.1) ships quinn-proto 0.11.9, which is below the fix threshold of 0.11.14.

Therefore: **Case A applies** (cross-stream impact), followed by **Case B** (create remediation tasks).

### Case A -- Cross-Stream Impact

Stream 2.1.x is also affected but is outside this issue's scope. The following actions would be taken:

1. **Post cross-stream impact comment** on TC-8021:
   > Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. Stream 2.1.x ships quinn-proto 0.11.9 in all versions (2.1.0, 2.1.1). These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

2. **Check for existing CVE Jiras** for stream 2.1.x by searching for sibling Vulnerability issues with label CVE-2026-31812 and stream suffix `[rhtpa-2.1]`.

3. **If no sibling CVE Jira exists for 2.1.x**: create preemptive remediation tasks with the `security-preemptive` label and "Related" link type back to TC-8021.

4. **If a sibling CVE Jira exists for 2.1.x**: skip preemptive task creation for that stream (it will be triaged through its own CVE issue).

### Case B -- Remediation Tasks for Stream 2.2.x

Since quinn-proto is a Cargo (source dependency) ecosystem, **two tasks** are required for the 2.2.x stream:

**Task 1 -- Upstream Backport**:
- Summary: `Backport quinn-proto fix for CVE-2026-31812 to release/0.4.z [rhtpa-2.2]`
- Description: Bump quinn-proto from 0.11.12 (or 0.11.9) to >= 0.11.14 in the upstream source repository (rhtpa-backend) on the `release/0.4.z` branch
- Labels: CVE-2026-31812, security-fix
- Link: Depend on TC-8021

**Task 2 -- Downstream Propagation**:
- Summary: `Propagate quinn-proto CVE-2026-31812 fix to rhtpa-release.0.4.z [rhtpa-2.2]`
- Description: Update the Konflux release repo (rhtpa-release.0.4.z) to pick up the new backend build containing the quinn-proto fix
- Labels: CVE-2026-31812, security-fix
- Link: Depend on TC-8021, Blocked by Task 1 (upstream backport)

### Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions `RHTPA 2.0.0` is incorrect. There is no 2.0.x stream configured.

**Correction** (scoped to stream 2.2.x):
- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14, which is at or above the fix threshold.

### Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8021
2. Post summary comment documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 replaced with RHTPA 2.2.0, 2.2.1, 2.2.2)
   - Cross-stream impact on 2.1.x
   - Remediation tasks created (2 tasks for stream 2.2.x, plus preemptive tasks for 2.1.x if no sibling CVE Jira exists)
   - @mention of the issue reporter
   - Comment Footnote per shared/comment-footnote.md

## Key Findings

- The PSIRT-assigned Affects Versions (`RHTPA 2.0.0`) is wrong -- RHTPA 2.0.0 does not correspond to any configured version stream
- The fix was already incorporated in versions 2.2.3+ (build tag v0.4.11 onward), which ship quinn-proto 0.11.14
- Versions 2.2.0 through 2.2.2 remain affected and require remediation
- Stream 2.1.x is entirely affected (all versions ship quinn-proto 0.11.9), requiring cross-stream notification and potential preemptive remediation
