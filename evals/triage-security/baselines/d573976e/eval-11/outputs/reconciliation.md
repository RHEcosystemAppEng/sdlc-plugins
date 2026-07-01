# Step 4.4 -- Preemptive Task Reconciliation

## Search for Preemptive Tasks

JQL query constructed from Security Configuration:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

Fields requested: `summary, status, labels, issuelinks`

### Search Results

The JQL search returns **1 result**:

| Key | Summary | Status | Labels |
|-----|---------|--------|--------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |

**Issue Links on TC-8022:**
- **Related**: TC-8020 (originating CVE Jira, stream [rhtpa-2.2])

## Stream Filtering

The current issue (TC-8021) has stream suffix `[rhtpa-2.1]`, corresponding to stream **rhtpa-2.1**.

TC-8022's summary contains `(rhtpa-2.1)` -- this matches the current issue's stream.

**Match found**: TC-8022 is a preemptive remediation task for CVE-2026-55123 in stream rhtpa-2.1.

## Reconciliation Analysis

TC-8022 was created during a prior triage of TC-8020 (stream [rhtpa-2.2]) as a proactive preemptive remediation task under Step 8 Case B. At that time, no CVE Jira existed for stream rhtpa-2.1, so a preemptive task was created with:
- The `security-preemptive` label to distinguish it from standard remediation
- A "Related" link to TC-8020 (the originating CVE from a different stream)

Now that TC-8021 (a proper CVE Jira for stream rhtpa-2.1) has been created by PSIRT, the preemptive task should be reconciled into a standard remediation task.

## Proposed Reconciliation Actions

The following Jira mutations are proposed (requiring engineer confirmation):

### Action 1: Link TC-8021 to TC-8022 with "Depend"

Create a standard remediation linkage between the new CVE Jira and the preemptive task:

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

This establishes TC-8022 as a remediation task that TC-8021 depends on (the standard link type used when triage-security creates remediation tasks).

### Action 2: Remove the `security-preemptive` label from TC-8022

The task is no longer preemptive -- it is now linked to a proper CVE Jira for its stream:

```
Current labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
Updated labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

### Action 3: Inform the engineer

```
Existing preemptive remediation task TC-8022 found for this CVE and
stream. Created from cross-stream analysis of TC-8020
(linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

## Reconciliation Outcome

- **Preemptive task TC-8022 reconciled**: linked to TC-8021 via "Depend", `security-preemptive` label removed
- **Existing "Related" link to TC-8020 preserved**: TC-8022 retains its historical link to the originating cross-stream CVE
- **Remediation task creation in Step 8 skipped**: the reconciled TC-8022 now serves as the standard remediation task for stream rhtpa-2.1, so no new task needs to be created
- **Record**: remediation already exists for stream 2.1.x via reconciled preemptive task TC-8022. Step 8 will check this record and skip task creation for this stream.
