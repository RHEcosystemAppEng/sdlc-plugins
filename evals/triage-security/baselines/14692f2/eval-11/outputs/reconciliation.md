# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## JQL Search

Query executed:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

Fields requested: summary, status, labels, issuelinks

## Search Results

One matching task found:

| Key | Summary | Status | Labels |
|-----|---------|--------|--------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |

### TC-8022 Issue Links

- **Related**: TC-8020 (originating CVE Jira, stream [rhtpa-2.2])

## Stream Filtering

- Current issue TC-8021 stream scope: **rhtpa-2.1** (from summary suffix `[rhtpa-2.1]`)
- TC-8022 summary contains `(rhtpa-2.1)` -- **matches current stream**
- TC-8022 is a valid preemptive task for this CVE and stream

## Reconciliation: Preemptive Task Found

TC-8022 was created as a proactive remediation task during the triage of TC-8020 (a sibling CVE Jira for stream rhtpa-2.2). Step 7 Case B of that prior triage detected that stream rhtpa-2.1 was also affected by CVE-2026-55123 but had no dedicated CVE Jira yet. It created TC-8022 as a preemptive remediation task with the `security-preemptive` label and a "Related" link to TC-8020.

Now that PSIRT has created TC-8021 -- the proper CVE Jira for stream rhtpa-2.1 -- Step 4.4 reconciliation applies.

## Actions Taken

### Action 1: Link TC-8021 to TC-8022 with "Depend"

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

This establishes the standard remediation linkage between the CVE Jira (TC-8021) and its remediation task (TC-8022), identical to what Step 7 would create for a new remediation task.

### Action 2: Remove "security-preemptive" label from TC-8022

Current labels on TC-8022: `ai-generated-jira, Security, CVE-2026-55123, security-preemptive`

Updated labels (removing `security-preemptive`):

```
jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because TC-8022 is no longer a preemptive task -- it is now a standard remediation task linked to its proper CVE Jira (TC-8021) via "Depend".

### Action 3: Record reconciliation for Step 7

The reconciliation is recorded so that Step 7 knows remediation already exists for stream rhtpa-2.1. Step 7 will skip new remediation task creation for this stream.

## Engineer Notification

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 7.
```
