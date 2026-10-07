# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## Context

TC-8021 is a new CVE Vulnerability issue for CVE-2026-55123 (tokio use-after-free),
scoped to stream `rhtpa-2.1` (2.1.x). A prior triage of TC-8020 (stream `rhtpa-2.2`)
identified cross-stream impact on stream 2.1.x and proactively created a preemptive
remediation task TC-8022 for the 2.1.x stream (Step 8 Case A).

Now that PSIRT has created a stream-specific CVE Jira (TC-8021) for stream rhtpa-2.1,
Step 4.4 reconciliation detects and absorbs the preemptive task.

## Step 4.4 Procedure

### 4.4.1 -- Search for preemptive tasks

JQL query:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

**Result**: 1 match found.

| Key | Summary | Status | Labels | Issue Links |
|-----|---------|--------|--------|-------------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related: TC-8020 |

### 4.4.2 -- Filter by stream

TC-8022's summary contains `(rhtpa-2.1)`, which matches the current issue's stream
suffix `[rhtpa-2.1]` (stream 2.1.x). This is a matching preemptive task.

### 4.4.3 -- Matching preemptive task found: reconciliation actions

Per Step 4.4 item 3, the following actions are performed:

**a. Link the new CVE Jira to the preemptive task with "Depend":**

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

This converts the relationship from "Related" (preemptive, cross-stream) to "Depend"
(standard remediation linkage). TC-8021 now depends on TC-8022 for remediation,
the same as any standard remediation task linked to its CVE Jira.

**b. Remove the `security-preemptive` label from TC-8022:**

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because TC-8022 is now linked to a proper
CVE Jira (TC-8021) via "Depend". It is no longer a preemptive task -- it is a standard
remediation task.

**c. Inform the engineer:**

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

**d. Record the reconciliation:**

Stream 2.1.x is marked as having existing remediation (TC-8022). Step 8 will skip
task creation for this stream.

## Link Topology After Reconciliation

```
TC-8020 (CVE Jira, stream rhtpa-2.2)
  |
  +-- Related --> TC-8022 (remediation task, stream rhtpa-2.1) [original link preserved]
                    |
TC-8021 (CVE Jira, stream rhtpa-2.1)
  |
  +-- Depend --> TC-8022 (remediation task, stream rhtpa-2.1) [new link from reconciliation]
```

TC-8022 now has two inbound links:
- **Related** from TC-8020 (the originating cross-stream CVE) -- created during Case A
- **Depend** from TC-8021 (the stream-specific CVE) -- created during reconciliation

The "Related" link to TC-8020 is preserved for traceability (it records why the task
was originally created). The "Depend" link to TC-8021 is the standard remediation
linkage that signals TC-8021's fix depends on TC-8022's completion.
