# Step 4.4 -- Preemptive Task Reconciliation Analysis

## Context

TC-8021 is a Vulnerability issue for CVE-2026-55123 (tokio use-after-free) scoped to stream [rhtpa-2.1]. A prior triage of TC-8020 (CVE-2026-55123 for stream [rhtpa-2.2]) performed a cross-stream impact analysis (Step 7 Case B) and identified that stream 2.1.x was also affected. Since no CVE Jira existed for stream 2.1.x at that time, a preemptive remediation task TC-8022 was created.

Now, PSIRT has created TC-8021 -- the stream-specific CVE Jira for 2.1.x. Step 4.4 must reconcile the preemptive task with this new CVE Jira.

## Step 4.4 Procedure

### 4.4.1 -- Search for preemptive tasks

JQL query:
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

**Result**: 1 issue found.

| Key | Summary | Status | Labels |
|-----|---------|--------|--------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |

### 4.4.2 -- Filter by stream

The current issue (TC-8021) has stream suffix `[rhtpa-2.1]`, which maps to stream 2.1.x.

TC-8022's summary contains `(rhtpa-2.1)`, which matches the current issue's stream scope.

**Match confirmed**: TC-8022 is a preemptive remediation task for the same CVE and the same stream as TC-8021.

### 4.4.3 -- Verify originating issue linkage

TC-8022 has an existing "Related" link to TC-8020 (the originating CVE Jira from stream [rhtpa-2.2]). This confirms TC-8022 was created as a preemptive task during TC-8020's triage.

### 4.4.4 -- Reconciliation actions

Per the Step 4.4 procedure, the following actions are required:

#### a. Link the new CVE Jira to the preemptive task with "Depend"

```
jira.create_link(
  inwardIssue: TC-8021,    # the new stream-specific CVE Jira
  outwardIssue: TC-8022,   # the preemptive remediation task
  type: "Depend"
)
```

This creates the standard remediation linkage between the CVE Jira and its remediation task, replacing the weaker "Related" linkage pattern used for preemptive tasks.

#### b. Remove the `security-preemptive` label from TC-8022

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because the task is no longer preemptive -- it is now linked to a proper CVE Jira (TC-8021) via "Depend" and functions as a standard remediation task.

#### c. Inform the engineer

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (stream [rhtpa-2.2]),
linked via "Related".

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 7.
```

#### d. Record the reconciliation

The reconciliation is recorded so that Step 7 knows remediation already exists for the 2.1.x stream and skips new task creation.

- Stream 2.1.x: remediation covered by TC-8022 (reconciled preemptive task)
- No new remediation tasks needed for this stream

## Link State After Reconciliation

| From | To | Link Type | Notes |
|------|----|-----------|-------|
| TC-8020 | TC-8022 | Related | Original preemptive linkage (unchanged) |
| TC-8021 | TC-8022 | Depend | New standard remediation linkage (added by reconciliation) |

TC-8022 is now linked to both the originating CVE (TC-8020, via Related) and the stream-specific CVE (TC-8021, via Depend). The Depend link to TC-8021 is the authoritative remediation linkage.

## Label State After Reconciliation

| Task | Before | After |
|------|--------|-------|
| TC-8022 | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | ai-generated-jira, Security, CVE-2026-55123 |

The `security-preemptive` label is removed, converting TC-8022 from a preemptive task to a standard remediation task.
