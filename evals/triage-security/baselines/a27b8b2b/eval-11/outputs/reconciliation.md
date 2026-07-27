# Step 4.4 -- Preemptive Task Reconciliation

## Search for Preemptive Tasks

Before creating new remediation tasks, Step 4.4 searches for existing preemptive
remediation tasks that may have been created by a prior cross-stream triage.

### JQL Query

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

Fields requested: `summary, status, labels, issuelinks`

### Search Results

The JQL search returns **1 result**:

| Key | Summary | Status | Labels |
|-----|---------|--------|--------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |

**Issue Links on TC-8022:**
- **Related**: TC-8020 (originating CVE Jira, stream [rhtpa-2.2])

## Stream Filtering

The current issue TC-8021 has stream suffix `[rhtpa-2.1]`, corresponding to
stream **rhtpa-2.1**.

Filter the search results by checking whether the task summary contains the
current stream name:

- **TC-8022** summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 **(rhtpa-2.1)**"
  -- contains `rhtpa-2.1` -- **MATCH**

Result: TC-8022 is a matching preemptive task for this CVE and stream.

## Reconciliation Actions

A matching preemptive task TC-8022 was found for CVE-2026-55123 in stream
rhtpa-2.1. The following reconciliation actions are proposed:

### Action 1: Link TC-8021 to TC-8022 with "Depend"

Create a standard remediation linkage between the new CVE Jira and the existing
preemptive task:

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

This establishes the same link type used for standard remediation tasks created
in Step 8 -- TC-8021 (CVE Jira) depends on TC-8022 (remediation task).

### Action 2: Remove the "security-preemptive" label from TC-8022

The task is now linked to a proper CVE Jira for its stream, so the
`security-preemptive` label is no longer applicable. Remove it while preserving
all other labels:

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

TC-8022 is now a standard remediation task -- the `security-preemptive` label
has been removed, and it is linked to TC-8021 via "Depend" (standard remediation
linkage) in addition to its existing "Related" link to TC-8020 (the originating
CVE from stream rhtpa-2.2).

### Action 3: Record reconciliation for Step 8

Mark that remediation already exists for stream rhtpa-2.1:
- **Stream**: rhtpa-2.1
- **Existing remediation task**: TC-8022
- **Reconciliation source**: preemptive task created from cross-stream analysis
  of TC-8020 (stream rhtpa-2.2)
- **Step 8 behavior**: skip remediation task creation for this stream

## Reconciliation Summary

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (stream [rhtpa-2.2]),
linked via "Related".

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```
