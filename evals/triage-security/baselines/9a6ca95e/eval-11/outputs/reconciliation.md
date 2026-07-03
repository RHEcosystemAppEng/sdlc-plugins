# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## Purpose

Step 4.4 checks whether a proactive remediation task already exists for the current CVE and stream, created by a prior Step 8 Case B run on a different stream's CVE Jira. This prevents duplicate remediation tasks when PSIRT creates stream-specific CVE Jiras after cross-stream proactive tasks were already created.

## JQL Search

Query:
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

Fields requested: summary, status, labels, issuelinks

### Search Results

| Key | Summary | Status | Labels |
|-----|---------|--------|--------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |

TC-8022 issue links:
- **Related**: TC-8020 (originating CVE Jira, stream [rhtpa-2.2])

## Stream Filter

Current issue TC-8021 stream suffix: `[rhtpa-2.1]`

TC-8022 summary contains `(rhtpa-2.1)` -- **matches** the current issue's stream.

**Result: Matching preemptive task found -- TC-8022.**

## Reconciliation Actions

Per Step 4.4 of `jira-triage-operations.md`, the following actions are taken when a matching preemptive task is found:

### a. Link CVE Jira to Preemptive Task (Depend)

Create a "Depend" link (standard remediation linkage) between the new CVE Jira and the preemptive task:

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

This establishes TC-8022 as the remediation task for TC-8021, identical to how a freshly created remediation task would be linked.

### b. Remove security-preemptive Label

Remove the `security-preemptive` label from TC-8022 because it is now linked to a proper CVE Jira (TC-8021). The task is no longer "preemptive" -- it is a standard remediation task.

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

### c. Engineer Notification

Present the following to the engineer:

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

### d. Record Reconciliation

Remediation already exists for stream 2.1.x via TC-8022. Step 8 will skip task creation for this stream -- no new remediation tasks need to be created.

## Link Topology After Reconciliation

```
TC-8020 (CVE Jira, stream rhtpa-2.2)
  |
  +--[Related]--> TC-8022 (remediation task, rhtpa-2.1)
                    ^
                    |
TC-8021 (CVE Jira, stream rhtpa-2.1)
  |
  +--[Depend]----> TC-8022 (remediation task, rhtpa-2.1)
```

- TC-8022 was originally created as a preemptive task during triage of TC-8020 (Case B cross-stream proactive remediation)
- TC-8022 was linked to TC-8020 via "Related" (preemptive task variant linkage)
- Now TC-8022 is also linked to TC-8021 via "Depend" (standard remediation linkage)
- The `security-preemptive` label has been removed from TC-8022
