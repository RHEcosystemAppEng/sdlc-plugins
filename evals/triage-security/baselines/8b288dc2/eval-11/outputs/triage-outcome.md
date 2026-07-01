# Triage Outcome: TC-8021 (CVE-2026-55123)

## Summary

TC-8021 is a Vulnerability issue for CVE-2026-55123 (tokio use-after-free, versions before 1.42.0) scoped to stream rhtpa-2.1. During Step 4.4 (Preemptive Task Reconciliation), an existing preemptive remediation task TC-8022 was found for this exact CVE and stream. TC-8022 had been created during a prior cross-stream triage of TC-8020 (the companion CVE Jira for stream rhtpa-2.2), which identified that the rhtpa-2.1 stream was also affected and proactively created a remediation task under Case B (cross-stream impact).

## How the Preemptive Task Was Reconciled

### Background

When TC-8020 (CVE-2026-55123, stream `[rhtpa-2.2]`) was triaged, Step 8 Case B detected that the rhtpa-2.1 stream was also affected by the same vulnerability. Since no CVE Jira existed for rhtpa-2.1 at that time, a preemptive remediation task (TC-8022) was created with:
- The `security-preemptive` label to distinguish it from standard remediation tasks
- A "Related" link to TC-8020 (the originating CVE Jira)
- Summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)"

### Reconciliation (Step 4.4)

When TC-8021 arrived as the stream-specific CVE Jira for rhtpa-2.1, Step 4.4 searched for preemptive tasks matching both labels `security-preemptive` and `CVE-2026-55123`. TC-8022 was returned and its summary confirmed it targets the rhtpa-2.1 stream.

Three reconciliation actions were performed:

1. **Linked TC-8021 to TC-8022 with "Depend"** -- This establishes the standard remediation relationship between the new CVE Jira and the existing task, identical to what would have been created if TC-8022 were generated fresh in Step 8.

2. **Removed the `security-preemptive` label from TC-8022** -- The label is no longer needed because TC-8022 now has a proper CVE Jira owner (TC-8021) in its stream. The task transitions from "preemptive" to "standard remediation" status.

3. **Recorded reconciliation to skip Step 8 task creation** -- Since TC-8022 already covers the remediation for rhtpa-2.1 (bump tokio to 1.42.0), no new remediation task is created in Step 8. This prevents duplicate tasks and preserves any work already done on TC-8022.

### Link Topology After Reconciliation

```
TC-8020 (CVE Jira, rhtpa-2.2)
  |
  +-- Related --> TC-8022 (Remediation task, rhtpa-2.1)
                    ^
TC-8021 (CVE Jira, rhtpa-2.1)
  |
  +-- Depend --> TC-8022 (Remediation task, rhtpa-2.1)
```

TC-8022 retains its original "Related" link to TC-8020 (the originating cross-stream CVE) and gains a new "Depend" link from TC-8021 (its proper stream CVE). The `security-preemptive` label is removed, and TC-8022's labels become: `ai-generated-jira`, `Security`, `CVE-2026-55123`.

## Step 8 Outcome

**Remediation task creation is skipped.** The preemptive task TC-8022 already exists and has been reconciled to serve as the standard remediation task for TC-8021. No new tasks are created. The triage proceeds to the post-triage summary, which documents the reconciliation and adds the `ai-cve-triaged` label to TC-8021.
