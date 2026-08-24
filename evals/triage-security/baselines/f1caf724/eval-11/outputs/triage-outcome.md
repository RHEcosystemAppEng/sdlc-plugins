# Triage Outcome for TC-8021

## Summary

CVE-2026-55123 (tokio use-after-free, CVSS 8.1 High) was triaged for stream
rhtpa-2.1 (2.1.x). The triage found that a preemptive remediation task
(TC-8022) already exists for this CVE and stream, created during prior
cross-stream triage of TC-8020 (the same CVE scoped to stream rhtpa-2.2).
The preemptive task was reconciled into a standard remediation task -- no
new tasks were created.

## Triage Path

1. **Step 0 -- Configuration validated**: Project CLAUDE.md contains all
   required Security Configuration sections (Product Lifecycle, Version Streams,
   Source Repositories).

2. **Step 1 -- Data extracted**: CVE-2026-55123 affects tokio versions before
   1.42.0 (fixed in 1.42.0). Issue is scoped to stream 2.1.x via summary suffix
   `[rhtpa-2.1]`. Ecosystem: Cargo (source dependency).

3. **Step 2 -- Version impact analysis**: Stream 2.1.x versions (2.1.0 and
   2.1.1) use backend tags v0.3.8 and v0.3.12 respectively. Lock file
   inspection at these tags would determine the shipped tokio version. The
   PSIRT-claimed Affects Versions (RHTPA 2.1.0, RHTPA 2.1.1) indicate both
   versions are affected.

4. **Step 3 -- Affects Versions**: PSIRT-assigned Affects Versions (RHTPA 2.1.0,
   RHTPA 2.1.1) are scoped correctly to the 2.1.x stream. Correction would
   proceed based on lock file evidence from Step 2.

5. **Step 4 -- Duplicate, sibling, overlap, and reconciliation check**:
   - **Step 4.1 (same-stream duplicates)**: No same-stream duplicates found.
   - **Step 4.2 (cross-stream coordination)**: TC-8020 is a different-stream
     sibling (stream rhtpa-2.2). A "Related" link would be created between
     TC-8021 and TC-8020.
   - **Step 4.3 (cross-CVE overlap)**: Upstream Affected Component field
     (customfield_10632) is configured with value "tokio". Search for other
     CVEs affecting the same component in the same stream would proceed.
   - **Step 4.4 (preemptive task reconciliation)**: **This is the key step.**
     JQL search found TC-8022 as a preemptive task matching CVE-2026-55123
     for stream rhtpa-2.1.

6. **Step 4.4 reconciliation actions**:
   - Linked TC-8021 (new CVE Jira) to TC-8022 (preemptive task) with "Depend"
   - Removed `security-preemptive` label from TC-8022 (labels become:
     ai-generated-jira, Security, CVE-2026-55123)
   - Recorded that remediation already exists for stream 2.1.x

7. **Step 8 -- Remediation**: Skipped new task creation for stream 2.1.x because
   Step 4.4 reconciliation confirmed that TC-8022 already provides the required
   remediation (bump tokio to >= 1.42.0). TC-8022 is now a standard remediation
   task linked to TC-8021 via "Depend".

## Outcome

**No new remediation tasks created.** The existing preemptive task TC-8022
(originally created during triage of TC-8020 for stream rhtpa-2.2) was
reconciled into a standard remediation task for TC-8021.

### Final State

| Issue | Type | Status | Role |
|-------|------|--------|------|
| TC-8021 | Vulnerability | Assigned | CVE tracker for stream rhtpa-2.1 |
| TC-8022 | Task | Open | Remediation task (reconciled from preemptive) |
| TC-8020 | Vulnerability | (existing) | CVE tracker for stream rhtpa-2.2 (originating) |

### Final Links

| From | To | Link Type | Purpose |
|------|----|-----------|---------|
| TC-8021 | TC-8022 | Depend | Standard remediation linkage (new) |
| TC-8020 | TC-8022 | Related | Cross-stream origination (pre-existing) |
| TC-8021 | TC-8020 | Related | Cross-stream sibling (new, from Step 4.2) |

### Label Changes

| Issue | Before | After |
|-------|--------|-------|
| TC-8021 | CVE-2026-55123, pscomponent:org/rhtpa-server | CVE-2026-55123, pscomponent:org/rhtpa-server, ai-cve-triaged |
| TC-8022 | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | ai-generated-jira, Security, CVE-2026-55123 |

### Why No New Tasks Were Created

The preemptive task reconciliation mechanism (Step 4.4) is designed to prevent
duplicate remediation tasks when PSIRT creates a stream-specific CVE Jira
after cross-stream analysis has already created proactive tasks. The workflow:

1. TC-8020 (CVE for rhtpa-2.2) was triaged first
2. Cross-stream analysis (Step 8 Case A) detected that stream rhtpa-2.1 was
   also affected but had no CVE Jira
3. TC-8022 was created as a preemptive task with `security-preemptive` label,
   linked to TC-8020 via "Related"
4. Later, PSIRT created TC-8021 (CVE for rhtpa-2.1)
5. During triage of TC-8021, Step 4.4 found TC-8022, linked it with "Depend",
   and removed the `security-preemptive` label
6. Step 8 skipped task creation because remediation already exists

This ensures continuity of work -- any progress already made on TC-8022 is
preserved, and the task is now properly linked to its own stream's CVE Jira.
