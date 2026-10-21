# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## Search for Preemptive Tasks

**JQL query executed:**

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

**Result:** 1 match found.

| Task Key | Summary | Status | Labels | Issue Links |
|----------|---------|--------|--------|-------------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related: TC-8020 |

## Stream Filtering

- Current issue stream (from Step 1): **rhtpa-2.1** (stream 2.1.x)
- TC-8022 summary contains `(rhtpa-2.1)` -- **matches** the current issue's stream
- Conclusion: TC-8022 is the preemptive remediation task for this CVE and stream

## Preemptive Task Origin

TC-8022 was created during triage of **TC-8020** (CVE-2026-55123, stream `[rhtpa-2.2]`). When TC-8020 was triaged, Step 8 Case A (cross-stream impact) detected that stream 2.1.x was also affected but had no CVE Jira of its own. A preemptive remediation task (TC-8022) was created with the `security-preemptive` label and linked to TC-8020 via "Related".

Now that TC-8021 has been created by PSIRT as the proper CVE Jira for stream `[rhtpa-2.1]`, the preemptive task must be reconciled.

## Reconciliation Actions

Per Step 4.4 of the triage-security skill, the following actions are performed:

### Action 1: Link CVE Jira to Preemptive Task (Depend)

Create a "Depend" link from the current CVE Jira to the preemptive task, establishing standard remediation linkage:

```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This converts the relationship from informal (preemptive task linked to originating CVE via "Related") to standard (remediation task linked to its own CVE Jira via "Depend").

### Action 2: Remove `security-preemptive` Label

Remove the `security-preemptive` label from TC-8022 since it is now linked to a proper CVE Jira:

```
current_labels = [ai-generated-jira, Security, CVE-2026-55123, security-preemptive]
updated_labels = [ai-generated-jira, Security, CVE-2026-55123]

jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

### Action 3: Record Reconciliation

Mark that remediation already exists for stream 2.1.x. This record prevents Step 8 from creating duplicate remediation tasks for this stream.

## Engineer Notification

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

## Impact on Later Steps

- **Step 8 (Remediation):** Task creation is **skipped** for stream 2.1.x because reconciliation has recorded that remediation already exists via TC-8022. No new upstream backport or downstream propagation tasks will be created.
- **Post-Triage Summary:** The summary comment will reference TC-8022 as the reconciled remediation task, noting that it was originally a preemptive task from TC-8020's cross-stream analysis.
- **Release Jira Linking (Step 7.5):** If a release Task exists for the 2.1.x stream, TC-8022 should still be linked to it (Blocks) and TC-8021 should be linked (Related), following standard post-creation release linking procedures.
