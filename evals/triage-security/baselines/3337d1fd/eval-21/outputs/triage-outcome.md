# Triage Outcome for TC-8020 (CVE-2026-31812)

## Summary

CVE-2026-31812 affects `quinn-proto` versions before 0.11.14, a denial-of-service
vulnerability where a remote attacker can cause a panic by sending a QUIC transport
frame that creates an excessive number of streams.

## Version Impact Summary

The issue is **scoped to stream 2.2.x** (from summary suffix `[rhtpa-2.2]`).

### In-scope stream (2.2.x)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | (retag of 2.2.1) | YES |
| 2.2.3 | 0.11.14 | NO (fixed) |
| 2.2.4 | 0.11.14 | NO (fixed) |

### Cross-stream impact (2.1.x)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

## Affects Versions Correction (Step 3)

PSIRT assigned `RHTPA 2.0.0`, which is incorrect -- no 2.0.x stream exists.

- **Current**: `[RHTPA 2.0.0]`
- **Proposed**: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

The correction is scoped to stream 2.2.x per the issue suffix. Versions 2.2.3
and 2.2.4 are excluded because they ship quinn-proto 0.11.14 (the fixed version).

## Triage Decision Path

### Step 7 -- Concurrent Triage Detection: BLOCKED

A concurrent triage was detected on the same upstream component (`quinn-proto`):

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

The engineer must choose one of three options before remediation tasks can be
created:

1. **Wait** -- pause and re-run after TC-8019 completes (recommended)
2. **Skip** -- skip remediation task creation entirely
3. **Proceed** -- create tasks with `concurrent-triage-overlap` label

**See `concurrent-triage.md` for the full analysis.**

### Triage Outcome (pending Step 7 resolution)

Assuming the engineer chooses to proceed (Option 3) or waits and then re-runs:

**Case A applies: Affected -- create remediation tasks.**

Three versions within the scoped stream (2.2.0, 2.2.1, 2.2.2) ship a vulnerable
version of quinn-proto (< 0.11.14). Versions 2.2.3 and 2.2.4 already ship the
fixed version (0.11.14).

**Case B also applies: Cross-stream impact.**

Stream 2.1.x is also affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9).
Since this is a scoped issue, a cross-stream impact comment would be posted,
and preemptive remediation tasks would be created for stream 2.1.x if no
companion CVE Jira exists for that stream.

### Planned Remediation Tasks (if engineer proceeds)

Since quinn-proto is a **Cargo** (source dependency) ecosystem package, **two tasks
per affected stream** would be created:

#### Stream 2.2.x (in-scope -- standard remediation)

1. **Upstream backport task**:
   - Summary: `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)`
   - Repository: backend (rhtpa-backend)
   - Target branch: `release/0.4.z`
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
   - Link type: Depend (to TC-8020)
   - If proceeding with concurrent triage: add `concurrent-triage-overlap` label

2. **Downstream propagation subtask**:
   - Summary: `Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)`
   - Repository: rhtpa-release.0.4.z
   - Target branch: main
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
   - Blocked by: upstream backport task
   - Link type: Depend (to TC-8020)

#### Stream 2.1.x (cross-stream -- preemptive remediation, Case B)

If no companion CVE Jira exists for stream 2.1.x:

3. **Preemptive upstream backport task**:
   - Summary: `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)`
   - Repository: backend (rhtpa-backend)
   - Target branch: `release/0.3.z`
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
   - Link type: Related (to TC-8020, because cross-stream)

4. **Preemptive downstream propagation subtask**:
   - Summary: `Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`
   - Repository: rhtpa-release.0.3.z
   - Target branch: main
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
   - Blocked by: preemptive upstream backport task
   - Link type: Related (to TC-8020)

### Coordination Guidance

Since the Deployment Context column is absent from the Source Repositories table
(backward compatibility), coordination guidance is omitted from remediation task
descriptions.

### Post-Triage Actions

After remediation tasks are created:

1. Add `ai-cve-triaged` label to TC-8020
2. Transition TC-8020 to In Progress
3. Post summary comment to TC-8020 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, 2.2.1, 2.2.2)
   - Remediation tasks created (upstream + downstream for 2.2.x)
   - Preemptive tasks created for 2.1.x (if applicable)
   - @mention of the issue reporter
4. If concurrent triage (Option 3): the `concurrent-triage-overlap` label
   ensures TC-8019's Step 4.3 will detect the overlap

## Key Findings

1. **PSIRT Affects Versions are incorrect**: RHTPA 2.0.0 does not correspond to
   any configured version stream. The correct affected versions for stream 2.2.x
   are RHTPA 2.2.0, 2.2.1, and 2.2.2.

2. **Partial fix already shipped**: Versions 2.2.3 and 2.2.4 already include
   quinn-proto 0.11.14 (the fixed version), so they are not affected.

3. **Cross-stream impact**: Stream 2.1.x is also affected (both versions ship
   quinn-proto 0.11.9), requiring either companion CVE Jiras from PSIRT or
   preemptive remediation tasks.

4. **Concurrent triage risk**: TC-8019 is being actively triaged for the same
   upstream component (quinn-proto). The engineer should coordinate with
   engineer-b@example.com to avoid duplicate remediation tasks. Waiting for
   TC-8019 to complete is the recommended approach.
