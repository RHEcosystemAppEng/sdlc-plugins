# Step 4.4 -- Preemptive Task Reconciliation for TC-8021

## Context

TC-8021 is a stream-scoped Vulnerability issue for CVE-2026-55123 (tokio
use-after-free) scoped to stream **rhtpa-2.1** (2.1.x). A prior triage of
TC-8020 (the same CVE for stream **rhtpa-2.2**) already performed cross-stream
impact analysis (Step 8 Case A) and created a preemptive remediation task for
stream rhtpa-2.1, since that stream lacked its own CVE Jira at the time.

## JQL Search

Per Step 4.4, the following JQL query is executed to search for preemptive
tasks matching this CVE:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

**Result**: TC-8022

## Matching Preemptive Task Found

| Field | Value |
|-------|-------|
| Key | TC-8022 |
| Summary | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) |
| Status | Open |
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |
| Issue Links | Related: TC-8020 (originating CVE Jira, stream rhtpa-2.2) |

## Stream Matching

The preemptive task summary contains `(rhtpa-2.1)`, which matches the current
issue's stream suffix `[rhtpa-2.1]` (stream 2.1.x). This confirms TC-8022
is a preemptive remediation task for the same CVE and the same stream as
TC-8021.

## Reconciliation Actions

Per Step 4.4 of the triage-security skill, when a matching preemptive task is
found, the following reconciliation actions are performed:

### a. Link the new CVE Jira to the preemptive task with "Depend"

```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This establishes the standard remediation linkage between the CVE Vulnerability
issue (TC-8021) and its remediation task (TC-8022), replacing the previous
"Related" link that connected TC-8022 to the originating cross-stream CVE
(TC-8020).

### b. Remove the `security-preemptive` label from TC-8022

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

Removing the `security-preemptive` label converts TC-8022 from a proactive
preemptive task into a standard remediation task now that it has a proper CVE
Jira (TC-8021) linked with the "Depend" relationship.

### c. Inform the engineer

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (stream rhtpa-2.2, linked via
"Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

### d. Record the reconciliation

Remediation for stream 2.1.x is marked as already existing. Step 8 will skip
task creation for this stream because TC-8022 already covers the required
remediation (bump tokio to >= 1.42.0 in the backend source repo on branch
release/0.3.z, then propagate to the Konflux release repo rhtpa-release.0.3.z).

## Link Landscape After Reconciliation

| Issue | Type | Linked To | Link Type | Notes |
|-------|------|-----------|-----------|-------|
| TC-8021 | Vulnerability (rhtpa-2.1) | TC-8022 | Depend | New link -- standard remediation |
| TC-8022 | Task (rhtpa-2.1) | TC-8020 | Related | Pre-existing link -- originating CVE |
| TC-8022 | Task (rhtpa-2.1) | TC-8021 | Depend | New link -- proper CVE for this stream |
| TC-8020 | Vulnerability (rhtpa-2.2) | TC-8022 | Related | Pre-existing link -- cross-stream |
