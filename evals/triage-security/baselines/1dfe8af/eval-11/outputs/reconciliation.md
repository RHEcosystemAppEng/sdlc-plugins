# Step 4.4 -- Preemptive Task Reconciliation

## Context

When triaging TC-8021 (CVE-2026-55123, stream `[rhtpa-2.1]`), Step 4.4 checks whether
a proactive remediation task already exists for this CVE and stream. Such a task would
have been created by a prior Step 7 Case B run on a different stream's CVE Jira.

## JQL Search

Search for preemptive tasks matching the current CVE:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

Fields requested: `summary, status, labels, issuelinks`

## Search Results

The JQL search returns one result:

| Key | Summary | Status | Labels |
|-----|---------|--------|--------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |

### Issue Links on TC-8022

- **Related**: TC-8020 (originating CVE Jira, stream `[rhtpa-2.2]`)

## Stream Filtering

The current issue TC-8021 has stream suffix `[rhtpa-2.1]`, which identifies stream `rhtpa-2.1`.

TC-8022's summary contains `(rhtpa-2.1)` -- this matches the current issue's stream.

**Result: TC-8022 is a matching preemptive task for CVE-2026-55123 in stream rhtpa-2.1.**

## Reconciliation Actions

Per Step 4.4 procedure, the following actions are taken:

### Action 1: Link CVE Jira to Preemptive Task with "Depend"

```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This establishes the standard remediation linkage between the CVE Vulnerability issue
(TC-8021) and the remediation task (TC-8022), identical to the linkage that would be
created if Step 7 were creating a new remediation task.

### Action 2: Remove "security-preemptive" Label from TC-8022

The preemptive task is now linked to its proper CVE Jira, so the `security-preemptive`
label is no longer needed. Updated labels:

```
Current labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
Updated labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

### Action 3: Inform the Engineer

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 7.
```

### Action 4: Record Reconciliation for Step 7

The reconciliation is recorded so that Step 7 knows remediation already exists for
stream 2.1.x. Step 7 will **skip** creating new remediation tasks for this stream
because Step 4.4 has already linked an existing task (TC-8022).

## Provenance

TC-8022 was originally created as a preemptive remediation task during the triage of
TC-8020 (CVE-2026-55123 for stream `[rhtpa-2.2]`). When that triage's Step 7 Case B
detected that stream 2.1.x was also affected but had no CVE Jira yet, it created
TC-8022 with:
- The `security-preemptive` label to mark it as proactive
- A "Related" link back to TC-8020 (the originating CVE Jira)
- The CVE-2026-55123 label for future JQL discovery

Now that PSIRT has created TC-8021 specifically for stream `[rhtpa-2.1]`, Step 4.4
reconciliation converts TC-8022 from a preemptive task into a standard remediation
task by linking it to TC-8021 with "Depend" and removing the preemptive label.
