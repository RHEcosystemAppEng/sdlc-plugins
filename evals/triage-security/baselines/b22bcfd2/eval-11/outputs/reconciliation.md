# Step 4.4 -- Preemptive Task Reconciliation

## Context

TC-8021 is a new CVE Jira for CVE-2026-55123, scoped to stream **rhtpa-2.1**. Before creating remediation tasks, Step 4.4 checks whether a proactive (preemptive) remediation task already exists for this CVE and stream.

A preemptive task may exist because a prior triage of the same CVE on a different stream (TC-8020, stream rhtpa-2.2) detected cross-stream impact and proactively created remediation tasks for stream rhtpa-2.1 under Step 8 Case B.

## JQL Search for Preemptive Tasks

The following JQL query searches for preemptive tasks matching CVE-2026-55123:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

Fields requested: `summary, status, labels, issuelinks`

### Search Results

| Issue Key | Summary | Status | Labels |
|-----------|---------|--------|--------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |

## Stream Matching

The preemptive task TC-8022's summary contains `(rhtpa-2.1)`, which matches the current issue TC-8021's stream scope (rhtpa-2.1). This confirms the task was created for the same stream.

## Preemptive Task Details

| Field | Value |
|-------|-------|
| Task Key | TC-8022 |
| Summary | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) |
| Status | Open |
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |
| Issue Links | Related: TC-8020 (originating CVE Jira, stream rhtpa-2.2) |

## Reconciliation Actions

Since a matching preemptive task (TC-8022) was found for CVE-2026-55123 in stream rhtpa-2.1, the following reconciliation actions are proposed:

### Action 1: Link TC-8021 to TC-8022 with "Depend"

**Proposed mutation:** Create a "Depend" link between the new CVE Jira and the preemptive task, establishing standard remediation linkage.

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

This replaces the existing "Related" link (from TC-8020) as the primary tracking relationship. TC-8022 is now a standard remediation task linked to its own stream's CVE Jira (TC-8021) via "Depend", and retains the "Related" link to the originating cross-stream CVE (TC-8020) for traceability.

### Action 2: Remove "security-preemptive" label from TC-8022

**Proposed mutation:** Remove the `security-preemptive` label from TC-8022. The task is no longer preemptive -- it is now linked to a proper CVE Jira for its stream.

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed. The remaining labels (`ai-generated-jira`, `Security`, `CVE-2026-55123`) are standard remediation task labels.

## Reconciliation Summary

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (stream rhtpa-2.2, linked via "Related").

Actions proposed:
- Link TC-8021 -> TC-8022 with "Depend" (standard remediation linkage)
- Remove "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

## Impact on Step 8

Because Step 4.4 reconciliation successfully linked an existing preemptive task (TC-8022) to the current CVE Jira (TC-8021), remediation already exists for stream rhtpa-2.1. **Step 8 will skip remediation task creation for this stream.** No new upstream backport task or downstream propagation subtask needs to be created -- TC-8022 already covers the fix.

## Final State of TC-8022 (After Reconciliation)

| Field | Before Reconciliation | After Reconciliation |
|-------|----------------------|---------------------|
| Labels | ai-generated-jira, Security, CVE-2026-55123, **security-preemptive** | ai-generated-jira, Security, CVE-2026-55123 |
| Issue Links | Related: TC-8020 | Related: TC-8020, **Depend: TC-8021** |
| Role | Preemptive remediation (proactive, no CVE Jira) | Standard remediation (linked to CVE Jira TC-8021) |
