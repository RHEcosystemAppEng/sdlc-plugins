# Triage Outcome: TC-8021 (CVE-2026-55123)

## Summary

TC-8021 is a Vulnerability issue for CVE-2026-55123 (tokio use-after-free, versions before 1.42.0) scoped to stream rhtpa-2.1. Triage determined that a preemptive remediation task (TC-8022) already exists for this CVE and stream, created during a prior cross-stream triage of TC-8020 (stream rhtpa-2.2). The preemptive task was reconciled into a standard remediation task -- no new tasks were created.

## Triage Decision: Reconciled with Existing Preemptive Task

### What happened

1. **Data Extraction (Step 1)**: Parsed TC-8021 and identified CVE-2026-55123 affecting the tokio crate (versions before 1.42.0, fixed in 1.42.0). The issue is scoped to stream 2.1.x via the `[rhtpa-2.1]` suffix. Ecosystem is Cargo.

2. **Version Impact Analysis (Step 2)**: The 2.1.x stream's supportability matrix shows two versions:
   - RHTPA 2.1.0 (tag v0.3.8): tokio version would be checked via `git show v0.3.8:Cargo.lock`
   - RHTPA 2.1.1 (tag v0.3.12): tokio version would be checked via `git show v0.3.12:Cargo.lock`
   
   Both versions in the 2.1.x stream are expected to ship tokio < 1.42.0 (affected), consistent with PSIRT's Affects Versions assignment of RHTPA 2.1.0 and RHTPA 2.1.1.

3. **Preemptive Task Reconciliation (Step 4.4)**: A JQL search for tasks with labels `security-preemptive` and `CVE-2026-55123` returned TC-8022, a preemptive remediation task for rhtpa-2.1 created from prior triage of TC-8020. The reconciliation:
   - **Linked** TC-8021 to TC-8022 with "Depend" (standard remediation linkage)
   - **Removed** the `security-preemptive` label from TC-8022
   - **Recorded** that remediation already exists for stream 2.1.x

4. **Remediation (Step 8)**: Because Step 4.4 reconciliation found and adopted the existing preemptive task (TC-8022), Step 8 skips new remediation task creation for stream 2.1.x. TC-8022 already contains the correct remediation instructions (bump tokio to >= 1.42.0 on the backend repository, upstream branch release/0.3.z).

### Why no new tasks were created

The preemptive task mechanism (Step 8 Case B) is designed to create remediation tasks proactively when cross-stream impact is detected. When the stream-specific CVE Jira later arrives (TC-8021 in this case), Step 4.4 reconciliation links the CVE to the existing task and removes the provisional label, converting it into a standard remediation task. This avoids duplicate task creation while ensuring remediation work is not lost.

### Final issue state

**TC-8021 (Vulnerability)**:
- Status: Assigned (transitioned from New per Step 0.7)
- Labels: CVE-2026-55123, pscomponent:org/rhtpa-server, ai-cve-triaged
- Affects Versions: RHTPA 2.1.0, RHTPA 2.1.1
- Issue Links:
  - Depend: TC-8022 (remediation task, formerly preemptive)

**TC-8022 (Remediation Task)**:
- Labels: ai-generated-jira, Security, CVE-2026-55123 (security-preemptive removed)
- Issue Links:
  - Related: TC-8020 (originating CVE Jira from stream rhtpa-2.2, unchanged)
  - Depend: TC-8021 (new link from reconciliation)
- Summary: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)

### Remediation task lineage

```
TC-8020 (CVE Jira, stream rhtpa-2.2)
  |
  |-- [Step 8 Case B] created TC-8022 (preemptive, stream rhtpa-2.1)
  |     labels: security-preemptive
  |     link: Related -> TC-8020
  |
TC-8021 (CVE Jira, stream rhtpa-2.1)
  |
  |-- [Step 4.4 reconciliation] adopted TC-8022
        labels: security-preemptive REMOVED
        link: Depend -> TC-8021 (new)
        link: Related -> TC-8020 (retained)
```

### Post-triage actions

- Add `ai-cve-triaged` label to TC-8021
- Post summary comment to TC-8021 documenting: version impact, reconciliation outcome, link to TC-8022, and @mention of the issue reporter
