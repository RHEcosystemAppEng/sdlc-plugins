# Triage Outcome: TC-8021

## Summary

TC-8021 (CVE-2026-55123, tokio use-after-free, stream [rhtpa-2.1]) was triaged with preemptive task reconciliation. An existing preemptive remediation task (TC-8022) was found and reconciled, so no new remediation tasks were created.

## How the Existing Preemptive Task Was Reconciled

### Background

TC-8020 was a prior CVE Jira for CVE-2026-55123 scoped to stream [rhtpa-2.2]. During its triage, Step 8 Case B (cross-stream impact) identified that stream rhtpa-2.1 was also affected but had no CVE Jira of its own at that time. A preemptive remediation task TC-8022 was created for stream rhtpa-2.1 with:

- Labels: `ai-generated-jira, Security, CVE-2026-55123, security-preemptive`
- Link: Related to TC-8020 (the originating CVE Jira)
- Summary: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)

### Reconciliation (Step 4.4)

When TC-8021 arrived as the stream-specific CVE Jira for rhtpa-2.1, Step 4.4 searched for preemptive tasks:

1. **JQL search**: `labels = 'security-preemptive' AND labels = 'CVE-2026-55123'` returned TC-8022.
2. **Stream filter**: TC-8022's summary contains `(rhtpa-2.1)`, matching TC-8021's stream suffix `[rhtpa-2.1]`. This confirmed TC-8022 was created for the same stream.
3. **Link creation**: TC-8021 was linked to TC-8022 with "Depend" link type -- the same link type used for standard remediation task linkage. This makes TC-8022 the official remediation task for TC-8021.
4. **Label removal**: The `security-preemptive` label was removed from TC-8022 because it is now linked to a proper CVE Jira. Its remaining labels are: `ai-generated-jira, Security, CVE-2026-55123`.
5. **Reconciliation recorded**: The stream rhtpa-2.1 was marked as having existing remediation coverage via TC-8022.

### Step 8 -- Remediation Task Creation Skipped

Step 8 normally creates remediation tasks for affected streams. However, because Step 4.4 already reconciled TC-8022 as the remediation task for stream rhtpa-2.1, Step 8 skipped task creation for this stream. There are no other streams in scope (TC-8021 is scoped to rhtpa-2.1 only), so no new remediation tasks were needed.

## Final State

### TC-8021 (Vulnerability issue)

- Status: Assigned (transitioned from New in Step 0.7)
- Labels: CVE-2026-55123, pscomponent:org/rhtpa-server, ai-cve-triaged
- Issue links:
  - **Depend**: TC-8021 --> TC-8022 (remediation task)

### TC-8022 (Remediation task, formerly preemptive)

- Status: Open
- Labels: ai-generated-jira, Security, CVE-2026-55123 (security-preemptive removed)
- Issue links:
  - **Related**: TC-8022 <-> TC-8020 (originating CVE Jira, stream rhtpa-2.2)
  - **Depend**: TC-8021 --> TC-8022 (from reconciliation)

### TC-8020 (Original CVE Jira, stream rhtpa-2.2)

- Unchanged by this triage. It originated the preemptive task TC-8022 during its own Case B cross-stream analysis.

## Triage Decision Chain

```
TC-8020 [rhtpa-2.2]  --(Case B cross-stream)-->  TC-8022 (preemptive, rhtpa-2.1)
                                                       |
TC-8021 [rhtpa-2.1]  --(Step 4.4 reconciliation)------+
                         Link: Depend
                         Label 'security-preemptive' removed
                         Step 8: task creation skipped
```
