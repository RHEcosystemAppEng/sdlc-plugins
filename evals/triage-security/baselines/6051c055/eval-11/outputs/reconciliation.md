# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## Search for Preemptive Tasks

### JQL Query

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

Fields requested: summary, status, labels, issuelinks

### Search Results

One matching task returned:

| Key | Summary | Status | Labels |
|-----|---------|--------|--------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |

TC-8022 existing issue links:
- **Related**: TC-8020 (originating CVE Jira, stream [rhtpa-2.2])

## Stream Filtering

- Current issue stream suffix: `[rhtpa-2.1]` --> stream name `rhtpa-2.1`
- TC-8022 summary contains `(rhtpa-2.1)` --> **matches current stream**

TC-8022 is a preemptive remediation task created for stream rhtpa-2.1 during the prior triage of TC-8020 (stream rhtpa-2.2, Case B cross-stream impact).

## Reconciliation Actions

### a. Link CVE Jira to preemptive task

Create a "Depend" link (standard remediation linkage) from the new CVE Jira to the existing preemptive task:

```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This establishes TC-8022 as the remediation task for TC-8021, using the same link type that Step 8 would use for newly created remediation tasks.

### b. Remove security-preemptive label

TC-8022 is now linked to a proper CVE Jira (TC-8021), so the `security-preemptive` label is no longer needed. Remove it while preserving all other labels:

Current labels: `[ai-generated-jira, Security, CVE-2026-55123, security-preemptive]`
Updated labels: `[ai-generated-jira, Security, CVE-2026-55123]`

```
jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

### c. Engineer notification

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 --> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

### d. Record reconciliation

Remediation for stream rhtpa-2.1 is now covered by TC-8022. Step 8 will skip task creation for this stream because reconciliation has already provided a remediation task.

## Issue Link State After Reconciliation

TC-8021 issue links:
- **Depend**: TC-8021 --> TC-8022 (remediation task)

TC-8022 issue links:
- **Related**: TC-8022 <-> TC-8020 (originating CVE Jira from prior triage)
- **Depend**: TC-8021 --> TC-8022 (new link from this reconciliation)

TC-8022 labels after reconciliation:
- ai-generated-jira, Security, CVE-2026-55123
- (`security-preemptive` removed)
