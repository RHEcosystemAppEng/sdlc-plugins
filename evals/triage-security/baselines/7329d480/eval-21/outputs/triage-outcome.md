# Triage Outcome -- TC-8020 (CVE-2026-31812)

## Summary

TC-8020 tracks CVE-2026-31812, a denial-of-service vulnerability in the
`quinn-proto` Rust crate (CVSS 7.5, High severity). The vulnerability affects
quinn-proto versions before 0.11.14 and is fixed in version 0.11.14.

## Version Impact Findings

The issue is scoped to the **2.2.x** stream (per summary suffix `[rhtpa-2.2]`).

### In-scope stream (2.2.x)

| Product Version | quinn-proto Version | Affected? |
|----------------|---------------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | 0.11.12 (retag of 2.2.1) | YES |
| 2.2.3 | 0.11.14 | NO (fixed) |
| 2.2.4 | 0.11.14 | NO (fixed) |

Three versions (2.2.0, 2.2.1, 2.2.2) are affected within the 2.2.x stream.
Two versions (2.2.3, 2.2.4) already ship the fixed quinn-proto version.

### Cross-stream impact (2.1.x)

| Product Version | quinn-proto Version | Affected? |
|----------------|---------------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

All 2.1.x versions are affected. This triggers **Case B** (cross-stream impact).

## Affects Versions Correction

The PSIRT-assigned Affects Versions of `RHTPA 2.0.0` is incorrect. There is no
2.0.x stream in the configured Version Streams. The corrected Affects Versions
(scoped to the 2.2.x stream) should be:

- **Current**: RHTPA 2.0.0
- **Corrected**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

## Triage Decision

### Primary determination: Case A -- Affected (create remediation tasks)

Supported versions within the 2.2.x stream (2.2.0, 2.2.1, 2.2.2) are affected.
Remediation tasks are required. Since quinn-proto is a **Cargo** (source
dependency) ecosystem package, two tasks would be created:

1. **Upstream backport task** -- Bump quinn-proto from the vulnerable version to
   >= 0.11.14 in the `rhtpa-backend` source repository on the `release/0.4.z`
   branch.
2. **Downstream propagation subtask** -- Update the backend reference in the
   Konflux release repo (`rhtpa-release.0.4.z`) to a build tag that includes
   the updated quinn-proto. This subtask is blocked by the upstream task.

### Secondary determination: Case B -- Cross-stream impact

The 2.1.x stream is also affected (all versions ship quinn-proto 0.11.9).
This requires:
- A cross-stream impact comment on TC-8020 noting that 2.1.x versions are
  also affected
- Checking for existing CVE Jiras for the 2.1.x stream with the same CVE label
- If no 2.1.x CVE Jira exists, creating preemptive remediation tasks with the
  `security-preemptive` label and "Related" link type

### Step 7 gate: Concurrent triage detected

Before creating any remediation tasks, Step 7 detected a concurrent triage:

- **TC-8019** is currently **In Progress**, assigned to **engineer-b@example.com**,
  and affects the same upstream component (**quinn-proto**).

This means another engineer is actively triaging a different CVE that also involves
quinn-proto. Creating remediation tasks for TC-8020 now risks producing duplicates
if TC-8019's remediation already bumps quinn-proto to >= 0.11.14.

**Three options were presented to the engineer:**

1. **Wait** -- Pause triage until TC-8019 completes. Then re-run from Step 4.3
   to check if TC-8019's remediation covers this CVE. Safest option to avoid
   duplicate work.

2. **Skip** -- Do not create remediation tasks. Add a Jira comment explaining
   the skip. Revisit later.

3. **Proceed** -- Create remediation tasks with a `concurrent-triage-overlap`
   label. This label ensures TC-8019's triage will detect the overlap via
   Step 4.3 (Cross-CVE Overlap Detection) and handle any redundancy.

**The triage is paused at Step 7 pending the engineer's choice.** No remediation
tasks have been created yet.

## Actions Completed (prior to Step 7 gate)

1. Validated project configuration (Step 0) -- all required sections present
2. Assigned TC-8020 to current user and transitioned to Assigned (Step 0.7)
3. Extracted CVE data (Step 1) -- all critical fields parsed successfully
4. Determined stream scope: 2.2.x (Step 1)
5. Determined ecosystem: Cargo (Step 1)
6. Performed version impact analysis (Step 2) -- 3 of 5 versions affected in 2.2.x
7. Identified Affects Versions correction needed (Step 3): RHTPA 2.0.0 is
   incorrect, should be RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
8. Detected concurrent triage on same component (Step 7) -- TC-8019 in progress

## Actions Pending (after engineer chooses Step 7 option)

- Execute Affects Versions correction in Jira (requires engineer confirmation)
- Create remediation tasks (if engineer chooses "Proceed" or "Wait" and re-runs)
- Post cross-stream impact comment for 2.1.x
- Add `ai-cve-triaged` label
- Post triage summary comment with @mention of reporter
