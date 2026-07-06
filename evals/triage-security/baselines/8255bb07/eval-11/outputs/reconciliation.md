# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## JQL Search

Query executed (simulated):

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

Fields requested: summary, status, labels, issuelinks

## Search Results

One matching preemptive task found:

| Field | Value |
|-------|-------|
| Key | TC-8022 |
| Summary | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) |
| Status | Open |
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |
| Issue Links | Related: TC-8020 (originating CVE Jira, stream rhtpa-2.2) |

## Stream Matching

- Current issue stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- Preemptive task summary contains: `(rhtpa-2.1)`
- **Match confirmed**: TC-8022 is a preemptive remediation task for the same CVE and the same stream as TC-8021.

## Origin

TC-8022 was created during the triage of TC-8020 (CVE-2026-55123 for stream rhtpa-2.2). The Step 8 Case B cross-stream analysis on TC-8020 identified that stream 2.1.x was also affected and had no CVE Jira at the time, so a preemptive remediation task was created with the `security-preemptive` label and a "Related" link back to TC-8020.

## Reconciliation Actions

Per Step 4.4 of jira-triage-operations.md, the following actions are taken:

### Action (a): Link TC-8021 to TC-8022 with "Depend"

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

This establishes the standard remediation linkage between the CVE Vulnerability issue (TC-8021) and its remediation task (TC-8022), identical to the link type used when creating new remediation tasks in Step 8.

### Action (b): Remove `security-preemptive` label from TC-8022

Current labels: `[ai-generated-jira, Security, CVE-2026-55123, security-preemptive]`
Updated labels: `[ai-generated-jira, Security, CVE-2026-55123]`

```
jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because the task is now linked to a proper CVE Jira (TC-8021). It is no longer a preemptive/orphan task -- it has been adopted by the stream-specific CVE issue.

### Action (c): Engineer notification

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

### Action (d): Record reconciliation

Reconciliation is recorded so that Step 8 knows remediation already exists for stream 2.1.x. The flag `remediation_exists_for_streams = ["2.1.x"]` is set internally, which causes Step 8 to skip task creation for this stream.

## Final State of TC-8022 After Reconciliation

| Field | Before | After |
|-------|--------|-------|
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | ai-generated-jira, Security, CVE-2026-55123 |
| Issue Links | Related: TC-8020 | Related: TC-8020, Depend: TC-8021 |
| Status | Open | Open (unchanged) |
| Summary | (unchanged) | (unchanged) |

## Final Link Graph

```
TC-8020 (CVE-2026-55123, stream rhtpa-2.2)
  |
  +-- Related --> TC-8022 (remediation task, originally preemptive)
                    |
TC-8021 (CVE-2026-55123, stream rhtpa-2.1)
  |
  +-- Depend --> TC-8022 (now standard remediation task)
```
