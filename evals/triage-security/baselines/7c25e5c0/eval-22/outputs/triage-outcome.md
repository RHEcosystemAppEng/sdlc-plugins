# Triage Outcome — TC-8021

## Version Impact Summary

Based on the security-matrix.md data for the 2.2.x stream (scoped by issue suffix [rhtpa-2.2]):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | — | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.11.14 | NO | = 0.11.14 (fixed) |
| 2.2.4 | 0.11.14 | NO | = 0.11.14 (fixed) |

Cross-stream analysis (2.1.x stream):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 0.11.9 | YES | < 0.11.14 |

## Step 7 — Concurrent Triage Detection

Step 7 executed the concurrent triage check for upstream component **quinn-proto**. The JQL search returned zero results — no other engineer is actively triaging a related CVE on the same component. The analysis proceeded directly to Case A/B/C branching without a concurrent triage warning.

No wait/skip/proceed options were presented since no conflict exists.

## Triage Decision

**Case A + Case B**: Some 2.2.x versions are affected (2.2.0, 2.2.1, 2.2.2), while others are not (2.2.3, 2.2.4). Additionally, the 2.1.x stream is affected (cross-stream impact).

### Remediation

For the **2.2.x stream** (in-scope):
- Create standard remediation tasks:
  - **Upstream backport task**: Remediate CVE-2026-31812 — bump quinn-proto to 0.11.14 (rhtpa-2.2)
  - **Downstream propagation subtask**: Propagate fix to Konflux release repo (rhtpa-release.0.4.z)
  - Labels: `['ai-generated-jira', 'Security', 'CVE-2026-31812']`
  - Link type: Depend (to TC-8021)

For the **2.1.x stream** (cross-stream, Case A):
- Post cross-stream impact comment on TC-8021
- Check for existing CVE Jira for 2.1.x stream — if none exists, create preemptive remediation tasks with `security-preemptive` label and `Related` link to TC-8021

### Post-Triage Actions

- Add `ai-cve-triaged` label to TC-8021
- Transition TC-8021 to In Progress
- Post summary comment with version impact table, remediation task links, and @mention of the reporter
