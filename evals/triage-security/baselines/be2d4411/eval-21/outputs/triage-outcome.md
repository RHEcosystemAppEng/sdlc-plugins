# Triage Outcome for TC-8020 (CVE-2026-31812)

## Summary

TC-8020 tracks CVE-2026-31812, a denial-of-service vulnerability in quinn-proto (versions before 0.11.14) with CVSS 7.5 (High). The issue is scoped to the 2.2.x version stream per its summary suffix `[rhtpa-2.2]`.

## Version Impact Summary

### Scoped Stream (2.2.x)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | fixed version |
| 2.2.4 | 0.11.14 | NO | fixed version |

### Cross-Stream Impact (2.1.x)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | |
| 2.1.1 | 0.11.9 | YES | |

## Affects Versions Correction

- **Before**: RHTPA 2.0.0 (incorrect -- no 2.0.x stream exists)
- **After**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Rationale**: Scoped to 2.2.x stream per issue suffix. Versions 2.2.3 and 2.2.4 are not affected (ship quinn-proto 0.11.14, at or above fix threshold).

## Triage Decision

### Step 7 -- Concurrent Triage Detection (BLOCKING)

Before proceeding to Case A/B/C remediation branching, concurrent triage detection identified that **TC-8019** is actively being triaged by **engineer-b@example.com** (status: In Progress) and affects the same upstream component (`quinn-proto`).

The engineer is presented with three options:

1. **Wait** -- Pause until TC-8019 completes, then re-run Step 4.3 to check overlap
2. **Skip** -- Skip remediation task creation; add explanatory Jira comment
3. **Proceed** -- Create tasks with `concurrent-triage-overlap` label for the other triage's Step 4.3 to detect

**The triage cannot proceed to remediation task creation until the engineer selects an option.**

### Pending Remediation Path (after Step 7 resolution)

Once the engineer resolves the concurrent triage gate, the following Case determination applies:

**Case A + Case B** -- the issue is both affected in its scoped stream and has cross-stream impact:

#### Case A: Affected (2.2.x stream)

Versions 2.2.0, 2.2.1, and 2.2.2 in the scoped 2.2.x stream ship a vulnerable version of quinn-proto (< 0.11.14). Since quinn-proto is a Cargo (source) dependency, **two remediation tasks** would be created:

1. **Upstream backport task** -- Backport the quinn-proto fix (bump to >= 0.11.14) in the rhtpa-backend source repository on the `release/0.4.z` branch. The upstream fix PR (quinn-rs/quinn#2048) is available as reference.

2. **Downstream propagation subtask** -- After the upstream fix lands, update the source tag reference in the Konflux release repo (`rhtpa-release.0.4.z`) to pick up the fixed version. This subtask is blocked by the upstream task.

Note: Versions 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 (the fixed version), so the upstream fix already exists on `release/0.4.z`. The remediation may only require a downstream propagation for the affected minor versions, depending on the release process.

#### Case B: Cross-Stream Impact (2.1.x stream)

The 2.1.x stream (versions 2.1.0 and 2.1.1) also ships vulnerable quinn-proto 0.11.9. Since this issue is scoped to 2.2.x, the 2.1.x impact is reported as cross-stream:

- A cross-stream impact comment would be posted to TC-8020 noting that the 2.1.x stream is also affected
- A search for sibling CVE Jiras with label CVE-2026-31812 and stream suffix `[rhtpa-2.1]` determines whether a companion issue already exists for 2.1.x
- If no companion CVE Jira exists for 2.1.x, proactive (preemptive) remediation tasks would be created with the `security-preemptive` label and "Related" link type
- If a companion CVE Jira exists, task creation is deferred to that issue's own triage

### Post-Triage Actions (after remediation)

1. Add `ai-cve-triaged` label to TC-8020
2. Post summary comment to TC-8020 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, 2.2.1, 2.2.2)
   - Triage outcome and remediation tasks created
   - @mention of the issue reporter (PSIRT analyst)
   - Comment Footnote per shared/comment-footnote.md

## Key Findings

1. **PSIRT Affects Versions was incorrect**: RHTPA 2.0.0 does not correspond to any configured version stream. Lock file analysis determined the correct affected versions in the 2.2.x stream.

2. **Partial fix already in stream**: The 2.2.x stream already has the fix in versions 2.2.3+ (quinn-proto 0.11.14). Only versions 2.2.0, 2.2.1, and 2.2.2 need remediation.

3. **Cross-stream impact**: The 2.1.x stream is also affected but is outside this issue's scope. Cross-stream coordination is needed.

4. **Concurrent triage blocking**: TC-8019 is actively triaging the same upstream component (quinn-proto). Remediation task creation is gated on the engineer's decision to wait, skip, or proceed with overlap labeling. This check runs before Case A/B/C branching to prevent duplicate remediation tasks.
