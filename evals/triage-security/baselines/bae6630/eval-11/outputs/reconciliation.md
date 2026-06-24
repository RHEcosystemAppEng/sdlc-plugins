# Step 4.4 -- Preemptive Task Reconciliation

## Context

TC-8021 is a new Vulnerability issue for CVE-2026-55123 (tokio use-after-free) scoped to stream `rhtpa-2.1` (suffix `[rhtpa-2.1]`). Before creating remediation tasks, Step 4.4 checks whether a proactive remediation task already exists for this CVE and stream.

## JQL Search

Query executed (simulated):

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

- TC-8022's summary contains `(rhtpa-2.1)`, which matches the current issue's stream suffix `[rhtpa-2.1]`.
- **Match confirmed**: TC-8022 is a preemptive remediation task for this exact CVE and stream.

## Origin

TC-8022 was created during prior triage of TC-8020 (CVE-2026-55123 for stream `[rhtpa-2.2]`). During that triage, Step 7 Case B identified that stream `2.1.x` was also affected but had no CVE Jira yet, so a preemptive remediation task was created with the `security-preemptive` label and linked to TC-8020 via "Related".

## Reconciliation Actions

Per Step 4.4 of the triage-security skill, the following actions are required:

### a. Link the new CVE Jira to the preemptive task

```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This establishes the standard remediation linkage (TC-8021 depends on TC-8022), converting the preemptive task into a proper remediation task for this CVE Jira.

### b. Remove the `security-preemptive` label

Current labels on TC-8022: `[ai-generated-jira, Security, CVE-2026-55123, security-preemptive]`

Updated labels (removing `security-preemptive`):

```
jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

### c. Engineer notification

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (stream [rhtpa-2.2], linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 7.
```

### d. Record reconciliation

Remediation already exists for stream `2.1.x` via TC-8022. Step 7 will **skip** task creation for this stream because the preemptive task has been reconciled and is now linked as a standard remediation task.

## Impact on Subsequent Steps

- **Step 7 (Remediation)**: No new remediation tasks will be created for stream `2.1.x`. TC-8022 already covers the required work (bumping tokio to >= 1.42.0 on the `release/0.3.z` branch of the backend repository).
- **TC-8022 link topology after reconciliation**:
  - "Related" to TC-8020 (originating CVE from stream rhtpa-2.2) -- existing link preserved
  - "Depend" from TC-8021 (this CVE Jira for stream rhtpa-2.1) -- newly created
