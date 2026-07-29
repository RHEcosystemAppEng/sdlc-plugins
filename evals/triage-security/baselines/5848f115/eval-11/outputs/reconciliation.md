# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## Purpose

When triaging a new CVE Jira for a specific stream, Step 4.4 checks whether a proactive remediation task already exists for this CVE and stream. Such tasks are created by a prior Step 8 Case A run on a different stream's CVE Jira.

## JQL Search

Query executed:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

Fields requested: summary, status, labels, issuelinks

## Search Results

One result returned:

| Field | Value |
|-------|-------|
| Key | TC-8022 |
| Summary | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) |
| Status | Open |
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |
| Issue Links | Related: TC-8020 (originating CVE Jira, stream rhtpa-2.2) |

## Stream Filter

- Current issue stream suffix: `[rhtpa-2.1]` -- stream name `rhtpa-2.1`
- TC-8022 summary contains `(rhtpa-2.1)` -- **match confirmed**

TC-8022 is a preemptive remediation task for the same CVE (CVE-2026-55123) and the same stream (rhtpa-2.1). It was created during cross-stream analysis of TC-8020 (a CVE Jira for stream rhtpa-2.2).

## Reconciliation Actions

Since a matching preemptive task was found, the following actions are performed:

### a. Link new CVE Jira to preemptive task with "Depend"

```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This creates the standard remediation linkage ("Depend") between the CVE Jira TC-8021 and the remediation task TC-8022. The preemptive task previously had only a "Related" link to TC-8020 (the originating CVE from another stream). Now it also has a "Depend" link to TC-8021, making it a proper remediation task for this CVE Jira.

### b. Remove the `security-preemptive` label

Current labels on TC-8022: `ai-generated-jira, Security, CVE-2026-55123, security-preemptive`

Updated labels (after removing `security-preemptive`): `ai-generated-jira, Security, CVE-2026-55123`

```
jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because TC-8022 is now linked to a proper CVE Jira (TC-8021) for its stream. It is no longer a preemptive task -- it is a standard remediation task.

### c. Engineer notification

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (stream rhtpa-2.2, linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

### d. Record reconciliation

Remediation for stream 2.1.x is recorded as already existing via TC-8022. Step 8 (Remediation) will skip task creation for this stream because a reconciled preemptive task covers it.

## Link State After Reconciliation

TC-8022 now has the following issue links:

| Link Type | Direction | Target | Purpose |
|-----------|-----------|--------|---------|
| Related | outward | TC-8020 | Originating CVE Jira from stream rhtpa-2.2 (created during Case A cross-stream analysis) |
| Depend | inward | TC-8021 | New CVE Jira for stream rhtpa-2.1 (standard remediation linkage, created by this reconciliation) |

This dual-link state is correct: TC-8022 was originally preemptive (Related to TC-8020) and is now also a proper remediation task (Depend from TC-8021).
