# Triage Outcome for TC-8021 (CVE-2026-31812 / quinn-proto)

## Summary

TC-8021 is a stream-scoped Vulnerability issue for CVE-2026-31812 affecting the quinn-proto Rust crate (versions before 0.11.14). The issue is scoped to the **2.2.x** stream via the `[rhtpa-2.2]` summary suffix.

## Triage Decision: Case B (Affected) + Case A (Cross-Stream Impact)

### Rationale

**Within the scoped 2.2.x stream**, three versions are affected:

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | (retag of 2.2.1) | YES |
| 2.2.3 | 0.11.14 | NO |
| 2.2.4 | 0.11.14 | NO |

Since supported versions within the issue's stream scope are affected, this is **Case B** (create remediation tasks).

**Cross-stream impact (Case A)**: The 2.1.x stream is also affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14). Since this issue is scoped to 2.2.x, the cross-stream impact on 2.1.x triggers **Case A** -- a cross-stream impact comment would be posted, and preemptive remediation tasks would be created for 2.1.x if no companion CVE Jira exists for that stream.

### Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions (`RHTPA 2.0.0`) is incorrect. RHTPA 2.0.0 does not correspond to any version in the configured version streams.

- **Current**: RHTPA 2.0.0
- **Proposed**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

This correction is scoped to the 2.2.x stream per the issue's `[rhtpa-2.2]` suffix. Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14 (at or above the fix threshold).

### Concurrent Triage (Step 7)

No concurrent triages detected on the same upstream component (quinn-proto). Proceeding with remediation task creation.

### Remediation Tasks (Step 8 -- Case B)

Quinn-proto is a **Cargo** (source dependency) ecosystem package. Per the ecosystem classification table, source dependency ecosystems produce **two tasks per affected stream**.

#### For stream 2.2.x (scoped -- standard remediation):

1. **Upstream backport/dependency bump task**: Bump quinn-proto to >= 0.11.14 in the backend repository on the `release/0.4.z` branch. Since versions 2.2.3+ already ship 0.11.14, the upstream fix is already available on this branch. This means the **dependency bump variant** applies (Step 2.5 confirms the fix is on the upstream branch). The task would use `cargo update -p quinn-proto` to pull in the fixed version.

2. **Downstream propagation task**: Update the backend source reference in the rhtpa-release.0.4.z Konflux release repo to pick up the upstream fix. Blocked by the upstream task.

Both tasks linked to TC-8021 via "Depend" link type. Both linked to the release Task (if created in Step 7.5) via "Blocks".

#### For stream 2.1.x (cross-stream -- Case A preemptive remediation):

If no companion CVE Jira exists for the 2.1.x stream:

1. **Preemptive upstream backport task**: Bump quinn-proto to >= 0.11.14 on the `release/0.3.z` branch. Labels include `security-preemptive`. Linked to TC-8021 via "Related" (not "Depend").

2. **Preemptive downstream propagation task**: Update backend source reference in rhtpa-release.0.3.z. Labels include `security-preemptive`. Linked to TC-8021 via "Related".

If a companion CVE Jira already exists for 2.1.x, skip preemptive task creation for that stream -- it will be triaged through its own issue.

### Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8021.
2. Post summary comment to TC-8021 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 replaced with RHTPA 2.2.0, 2.2.1, 2.2.2)
   - Remediation tasks created (upstream/bump + downstream for 2.2.x)
   - Preemptive tasks created for 2.1.x (if applicable)
   - Release Jira references (if Step 7.5 produced release Epic/Task)
   - @mention of the issue reporter
   - Comment Footnote per shared/comment-footnote.md

### VEX Justification

Not applicable -- this is not a "Not a Bug" closure. Affected versions exist within the scoped stream, so remediation tasks are created (Case B), not closed (Case C).

### Pre-Creation Checklist

- [x] **Task count per stream**: Cargo (source dependency) produces 2 tasks per stream (dependency bump + downstream propagation for 2.2.x; upstream backport + downstream propagation for 2.1.x preemptive)
- [x] **Cross-stream coverage**: 2.1.x is affected and would receive preemptive tasks (or has an existing sibling CVE Jira)
- [x] **Link types**: "Depend" for tasks linked to TC-8021 (scoped stream); "Related" for preemptive tasks linked to TC-8021 (cross-stream); "Blocks" for upstream to downstream within a stream
- [x] **Preemptive labels**: 2.1.x tasks carry `security-preemptive` label
- [x] **Coordination guidance**: Deployment context defaults to `upstream` (column absent from Source Repositories table), so coordination guidance subsection is omitted
- [x] **Release Jira linking**: Applicable if Step 7.5 produced release Tasks
- [x] **Dedup consistency**: No dedup detected (Step 7 returned zero concurrent triages; Step 7.5.3 would check at runtime)
