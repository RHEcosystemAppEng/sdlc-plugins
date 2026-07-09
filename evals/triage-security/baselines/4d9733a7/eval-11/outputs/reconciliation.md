# Step 4.4 -- Preemptive Task Reconciliation

## 4.4.1 -- Search for Preemptive Tasks

**Proposed JQL query:**

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

Fields requested: summary, status, labels, issuelinks

## 4.4.2 -- Search Results

One result returned:

- **TC-8022** -- Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)
  - Status: Open
  - Labels: ai-generated-jira, Security, CVE-2026-55123, security-preemptive
  - Issue Links:
    - Related: TC-8020 (originating CVE Jira, stream [rhtpa-2.2])

## 4.4.3 -- Filter by Current Stream

The current issue (TC-8021) is scoped to stream **rhtpa-2.1**. The preemptive task TC-8022's summary contains `(rhtpa-2.1)` -- this **matches** the current stream.

**Match confirmed**: TC-8022 is a preemptive task for CVE-2026-55123 in stream rhtpa-2.1.

## 4.4.4 -- Reconciliation Actions (Proposed)

### a. Link new CVE Jira to preemptive task

**Proposed:**
```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This uses the standard remediation linkage (Depend), not the preemptive "Related" link. TC-8022 is now a proper remediation task for TC-8021.

### b. Remove security-preemptive label

**Proposed:**
```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because the task is now linked to a proper CVE Jira (TC-8021) and is no longer a preemptive task.

### c. Inform the engineer

> Existing preemptive remediation task TC-8022 found for this CVE and stream.
> Created from cross-stream analysis of TC-8020 (stream [rhtpa-2.2]),
> linked via "Related".
>
> Actions taken (proposed):
> - Linked TC-8021 -> TC-8022 with "Depend"
> - Removed "security-preemptive" label from TC-8022
>
> The preemptive task is now a standard remediation task for this CVE Jira.
> Skipping new remediation task creation in Step 8.

### d. Record reconciliation

Remediation already exists for stream rhtpa-2.1 via reconciled preemptive task TC-8022. Step 8 will **skip** remediation task creation for this stream.

All actions above are **proposals** requiring engineer confirmation before execution.
