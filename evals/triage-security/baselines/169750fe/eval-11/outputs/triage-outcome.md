# Triage Outcome: TC-8021 (CVE-2026-55123, stream rhtpa-2.1)

## Summary

TC-8021 is a Vulnerability issue for CVE-2026-55123 (tokio use-after-free in task abort), scoped to stream rhtpa-2.1. During Step 4.4 (Preemptive Task Reconciliation), an existing preemptive remediation task TC-8022 was found and reconciled. No new remediation tasks were created.

## How the Existing Preemptive Task Was Reconciled

### Background

TC-8020 was a prior CVE Jira for CVE-2026-55123 scoped to stream rhtpa-2.2. During its triage (Step 8, Case A -- cross-stream impact), the analysis detected that stream rhtpa-2.1 was also affected but had no CVE Jira of its own. A preemptive remediation task TC-8022 was created for stream rhtpa-2.1 with:
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
- Link: "Related" to TC-8020 (the originating CVE Jira)
- Summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)"

### Reconciliation (Step 4.4)

When TC-8021 arrived as the PSIRT-created CVE Jira for stream rhtpa-2.1, Step 4.4 searched for preemptive tasks:

1. **JQL search**: `labels = 'security-preemptive' AND labels = 'CVE-2026-55123'` returned TC-8022.
2. **Stream filter**: TC-8022 summary contains `(rhtpa-2.1)`, matching TC-8021's stream suffix `[rhtpa-2.1]`.
3. **Reconciliation actions**:
   - **Linked** TC-8021 to TC-8022 with "Depend" link type (standard remediation linkage).
   - **Removed** `security-preemptive` label from TC-8022, converting it to a standard remediation task.
4. **Recorded** that remediation already exists for stream 2.1.x.

### Impact on Step 8

Step 8 (Remediation) skips task creation entirely for stream rhtpa-2.1 because Step 4.4 recorded that a reconciled remediation task (TC-8022) already exists. The preemptive task has been promoted to a standard remediation task with proper "Depend" linkage to its stream-specific CVE Jira.

## Final Link Topology

```
TC-8020 (CVE Jira, rhtpa-2.2)
  |
  +-- Related --> TC-8022 (remediation task, rhtpa-2.1, originally preemptive)
                    |
TC-8021 (CVE Jira, rhtpa-2.1)
  |
  +-- Depend  --> TC-8022 (remediation task, rhtpa-2.1, now standard)
```

TC-8022 retains both links:
- "Related" to TC-8020 -- traces its origin from the cross-stream triage
- "Depend" from TC-8021 -- standard remediation linkage to its own stream's CVE Jira

## Labels on TC-8022 After Reconciliation

Before: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
After: `ai-generated-jira`, `Security`, `CVE-2026-55123`

The `security-preemptive` label is removed because the task is no longer preemptive -- it is now linked to a proper CVE Jira (TC-8021) for its stream.
