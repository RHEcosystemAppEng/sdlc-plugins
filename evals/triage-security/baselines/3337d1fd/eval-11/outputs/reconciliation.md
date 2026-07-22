# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## Search for Preemptive Tasks

### JQL Query

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

### Search Results

| Task Key | Summary | Status | Labels | Issue Links |
|----------|---------|--------|--------|-------------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related: TC-8020 |

## Stream Matching

- Current issue stream suffix: `[rhtpa-2.1]`
- TC-8022 summary contains: `(rhtpa-2.1)`
- **Match confirmed**: TC-8022 is a preemptive remediation task for this CVE and this stream.

## Preemptive Task Origin

TC-8022 was created during a prior triage of TC-8020 (CVE-2026-55123, stream `[rhtpa-2.2]`). During that triage's Step 8 Case B (cross-stream impact), the version impact analysis identified that the 2.1.x stream was also affected by CVE-2026-55123. Since no CVE Jira existed for the 2.1.x stream at the time, a preemptive remediation task (TC-8022) was created with:
- The `security-preemptive` label to distinguish it from standard remediation tasks
- A "Related" link to TC-8020 (the originating CVE Jira from stream 2.2.x)

## Reconciliation Actions

Now that TC-8021 (the stream-specific CVE Jira for rhtpa-2.1) exists, reconciliation converts the preemptive task into a standard remediation task:

### Action 1: Link CVE Jira to preemptive task with "Depend"

```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This establishes the standard remediation linkage between the CVE Jira (TC-8021) and the remediation task (TC-8022), identical to how Step 8 Case A links newly created tasks.

### Action 2: Remove the `security-preemptive` label

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

Removing the `security-preemptive` label converts TC-8022 from a proactive/provisional task into a standard remediation task that is now backed by a proper CVE Jira.

### Action 3: Inform the engineer

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

### Action 4: Record reconciliation

Remediation already exists for stream 2.1.x via TC-8022. Step 8 will skip task creation for this stream -- no new remediation tasks are needed.

## Post-Reconciliation State of TC-8022

| Field | Before Reconciliation | After Reconciliation |
|-------|----------------------|---------------------|
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | ai-generated-jira, Security, CVE-2026-55123 |
| Link to TC-8020 | Related | Related (unchanged) |
| Link to TC-8021 | _(none)_ | Depend (new) |
| Status | Open | Open (unchanged) |
| Role | Preemptive (provisional) | Standard remediation task |
