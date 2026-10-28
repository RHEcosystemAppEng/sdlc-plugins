# Triage Outcome: TC-8021

## Summary

TC-8021 (CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1]) was triaged with **preemptive task reconciliation**. An existing preemptive remediation task (TC-8022) was found and reconciled, eliminating the need to create new remediation tasks.

## Background

1. **TC-8020** was the first CVE Jira for CVE-2026-55123, scoped to stream **rhtpa-2.2**.
2. During TC-8020's triage, Step 8 Case A (cross-stream impact) detected that stream **2.1.x** was also affected by the same vulnerability in tokio.
3. Since no CVE Jira existed for stream rhtpa-2.1 at that time, a **preemptive remediation task** TC-8022 was created with the `security-preemptive` label and linked to TC-8020 via a "Related" link.
4. Subsequently, PSIRT created **TC-8021** as the stream-specific CVE Jira for rhtpa-2.1.

## How Reconciliation Worked

When TC-8021 was triaged, Step 4.4 (Preemptive Task Reconciliation) searched for preemptive tasks matching:
- Label `security-preemptive`
- Label `CVE-2026-55123`

The search returned TC-8022, whose summary contains `(rhtpa-2.1)` matching the current issue's stream suffix `[rhtpa-2.1]`.

### Actions Taken

1. **Depend link created**: TC-8021 --> TC-8022 (standard remediation linkage). This connects the CVE Jira to its remediation task using the same link type as standard triage.

2. **security-preemptive label removed** from TC-8022. Updated labels: `[ai-generated-jira, Security, CVE-2026-55123]`. The task is now a standard remediation task.

3. **Step 8 skipped for stream 2.1.x**: Because reconciliation recorded that remediation already exists for this stream, no new remediation tasks were created. TC-8022 already contains the correct remediation instructions (bump tokio to 1.42.0).

## Effect on TC-8022

Before reconciliation:
- **Role**: Preemptive remediation task (created proactively for a stream without its own CVE Jira)
- **Link to TC-8020**: Related (provenance -- records which triage created it)
- **Link to TC-8021**: (none -- TC-8021 did not yet exist)
- **Labels**: ai-generated-jira, Security, CVE-2026-55123, **security-preemptive**

After reconciliation:
- **Role**: Standard remediation task (linked to its own CVE Jira)
- **Link to TC-8020**: Related (provenance -- retained, unchanged)
- **Link to TC-8021**: **Depend** (standard remediation linkage)
- **Labels**: ai-generated-jira, Security, CVE-2026-55123 (security-preemptive removed)

## Why This Matters

Preemptive task reconciliation prevents duplicate remediation work. Without Step 4.4, the triage of TC-8021 would have created a second remediation task for the same CVE and stream, duplicating TC-8022. Instead, reconciliation:

- Reuses the existing task (no wasted engineering effort)
- Establishes proper Depend linkage from the CVE Jira to the remediation task
- Removes the preemptive marker so the task is treated as a standard remediation task going forward
- Preserves the provenance link to TC-8020, maintaining the audit trail of how the task was originally created

## Triage Status

- **Outcome**: Remediation exists (reconciled preemptive task)
- **New tasks created**: 0
- **Preemptive tasks reconciled**: 1 (TC-8022)
- **Step 8 remediation**: Skipped for stream 2.1.x (reconciliation recorded that remediation already exists)
