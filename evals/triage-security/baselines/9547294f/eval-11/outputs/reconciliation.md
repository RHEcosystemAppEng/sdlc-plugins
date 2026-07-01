# Step 4.4 -- Preemptive Task Reconciliation

## Search for Preemptive Tasks

Per Step 4.4 of the triage-security skill, before creating new remediation tasks, we search for existing preemptive tasks that may have been created by a prior cross-stream triage.

### JQL Query

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

Fields requested: summary, status, labels, issuelinks

### Search Results

The JQL search returns **one result**:

| Key | Summary | Status | Labels |
|-----|---------|--------|--------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |

### Stream Matching

The current issue TC-8021 has stream suffix `[rhtpa-2.1]`, mapping to stream `rhtpa-2.1`.

TC-8022's summary contains `(rhtpa-2.1)` -- this matches the current issue's stream. The preemptive task was created for the same stream as the current CVE Jira.

### Preemptive Task Details

- **Task Key**: TC-8022
- **Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)
- **Status**: Open
- **Labels**: ai-generated-jira, Security, CVE-2026-55123, security-preemptive
- **Issue Links**: Related to TC-8020 (originating CVE Jira, stream [rhtpa-2.2])
- **Origin**: Created proactively from cross-stream impact analysis of TC-8020 (stream rhtpa-2.2) during a prior triage session

## Reconciliation Actions

Since a matching preemptive task (TC-8022) exists for CVE-2026-55123 in stream rhtpa-2.1, the following reconciliation actions are proposed:

### 1. Link the new CVE Jira to the preemptive task (Depend)

Proposed action: Create a "Depend" link from TC-8021 to TC-8022 (standard remediation linkage).

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

This establishes the standard remediation dependency -- TC-8021 (Vulnerability) depends on TC-8022 (remediation Task) for resolution.

### 2. Remove the `security-preemptive` label from TC-8022

Proposed action: Remove the `security-preemptive` label from TC-8022. The task is now linked to a proper CVE Jira (TC-8021) and is no longer a preemptive task.

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

### 3. Record reconciliation for Step 8

Remediation already exists for stream rhtpa-2.1 via TC-8022. Step 8 will skip remediation task creation for this stream because the preemptive task has been reconciled.

## Reconciliation Summary

```
Existing preemptive remediation task TC-8022 found for CVE-2026-55123 in stream rhtpa-2.1.
Created from cross-stream analysis of TC-8020 (stream rhtpa-2.2), linked via "Related".

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend" (standard remediation linkage)
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

## Sibling Landscape

For completeness, here is the companion issue landscape for CVE-2026-55123:

| Issue | Stream | Status | Affects Versions | Role |
|-------|--------|--------|------------------|------|
| TC-8020 | rhtpa-2.2 | (prior triage) | RHTPA 2.2.0, RHTPA 2.2.1 | Originating CVE (created preemptive task TC-8022) |
| TC-8021 (current) | rhtpa-2.1 | New | RHTPA 2.1.0, RHTPA 2.1.1 | New CVE Jira -- reconciled with TC-8022 |
| TC-8022 | rhtpa-2.1 | Open | -- | Remediation Task (formerly preemptive, now standard) |
