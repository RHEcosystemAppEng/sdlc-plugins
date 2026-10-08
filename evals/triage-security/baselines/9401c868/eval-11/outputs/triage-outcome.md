# Triage Outcome: TC-8021

## Summary

CVE-2026-55123 (tokio use-after-free in task abort) was triaged for stream
rhtpa-2.1 (2.1.x). The triage identified an existing preemptive remediation
task (TC-8022) that was created during a prior cross-stream triage of TC-8020
(stream rhtpa-2.2). The preemptive task was reconciled per Step 4.4 rather
than creating new remediation tasks.

## Outcome: Preemptive Task Reconciled -- No New Tasks Created

### What happened

1. **Step 1 (Data Extraction)**: Parsed TC-8021 and extracted CVE-2026-55123
   metadata. The issue is scoped to stream 2.1.x via the `[rhtpa-2.1]` summary
   suffix. The vulnerable library is `tokio` (Cargo ecosystem), affected
   versions before 1.42.0, fixed in 1.42.0. CVSS 8.1 (High).

2. **Step 4.4 (Preemptive Task Reconciliation)**: A JQL search for tasks with
   labels `security-preemptive` and `CVE-2026-55123` returned TC-8022.
   TC-8022's summary contains `(rhtpa-2.1)`, matching the current issue's
   stream scope. TC-8022 was originally created as a preemptive remediation
   task during the triage of TC-8020 (the CVE Jira for stream rhtpa-2.2).

3. **Reconciliation actions**:
   - Linked TC-8021 to TC-8022 with "Depend" (standard remediation linkage)
   - Removed the `security-preemptive` label from TC-8022
   - TC-8022 is now a standard remediation task linked to its own stream's
     CVE Jira (TC-8021)

4. **Step 8 (Remediation)**: Skipped task creation for stream 2.1.x because
   remediation already exists via TC-8022. No new upstream backport,
   dependency bump, or downstream propagation tasks were created.

## Why This Is Correct

The preemptive task reconciliation mechanism (Step 4.4) exists precisely for
this scenario: when PSIRT creates per-stream CVE Jiras at different times,
the first triage (TC-8020 for rhtpa-2.2) may proactively create remediation
tasks for other affected streams that lack their own CVE Jira. When the
stream-specific CVE Jira arrives later (TC-8021 for rhtpa-2.1), Step 4.4
detects the preemptive task, links it to the new CVE Jira, and removes the
preemptive label -- converting it into a standard remediation task without
duplicating work.

This avoids:
- **Duplicate remediation tasks** for the same CVE and stream
- **Orphaned preemptive tasks** that remain unlinked to their proper CVE Jira
- **Lost traceability** -- the Depend link from TC-8021 to TC-8022 creates
  the standard CVE-to-remediation relationship

## Final State

| Issue | Type | Status | Role |
|-------|------|--------|------|
| TC-8020 | Vulnerability | (prior triage) | Originating CVE Jira (stream rhtpa-2.2) |
| TC-8021 | Vulnerability | Assigned | CVE Jira for stream rhtpa-2.1 (this triage) |
| TC-8022 | Task | Open | Remediation task for rhtpa-2.1 (reconciled from preemptive) |

### Links

- TC-8021 --Depend--> TC-8022 (standard remediation link, created by reconciliation)
- TC-8020 --Related--> TC-8022 (original preemptive link, preserved from prior triage)

### Labels on TC-8022 (after reconciliation)

- ai-generated-jira
- Security
- CVE-2026-55123
- ~~security-preemptive~~ (removed)
