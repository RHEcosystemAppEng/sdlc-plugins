# Step 4.4 — Preemptive Task Reconciliation

## Search for Preemptive Tasks

JQL query executed:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

**Result**: 1 task returned.

| Task Key | Summary | Status | Labels | Issue Links |
|----------|---------|--------|--------|-------------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related: TC-8020 (originating CVE, stream [rhtpa-2.2]) |

## Stream Matching

The current issue TC-8021 has stream suffix `[rhtpa-2.1]` → stream name `rhtpa-2.1`.

TC-8022's summary contains `(rhtpa-2.1)` — this matches the current issue's stream.

**Match confirmed**: TC-8022 is a preemptive remediation task for CVE-2026-55123 in the same stream (rhtpa-2.1).

## Reconciliation Actions

Since a matching preemptive task was found, the following reconciliation actions are proposed:

### 1. Link new CVE Jira to preemptive task (Depend)

```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This establishes the standard remediation linkage between the new CVE Jira (TC-8021) and the existing remediation task (TC-8022), identical to how newly created remediation tasks are linked.

### 2. Remove `security-preemptive` label from TC-8022

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because TC-8022 is now linked to a proper CVE Jira (TC-8021) via Depend. It is no longer a preemptive task — it is now a standard remediation task.

### 3. Record reconciliation for Step 8

Remediation already exists for stream rhtpa-2.1 via reconciled preemptive task TC-8022. Step 8 will skip new remediation task creation for this stream.

## Reconciliation Summary

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 → TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```
