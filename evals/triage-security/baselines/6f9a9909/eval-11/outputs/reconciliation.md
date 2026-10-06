# Step 4.4 -- Preemptive Task Reconciliation

## Search for Preemptive Tasks

**JQL query:**
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

**Result:** 1 matching task found.

| Key | Summary | Status | Labels | Issue Links |
|-----|---------|--------|--------|-------------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related: TC-8020 |

## Stream Matching

The current issue TC-8021 has stream suffix `[rhtpa-2.1]` (stream 2.1.x).

TC-8022's summary contains `(rhtpa-2.1)`, which matches the current issue's stream.

**Result: Matching preemptive task found.**

## Reconciliation Actions

Since a matching preemptive task (TC-8022) was found for this CVE and stream, the following actions are taken:

### a. Link the new CVE Jira to the preemptive task

```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This establishes the standard remediation linkage ("Depend") between the CVE Vulnerability issue TC-8021 and the remediation task TC-8022.

### b. Remove the `security-preemptive` label

The `security-preemptive` label is removed from TC-8022 because it is now linked to a proper CVE Jira for its stream.

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

### c. Engineer notification

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

### d. Record the reconciliation

Remediation already exists for stream 2.1.x via TC-8022. Step 8 (Case B) will skip task creation for this stream because a reconciled preemptive task already covers it.

## Provenance

- **Originating CVE Jira:** TC-8020 (stream [rhtpa-2.2])
- **Preemptive task:** TC-8022 (created during TC-8020 triage, Step 8 Case A cross-stream analysis)
- **Current CVE Jira:** TC-8021 (stream [rhtpa-2.1])
- **Link chain:** TC-8022 is "Related" to TC-8020 (originating CVE) and now "Depend" linked to TC-8021 (stream-specific CVE)
