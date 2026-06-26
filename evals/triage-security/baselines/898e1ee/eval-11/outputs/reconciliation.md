# Step 4.4 — Preemptive Task Reconciliation Analysis

## Context

TC-8021 is a Vulnerability issue for CVE-2026-55123 (tokio use-after-free) scoped to stream `rhtpa-2.1`. A prior triage of TC-8020 (the same CVE for stream `rhtpa-2.2`) ran Step 7 Case B and detected that stream 2.1.x was also affected but had no CVE Jira at that time. That Case B run created a preemptive remediation task TC-8022 for stream rhtpa-2.1.

## JQL Search

Step 4.4 searches for preemptive tasks matching the current CVE:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

**Result:** TC-8022 — "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)"

## TC-8022 Details (Preemptive Task)

| Field | Value |
|-------|-------|
| Key | TC-8022 |
| Summary | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) |
| Status | Open |
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |
| Issue Links | Related: TC-8020 (originating CVE Jira, stream rhtpa-2.2) |

## Stream Matching

Step 4.4 filters JQL results to match the current issue's stream. The current issue TC-8021 has stream suffix `[rhtpa-2.1]`. TC-8022's summary contains `(rhtpa-2.1)`, which matches. Therefore TC-8022 is confirmed as the preemptive task for this stream.

## Reconciliation Actions

Per Step 4.4 of `jira-triage-operations.md`, the following actions are taken:

### 1. Link TC-8021 to TC-8022 with "Depend" link type

This is the standard remediation linkage used when triage-security links a CVE Jira to its remediation task.

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

### 2. Remove the `security-preemptive` label from TC-8022

The preemptive task is now linked to a proper CVE Jira (TC-8021), so the `security-preemptive` label is no longer appropriate. It transitions from a preemptive task to a standard remediation task.

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

### 3. Engineer notification

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 7.
```

### 4. Record reconciliation

The reconciliation is recorded so that Step 7 knows remediation already exists for stream rhtpa-2.1. Step 7 will skip creating new remediation tasks for this stream.

## Link Topology After Reconciliation

```
TC-8020 (CVE Jira, stream rhtpa-2.2)
  |
  |-- Related --> TC-8022 (remediation task, stream rhtpa-2.1)
  
TC-8021 (CVE Jira, stream rhtpa-2.1)  <-- current issue
  |
  |-- Depend --> TC-8022 (remediation task, stream rhtpa-2.1)
```

TC-8022 retains its "Related" link to TC-8020 (the originating CVE that triggered its creation) and gains a "Depend" link from TC-8021 (the now-arrived CVE Jira for its own stream).
