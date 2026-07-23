# Triage Outcome for TC-8020 (CVE-2026-31812 / quinn-proto)

## Triage Summary

| Attribute | Value |
|-----------|-------|
| Issue | TC-8020 |
| CVE | CVE-2026-31812 |
| Library | quinn-proto |
| Affected range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Ecosystem | Cargo |
| Issue stream scope | 2.2.x |

## Version Impact Summary

### In-scope stream (2.2.x)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | 0.11.12 | YES (retag of 2.2.1) |
| 2.2.3 | 0.11.14 | NO (fixed) |
| 2.2.4 | 0.11.14 | NO (fixed) |

### Out-of-scope stream (2.1.x)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

## Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Version `RHTPA 2.0.0` is incorrect -- no 2.0.x stream exists in the configuration.

**Proposed correction** (scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`):

```
Current: [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14, which is the fixed version. Versions from stream 2.1.x are excluded because this issue is scoped to 2.2.x only.

## Triage Decision

**Case A + Case B apply:**

1. **Case A (Affected)**: The issue's in-scope stream (2.2.x) has affected versions (2.2.0, 2.2.1, 2.2.2). Remediation tasks are needed.

2. **Case B (Cross-stream impact)**: The version impact analysis reveals that stream 2.1.x (outside this scoped issue's scope) is also affected. A cross-stream impact comment would be posted to TC-8020, and proactive remediation tasks would be created for stream 2.1.x if no companion CVE Jira exists for that stream.

### Remediation Tasks (Case A -- pending Step 7 resolution)

Since quinn-proto is a Cargo (source) dependency, **two tasks** per affected stream are needed:

**For stream 2.2.x:**

1. **Upstream backport task**: Bump quinn-proto to >= 0.11.14 on branch `release/0.4.z` in the `backend` repository.
   - Summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)"
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
   - Linked to TC-8020 with "Depend"

2. **Downstream propagation subtask**: Update the backend source reference in `rhtpa-release.0.4.z` to pick up the upstream fix.
   - Summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)"
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
   - Blocked by the upstream backport task

### Cross-Stream Impact (Case B)

Stream 2.1.x is also affected (versions 2.1.0 and 2.1.1 ship quinn-proto 0.11.9). Since TC-8020 is scoped to 2.2.x:

- A cross-stream impact comment would be posted on TC-8020
- If no companion CVE Jira exists for stream 2.1.x, preemptive remediation tasks would be created with the `security-preemptive` label and "Related" link type

## Step 7 Gate -- Concurrent Triage Detection

**Remediation task creation is currently blocked by Step 7.**

A concurrent triage was detected: TC-8019 is `In Progress`, assigned to `engineer-b@example.com`, and also targets the `quinn-proto` upstream component (customfield_10632).

The engineer must choose one of three options before proceeding:

1. **Wait** -- Pause until TC-8019 completes, then re-run Step 4.3 to check for overlap. Recommended if TC-8019's remediation may already cover the quinn-proto >= 0.11.14 threshold.

2. **Skip** -- Skip task creation entirely. The triage analysis is recorded but no remediation tasks are created. A Jira comment documents the skip reason.

3. **Proceed** -- Create tasks with a `concurrent-triage-overlap` label. TC-8019's Step 4.3 will detect the overlap later and reconcile.

**Until the engineer makes a choice, no remediation tasks are created and no Jira mutations beyond Steps 1-6 are performed.**

## Post-Triage Actions (after Step 7 resolution)

Once the Step 7 gate is resolved and remediation tasks are created:

1. Add `ai-cve-triaged` label to TC-8020
2. Post summary comment on TC-8020 with:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2)
   - Remediation task links
   - @mention of the issue reporter
   - Comment Footnote (per skill name `triage-security`)
3. Transition TC-8020 to In Progress
