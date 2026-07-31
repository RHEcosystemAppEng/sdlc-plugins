# Triage Outcome for TC-8020

## Summary

CVE-2026-31812 affects quinn-proto (versions before 0.11.14). The issue is scoped to the 2.2.x stream. Version impact analysis shows that versions 2.2.0, 2.2.1, and 2.2.2 are affected (shipping quinn-proto < 0.11.14), while versions 2.2.3 and 2.2.4 are not affected (shipping quinn-proto 0.11.14). Cross-stream analysis shows the 2.1.x stream is also affected.

## Concurrent Triage Gate (Step 7)

Before proceeding to remediation (Case A/B/C branching in Step 8), the concurrent triage detection in Step 7 identified an active triage on the same upstream component:

- **TC-8019** is In Progress, assigned to engineer-b@example.com, and affects the same upstream component `quinn-proto` (customfield_10632).

This blocks automatic progression to Step 8. The engineer must choose one of three options:

1. **Wait** -- pause and re-run after TC-8019 completes
2. **Skip** -- skip remediation task creation entirely
3. **Proceed** -- create tasks with `concurrent-triage-overlap` label

## Pending Triage Decision (Contingent on Step 7 Resolution)

If the engineer chooses **Proceed** (option 3) or **Wait** and later re-runs:

### Case A: Cross-stream impact (scoped issue)

This issue is scoped to 2.2.x, but 2.1.x versions are also affected. Case A applies:
- Post cross-stream impact comment noting 2.1.x is affected
- Check for existing sibling CVE Jiras for the 2.1.x stream
- If no sibling exists, create preemptive remediation tasks for 2.1.x with `security-preemptive` label

### Case B: Remediation tasks for 2.2.x stream

Since versions 2.2.0, 2.2.1, and 2.2.2 are affected within the issue's scope:
- **Ecosystem**: Cargo (source dependency) -- 2 tasks per stream
- **Upstream backport task**: Bump quinn-proto to >= 0.11.14 in the backend repository on branch release/0.4.z
- **Downstream propagation task**: Update backend source reference in rhtpa-release.0.4.z to pick up the upstream fix

### Affects Versions Correction (Step 3)

Current: [RHTPA 2.0.0] (incorrect -- RHTPA 2.0.0 does not exist in the configured streams)
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2] (scoped to 2.2.x stream only)

### Key Constraint

No remediation tasks can be created until the engineer resolves the Step 7 concurrent triage warning. This prevents duplicate work when TC-8019 (also targeting quinn-proto) may already be creating overlapping remediation tasks.
