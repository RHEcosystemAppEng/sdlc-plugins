# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## JQL Search

Search for preemptive tasks matching CVE-2026-55123:

```
jira.search_jql(
  "project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC",
  fields: ["summary", "status", "labels", "issuelinks"]
)
```

### Search Results

| Key | Summary | Status | Labels | Issue Links |
|-----|---------|--------|--------|-------------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related: TC-8020 |

## Stream Matching

The current issue TC-8021 has stream suffix `[rhtpa-2.1]`, mapping to stream 2.1.x.

TC-8022's summary contains `(rhtpa-2.1)` -- this matches the current issue's stream scope.

**Result: Matching preemptive task found.**

## Reconciliation Actions

Per Step 4.4 of the triage-security skill, the following actions are taken:

### a. Link TC-8021 to TC-8022 with "Depend"

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

This establishes the standard remediation linkage between the CVE Jira (TC-8021) and the remediation task (TC-8022), identical to how a newly created remediation task would be linked.

### b. Remove the `security-preemptive` label from TC-8022

Current labels on TC-8022: `ai-generated-jira, Security, CVE-2026-55123, security-preemptive`

Updated labels (with `security-preemptive` removed): `ai-generated-jira, Security, CVE-2026-55123`

```
jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because TC-8022 is now linked to a proper CVE Jira (TC-8021) for its stream. It is no longer a preemptive/orphan task -- it is a standard remediation task.

### c. Engineer Notification

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

### d. Record Reconciliation

Remediation for stream 2.1.x is recorded as already covered by TC-8022. Step 8 will skip task creation for this stream.

## Link Topology After Reconciliation

```
TC-8020 (CVE Jira, stream rhtpa-2.2)
  |
  +-- Related --> TC-8022 (remediation task, stream rhtpa-2.1)
                    |
TC-8021 (CVE Jira, stream rhtpa-2.1)
  |
  +-- Depend --> TC-8022 (remediation task, stream rhtpa-2.1)
```

TC-8022 retains its "Related" link to TC-8020 (the originating CVE from the cross-stream triage) and now also has a "Depend" link from TC-8021 (the stream-specific CVE Jira). The `security-preemptive` label is removed, converting it from a preemptive task to a standard remediation task.
