# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## Context

TC-8021 is a Vulnerability issue for CVE-2026-55123 (tokio use-after-free) scoped to
stream [rhtpa-2.1]. A prior triage of TC-8020 (the same CVE for stream [rhtpa-2.2])
had already identified that stream 2.1.x was also affected and created a preemptive
remediation task TC-8022 via Step 8 Case B cross-stream proactive remediation.

## Step 4.4.1 -- Search for Preemptive Tasks

JQL query executed:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

Fields requested: summary, status, labels, issuelinks

### Result

| Key | Summary | Status | Labels |
|-----|---------|--------|--------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |

Issue links on TC-8022:
- **Related**: TC-8020 (originating CVE Jira, stream [rhtpa-2.2])

## Step 4.4.2 -- Filter to Current Stream

Current issue stream suffix: `[rhtpa-2.1]`
TC-8022 summary contains: `(rhtpa-2.1)`

**Match confirmed** -- TC-8022 is a preemptive remediation task for the same CVE
(CVE-2026-55123) and the same stream (rhtpa-2.1) as TC-8021.

## Step 4.4.3 -- Reconciliation Actions

Since a matching preemptive task was found, the following actions are proposed:

### a. PROPOSAL: Create Depend link from TC-8021 to TC-8022

Check TC-8021's existing issuelinks: none (no existing links on TC-8021).
No existing Depend link to TC-8022 found -- link creation is needed.

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

This establishes standard remediation linkage between the CVE Jira (TC-8021) and
the remediation task (TC-8022), identical to how new remediation tasks are linked.

### b. PROPOSAL: Remove security-preemptive label from TC-8022

Current labels on TC-8022: `ai-generated-jira, Security, CVE-2026-55123, security-preemptive`

Updated labels (removing security-preemptive):
`ai-generated-jira, Security, CVE-2026-55123`

```
jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

Removing the `security-preemptive` label converts TC-8022 from a proactive/preemptive
task into a standard remediation task, now properly linked to its own stream's CVE Jira.

### c. Engineer Notification

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (stream [rhtpa-2.2], linked
via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

### d. Reconciliation Recorded

Remediation already exists for stream 2.1.x via TC-8022. Step 8 will skip
task creation for this stream. No new remediation tasks need to be created.

## Link Topology After Reconciliation

```
TC-8020 (CVE Jira, stream [rhtpa-2.2])
  |
  +-- Related --> TC-8022 (remediation task, rhtpa-2.1)
                    ^
                    |
TC-8021 (CVE Jira, stream [rhtpa-2.1])
  |
  +-- Depend ---> TC-8022 (remediation task, rhtpa-2.1)
```

TC-8022 now has:
- A **Related** link to TC-8020 (the originating CVE from the prior cross-stream triage)
- A **Depend** link from TC-8021 (the newly triaged CVE for this stream)
- The `security-preemptive` label removed (it is now a standard remediation task)
