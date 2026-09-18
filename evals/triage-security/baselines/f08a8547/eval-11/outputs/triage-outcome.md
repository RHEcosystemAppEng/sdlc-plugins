# Triage Outcome: TC-8021

## Summary

**Issue:** TC-8021 -- CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1]
**CVE:** CVE-2026-55123
**Library:** tokio (Cargo/Rust crate)
**Fix threshold:** >= 1.42.0
**Stream scope:** 2.1.x (scoped issue)
**CVSS:** 8.1 (High)

## Preemptive Task Reconciliation Result

The triage for TC-8021 was resolved through Step 4.4 preemptive task reconciliation. No new remediation tasks were created.

### What Happened

1. **Prior triage of TC-8020** (CVE-2026-55123 for stream rhtpa-2.2) had already identified that stream 2.1.x was also affected by the same vulnerability through its Case A cross-stream impact analysis.

2. **Preemptive task TC-8022** was created during that prior triage as a proactive remediation task for stream rhtpa-2.1. It carried the `security-preemptive` label and was linked to TC-8020 (the rhtpa-2.2 CVE Jira) with a "Related" link.

3. **When TC-8021 arrived** (PSIRT created the stream-specific CVE Jira for rhtpa-2.1), Step 4.4 searched for preemptive tasks matching CVE-2026-55123 and found TC-8022.

4. **Reconciliation** converted TC-8022 from a preemptive task to a standard remediation task:
   - Created a "Depend" link from TC-8021 to TC-8022 (standard remediation linkage)
   - Removed the `security-preemptive` label from TC-8022
   - Preserved the existing "Related" link from TC-8022 to TC-8020 for cross-stream traceability

### Why No New Tasks Were Created

Step 8 (Remediation, Case B) was skipped for stream 2.1.x because the reconciliation in Step 4.4 confirmed that TC-8022 already covers the required remediation:
- TC-8022's summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)"
- This matches the fix threshold (tokio >= 1.42.0) and the correct stream (rhtpa-2.1)
- Creating additional tasks would be duplicative

## Triage Actions Summary

| Step | Action | Result |
|------|--------|--------|
| 0 | Validate Configuration | Passed -- Security Configuration found in CLAUDE.md |
| 1 | Data Extraction | CVE-2026-55123, tokio, affected < 1.42.0, fixed 1.42.0, Cargo ecosystem |
| 1 | Stream Scope Resolution | [rhtpa-2.1] mapped to stream 2.1.x |
| 4.4 | Preemptive Task Search | Found TC-8022 (preemptive task for rhtpa-2.1, created from TC-8020 triage) |
| 4.4 | Link CVE to Preemptive Task | Created "Depend" link: TC-8021 -> TC-8022 |
| 4.4 | Remove Preemptive Label | Removed `security-preemptive` from TC-8022 |
| 4.4 | Record Reconciliation | Marked stream 2.1.x as having existing remediation |
| 8 | Remediation | Skipped -- preemptive task TC-8022 already covers stream 2.1.x |

## Final Issue State

### TC-8021 (CVE Jira for rhtpa-2.1)
- **Status:** Assigned (transitioned from New in Step 0.7)
- **Labels:** CVE-2026-55123, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Issue Links:**
  - Depend: TC-8022 (remediation task, formerly preemptive)

### TC-8022 (Reconciled Remediation Task)
- **Status:** Open (unchanged)
- **Labels:** ai-generated-jira, Security, CVE-2026-55123 (`security-preemptive` removed)
- **Issue Links:**
  - Related: TC-8020 (originating CVE Jira from stream rhtpa-2.2)
  - Depend: TC-8021 (newly linked CVE Jira for stream rhtpa-2.1)

## Key Design Points

The preemptive task reconciliation mechanism (Step 4.4) ensures that:

1. **No duplicate tasks** are created when PSIRT creates per-stream CVE Jiras after cross-stream proactive tasks already exist
2. **Traceability is maintained** -- both the originating CVE (TC-8020, rhtpa-2.2) and the stream-specific CVE (TC-8021, rhtpa-2.1) are linked to the remediation task
3. **Label hygiene** is enforced -- the `security-preemptive` label is removed once the task has a proper CVE Jira owner, preventing it from appearing in future reconciliation searches for unlinked preemptive tasks
4. **Existing work is preserved** -- if TC-8022 was already in progress or had PRs attached, none of that work is lost by the reconciliation
