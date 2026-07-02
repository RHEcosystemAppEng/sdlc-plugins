# Triage Outcome for TC-8021 (CVE-2026-31812 / quinn-proto)

## Summary

CVE-2026-31812 affects quinn-proto versions before 0.11.14, causing a denial-of-service
via panic on large stream counts. The triage outcome is **Case A + Case B**: create
remediation tasks for the scoped 2.2.x stream, and create proactive (preemptive)
remediation tasks for the cross-stream-affected 2.1.x stream.

## Version Impact Table

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | Outside issue scope |
| 2.1.1 | 2.1.x | 0.11.9 | YES | Outside issue scope |
| 2.2.0 | 2.2.x | 0.11.9 | YES | In scope |
| 2.2.1 | 2.2.x | 0.11.12 | YES | In scope |
| 2.2.2 | 2.2.x | (retag) | YES | same as 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | Fixed version shipped |
| 2.2.4 | 2.2.x | 0.11.14 | NO | Fixed version shipped |

## Step 7 -- Concurrent Triage Detection

No concurrent triages detected for upstream component `quinn-proto`. The JQL search
for in-progress triages with `cf[10632] ~ 'quinn-proto'` returned zero results.
Proceeding silently to Case A/B/C branching per the skill protocol.

## Triage Decision

### Case A -- Affected (scoped stream 2.2.x)

Versions 2.2.0, 2.2.1, and 2.2.2 within the issue's scoped stream (2.2.x) ship
quinn-proto < 0.11.14 and are affected by CVE-2026-31812.

**PROPOSED Affects Versions correction:**
- Current: `[RHTPA 2.0.0]` (incorrect -- no 2.0.x stream exists)
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

**PROPOSED remediation tasks** (source dependency ecosystem -- Cargo -- two tasks):

1. **Upstream backport task:**
   - Summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)"
   - Repository: backend
   - Target Branch: release/0.4.z
   - Labels: `[ai-generated-jira, Security, CVE-2026-31812]`
   - Description: Update quinn-proto dependency to >= 0.11.14 in Cargo.lock.
     Upstream fix PR: quinn-rs/quinn#2048. Advisory: GHSA-2026-qp73-x4mq.
   - Link to TC-8021 with type "Depend"

2. **Downstream propagation subtask:**
   - Summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)"
   - Repository: rhtpa-release.0.4.z
   - Target Branch: main
   - Labels: `[ai-generated-jira, Security, CVE-2026-31812]`
   - Description: Update backend source reference in rhtpa-release.0.4.z to pick up
     the quinn-proto fix. Source pinning method: artifacts.lock.yaml (download URL
     contains tag).
   - Blocked by: upstream backport task (link type "Blocks")
   - Link to TC-8021 with type "Depend"

### Case B -- Cross-Stream Impact (2.1.x stream)

The version impact analysis reveals that the 2.1.x stream (versions 2.1.0, 2.1.1) is
also affected -- both ship quinn-proto 0.11.9 which is within the vulnerable range.
The 2.1.x stream is outside this issue's scope (issue is scoped to 2.2.x).

**PROPOSED cross-stream impact comment on TC-8021:**

> Cross-stream impact: quinn-proto (< 0.11.14) also affects stream 2.1.x based on
> lock file analysis. This stream is tracked by companion issues (see Related links)
> or may require separate PSIRT triage.

**Check for existing CVE Jiras for 2.1.x:** Search for sibling Vulnerability issues with
label `CVE-2026-31812` and summary suffix `[rhtpa-2.1]`. If no sibling exists for 2.1.x,
create preemptive remediation tasks:

1. **Preemptive upstream backport task (2.1.x):**
   - Summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)"
   - Labels: `[ai-generated-jira, Security, CVE-2026-31812, security-preemptive]`
   - Repository: backend
   - Target Branch: release/0.3.z
   - Link to TC-8021 with type "Related" (not "Depend" -- preemptive)

2. **Preemptive downstream propagation subtask (2.1.x):**
   - Summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)"
   - Labels: `[ai-generated-jira, Security, CVE-2026-31812, security-preemptive]`
   - Repository: rhtpa-release.0.3.z
   - Target Branch: main
   - Link to TC-8021 with type "Related" (not "Depend" -- preemptive)
   - Blocked by: preemptive upstream backport task (link type "Blocks")

**PROPOSED comment on TC-8021 listing preemptive tasks:**

> Preemptive remediation tasks created for streams without CVE Jiras:
> - 2.1.x: [upstream-task-key] (security-preemptive), [downstream-task-key] (security-preemptive)
>
> These tasks use the "Related" link type and carry the security-preemptive label.
> When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link
> them and remove the label.

### Post-Triage Actions

**PROPOSED Jira mutations (all require engineer confirmation):**

1. Add label `ai-cve-triaged` to TC-8021
2. Correct Affects Versions: `[RHTPA 2.0.0]` -> `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
3. Create upstream backport task for 2.2.x stream
4. Create downstream propagation subtask for 2.2.x stream (blocked by upstream task)
5. Link both tasks to TC-8021 with type "Depend"
6. Create preemptive upstream task for 2.1.x stream (if no sibling CVE Jira exists)
7. Create preemptive downstream subtask for 2.1.x stream (if no sibling CVE Jira exists)
8. Link preemptive tasks to TC-8021 with type "Related"
9. Transition TC-8021 to In Progress
10. Post summary comment on TC-8021 with version impact table, triage outcome,
    remediation task links, and @mention of the reporter

All mutations are PROPOSALS requiring explicit engineer confirmation before execution.
