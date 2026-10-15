# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## Search for Preemptive Tasks

### JQL Query

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

### Search Results

| Task Key | Summary | Status | Labels | Issue Links |
|----------|---------|--------|--------|-------------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related: TC-8020 |

## Stream Matching

- Current issue stream suffix: `[rhtpa-2.1]`
- TC-8022 summary contains: `(rhtpa-2.1)`
- **Match confirmed**: TC-8022 is a preemptive remediation task for the same CVE and the same stream as TC-8021.

## Preemptive Task Origin

TC-8022 was created proactively during the triage of TC-8020 (CVE-2026-55123 for stream `[rhtpa-2.2]`). When TC-8020 was triaged, Step 8 Case A cross-stream impact analysis identified that stream 2.1.x was also affected but had no stream-specific CVE Jira at the time. A preemptive remediation task (TC-8022) was created with the `security-preemptive` label and linked to TC-8020 via "Related".

Now that PSIRT has created TC-8021 as the stream-specific CVE Jira for `[rhtpa-2.1]`, the preemptive task must be reconciled.

## Proposed Reconciliation Actions

### Action 1: Link TC-8021 to TC-8022 with "Depend"

Create a standard remediation linkage between the new CVE Jira and the existing preemptive task:

```
jira.create_link(
  inwardIssue: "TC-8021",    # current CVE Jira (rhtpa-2.1)
  outwardIssue: "TC-8022",   # preemptive remediation task
  type: "Depend"
)
```

This converts the preemptive "Related" linkage into the standard "Depend" remediation linkage pattern, establishing TC-8022 as the remediation task for TC-8021.

### Action 2: Remove `security-preemptive` label from TC-8022

The `security-preemptive` label is no longer applicable because TC-8022 is now linked to a proper CVE Jira (TC-8021):

```
jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

Current labels: `ai-generated-jira, Security, CVE-2026-55123, security-preemptive`
Updated labels: `ai-generated-jira, Security, CVE-2026-55123`

### Action 3: Record reconciliation -- skip Step 8 task creation

Remediation already exists for stream 2.1.x via TC-8022. Step 8 will skip new remediation task creation for this stream.

## Reconciliation Summary

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (stream [rhtpa-2.2]),
linked via "Related".

Proposed actions:
- Link TC-8021 -> TC-8022 with "Depend"
- Remove "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

## Link Topology After Reconciliation

```
TC-8020 (CVE Jira, rhtpa-2.2)
  |-- Related --> TC-8022 (remediation task, rhtpa-2.1) [existing link, retained]

TC-8021 (CVE Jira, rhtpa-2.1)
  |-- Depend --> TC-8022 (remediation task, rhtpa-2.1) [new link from reconciliation]
```

TC-8022 is now linked to both its originating CVE (TC-8020 via "Related", from the original cross-stream triage) and the stream-specific CVE (TC-8021 via "Depend", from this reconciliation).
