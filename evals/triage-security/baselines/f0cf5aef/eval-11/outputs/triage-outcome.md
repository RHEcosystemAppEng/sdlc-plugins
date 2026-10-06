# Triage Outcome: TC-8021

## Summary

TC-8021 (CVE-2026-55123, tokio use-after-free, stream [rhtpa-2.1]) was triaged with a preemptive task reconciliation outcome. No new remediation tasks were created because an existing preemptive remediation task (TC-8022) already covers this CVE and stream.

## How the Preemptive Task Was Reconciled

### Background

TC-8020 was the first CVE Jira created by PSIRT for CVE-2026-55123, scoped to stream [rhtpa-2.2]. During its triage (Step 8, Case A), the cross-stream impact analysis detected that stream 2.1.x was also affected. Since no CVE Jira existed for stream 2.1.x at that time, a preemptive remediation task (TC-8022) was created with:

- **Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)
- **Labels**: ai-generated-jira, Security, CVE-2026-55123, security-preemptive
- **Link**: Related to TC-8020 (the originating CVE Jira)

The `security-preemptive` label marked TC-8022 as a proactive task awaiting reconciliation when a proper CVE Jira arrives for stream 2.1.x.

### Reconciliation (Step 4.4)

When TC-8021 arrived (PSIRT-created CVE Jira for stream [rhtpa-2.1]), Step 4.4 searched for preemptive tasks:

```
JQL: project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123'
Result: TC-8022
```

TC-8022's summary contains `(rhtpa-2.1)`, matching TC-8021's stream scope. The reconciliation performed three actions:

1. **Linked TC-8021 to TC-8022 with "Depend"** -- establishing the standard remediation linkage between the CVE Jira and its remediation task.
2. **Removed the `security-preemptive` label from TC-8022** -- converting it from a preemptive task to a standard remediation task. Updated labels: `ai-generated-jira, Security, CVE-2026-55123`.
3. **Recorded remediation coverage** -- marked stream 2.1.x as already having a remediation task so Step 8 skips new task creation.

### Step 8 Impact

Because Step 4.4 recorded that remediation already exists for stream 2.1.x via TC-8022, Step 8 (Remediation) skips new task creation entirely for this stream. No duplicate tasks are produced.

## Final State

### TC-8021 (CVE Jira, stream rhtpa-2.1)
- **Status**: Assigned (after Step 0.7)
- **Labels**: CVE-2026-55123, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Affects Versions**: RHTPA 2.1.0, RHTPA 2.1.1 (confirmed by lock file analysis)
- **Issue Links**:
  - Depend: TC-8022 (remediation task)

### TC-8022 (Remediation Task, stream rhtpa-2.1)
- **Status**: Open
- **Labels**: ai-generated-jira, Security, CVE-2026-55123 (security-preemptive removed)
- **Issue Links**:
  - Related: TC-8020 (originating CVE Jira, stream rhtpa-2.2)
  - Depend: TC-8021 (stream-specific CVE Jira, stream rhtpa-2.1)

### TC-8020 (Originating CVE Jira, stream rhtpa-2.2)
- Unchanged by this triage. Retains its Related link to TC-8022.

## Triage Decision

**Outcome**: Preemptive task reconciliation -- no new remediation tasks created.

**Rationale**: TC-8022 was already created during cross-stream triage of TC-8020 and covers the exact same remediation (bump tokio to 1.42.0) for stream 2.1.x. Creating a new task would duplicate the work. Instead, TC-8022 was linked to TC-8021 with the standard "Depend" link type and its preemptive label was removed, fully integrating it as the remediation task for TC-8021.
