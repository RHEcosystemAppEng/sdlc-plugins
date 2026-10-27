# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## JQL Search

Query:
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

### Search Results

| Key | Summary | Status | Labels |
|-----|---------|--------|--------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |

TC-8022 existing issue links:
- **Related**: TC-8020 (originating CVE Jira, stream [rhtpa-2.2])

## Stream Filter

Current issue stream suffix: `[rhtpa-2.1]`

TC-8022 summary contains `(rhtpa-2.1)` -- **matches** the current issue's stream.

Result: **1 matching preemptive task found** (TC-8022).

## Reconciliation Actions

A preemptive remediation task TC-8022 exists for CVE-2026-55123 on stream rhtpa-2.1. It was created during cross-stream analysis of TC-8020 (the CVE Jira for the rhtpa-2.2 stream). Now that PSIRT has created TC-8021 as the stream-specific CVE Jira for rhtpa-2.1, the preemptive task is reconciled into a standard remediation task.

### Action 1: Link TC-8021 to TC-8022 with "Depend"

```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This creates the standard remediation linkage (same as Case B task creation would produce), linking the CVE Vulnerability issue to its remediation Task.

### Action 2: Remove `security-preemptive` label from TC-8022

Current labels on TC-8022: `ai-generated-jira, Security, CVE-2026-55123, security-preemptive`

Updated labels (after removing `security-preemptive`): `ai-generated-jira, Security, CVE-2026-55123`

```
jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

Removing the `security-preemptive` label converts TC-8022 from a preemptive task into a standard remediation task. It is now linked to its own stream's CVE Jira (TC-8021) via "Depend" and retains its existing "Related" link to the originating cross-stream CVE (TC-8020).

### Action 3: Record reconciliation

Remediation for stream 2.1.x is marked as already existing. Step 8 will skip remediation task creation for this stream because the preemptive task TC-8022 has been reconciled into the standard remediation path.

## Engineer Notification

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (stream [rhtpa-2.2], linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```
