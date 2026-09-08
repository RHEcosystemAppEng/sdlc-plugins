# Triage Outcome for TC-8020

## Issue Summary

- **Issue**: TC-8020
- **CVE**: CVE-2026-31812
- **Library**: quinn-proto (Cargo / Rust crate)
- **Affected range**: versions before 0.11.14
- **Fixed version**: 0.11.14
- **CVSS**: 7.5 (High)
- **Stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)

## Triage Decision: Case B (Affected) with Case A (Cross-Stream Impact)

### Rationale

The version impact analysis determined that multiple supported versions ship a vulnerable version of quinn-proto (< 0.11.14):

**Within issue scope (2.2.x stream):**
- 2.2.0 ships quinn-proto 0.11.9 -- AFFECTED
- 2.2.1 ships quinn-proto 0.11.12 -- AFFECTED
- 2.2.2 is a retag of 2.2.1 -- AFFECTED (same as 2.2.1)
- 2.2.3 ships quinn-proto 0.11.14 -- NOT affected (fixed version)
- 2.2.4 ships quinn-proto 0.11.14 -- NOT affected (fixed version)

**Outside issue scope (2.1.x stream -- cross-stream impact):**
- 2.1.0 ships quinn-proto 0.11.9 -- AFFECTED
- 2.1.1 ships quinn-proto 0.11.9 -- AFFECTED

Since the issue is scoped to the 2.2.x stream but the 2.1.x stream is also affected, this triggers both Case A (cross-stream impact notification) and Case B (remediation task creation for the scoped stream).

### Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, which is incorrect -- no 2.0.x stream exists. Based on the version impact analysis scoped to the 2.2.x stream, the corrected Affects Versions should be:

- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are excluded because they ship the fixed version (0.11.14). Versions from the 2.1.x stream are excluded because this issue is scoped to 2.2.x -- those are tracked by companion issues.

### Concurrent Triage Gate (Step 7)

A concurrent triage was detected: **TC-8019** is In Progress, assigned to engineer-b@example.com, and targets the same upstream component (quinn-proto). The engineer must choose one of three options before remediation task creation can proceed:

1. **Wait** -- pause until TC-8019 completes, then re-check for overlap
2. **Skip** -- skip remediation task creation entirely
3. **Proceed** -- create tasks with `concurrent-triage-overlap` label

This gate blocks progression to Case A/B task creation.

### Remediation Plan (pending Step 7 resolution)

If the engineer chooses to proceed (Option 3) or wait and later resume:

#### Case A: Cross-Stream Impact Comment

Post a comment on TC-8020:
> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. The 2.1.x stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

Check for existing sibling CVE Jiras for the 2.1.x stream. If none exist, create preemptive remediation tasks for the 2.1.x stream with the `security-preemptive` label and "Related" link type.

#### Case B: Remediation Tasks for 2.2.x Stream

Since quinn-proto is a **source dependency** (Cargo ecosystem), create **two tasks** per stream:

**Task 1 -- Upstream backport:**
- Summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)"
- Repository: rhtpa-backend (backend)
- Target Branch: release/0.4.z
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
- Description: Bump quinn-proto to >= 0.11.14 in Cargo.lock
- Upstream fix PR: https://github.com/quinn-rs/quinn/pull/2048
- Link: Depend on TC-8020

**Task 2 -- Downstream propagation (blocked by Task 1):**
- Summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)"
- Repository: rhtpa-release.0.4.z
- Target Branch: main
- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
- Link: Depend on TC-8020; Blocks relationship from Task 1

### Post-Triage Actions

After remediation task creation:
1. Add `ai-cve-triaged` label to TC-8020
2. Transition TC-8020 to In Progress
3. Post summary comment with version impact table, Affects Versions correction, and links to all created tasks (with @mention of the issue reporter)
4. Include the Comment Footnote in all Jira comments

### Key Findings

1. **PSIRT Affects Versions was wrong**: RHTPA 2.0.0 does not exist as a version stream. Corrected to RHTPA 2.2.0, 2.2.1, 2.2.2.
2. **Fix already shipped in later versions**: 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version). The vulnerability was remediated in build v0.4.11.
3. **Cross-stream impact**: The 2.1.x stream is also affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9), requiring Case A cross-stream notification and potential preemptive remediation tasks.
4. **Concurrent triage blocker**: TC-8019 is actively being triaged on the same component (quinn-proto). Remediation task creation is gated pending the engineer's decision on how to handle the concurrency.
