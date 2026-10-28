# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## Search for Preemptive Tasks

**JQL executed (simulated):**

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

**Result:** 1 match found.

## Matching Preemptive Task

| Field | Value |
|-------|-------|
| Key | TC-8022 |
| Summary | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) |
| Status | Open |
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |
| Issue Links | Related: TC-8020 (originating CVE Jira, stream [rhtpa-2.2]) |

## Stream Match Verification

- Current issue stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- Preemptive task summary contains: `(rhtpa-2.1)` -- **match confirmed**
- The preemptive task TC-8022 was created for stream rhtpa-2.1 during prior triage of TC-8020 (stream rhtpa-2.2, Case A cross-stream impact analysis)

## Reconciliation Actions

A matching preemptive task (TC-8022) was found for this CVE and stream. The following reconciliation actions are performed:

### Action 1: Create Depend Link

Link the new CVE Jira (TC-8021) to the preemptive task (TC-8022) with "Depend" link type (standard remediation linkage):

```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This establishes TC-8022 as the remediation task for TC-8021, using the same link topology as standard triage-created remediation tasks.

### Action 2: Remove security-preemptive Label

Remove the `security-preemptive` label from TC-8022, since it is now linked to a proper CVE Jira (TC-8021):

```
Current labels: [ai-generated-jira, Security, CVE-2026-55123, security-preemptive]
Updated labels: [ai-generated-jira, Security, CVE-2026-55123]

jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because TC-8022 is no longer preemptive -- it is now a standard remediation task linked to its own CVE Jira via Depend.

### Reconciliation Record

- **Remediation already exists for stream 2.1.x** -- Step 8 will skip new remediation task creation for this stream.
- TC-8022 transitions from a preemptive task (linked via "Related" to TC-8020) to a standard remediation task (linked via "Depend" to TC-8021).
- The "Related" link between TC-8022 and TC-8020 is retained -- it records the provenance (which cross-stream triage originally created the task).

## Link Topology After Reconciliation

```
TC-8020 (CVE Jira, stream rhtpa-2.2)
  |
  +-- Related --> TC-8022 (remediation task for rhtpa-2.1, provenance link)
                    ^
                    |
TC-8021 (CVE Jira, stream rhtpa-2.1)
  |
  +-- Depend ---> TC-8022 (remediation task for rhtpa-2.1, standard linkage)
```
