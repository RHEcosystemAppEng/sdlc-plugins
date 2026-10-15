# Step 4.4 -- Preemptive Task Reconciliation

## Search for Preemptive Tasks

A JQL search is performed to find existing preemptive remediation tasks for the current CVE:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

### Search Results

| Task Key | Summary | Status | Labels | Issue Links |
|----------|---------|--------|--------|-------------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related: TC-8020 |

**1 result returned.**

## Stream Filtering

Filter results to match the current stream (**rhtpa-2.1**) by checking the task summary for the stream name:

- TC-8022 summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 **(rhtpa-2.1)**"
- Contains stream name `rhtpa-2.1`: **YES -- match confirmed**

TC-8022 is a preemptive remediation task for CVE-2026-55123 in stream rhtpa-2.1, created from prior cross-stream triage of TC-8020 (stream [rhtpa-2.2]).

## Reconciliation Actions

A matching preemptive task was found. The following reconciliation actions are proposed:

### Action 1: Link TC-8021 to TC-8022 with "Depend" (standard remediation linkage)

Proposed operation:
```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

This establishes the standard remediation linkage between the CVE Vulnerability issue (TC-8021) and its remediation task (TC-8022), identical to the linkage that would be created if triage had produced a new task.

### Action 2: Remove the 'security-preemptive' label from TC-8022

Current labels on TC-8022: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`

Proposed updated labels: `ai-generated-jira`, `Security`, `CVE-2026-55123`

Proposed operation:
```
jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because TC-8022 is now linked to a proper CVE Jira (TC-8021) via "Depend". It is no longer a proactive preemptive task -- it is a standard remediation task.

### Action 3: Record reconciliation for Step 8

Remediation already exists for the **2.1.x** stream via TC-8022. Step 8 will skip remediation task creation for this stream.

## Reconciliation Summary

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions proposed:
- Link TC-8021 -> TC-8022 with "Depend" (standard remediation linkage)
- Remove "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

> **Note**: No Jira operations were actually performed. All actions above are proposals only.
