# Step 4.4 -- Preemptive Task Reconciliation

## JQL Search

Per the Step 4.4 procedure, search for preemptive tasks matching the current CVE:

```
jira.search_jql(
  "project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC",
  fields: ["summary", "status", "labels", "issuelinks"]
)
```

### Search Results

The JQL search returns one result:

| Key | Summary | Status | Labels | Issue Links |
|-----|---------|--------|--------|-------------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related: TC-8020 |

## Stream Filtering

Per Step 4.4 procedure item 2: filter results to tasks whose summary contains the current issue's stream name.

- Current issue TC-8021 has stream suffix `[rhtpa-2.1]` -- stream name is `rhtpa-2.1`
- TC-8022 summary contains `(rhtpa-2.1)` -- **matches** the current stream

**Result**: TC-8022 is a matching preemptive task for CVE-2026-55123 in stream rhtpa-2.1.

## Reconciliation Actions (Step 4.4, item 3)

A matching preemptive task was found. The following actions are performed:

### 3a. Link the new CVE Jira to the preemptive task

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

This creates a standard remediation "Depend" link from the CVE Jira (TC-8021) to the preemptive task (TC-8022), converting the preemptive task into a proper remediation task for this CVE.

### 3b. Remove the `security-preemptive` label

Current labels on TC-8022: `ai-generated-jira, Security, CVE-2026-55123, security-preemptive`

Updated labels (after filtering out `security-preemptive`): `ai-generated-jira, Security, CVE-2026-55123`

```
jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

### 3c. Engineer notification

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 7.
```

### 3d. Record the reconciliation

Remediation for stream rhtpa-2.1 is now covered by TC-8022. Step 7 will skip task creation for this stream because the preemptive task has been reconciled.

## Link State After Reconciliation

TC-8022 now has the following issue links:

| Link Type | Direction | Linked Issue | Context |
|-----------|-----------|--------------|---------|
| Related | outward | TC-8020 | Originating CVE Jira (stream rhtpa-2.2) that triggered preemptive task creation |
| Depend | inward | TC-8021 | Current CVE Jira (stream rhtpa-2.1) -- standard remediation linkage |

TC-8021 now has:

| Link Type | Direction | Linked Issue | Context |
|-----------|-----------|--------------|---------|
| Depend | outward | TC-8022 | Remediation task (formerly preemptive, now standard) |

## Summary

The preemptive remediation task TC-8022 was originally created during the triage of TC-8020 (CVE-2026-55123 for stream rhtpa-2.2) as a Case B cross-stream proactive remediation task. When PSIRT subsequently created TC-8021 as the stream-specific CVE Jira for rhtpa-2.1, Step 4.4 reconciliation detected the existing preemptive task, linked it properly to the new CVE Jira with a "Depend" relationship, and removed the `security-preemptive` label to convert it into a standard remediation task. This avoids duplicate task creation in Step 7.
