# Step 4.4 — Preemptive Task Reconciliation: TC-8021

## Search for Preemptive Tasks

**JQL executed:**

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

**Fields requested:** summary, status, labels, issuelinks

**Results:** 1 issue returned

| Key | Summary | Status | Labels |
|-----|---------|--------|--------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |

## Stream Filter

- Current issue stream (from summary suffix): **rhtpa-2.1**
- TC-8022 summary contains `(rhtpa-2.1)` — **matches** current stream

## Reconciliation Actions

### Action 1: Link TC-8021 to TC-8022 with "Depend" link type

The new CVE Jira is linked to the existing preemptive remediation task using the standard remediation linkage type.

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

### Action 2: Remove `security-preemptive` label from TC-8022

The preemptive task is now linked to a proper CVE Jira, so the `security-preemptive` label is removed. The task becomes a standard remediation task.

**Current labels on TC-8022:** ai-generated-jira, Security, CVE-2026-55123, security-preemptive

**Updated labels (after removing `security-preemptive`):** ai-generated-jira, Security, CVE-2026-55123

```
jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

## Reconciliation Summary

Existing preemptive remediation task TC-8022 found for this CVE and stream. Created from cross-stream analysis of TC-8020 (linked via "Related" — originating CVE Jira for stream [rhtpa-2.2]).

Actions taken:
- Linked TC-8021 to TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira. Remediation already exists for stream rhtpa-2.1 — Step 7 will skip new remediation task creation for this stream.
