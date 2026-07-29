# Triage Outcome: TC-8021

## Summary

**Issue**: TC-8021 -- CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1]
**CVE**: CVE-2026-55123
**Library**: tokio
**Stream**: 2.1.x (rhtpa-2.1)
**CVSS**: 8.1 (High)
**Outcome**: Preemptive task reconciled -- no new remediation tasks needed

## What Happened

TC-8021 is a stream-scoped CVE Jira for stream rhtpa-2.1, tracking CVE-2026-55123 (a use-after-free in the tokio crate affecting versions before 1.42.0).

During Step 4.4 (Preemptive Task Reconciliation), a JQL search for tasks with labels `security-preemptive` and `CVE-2026-55123` returned **TC-8022** -- a preemptive remediation task for stream rhtpa-2.1 that was created during a prior triage of TC-8020 (the CVE Jira for the same vulnerability on stream rhtpa-2.2).

### Origin of TC-8022

TC-8020 was a CVE Jira for CVE-2026-55123 scoped to stream rhtpa-2.2. During its triage, the version impact analysis (Step 2) revealed that stream 2.1.x was also affected by the same vulnerability. Since no CVE Jira existed for stream 2.1.x at that time, the triage's Step 8 Case A (cross-stream impact) created TC-8022 as a preemptive remediation task:

- TC-8022 was labeled with `security-preemptive` to indicate it was proactively created, not backed by a stream-specific CVE Jira
- TC-8022 was linked to TC-8020 with "Related" (not "Depend", since TC-8020 belongs to a different stream)
- TC-8022's summary included `(rhtpa-2.1)` to identify the target stream

### Reconciliation

When TC-8021 arrived (the PSIRT-created CVE Jira for stream rhtpa-2.1), Step 4.4 reconciliation detected TC-8022 and performed the following:

1. **Created a "Depend" link** from TC-8021 to TC-8022 -- establishing the standard remediation linkage between the CVE Jira and its remediation task
2. **Removed the `security-preemptive` label** from TC-8022 -- the task is no longer preemptive since it now has a proper CVE Jira backing it
3. **Recorded the reconciliation** -- Step 8 skips task creation for stream 2.1.x because TC-8022 already covers it

## Step 8 Impact

Because the preemptive task was reconciled, Step 8 (Remediation) does not create new remediation tasks for stream 2.1.x. TC-8022 serves as the remediation task for TC-8021, just as if triage had created it directly. This avoids duplicate work -- the remediation task TC-8022 (which may already be in progress or have an assigned engineer) is preserved and simply re-linked to its proper CVE Jira.

## Final Issue State

### TC-8021 (CVE Jira)

| Field | Value |
|-------|-------|
| Status | Assigned |
| Labels | CVE-2026-55123, pscomponent:org/rhtpa-server, ai-cve-triaged |
| Affects Versions | (corrected per Step 3 based on version impact analysis) |
| Issue Links | Depend: TC-8022 (remediation task) |

### TC-8022 (Remediation Task, formerly preemptive)

| Field | Before Reconciliation | After Reconciliation |
|-------|-----------------------|----------------------|
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | ai-generated-jira, Security, CVE-2026-55123 |
| Issue Links | Related: TC-8020 | Related: TC-8020, Depend (inward from TC-8021) |
| Role | Preemptive task (no backing CVE Jira for this stream) | Standard remediation task (backed by TC-8021) |

## Reconciliation Flow Diagram

```
TC-8020 (CVE Jira, rhtpa-2.2)
  |
  | [Prior triage - Step 8 Case A]
  | Created preemptive task for rhtpa-2.1
  |
  v
TC-8022 (Preemptive task, rhtpa-2.1)
  ^   - labels: security-preemptive
  |   - link: Related -> TC-8020
  |
  | [Step 4.4 Reconciliation]
  | - Added Depend link from TC-8021
  | - Removed security-preemptive label
  |
TC-8021 (CVE Jira, rhtpa-2.1) <-- current triage
      - link: Depend -> TC-8022
      - No new tasks created (reconciled)
```

## Key Principle

The preemptive task pattern ensures that remediation work can begin before PSIRT creates stream-specific CVE Jiras. When the CVE Jira eventually arrives, Step 4.4 reconciliation seamlessly converts the preemptive task into a standard remediation task by adjusting links and labels, without duplicating work or losing the task's history and any progress already made.
