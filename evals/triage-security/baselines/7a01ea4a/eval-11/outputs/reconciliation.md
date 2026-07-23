# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## Context

TC-8021 is a CVE Vulnerability issue for CVE-2026-55123 (tokio use-after-free) scoped to stream `rhtpa-2.1` (suffix `[rhtpa-2.1]`). A prior triage of TC-8020 (the same CVE for stream `rhtpa-2.2`) already identified cross-stream impact on the 2.1.x stream and created a preemptive remediation task.

## Step 4.4 Execution

### 4.4.1 -- Search for preemptive tasks

JQL query:
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

**Result**: 1 issue returned -- **TC-8022**

### 4.4.2 -- Filter to matching stream

TC-8022 summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)"

The summary contains `(rhtpa-2.1)`, which matches the current issue's stream suffix `[rhtpa-2.1]`. This is a matching preemptive task.

### 4.4.3 -- Preemptive task details

| Field | Value |
|-------|-------|
| Key | TC-8022 |
| Summary | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) |
| Status | Open |
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |
| Existing links | Related: TC-8020 (originating CVE Jira, stream rhtpa-2.2) |

### 4.4.4 -- Reconciliation actions

A matching preemptive remediation task (TC-8022) was found for CVE-2026-55123 and stream rhtpa-2.1. The following reconciliation actions are required:

**a. Link the new CVE Jira to the preemptive task (Depend):**
```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```
This establishes the standard remediation linkage between the CVE Vulnerability issue (TC-8021) and its remediation task (TC-8022).

**b. Remove the `security-preemptive` label from TC-8022:**

Current labels: `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`
Updated labels: `["ai-generated-jira", "Security", "CVE-2026-55123"]`

```
jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because TC-8022 is now linked to a proper CVE Jira (TC-8021) for its stream. It transitions from a preemptive task to a standard remediation task.

**c. Inform the engineer:**

> Existing preemptive remediation task TC-8022 found for this CVE and stream.
> Created from cross-stream analysis of TC-8020 (stream rhtpa-2.2, linked via "Related").
>
> Actions taken:
> - Linked TC-8021 -> TC-8022 with "Depend"
> - Removed "security-preemptive" label from TC-8022
>
> The preemptive task is now a standard remediation task for this CVE Jira.
> Skipping new remediation task creation in Step 8.

**d. Record reconciliation:**

Remediation already exists for the rhtpa-2.1 stream via TC-8022. Step 8 will skip remediation task creation for this stream because the preemptive task fully covers the required fix (bump tokio to >= 1.42.0).

## Link Topology After Reconciliation

```
TC-8020 (CVE Vuln, rhtpa-2.2)
  |
  +-- Related --> TC-8022 (Remediation Task, rhtpa-2.1)  [original link from Case B]
                    ^
TC-8021 (CVE Vuln, rhtpa-2.1)
  |
  +-- Depend ---> TC-8022 (Remediation Task, rhtpa-2.1)  [new link from Step 4.4]
```

TC-8022 now has two links:
- **Related** to TC-8020 (the originating CVE from stream rhtpa-2.2 that triggered the preemptive creation)
- **Depend** from TC-8021 (the stream-specific CVE that now owns this remediation task)
