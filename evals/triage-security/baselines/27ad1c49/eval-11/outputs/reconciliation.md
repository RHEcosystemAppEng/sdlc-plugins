# Step 4.4 -- Preemptive Task Reconciliation Analysis for TC-8021

## Context

TC-8021 is a PSIRT-created Vulnerability issue for CVE-2026-55123 (tokio use-after-free) scoped to stream `[rhtpa-2.1]`. Step 4.4 checks whether a proactive remediation task already exists for this CVE and stream, created by a prior Case A cross-stream triage of a different stream's CVE Jira.

## Preemptive Task Search

### JQL Query

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

### Search Results

| Key | Summary | Status | Labels | Issue Links |
|-----|---------|--------|--------|-------------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related: TC-8020 |

## Stream Matching

- Current issue stream suffix: `[rhtpa-2.1]`
- TC-8022 summary contains: `(rhtpa-2.1)`
- **Match confirmed**: TC-8022 is the preemptive remediation task for the current issue's stream (rhtpa-2.1 / 2.1.x).

## Originating Issue

- TC-8022 was created during triage of **TC-8020** (CVE-2026-55123, stream `[rhtpa-2.2]`)
- TC-8020's Step 8 Case A detected that stream 2.1.x was also affected but had no stream-specific CVE Jira at that time
- TC-8022 was created as a preemptive remediation task with the `security-preemptive` label and linked to TC-8020 via "Related"

## Reconciliation Actions (Step 4.4)

Per the Step 4.4 procedure, the following actions are required:

### a. Link the new CVE Jira to the preemptive task (Depend)

```
jira.create_link(
  inwardIssue: TC-8021,     (current CVE Jira)
  outwardIssue: TC-8022,    (preemptive task)
  type: "Depend"
)
```

This establishes the standard remediation linkage between TC-8021 and TC-8022, the same link type used for non-preemptive remediation tasks.

### b. Remove the security-preemptive label from TC-8022

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because TC-8022 is now linked to its own stream-specific CVE Jira (TC-8021). It is no longer preemptive -- it is a standard remediation task.

### c. Engineer notification

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

### d. Record the reconciliation

The reconciliation is recorded so that Step 8 (Remediation) skips task creation for the 2.1.x stream. TC-8022 already covers the required upstream remediation (bump tokio to >= 1.42.0 on release/0.3.z branch). No new remediation tasks need to be created.

## Reconciliation Outcome

| Check | Result |
|-------|--------|
| Preemptive task found? | YES -- TC-8022 |
| Stream match? | YES -- (rhtpa-2.1) in summary matches [rhtpa-2.1] suffix |
| Originating CVE Jira | TC-8020 (stream [rhtpa-2.2]) |
| Link created | TC-8021 -> TC-8022 (Depend) |
| Label removed | security-preemptive removed from TC-8022 |
| Step 8 impact | Skip remediation task creation for 2.1.x stream |
