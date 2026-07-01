# Triage Outcome -- TC-8021 (CVE-2026-55123, tokio, stream rhtpa-2.1)

## Summary

Triage of TC-8021 identified an existing preemptive remediation task (TC-8022) that was created during a prior cross-stream triage of TC-8020 (stream rhtpa-2.2). The Step 4.4 preemptive task reconciliation protocol was applied to link and normalize this task.

## Step 4.4 Reconciliation -- How the Preemptive Task Was Handled

### Background

When TC-8020 (CVE-2026-55123, stream [rhtpa-2.2]) was triaged previously, the cross-stream version impact analysis (Step 8 Case B) detected that stream rhtpa-2.1 was also affected but had no CVE Jira. A proactive preemptive remediation task TC-8022 was created with:
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
- Link: "Related" to TC-8020 (originating CVE, different stream)

### Detection

During triage of TC-8021, Step 4.4 searched for preemptive tasks:

```
JQL: project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

This returned TC-8022. The task summary contains `(rhtpa-2.1)` which matches the current issue's stream suffix `[rhtpa-2.1]`.

### Reconciliation Actions (proposed)

The following actions are proposed for engineer confirmation:

1. **Link TC-8021 to TC-8022 with "Depend"** -- establishes standard remediation linkage between the CVE Jira and the remediation task.
   ```
   jira.create_link(
     inwardIssue: "TC-8021",
     outwardIssue: "TC-8022",
     type: "Depend"
   )
   ```

2. **Remove `security-preemptive` label from TC-8022** -- the task is no longer preemptive; it is now a standard remediation task linked to a proper CVE Jira.
   ```
   jira.edit_issue("TC-8022", fields={
     "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
   })
   ```

3. **Skip Step 8 remediation task creation** -- because Step 4.4 reconciliation already linked an existing remediation task for this stream, Step 8 does not create new remediation tasks. The preemptive task TC-8022 already covers the required work (bump tokio to >= 1.42.0 in the rhtpa-2.1 stream).

### Rationale

The reconciliation converts the preemptive task into a standard remediation task:
- Before: TC-8022 was linked to TC-8020 via "Related" (cross-stream reference) and carried the `security-preemptive` label
- After: TC-8022 is linked to TC-8021 via "Depend" (standard remediation linkage), the `security-preemptive` label is removed, and the existing "Related" link to TC-8020 remains for cross-stream traceability

## Step 8 -- Remediation

**Skipped.** Step 4.4 reconciliation already linked existing preemptive remediation task TC-8022 to TC-8021. No new remediation tasks are created for stream rhtpa-2.1.

The existing task TC-8022 already describes the required remediation:
- Bump tokio to >= 1.42.0 in the backend repository (stream rhtpa-2.1)
- Task was created with the correct stream scope, labels, and acceptance criteria

## Post-Triage Summary

Proposed post-triage actions:

1. **Add `ai-cve-triaged` label** to TC-8021 to mark it as triaged
2. **Post summary comment** to TC-8021 documenting:
   - CVE-2026-55123 affects tokio < 1.42.0
   - Stream rhtpa-2.1 versions (RHTPA 2.1.0, RHTPA 2.1.1) are affected
   - Preemptive remediation task TC-8022 was reconciled (linked via Depend, security-preemptive label removed)
   - No new remediation tasks created -- TC-8022 covers the fix
   - Comment includes the Comment Footnote per skill requirements
3. **Transition** TC-8021 to In Progress (if confirmed by engineer)

## Important Notes

- All actions above are **proposed** and require engineer confirmation before execution. No Jira mutations have been performed.
- The reconciliation approach follows the guardrail that every Jira mutation requires explicit approval.
- TC-8022's "Related" link to TC-8020 remains intact -- it provides cross-stream traceability alongside the new "Depend" link to TC-8021.
