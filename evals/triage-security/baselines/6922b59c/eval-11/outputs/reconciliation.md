# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## Context

TC-8021 is a new CVE Vulnerability issue for CVE-2026-55123 (tokio use-after-free)
scoped to stream **rhtpa-2.1** (2.1.x). A prior triage of TC-8020 (the same CVE
for stream rhtpa-2.2) had already performed cross-stream impact analysis (Step 8,
Case A) and created a preemptive remediation task for stream 2.1.x.

## Step 4.4 JQL Search

Search query:
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

### Search Results

| Key | Summary | Status | Labels | Issue Links |
|-----|---------|--------|--------|-------------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related: TC-8020 |

## Stream Filter

TC-8022's summary contains `(rhtpa-2.1)`, which matches the current issue's stream
scope (`[rhtpa-2.1]` from the TC-8021 summary). This confirms TC-8022 is the
preemptive remediation task for this CVE and stream.

## Matching Preemptive Task Found: TC-8022

TC-8022 was created proactively during the triage of TC-8020 (stream rhtpa-2.2).
It carries the `security-preemptive` label and is linked to TC-8020 via "Related"
(because TC-8020 belongs to a different stream). Now that TC-8021 (the proper CVE
Jira for stream rhtpa-2.1) exists, the preemptive task must be reconciled.

## Reconciliation Actions

### a. Link the new CVE Jira to the preemptive task (Depend)

```
jira.create_link(
  inwardIssue: TC-8021,    // current CVE Jira for stream rhtpa-2.1
  outwardIssue: TC-8022,   // preemptive remediation task
  type: "Depend"
)
```

This establishes the standard remediation linkage (same as a freshly created
remediation task would have).

### b. Remove the `security-preemptive` label from TC-8022

Current labels: `[ai-generated-jira, Security, CVE-2026-55123, security-preemptive]`

Updated labels: `[ai-generated-jira, Security, CVE-2026-55123]`

```
jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

Removing the `security-preemptive` label promotes TC-8022 from a preemptive task
to a standard remediation task, now properly linked to its own stream's CVE Jira.

### c. Engineer Notification

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (stream [rhtpa-2.2]), linked
via "Related".

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

### d. Record Reconciliation

Remediation already exists for stream 2.1.x via TC-8022. Step 8 will skip
task creation for this stream.

## Link Topology After Reconciliation

```
TC-8020 (CVE Jira, stream rhtpa-2.2)
  |-- Related --> TC-8022 (remediation task, stream rhtpa-2.1)
                       ^
TC-8021 (CVE Jira, stream rhtpa-2.1)
  |-- Depend --> TC-8022 (remediation task, stream rhtpa-2.1)
```

TC-8022 now has two links:
1. **Related** to TC-8020 -- originating cross-stream CVE (pre-existing from Case A)
2. **Depend** from TC-8021 -- the proper stream-scoped CVE Jira (new from reconciliation)

The `security-preemptive` label has been removed, completing the promotion from
preemptive to standard remediation task.
