# Step 4.4 -- Preemptive Task Reconciliation

## Context

TC-8021 is a new CVE Jira for CVE-2026-55123 (tokio use-after-free) scoped to stream `rhtpa-2.1` (2.1.x). Before creating new remediation tasks in Step 8, Step 4.4 checks whether a proactive remediation task already exists for this CVE and stream, created by a prior Case A cross-stream analysis on a different stream's CVE Jira.

## JQL Search

Query executed:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

Fields requested: `summary, status, labels, issuelinks`

## Search Results

One matching task found:

| Field | Value |
|-------|-------|
| Key | TC-8022 |
| Summary | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) |
| Status | Open |
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |
| Issue Links | Related: TC-8020 (originating CVE Jira, stream [rhtpa-2.2]) |

## Filtering

- Task summary contains `(rhtpa-2.1)` which matches the current issue's stream scope `rhtpa-2.1`.
- Result: **Match confirmed** -- TC-8022 is a preemptive remediation task for this exact CVE and stream.

## Origin

TC-8022 was created during a prior triage of TC-8020 (CVE-2026-55123 for stream [rhtpa-2.2]). During that triage's Step 8 Case A (cross-stream impact), the analysis determined that stream 2.1.x was also affected. Because no CVE Jira existed for stream rhtpa-2.1 at that time, a preemptive remediation task was created with:
- The `security-preemptive` label to mark it as proactive
- A "Related" link to TC-8020 (the originating CVE Jira)

Now that PSIRT has created TC-8021 as the proper CVE Jira for stream rhtpa-2.1, Step 4.4 reconciliation converts the preemptive task into a standard remediation task.

## Reconciliation Actions

### 1. Link the new CVE Jira to the preemptive task

```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This creates the standard remediation linkage (same "Depend" type used when triage-security creates remediation tasks directly).

### 2. Remove the `security-preemptive` label

Current labels on TC-8022: `ai-generated-jira, Security, CVE-2026-55123, security-preemptive`

Updated labels (removing `security-preemptive`):

```
jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because TC-8022 is now linked to a proper CVE Jira (TC-8021) via "Depend" and no longer needs the preemptive marker.

### 3. Inform the engineer

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

### 4. Record reconciliation

Remediation already exists for stream 2.1.x via TC-8022. Step 8 will skip task creation for this stream.

## Final Link State of TC-8022

After reconciliation, TC-8022 has the following links:

| Link Type | Direction | Issue | Purpose |
|-----------|-----------|-------|---------|
| Related | TC-8022 <-> TC-8020 | Originating CVE Jira (stream rhtpa-2.2) | Created during Case A cross-stream analysis |
| Depend | TC-8021 -> TC-8022 | Current CVE Jira (stream rhtpa-2.1) | Standard remediation linkage from reconciliation |

## Final Label State of TC-8022

| Before Reconciliation | After Reconciliation |
|-----------------------|----------------------|
| ai-generated-jira, Security, CVE-2026-55123, security-preemptive | ai-generated-jira, Security, CVE-2026-55123 |
