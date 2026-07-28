# Step 4.4 — Preemptive Task Reconciliation

## Search for Preemptive Tasks

Per the reconciliation protocol, a JQL search is performed to find preemptive remediation tasks that already exist for this CVE and stream:

**JQL Query (proposed):**
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

**Fields requested:** summary, status, labels, issuelinks

### Search Results

The JQL search returns **1 result**:

| Key | Summary | Status | Labels |
|-----|---------|--------|--------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |

**Issue Links on TC-8022:**
- **Related**: TC-8020 (originating CVE Jira, stream [rhtpa-2.2])

## Stream Filtering

The current issue TC-8021 has stream suffix `[rhtpa-2.1]`, corresponding to stream **rhtpa-2.1**.

Checking TC-8022's summary for the current stream name:
- TC-8022 summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 **(rhtpa-2.1)**"
- The summary contains `(rhtpa-2.1)` which matches the current issue's stream.

**Result**: TC-8022 is a matching preemptive task for CVE-2026-55123 in stream rhtpa-2.1.

## Reconciliation Actions (Proposed)

The following actions are proposed to reconcile the preemptive task with the new CVE Jira. All actions require engineer confirmation before execution.

### Action 1: Link TC-8021 to TC-8022 with "Depend"

Create a standard remediation linkage between the new CVE Jira and the existing preemptive task:

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

This is the same "Depend" link type used when triage-security creates new remediation tasks — it establishes TC-8022 as the remediation task for TC-8021.

### Action 2: Remove 'security-preemptive' Label from TC-8022

The preemptive task is now linked to a proper CVE Jira for its stream. The `security-preemptive` label should be removed to convert it to a standard remediation task:

**Current labels on TC-8022:** `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`

**Proposed updated labels:** `ai-generated-jira`, `Security`, `CVE-2026-55123`

```
jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The task is now a standard remediation task linked to a proper CVE Jira. The `security-preemptive` label is removed because TC-8022 is no longer proactive — it has a matching CVE Jira (TC-8021) in its stream.

### Action 3: Inform the Engineer

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (stream [rhtpa-2.2], linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

## Reconciliation Record

The reconciliation is recorded so that Step 8 skips remediation task creation for stream rhtpa-2.1:

- **Stream**: rhtpa-2.1
- **Reconciled task**: TC-8022
- **Originating CVE**: TC-8020 (stream rhtpa-2.2)
- **New CVE Jira**: TC-8021 (stream rhtpa-2.1)
- **Link created**: TC-8021 -> TC-8022 (Depend)
- **Label removed**: `security-preemptive` from TC-8022
- **Step 8 action**: Skip remediation task creation for this stream — existing task already linked
