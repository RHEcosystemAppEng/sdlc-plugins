# Triage Outcome -- TC-8021

## Summary

TC-8021 (CVE-2026-55123 tokio use-after-free, stream `[rhtpa-2.1]`) was triaged
with an existing preemptive remediation task (TC-8022) successfully reconciled.
**No new remediation tasks were created** because Step 4.4 linked the existing
preemptive task.

## How the Existing Preemptive Task Was Reconciled

### Background

TC-8020 was the first CVE Jira created for CVE-2026-55123, scoped to stream
`[rhtpa-2.2]`. During its triage, Step 7 Case B (cross-stream impact) detected
that stream 2.1.x was also affected by the tokio vulnerability but had no CVE
Jira yet. The triage proactively created TC-8022 as a preemptive remediation
task for stream rhtpa-2.1 with:
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
- Link: "Related" to TC-8020 (the originating CVE Jira)

Later, PSIRT created TC-8021 as the official CVE Jira for stream `[rhtpa-2.1]`.

### Reconciliation During TC-8021 Triage

When TC-8021 was triaged, Step 4.4 performed preemptive task reconciliation:

1. **JQL search** for tasks with labels `security-preemptive` AND `CVE-2026-55123`
   returned TC-8022.

2. **Stream filtering** confirmed TC-8022's summary contains `(rhtpa-2.1)`,
   matching the current issue's stream suffix `[rhtpa-2.1]`.

3. **Reconciliation actions**:
   - Created a "Depend" link from TC-8021 (CVE Jira) to TC-8022 (remediation task),
     establishing standard remediation linkage.
   - Removed the `security-preemptive` label from TC-8022, converting it from a
     preemptive task into a standard remediation task.
   - TC-8022's existing "Related" link to TC-8020 remains intact, preserving
     cross-stream provenance.

4. **Step 7 was skipped** for remediation task creation. Because Step 4.4 already
   linked an existing remediation task (TC-8022) for this stream, Step 7 did not
   create new upstream backport or downstream propagation tasks. The reconciled
   TC-8022 serves as the remediation task for TC-8021.

## Final State of Jira Issues

### TC-8021 (CVE Vulnerability Issue -- stream rhtpa-2.1)
- **Status**: New (pending remediation)
- **Labels**: CVE-2026-55123, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Affects Versions**: RHTPA 2.1.0, RHTPA 2.1.1
- **Issue Links**:
  - Depend -> TC-8022 (remediation task, reconciled from preemptive)

### TC-8022 (Remediation Task -- reconciled)
- **Status**: Open
- **Labels**: ai-generated-jira, Security, CVE-2026-55123 (security-preemptive removed)
- **Issue Links**:
  - Related -> TC-8020 (originating CVE Jira from stream rhtpa-2.2)
  - Depend <- TC-8021 (newly linked CVE Jira for stream rhtpa-2.1)

### TC-8020 (Original CVE Jira -- stream rhtpa-2.2)
- Unchanged by this triage. Retains its existing links and status.

## Key Decision Points

| Step | Decision | Rationale |
|------|----------|-----------|
| Step 1 | Stream scoped to 2.1.x | Summary suffix `[rhtpa-2.1]` maps to 2.1.x stream |
| Step 4.4 | Reconcile TC-8022 | JQL found preemptive task matching CVE and stream |
| Step 4.4 | Link with "Depend" | Standard remediation linkage (same as new task creation) |
| Step 4.4 | Remove security-preemptive label | Task now linked to proper CVE Jira |
| Step 7 | Skip task creation | Remediation already exists via reconciled TC-8022 |
