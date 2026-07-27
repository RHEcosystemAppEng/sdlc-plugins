# Triage Outcome -- TC-8021

## Summary

TC-8021 (CVE-2026-55123: tokio use-after-free in task abort, stream [rhtpa-2.1]) was triaged with a **preemptive task reconciliation** outcome. An existing preemptive remediation task (TC-8022) was found and reconciled, eliminating the need to create new remediation tasks.

## Reconciliation Explanation

### What happened

1. **Prior triage of TC-8020** (CVE-2026-55123 for stream [rhtpa-2.2]) ran Step 8 Case A cross-stream impact analysis. It detected that stream 2.1.x was also affected by the vulnerability (tokio versions before 1.42.0).

2. **Preemptive task TC-8022 was created** for stream rhtpa-2.1 during that prior triage because no CVE Jira existed yet for stream 2.1.x. TC-8022 was:
   - Labeled with `security-preemptive` to mark it as proactively created
   - Linked to TC-8020 via "Related" (not "Depend", since TC-8020 is a different stream's CVE)
   - Given the CVE-2026-55123 label for discoverability

3. **PSIRT subsequently created TC-8021** as the proper CVE Jira for stream rhtpa-2.1, triggering this triage.

4. **Step 4.4 reconciliation** during this triage of TC-8021 found TC-8022 via a JQL search for tasks with labels `security-preemptive` and `CVE-2026-55123`. The task summary contains `(rhtpa-2.1)`, confirming it matches the current issue's stream scope.

### Reconciliation actions performed

| Action | Detail |
|--------|--------|
| Link created | TC-8021 -> TC-8022 with "Depend" (standard remediation linkage) |
| Label removed | `security-preemptive` removed from TC-8022 |
| Step 8 skipped | No new remediation tasks created -- TC-8022 already covers this stream |

### Why this is correct

- TC-8022 already contains the correct remediation plan: bump tokio to 1.42.0 in stream rhtpa-2.1.
- Creating a new remediation task would duplicate TC-8022, leading to confusion and wasted effort.
- By linking TC-8021 to TC-8022 with "Depend" and removing the `security-preemptive` label, TC-8022 is promoted from a preemptive task to a standard remediation task owned by this CVE Jira.
- The "Related" link from TC-8022 to TC-8020 (the originating CVE from stream rhtpa-2.2) is preserved, maintaining full traceability.

## Issue State After Triage

### TC-8021 (current CVE Jira)

| Field | Value |
|-------|-------|
| Status | Assigned |
| Labels | CVE-2026-55123, pscomponent:org/rhtpa-server, ai-cve-triaged |
| Affects Versions | RHTPA 2.1.0, RHTPA 2.1.1 |
| Issue Links | Depend: TC-8022 (remediation task) |

### TC-8022 (reconciled remediation task)

| Field | Before | After |
|-------|--------|-------|
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | ai-generated-jira, Security, CVE-2026-55123 |
| Issue Links | Related: TC-8020 | Related: TC-8020, Depend: TC-8021 |
| Status | Open | Open (unchanged) |

### TC-8020 (originating CVE Jira, stream rhtpa-2.2)

No changes made to TC-8020 during this triage. Its existing relationship to TC-8022 via "Related" link is preserved.

## Triage Decision

- **Outcome**: Preemptive task reconciled -- no new remediation tasks needed
- **Reason**: TC-8022 already provides the correct remediation (bump tokio to 1.42.0) for stream rhtpa-2.1
- **Step 8 action**: Skipped task creation for stream 2.1.x; reconciliation in Step 4.4 recorded that remediation already exists
