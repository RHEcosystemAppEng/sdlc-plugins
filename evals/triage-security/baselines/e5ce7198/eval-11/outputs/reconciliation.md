# Step 4.4 -- Preemptive Task Reconciliation for TC-8021

## Context

TC-8021 is a Vulnerability issue for CVE-2026-55123 (tokio use-after-free), scoped to stream **rhtpa-2.1** via the summary suffix `[rhtpa-2.1]`. A prior triage of TC-8020 (same CVE, stream rhtpa-2.2) performed cross-stream impact analysis (Step 7 Case B) and created a preemptive remediation task for stream 2.1.x because no stream-specific CVE Jira existed at that time.

## Step 4.4 Procedure

### 1. Search for preemptive tasks

JQL query executed (simulated):

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

**Result**: 1 issue returned -- **TC-8022**

### 2. Filter to current stream

TC-8022 summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)"

The summary contains `(rhtpa-2.1)`, which matches the current issue's stream suffix `[rhtpa-2.1]`.

**Match confirmed**: TC-8022 is a preemptive remediation task for this CVE and this stream.

### 3. Preemptive task details

| Field | Value |
|-------|-------|
| Key | TC-8022 |
| Summary | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) |
| Status | Open |
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |
| Issue Links | Related: TC-8020 (originating CVE Jira, stream rhtpa-2.2) |

### 4. Proposed reconciliation actions

Per Step 4.4 of jira-triage-operations.md, the following actions are proposed:

#### a. Link TC-8021 to TC-8022 with "Depend"

```
Proposed: jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This establishes the standard remediation linkage between the new CVE Jira (TC-8021) and the existing remediation task (TC-8022), consistent with the link type used when triage-security creates new remediation tasks in Step 7 Case A.

#### b. Remove the `security-preemptive` label from TC-8022

```
Proposed: jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because TC-8022 is now linked to a proper stream-specific CVE Jira (TC-8021). It transitions from a preemptive task to a standard remediation task.

#### c. Engineer notification

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 7.
```

### 5. Record reconciliation

Remediation for stream 2.1.x is marked as **already covered** by TC-8022. Step 7 will skip new remediation task creation for this stream.

## Link topology after reconciliation

```
TC-8020 (CVE Jira, stream rhtpa-2.2)
  |
  +-- Related --> TC-8022 (remediation task, rhtpa-2.1)
                    ^
TC-8021 (CVE Jira, stream rhtpa-2.1)
  |
  +-- Depend --> TC-8022 (remediation task, rhtpa-2.1)
```

TC-8022 retains its "Related" link to TC-8020 (the originating CVE that triggered its creation) and gains a "Depend" link from TC-8021 (the stream-specific CVE Jira it now serves). The `security-preemptive` label is removed, completing the reconciliation.
