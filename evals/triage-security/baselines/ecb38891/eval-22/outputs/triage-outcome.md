# Triage Outcome -- TC-8021

## Step 7 Result

Step 7 (Concurrent Triage Detection) executed the concurrent triage check for upstream component `quinn-proto` using the Upstream Affected Component custom field (`customfield_10632`).

The JQL search returned **zero results** -- no other engineer is actively triaging a different CVE that affects the same upstream component. No concurrent triage warning was presented, and no wait/skip/proceed options were offered.

The analysis proceeds directly to Case A/B/C branching.

## Version Impact Summary

Based on the security-matrix.md data for the scoped stream (2.2.x):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.11.14 | NO | >= 0.11.14 |
| 2.2.4 | 0.11.14 | NO | >= 0.11.14 |

## Case Determination

Supported versions within the scoped stream (2.2.x) are affected (2.2.0, 2.2.1, 2.2.2). This is **Case B: Affected -- create remediation tasks**.

Additionally, the cross-stream version impact (2.1.x stream) shows:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 0.11.9 | YES | < 0.11.14 |

Since TC-8021 is scoped to the 2.2.x stream and other streams are also affected, **Case A** applies: post a cross-stream impact comment noting that stream 2.1.x is also affected.

Then proceed with **Case B** to create remediation tasks for the 2.2.x stream (the issue's scope):

- **Upstream backport task**: Remediate CVE-2026-31812 by bumping quinn-proto to >= 0.11.14 in the backend source repository on branch `release/0.4.z`
- **Downstream propagation subtask**: Update the backend source reference in the Konflux release repo `rhtpa-release.0.4.z` to pick up the upstream fix (blocked by the upstream task)

Both tasks are linked to TC-8021 with "Depend" link type, and the downstream task is linked to the upstream task with "Blocks" link type.

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8021
2. Transition TC-8021 to In Progress
3. Post summary comment with version impact table, Affects Versions correction, remediation task links, and @mention of the reporter
