# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## Context

TC-8021 is a PSIRT-created Vulnerability issue for CVE-2026-55123 (tokio use-after-free) scoped to stream rhtpa-2.1. A prior triage of TC-8020 (the same CVE for stream rhtpa-2.2) identified cross-stream impact on rhtpa-2.1 and proactively created a remediation task TC-8022 via Step 8 Case B.

## Step 4.4 Procedure

### 4.4.1 -- Search for preemptive tasks

JQL query:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

**Result**: 1 task returned.

| Key | Summary | Status | Labels |
|-----|---------|--------|--------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |

### 4.4.2 -- Filter to current stream

TC-8022 summary contains `(rhtpa-2.1)` which matches the current issue's stream suffix `[rhtpa-2.1]`.

**Match confirmed**: TC-8022 is a preemptive remediation task for this CVE and this stream.

### 4.4.3 -- Matching preemptive task found -- reconciliation actions

Per Step 4.4 item 3, the following actions are performed:

#### a. Link the new CVE Jira to the preemptive task with "Depend"

```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This establishes the standard remediation linkage between the CVE Vulnerability issue (TC-8021) and its remediation task (TC-8022), identical to the link that would have been created if the task were generated fresh in Step 8 Case A.

#### b. Remove the `security-preemptive` label from TC-8022

Current labels on TC-8022: `ai-generated-jira, Security, CVE-2026-55123, security-preemptive`

Updated labels (removing `security-preemptive`):

```
jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because TC-8022 is now linked to a proper stream-specific CVE Jira (TC-8021). It is no longer a preemptive task -- it is a standard remediation task.

#### c. Inform the engineer

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

#### d. Record the reconciliation

Remediation already exists for stream rhtpa-2.1 via TC-8022. Step 8 will skip task creation for this stream.

## Issue Link State After Reconciliation

TC-8022 now has the following links:

| Link Type | Direction | Linked Issue | Purpose |
|-----------|-----------|-------------|---------|
| Related | TC-8022 <-> TC-8020 | Originating CVE Jira (stream rhtpa-2.2) | Cross-stream provenance (from original Case B creation) |
| Depend | TC-8021 -> TC-8022 | Current CVE Jira (stream rhtpa-2.1) | Standard remediation linkage (from reconciliation) |

## Label State After Reconciliation

| Label | Before | After | Reason |
|-------|--------|-------|--------|
| ai-generated-jira | Present | Present | Retained -- standard label for AI-generated tasks |
| Security | Present | Present | Retained -- security-related task |
| CVE-2026-55123 | Present | Present | Retained -- CVE traceability |
| security-preemptive | Present | **Removed** | Task is now linked to a proper CVE Jira; no longer preemptive |
