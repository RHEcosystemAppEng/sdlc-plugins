# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## Overview

When triaging TC-8021 (CVE-2026-55123 for stream rhtpa-2.1), Step 4.4 checks whether a proactive remediation task already exists for this CVE and stream. Such a task would have been created by a prior Case A (cross-stream impact) run on a different stream's CVE Jira.

## JQL Search

Search for preemptive tasks matching the current CVE:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

Fields requested: summary, status, labels, issuelinks

## Search Results

The JQL search returned **one result**:

| Field | Value |
|-------|-------|
| Key | TC-8022 |
| Summary | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) |
| Status | Open |
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |
| Issue Links | Related: TC-8020 (originating CVE Jira, stream [rhtpa-2.2]) |

## Stream Matching

- Current issue stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- TC-8022 summary contains: `(rhtpa-2.1)` -- **matches** the current issue's stream

TC-8022 is a preemptive remediation task created for stream rhtpa-2.1 during the cross-stream analysis of TC-8020 (the CVE-2026-55123 issue for stream rhtpa-2.2). This is exactly the scenario Step 4.4 is designed to handle.

## Reconciliation Actions

Since a matching preemptive task (TC-8022) was found for this CVE and stream, the following reconciliation actions are performed:

### Action 1: Link CVE Jira to Preemptive Task with "Depend"

```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This converts the preemptive task into a standard remediation task by linking it to its own stream's CVE Jira (TC-8021) with the standard "Depend" link type. Previously, TC-8022 was linked to TC-8020 (the originating CVE from stream rhtpa-2.2) with "Related" only.

### Action 2: Remove `security-preemptive` Label

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because TC-8022 is now linked to a proper CVE Jira (TC-8021) for its stream. It is no longer a "preemptive" task -- it is a standard remediation task.

### Action 3: Inform the Engineer

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (stream [rhtpa-2.2], linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

### Action 4: Record Reconciliation

Remediation already exists for stream 2.1.x via the reconciled preemptive task TC-8022. Step 8 (Remediation) will skip task creation for this stream because:

- TC-8022 already covers the upstream backport (bump tokio to >= 1.42.0) for stream 2.1.x
- Creating new remediation tasks would be duplicative

## Post-Reconciliation Link State

After reconciliation, TC-8022's links are:

| Link Type | Direction | Target | Purpose |
|-----------|-----------|--------|---------|
| Related | TC-8022 <-> TC-8020 | Originating CVE Jira (stream rhtpa-2.2) | Cross-stream origin traceability |
| Depend | TC-8021 -> TC-8022 | Current CVE Jira (stream rhtpa-2.1) | Standard remediation linkage |

TC-8022's updated labels: `ai-generated-jira`, `Security`, `CVE-2026-55123` (the `security-preemptive` label has been removed).
