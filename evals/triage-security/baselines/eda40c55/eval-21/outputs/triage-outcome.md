# Triage Outcome -- TC-8020

## CVE Summary

- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Fix threshold**: >= 0.11.14
- **CVSS**: 7.5 (High)
- **Ecosystem**: Cargo (Rust crate)

## Version Impact Table

| Stream | Product Version | Build Tag | quinn-proto | Affected? |
|--------|----------------|-----------|-------------|-----------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES |
| 2.2.x | 2.2.2 | v0.4.9 | 0.11.12 | YES (retag of 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO (fixed) |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO (fixed) |

## Affects Versions Correction (Step 3)

The issue is scoped to stream **2.2.x** (from summary suffix `[rhtpa-2.2]`).

- **Current (PSIRT-assigned)**: RHTPA 2.0.0
- **Proposed correction**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

RHTPA 2.0.0 is incorrect -- there is no 2.0.x stream. The affected 2.2.x versions are 2.2.0, 2.2.1, and 2.2.2. Versions 2.2.3 and 2.2.4 are NOT affected because they already ship quinn-proto 0.11.14 (the fix version).

The 2.1.x versions (2.1.0, 2.1.1) are also affected but belong to a different stream. They are excluded from this issue's Affects Versions correction per stream-scoping rules and are handled via Case B cross-stream notification.

## Concurrent Triage Detection (Step 7)

A concurrent triage was detected: **TC-8019** is In Progress on the same upstream component (`quinn-proto`), assigned to engineer-b@example.com.

The engineer is presented with three options before proceeding to Case A/B/C:

1. **Wait** -- pause until TC-8019 completes, then re-run to detect overlap
2. **Skip** -- skip remediation task creation
3. **Proceed** -- create tasks with `concurrent-triage-overlap` label

The engineer must choose before the skill proceeds to Step 8.

## Triage Decision (Step 8) -- Pending Concurrent Triage Resolution

Assuming the engineer chooses to **proceed** (Option 3), the triage would branch as follows:

### Case A: Affected -- Create Remediation Tasks

The scoped stream (2.2.x) has affected versions (2.2.0, 2.2.1, 2.2.2), so remediation tasks are needed. Since quinn-proto is a **Cargo** (source dependency) ecosystem, **two tasks** would be created:

1. **Upstream backport task**: Backport the quinn-proto fix (bump to >= 0.11.14) in the `rhtpa-backend` source repository on branch `release/0.4.z`.
   - Labels: CVE-2026-31812, security, concurrent-triage-overlap
   - Link: Depend from TC-8020

2. **Downstream propagation subtask**: Update the quinn-proto version reference in the Konflux release repo (`rhtpa-release.0.4.z`) after the upstream fix lands.
   - Blocked by the upstream task
   - Labels: CVE-2026-31812, security, concurrent-triage-overlap
   - Link: Depend from TC-8020

Both tasks would carry the `concurrent-triage-overlap` label (from Step 7, Option 3) to enable TC-8019's Step 4.3 cross-CVE overlap detection to identify the relationship.

### Case B: Cross-Stream Impact

The version impact analysis reveals that stream **2.1.x** is also affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9). Since this issue is scoped to 2.2.x, a cross-stream impact comment would be posted:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. This stream is tracked by companion issues
(see Related links) or may require separate PSIRT triage.
```

A check for existing CVE Jiras for the 2.1.x stream would be performed (Step 4 sibling search). If no sibling CVE Jira exists for the 2.1.x stream, **preemptive remediation tasks** would be created for that stream with the `security-preemptive` label and "Related" link type.

### Case C: Not Applicable

Case C (close as Not a Bug) does not apply here because supported versions within the scoped stream are affected.

## Post-Triage Actions

After remediation:
1. Add `ai-cve-triaged` label to TC-8020
2. Post summary comment to TC-8020 with:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2)
   - Remediation task links
   - Cross-stream impact notice for 2.1.x
   - Concurrent triage note regarding TC-8019
   - @mention of the issue reporter
   - Comment Footnote per shared/comment-footnote.md
