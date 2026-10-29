# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## Purpose

When triaging a new CVE Jira for a specific stream, Step 4.4 checks whether a proactive remediation task already exists for this CVE and stream. Such tasks are created by Step 8 Case A (cross-stream impact) during a prior triage of a different stream's CVE Jira. If a matching preemptive task is found, it is reconciled -- linked to the new CVE Jira and converted from a preemptive task to a standard remediation task.

## JQL Search

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

Fields requested: summary, status, labels, issuelinks

## Search Results

| Key | Summary | Status | Labels | Issue Links |
|-----|---------|--------|--------|-------------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related: TC-8020 |

## Stream Filter

- Current issue stream suffix: `[rhtpa-2.1]`
- TC-8022 summary contains: `(rhtpa-2.1)` -- **matches** the current issue's stream

**Result: Matching preemptive task found -- TC-8022.**

## Reconciliation Analysis

TC-8022 was created during a prior triage of TC-8020, which is the CVE-2026-55123 Vulnerability issue for stream [rhtpa-2.2]. During that triage, the cross-stream impact analysis (Step 8 Case A) identified that stream 2.1.x was also affected by the tokio vulnerability. Since no CVE Jira existed for stream rhtpa-2.1 at that time, a preemptive remediation task was created:

- TC-8022 carries the `security-preemptive` label to indicate it was created proactively
- TC-8022 is linked via "Related" to TC-8020 (the originating CVE Jira from stream rhtpa-2.2)
- TC-8022's remediation target (bump tokio to 1.42.0) matches the fix threshold for this CVE

Now that PSIRT has created TC-8021 as the stream-specific CVE Jira for rhtpa-2.1, the preemptive task must be reconciled and converted to a standard remediation task.

## Proposed Reconciliation Actions

### Action 1: Link TC-8021 to TC-8022 (Depend)

**PROPOSAL** -- Create a "Depend" link from the new CVE Jira to the preemptive task, converting it to a standard remediation linkage:

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

Rationale: The "Depend" link type is the standard remediation linkage used when triage-security creates remediation tasks (per remediation-templates.md). This replaces the "Related" link to TC-8020 with a proper "Depend" link to TC-8021 as the authoritative CVE tracker for this stream.

### Action 2: Remove "security-preemptive" label from TC-8022

**PROPOSAL** -- Update TC-8022's labels to remove the preemptive marker:

```
Current labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
Updated labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

Rationale: The `security-preemptive` label is removed because TC-8022 is now linked to its own stream-specific CVE Jira (TC-8021). It is no longer a preemptive task -- it is a standard remediation task.

### Action 3: Record reconciliation for Step 8

Mark that remediation already exists for the 2.1.x stream so that Step 8 skips new remediation task creation for this stream.

- Stream: 2.1.x
- Existing remediation task: TC-8022
- Skip task creation: **yes**
- Reason: Preemptive task reconciled -- TC-8022 now serves as the standard remediation task for TC-8021

## Summary for Engineer

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (stream [rhtpa-2.2], linked via "Related").

Actions proposed:
- Link TC-8021 -> TC-8022 with "Depend" (standard remediation linkage)
- Remove "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```
