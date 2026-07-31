# Step 4.4 -- Preemptive Task Reconciliation for TC-8021

## JQL Search for Preemptive Tasks

Per SKILL.md Step 4.4, search for existing preemptive remediation tasks matching
the current CVE:

```
jira.search_jql(
  "project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC",
  fields: ["summary", "status", "labels", "issuelinks"]
)
```

### Search Results

| Key | Summary | Status | Labels |
|-----|---------|--------|--------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |

### Stream Filtering

Per Step 4.4 item 2: filter results to tasks whose summary contains the current
issue's stream name. The current issue has stream suffix `[rhtpa-2.1]`.

- TC-8022 summary contains `(rhtpa-2.1)` -- **matches** the current stream.

Result: **1 matching preemptive task found** (TC-8022).

## Reconciliation Actions

Per Step 4.4 item 3, the following actions are performed on the matching
preemptive task:

### 3a. Link CVE Jira to preemptive task with "Depend"

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

This uses the standard remediation linkage ("Depend"), the same link type used
when triage-security creates remediation tasks in Step 8 Case B. The preemptive
task is now linked to its proper CVE Jira.

### 3b. Remove the 'security-preemptive' label

Current labels on TC-8022: `[ai-generated-jira, Security, CVE-2026-55123, security-preemptive]`
Updated labels (removing security-preemptive): `[ai-generated-jira, Security, CVE-2026-55123]`

```
jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because TC-8022 is now linked to a
proper CVE Jira (TC-8021). It is no longer a preemptive task -- it is a standard
remediation task.

### 3c. Engineer notification

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

### 3d. Record reconciliation

Reconciliation recorded: remediation already exists for stream 2.1.x via
TC-8022 (formerly preemptive, now standard). Step 8 will skip task creation
for this stream.

## TC-8022 State After Reconciliation

| Field | Before | After |
|-------|--------|-------|
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | ai-generated-jira, Security, CVE-2026-55123 |
| Issue Links | Related: TC-8020 | Related: TC-8020, Depend: TC-8021 |
| Status | Open | Open (unchanged) |
| Role | Preemptive remediation task | Standard remediation task |
