# Step 4.4 -- Preemptive Task Reconciliation

## Search for Preemptive Tasks

Search for existing preemptive remediation tasks matching the current CVE (CVE-2026-55123):

**JQL query:**
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

**Fields requested:** summary, status, labels, issuelinks

### Search Results

| Issue Key | Summary | Status | Labels |
|-----------|---------|--------|--------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |

**Result count:** 1

## Stream Filtering

Filter results to match the current issue's stream (rhtpa-2.1):

- TC-8022 summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 **(rhtpa-2.1)**"
- Current issue stream: **rhtpa-2.1**
- Match: **YES** -- the task summary contains "(rhtpa-2.1)" which matches the current issue's stream

## Matching Preemptive Task Found: TC-8022

TC-8022 is a preemptive remediation task for CVE-2026-55123 in stream rhtpa-2.1, created during a prior cross-stream triage of TC-8020 (stream rhtpa-2.2). It carries the `security-preemptive` label and is linked to TC-8020 via a "Related" link.

### Current state of TC-8022:
- **Status**: Open
- **Labels**: ai-generated-jira, Security, CVE-2026-55123, security-preemptive
- **Issue Links**: Related to TC-8020 (originating CVE Jira, stream [rhtpa-2.2])

## Reconciliation Actions

### Action 1: Link CVE Jira to preemptive task with "Depend"

Create a standard remediation linkage between the new CVE Jira TC-8021 and the existing preemptive task TC-8022:

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

This is the standard remediation linkage -- the same link type used when triage-security creates new remediation tasks in Step 8.

### Action 2: Remove the 'security-preemptive' label from TC-8022

The task is now linked to a proper CVE Jira (TC-8021) for this stream, so the `security-preemptive` label is no longer needed. The task transitions from a proactive preemptive task to a standard remediation task.

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed. The remaining labels (ai-generated-jira, Security, CVE-2026-55123) are standard remediation task labels.

### Action 3: Inform the engineer

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (stream [rhtpa-2.2], linked via "Related").

Actions taken:
- Linked TC-8021 --> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

### Action 4: Record reconciliation for Step 8

Mark that remediation already exists for stream rhtpa-2.1 so that Step 8 skips task creation for this stream. The existing task TC-8022 already covers the needed remediation (bumping tokio to 1.42.0 in the rhtpa-2.1 stream).

## Post-Reconciliation State of TC-8022

| Field | Before | After |
|-------|--------|-------|
| Labels | ai-generated-jira, Security, CVE-2026-55123, **security-preemptive** | ai-generated-jira, Security, CVE-2026-55123 |
| Issue Links | Related: TC-8020 | Related: TC-8020, **Depend: TC-8021** |
| Status | Open | Open (unchanged) |

TC-8022 is now a standard remediation task:
- Linked to TC-8021 (its own stream's CVE Jira) via "Depend" -- standard remediation linkage
- Linked to TC-8020 (originating cross-stream CVE Jira) via "Related" -- historical provenance
- No longer carries the `security-preemptive` label
