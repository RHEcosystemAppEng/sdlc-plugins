# Step 4.4 -- Preemptive Task Reconciliation

## Search for Preemptive Tasks

### JQL Query

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

### Search Results

| Key | Summary | Status | Labels |
|-----|---------|--------|--------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |

TC-8022 has issue links:
- **Related**: TC-8020 (originating CVE Jira, stream [rhtpa-2.2])

## Stream Filtering

- Current issue stream (from TC-8021 summary suffix): **rhtpa-2.1**
- TC-8022 summary contains "(rhtpa-2.1)": **YES -- match confirmed**
- TC-8022 is a preemptive remediation task for the same CVE and the same stream

## Reconciliation Actions

A matching preemptive task was found. The following actions are taken per Step 4.4:

### Action (a): Link TC-8021 to TC-8022

Create a "Depend" link (standard remediation linkage) between the new CVE Jira and the preemptive task:

```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This establishes TC-8022 as the remediation task for TC-8021, using the same link type that would be used if a new remediation task were created in Step 8.

### Action (b): Remove 'security-preemptive' label from TC-8022

The preemptive task is now linked to a proper CVE Jira, so the `security-preemptive` label is no longer needed:

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed. The remaining labels (`ai-generated-jira`, `Security`, `CVE-2026-55123`) are preserved.

### Action (c): Inform the engineer

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

### Action (d): Record reconciliation

Reconciliation is recorded so that Step 8 skips remediation task creation for stream rhtpa-2.1. The preemptive task TC-8022 already contains the correct remediation instructions (bump tokio to 1.42.0) and is now properly linked to TC-8021.

## Provenance Chain

The full provenance chain for TC-8022:

1. **TC-8020** (CVE-2026-55123, stream [rhtpa-2.2]) -- original CVE Jira triaged first
2. During TC-8020's triage, Step 8 Case B detected cross-stream impact on stream rhtpa-2.1
3. **TC-8022** was created as a preemptive remediation task with `security-preemptive` label and "Related" link to TC-8020
4. **TC-8021** (CVE-2026-55123, stream [rhtpa-2.1]) -- current CVE Jira, arrived later
5. Step 4.4 reconciliation links TC-8021 to TC-8022 with "Depend" and removes the `security-preemptive` label
6. TC-8022 is now a standard remediation task linked to both TC-8020 (Related) and TC-8021 (Depend)
