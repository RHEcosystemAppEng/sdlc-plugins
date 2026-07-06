# Triage Outcome -- TC-8020

## Issue Summary

- **Issue**: TC-8020
- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Fix Threshold**: >= 0.11.14
- **Stream Scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **CVSS**: 7.5 (High)

## Version Impact Summary

### Stream 2.2.x (in scope)

| Product Version | quinn-proto | Affected? |
|-----------------|-------------|-----------|
| RHTPA 2.2.0 | 0.11.9 | YES |
| RHTPA 2.2.1 | 0.11.12 | YES |
| RHTPA 2.2.2 | 0.11.12 (retag) | YES |
| RHTPA 2.2.3 | 0.11.14 | NO (fixed) |
| RHTPA 2.2.4 | 0.11.14 | NO (fixed) |

### Stream 2.1.x (out of scope -- cross-stream)

| Product Version | quinn-proto | Affected? |
|-----------------|-------------|-----------|
| RHTPA 2.1.0 | 0.11.9 | YES |
| RHTPA 2.1.1 | 0.11.9 | YES |

## Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions (`RHTPA 2.0.0`) is incorrect. There is no 2.0.x stream in the configured Version Streams. Based on lock file analysis scoped to the 2.2.x stream, the corrected Affects Versions should be:

- **Current**: `[RHTPA 2.0.0]`
- **Proposed**: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14, which is the fixed version and is not vulnerable.

## Concurrent Triage Detection (Step 7)

A concurrent triage was detected: **TC-8019** is `In Progress`, assigned to `engineer-b@example.com`, and also targets the `quinn-proto` upstream component (customfield_10632).

Three options were presented to the engineer:

1. **Wait** -- Pause until TC-8019 completes, then re-run Step 4.3 to detect overlap
2. **Skip** -- Skip remediation task creation, add explanatory comment
3. **Proceed** -- Create tasks with `concurrent-triage-overlap` label for later reconciliation

The engineer must choose before Case A/B/C branching proceeds.

## Triage Decision (pending Step 7 resolution)

The triage analysis is complete through Step 7. The branching decision depends on the engineer's response to the concurrent triage warning:

### If proceeding to Case A/B/C:

**Case A applies**: Supported versions within the 2.2.x stream are affected (RHTPA 2.2.0, 2.2.1, 2.2.2). Remediation tasks would be created for the 2.2.x stream:

- **Upstream backport task**: Backport the quinn-proto fix (>= 0.11.14) into the source repository on the `release/0.4.z` branch. The upstream fix PR is quinn-rs/quinn#2048.
- **Downstream propagation subtask**: Update the backend component reference in the Konflux release repo (`rhtpa-release.0.4.z`) to a tag that includes quinn-proto >= 0.11.14. Blocked by the upstream task.

**Case B also applies**: Cross-stream impact detected. The 2.1.x stream (out of scope for this issue) is also affected -- all versions (RHTPA 2.1.0, 2.1.1) ship quinn-proto 0.11.9, which is vulnerable. A cross-stream impact comment would be posted, and if no sibling CVE Jira exists for the 2.1.x stream, preemptive remediation tasks with the `security-preemptive` label would be created for that stream.

### If waiting (Option 1):

Triage pauses. The engineer should re-run after TC-8019 completes. At that point, Step 4.3 cross-CVE overlap detection will determine if TC-8019's remediation already bumps quinn-proto past 0.11.14, potentially allowing TC-8020 to be closed without new tasks.

### If skipping (Option 2):

No remediation tasks are created. A comment is added to TC-8020 documenting that task creation was skipped due to concurrent triage on TC-8019. The Affects Versions correction and ai-cve-triaged label are still applied.

## Post-Triage Actions (applicable regardless of Step 7 choice)

1. Add `ai-cve-triaged` label to TC-8020
2. Post summary comment documenting version impact table, Affects Versions correction, triage outcome, and @mention of the issue reporter
3. Comment includes the Comment Footnote per skill requirements
