# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## Search for Preemptive Tasks

Per Step 4.4, a JQL search was executed for preemptive remediation tasks matching
the current CVE:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

### Search Results

| Task Key | Summary | Status | Labels | Issue Links |
|----------|---------|--------|--------|-------------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related: TC-8020 |

## Stream Matching

The current issue TC-8021 has stream suffix `[rhtpa-2.1]` (stream 2.1.x).

TC-8022's summary contains `(rhtpa-2.1)` -- this matches the current issue's
stream. TC-8022 is a preemptive remediation task for the same CVE and same stream.

## Reconciliation Origin

TC-8022 was created proactively during the triage of TC-8020 (CVE-2026-55123
for stream [rhtpa-2.2]). When TC-8020's triage reached Step 8 Case A
(cross-stream impact), it identified that stream 2.1.x was also affected but
had no CVE Jira of its own at the time. A preemptive remediation task (TC-8022)
was created with the `security-preemptive` label and linked to TC-8020 via
"Related" (not "Depend", because the originating CVE belongs to a different
stream).

Now that PSIRT has created TC-8021 as the stream-specific CVE Jira for rhtpa-2.1,
the preemptive task must be reconciled per Step 4.4.

## Reconciliation Actions

Per Step 4.4 procedure, the following actions are taken:

### a. Link the new CVE Jira to the preemptive task

```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This establishes the standard remediation linkage (Depend) between the CVE
Jira and its remediation task, replacing the "Related" link that connected
TC-8022 to the originating cross-stream CVE TC-8020.

### b. Remove the `security-preemptive` label

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because TC-8022 is now linked to
a proper CVE Jira (TC-8021) for its stream. It is no longer a preemptive task
-- it is a standard remediation task.

### c. Engineer notification

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

### d. Record reconciliation

Remediation for stream 2.1.x is recorded as already existing via TC-8022.
Step 8 will skip task creation for this stream -- no new remediation tasks
are needed.

## Link Topology After Reconciliation

```
TC-8020 (CVE Jira, stream rhtpa-2.2)
  |-- Related --> TC-8022 (original preemptive link, preserved)

TC-8021 (CVE Jira, stream rhtpa-2.1)
  |-- Depend --> TC-8022 (new standard remediation link)

TC-8022 (Remediation Task, stream rhtpa-2.1)
  Labels: ai-generated-jira, Security, CVE-2026-55123
  (security-preemptive label REMOVED)
```
