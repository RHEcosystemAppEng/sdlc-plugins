# Step 4.4 -- Preemptive Task Reconciliation

## Search for Preemptive Tasks

**JQL query:**
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

**Result:** 1 task found -- **TC-8022**

## Preemptive Task Details

| Field | Value |
|-------|-------|
| Key | TC-8022 |
| Summary | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) |
| Status | Open |
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |
| Issue Links | Related: TC-8020 (originating CVE Jira, stream [rhtpa-2.2]) |

## Stream Matching

- Current issue TC-8021 stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- TC-8022 summary contains `(rhtpa-2.1)` -- **match confirmed**
- TC-8022 was created by a prior Step 8 Case B run during triage of TC-8020 (stream [rhtpa-2.2])

## Reconciliation Actions

### 1. Link TC-8021 to TC-8022 with "Depend"

Standard remediation linkage -- the new CVE Jira depends on the preemptive task for its fix.

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

This is the same link type used when triage-security creates remediation tasks in Step 8. The preemptive task is now linked to a proper CVE Jira as a standard remediation task.

### 2. Remove 'security-preemptive' label from TC-8022

The task is no longer preemptive -- it is now a standard remediation task linked to its own stream's CVE Jira.

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

### 3. Engineer Notification

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

### 4. Record Reconciliation

Remediation for stream 2.1.x is marked as **already reconciled**. Step 8 will skip task creation for this stream because TC-8022 already covers the required fix (bump tokio to 1.42.0).

## Link Topology After Reconciliation

```
TC-8020 (CVE Jira, stream rhtpa-2.2)
  |
  +-- Related --> TC-8022 (remediation task, rhtpa-2.1)
                    |
TC-8021 (CVE Jira, stream rhtpa-2.1)
  |
  +-- Depend --> TC-8022 (remediation task, rhtpa-2.1)
```

TC-8022 retains its "Related" link to TC-8020 (the originating CVE that triggered its creation) and now also has a "Depend" link from TC-8021 (the stream-specific CVE Jira it was created to remediate).
