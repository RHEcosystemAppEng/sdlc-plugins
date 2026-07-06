# Triage Outcome for TC-8021 (CVE-2026-31812 / quinn-proto)

## Summary

TC-8021 is a Vulnerability issue for CVE-2026-31812, affecting quinn-proto (versions before 0.11.14), scoped to the **2.2.x** stream via the `[rhtpa-2.2]` suffix.

## Version Impact Table

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | out of scope (cross-stream) |
| 2.1.1 | 2.1.x | 0.11.9 | YES | out of scope (cross-stream) |
| 2.2.0 | 2.2.x | 0.11.9 | YES | in scope |
| 2.2.1 | 2.2.x | 0.11.12 | YES | in scope |
| 2.2.2 | 2.2.x | -- | YES | in scope, retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | fixed version shipped |
| 2.2.4 | 2.2.x | 0.11.14 | NO | fixed version shipped |

## Concurrent Triage Detection (Step 7)

No concurrent triages detected on the quinn-proto component. JQL search returned zero results. Proceeding to Case A/B/C branching.

## Case Determination

### Case A: Affected -- remediation required

Within the scoped 2.2.x stream, versions **2.2.0, 2.2.1, and 2.2.2** ship quinn-proto versions below the fix threshold of 0.11.14. These versions are affected and require remediation.

Since quinn-proto is a **Cargo** ecosystem dependency (source dependency), remediation produces **two tasks**:

1. **Upstream backport task** -- bump quinn-proto to >= 0.11.14 in the rhtpa-backend source repository on the `release/0.4.z` branch. The upstream fix PR (quinn-rs/quinn#2048) is already available, and tags v0.4.11 and v0.4.12 already ship the fix (0.11.14), indicating the upstream branch has already been fixed.

2. **Downstream propagation subtask** -- update the source tag reference in the Konflux release repo (rhtpa-release.0.4.z) artifacts.lock.yaml to point to an upstream tag that includes quinn-proto >= 0.11.14 (i.e., v0.4.11 or later). This subtask is blocked by the upstream task.

Since the upstream branch already has the fix at tags v0.4.11+ (quinn-proto 0.11.14), the upstream backport task may already be satisfied. The downstream propagation involves ensuring that any new release builds for versions 2.2.0/2.2.1/2.2.2 use updated source pins.

### Case B: Cross-stream impact

The 2.1.x stream is also affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9). Since this issue is scoped to 2.2.x, the 2.1.x impact is handled via Case B:

- Post a cross-stream impact comment on TC-8021 noting that stream 2.1.x is also affected.
- Search for sibling Vulnerability issues with label CVE-2026-31812 and stream suffix `[rhtpa-2.1]`.
  - If a sibling exists for 2.1.x: link it as Related (no duplicate task creation for that stream).
  - If no sibling exists for 2.1.x: create preemptive remediation tasks for the 2.1.x stream with the `security-preemptive` label, linked as "Related" (not "Depend") to TC-8021.

### Case C: Not applicable

Case C (close as Not a Bug) does not apply because supported versions within the 2.2.x scope ARE affected.

## Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, which is incorrect -- there is no 2.0.x version stream configured. The correct Affects Versions, scoped to the 2.2.x stream, are:

- Current: [RHTPA 2.0.0]
- Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

Versions 2.2.3 and 2.2.4 are excluded because they ship the fixed version (0.11.14).

## Triage Decision

**Create remediation tasks for the 2.2.x stream (Case A) and handle cross-stream impact for the 2.1.x stream (Case B).**

The issue should NOT be closed. Remediation is needed for versions 2.2.0, 2.2.1, and 2.2.2 within the scoped stream. The Affects Versions field must be corrected from RHTPA 2.0.0 to [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]. The `ai-cve-triaged` label should be added after all triage actions are complete.
