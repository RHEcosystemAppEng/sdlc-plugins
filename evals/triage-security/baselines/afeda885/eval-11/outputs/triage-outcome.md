# Triage Outcome: TC-8021

## Summary

TC-8021 (CVE-2026-55123: tokio use-after-free, stream [rhtpa-2.1]) was triaged with **preemptive task reconciliation**. An existing preemptive remediation task (TC-8022) was found and reconciled, eliminating the need to create new remediation tasks.

## How the Existing Preemptive Task Was Reconciled

### Background

1. **TC-8020** was the first CVE Jira created by PSIRT for CVE-2026-55123, scoped to stream [rhtpa-2.2].
2. During TC-8020's triage, Step 7 Case B (cross-stream impact) identified that stream 2.1.x was also affected by the vulnerable tokio version.
3. Since no CVE Jira existed for stream 2.1.x at that time, a **preemptive remediation task TC-8022** was created with:
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
   - Link: "Related" to TC-8020 (the originating CVE Jira)
   - Summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)"

### Reconciliation Trigger

PSIRT subsequently created TC-8021 -- the stream-specific CVE Jira for [rhtpa-2.1]. When TC-8021 was triaged, Step 4.4 (Preemptive Task Reconciliation) detected the existing preemptive task.

### Reconciliation Actions

Step 4.4 performed the following reconciliation:

1. **JQL search** for preemptive tasks: `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123'` returned TC-8022.
2. **Stream match confirmed**: TC-8022's summary contains `(rhtpa-2.1)`, matching TC-8021's stream suffix `[rhtpa-2.1]`.
3. **Linked TC-8021 to TC-8022** with link type "Depend" -- this is the standard remediation linkage, converting the preemptive relationship into a proper CVE-to-remediation dependency.
4. **Removed the `security-preemptive` label** from TC-8022 -- the task is no longer preemptive because it now has a proper CVE Jira owner.
5. **Recorded the reconciliation** so Step 7 skips new task creation for the 2.1.x stream.

### Effect on Step 7

Because Step 4.4 recorded that remediation for stream 2.1.x already exists (via reconciled TC-8022), Step 7 does not create new remediation tasks. The triage outcome is:

- **No new tasks created** -- TC-8022 already covers the remediation (bump tokio to >= 1.42.0 on stream 2.1.x)
- **TC-8022 is now a standard remediation task** -- linked to TC-8021 via "Depend", with the `security-preemptive` label removed

## Final Issue State

### TC-8021 (Vulnerability)
- Status: Transitioned to In Progress
- Labels: CVE-2026-55123, pscomponent:org/rhtpa-server, ai-cve-triaged
- Affects Versions: RHTPA 2.1.0, RHTPA 2.1.1 (confirmed correct per PSIRT assignment)
- Issue Links:
  - Depend: TC-8022 (remediation task -- reconciled from preemptive)

### TC-8022 (Task -- reconciled)
- Status: Open (unchanged)
- Labels: ai-generated-jira, Security, CVE-2026-55123 (security-preemptive removed)
- Issue Links:
  - Related: TC-8020 (originating CVE from stream [rhtpa-2.2] -- unchanged)
  - Depend: TC-8021 (new stream-specific CVE Jira -- added by reconciliation)

### TC-8020 (Vulnerability -- originating issue, unchanged)
- Issue Links:
  - Related: TC-8022 (preemptive task created during its triage -- unchanged)

## Post-Triage Summary Comment

The following summary comment would be posted to TC-8021:

```
Triage complete for CVE-2026-55123 (tokio use-after-free).

Version impact (stream 2.1.x):
| Version | tokio | Affected? |
|---------|-------|-----------|
| 2.1.0   | < 1.42.0 | YES |
| 2.1.1   | < 1.42.0 | YES |

Affects Versions: RHTPA 2.1.0, RHTPA 2.1.1 (confirmed correct, no correction needed).

Preemptive task reconciliation: existing remediation task TC-8022 (created
from cross-stream analysis of TC-8020, stream [rhtpa-2.2]) was found and
reconciled:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

No new remediation tasks created -- TC-8022 covers the fix for this stream.

@<reporter> (PSIRT analyst)
```

## Key Design Points of Reconciliation

1. **No duplicate work**: The preemptive task mechanism ensures remediation starts early (during the first stream's triage), and reconciliation ensures no duplicate tasks are created when PSIRT catches up with stream-specific CVE Jiras.
2. **Link type upgrade**: The "Related" link (weak, informational) is supplemented by a "Depend" link (strong, dependency-tracking) to the proper stream-specific CVE Jira. The original "Related" link to the originating CVE is preserved for audit trail.
3. **Label lifecycle**: The `security-preemptive` label serves as a marker for tasks awaiting reconciliation. Once a proper CVE Jira exists and the Depend link is established, the label is removed. This allows JQL queries to distinguish between preemptive tasks still awaiting reconciliation and tasks that have been properly assigned to a CVE Jira.
