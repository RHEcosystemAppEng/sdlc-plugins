# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## JQL Search

Query executed:
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

### Search Results

| Key | Summary | Status | Labels | Issue Links |
|-----|---------|--------|--------|-------------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related: TC-8020 |

## Stream Matching

- Current issue stream suffix: `[rhtpa-2.1]`
- TC-8022 summary contains `(rhtpa-2.1)` -- **match confirmed**
- TC-8022 was created as a preemptive remediation task during cross-stream analysis of TC-8020 (stream `[rhtpa-2.2]`), linked to TC-8020 via "Related"

## Reconciliation Actions

A matching preemptive task (TC-8022) was found for CVE-2026-55123 in the rhtpa-2.1 stream. The following reconciliation actions are performed per Step 4.4:

### Action 1: Link TC-8021 to TC-8022 with "Depend"

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

This establishes the standard remediation linkage between the CVE Jira (TC-8021) and its remediation task (TC-8022), replacing the previous "Related" relationship that was only with the originating cross-stream CVE (TC-8020).

### Action 2: Remove "security-preemptive" label from TC-8022

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because TC-8022 is now linked to a proper CVE Jira (TC-8021) for its stream. It is no longer a preemptive task -- it is a standard remediation task.

### Action 3: Record reconciliation for Step 8

Remediation already exists for the rhtpa-2.1 stream via TC-8022. Step 8 will **skip new remediation task creation** for this stream.

## Engineer Notification

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```
