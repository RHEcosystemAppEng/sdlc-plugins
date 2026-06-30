# Step 4.4 -- Preemptive Task Reconciliation for TC-8021

## Context

TC-8021 is a new Vulnerability issue for CVE-2026-55123 (tokio) scoped to stream rhtpa-2.1 (2.1.x). Per the triage-security methodology Step 4.4, when triaging a new CVE Jira for a specific stream, we must check whether a proactive remediation task already exists for this CVE and stream, created by a prior Step 7 Case B run on a different stream's CVE Jira.

## Step 4.4 Procedure

### 4.4.1 -- Search for preemptive tasks

JQL query executed:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

**Result**: 1 task returned -- **TC-8022**

### 4.4.2 -- Filter results to matching stream

TC-8022 summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)"

The summary contains `(rhtpa-2.1)` which matches the current issue's stream suffix `[rhtpa-2.1]` (stream 2.1.x).

**Match confirmed**: TC-8022 is a preemptive remediation task for the same CVE (CVE-2026-55123) and same stream (rhtpa-2.1 / 2.1.x).

### 4.4.3 -- Preemptive task details

| Field | Value |
|-------|-------|
| Task key | TC-8022 |
| Summary | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) |
| Status | Open |
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |
| Issue Links | Related: TC-8020 (originating CVE Jira, stream [rhtpa-2.2]) |

TC-8022 was created by a prior triage of TC-8020 (the CVE-2026-55123 Vulnerability issue for stream rhtpa-2.2). During that triage, Step 7 Case B identified that stream 2.1.x was also affected but had no CVE Jira at the time, so a preemptive remediation task was created and linked to TC-8020 with a "Related" link.

### 4.4.4 -- Reconciliation actions

Per Step 4.4 methodology, the following actions are required:

**a. Link the new CVE Jira to the preemptive task with "Depend":**

```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This establishes the standard remediation linkage between TC-8021 (the CVE Vulnerability issue for stream 2.1.x) and TC-8022 (the remediation task).

**b. Remove the `security-preemptive` label from TC-8022:**

Current labels on TC-8022: `[ai-generated-jira, Security, CVE-2026-55123, security-preemptive]`

Updated labels (after removing `security-preemptive`): `[ai-generated-jira, Security, CVE-2026-55123]`

```
jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because TC-8022 is now linked to a proper CVE Jira (TC-8021) via "Depend". It is no longer a preemptive/orphan task -- it is a standard remediation task.

**c. Inform the engineer:**

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 7.
```

**d. Record the reconciliation:**

Remediation already exists for stream 2.1.x via TC-8022. Step 7 will skip task creation for this stream.

## Reconciliation Summary

| Aspect | Detail |
|--------|--------|
| Preemptive task found | TC-8022 |
| Stream match | rhtpa-2.1 (2.1.x) -- confirmed |
| CVE match | CVE-2026-55123 -- confirmed |
| Originating CVE Jira | TC-8020 (stream rhtpa-2.2) |
| New link created | TC-8021 -> TC-8022 (Depend) |
| Existing link retained | TC-8020 -> TC-8022 (Related) |
| Label removed | security-preemptive |
| Labels retained | ai-generated-jira, Security, CVE-2026-55123 |
| Step 7 impact | Skip new remediation task creation for stream 2.1.x |
