# Triage Outcome: TC-8021 -- CVE-2026-55123 tokio Use-After-Free [rhtpa-2.1]

## Outcome: Preemptive Task Reconciled -- No New Remediation Tasks Required

### Background

TC-8021 is a PSIRT-created Vulnerability issue for CVE-2026-55123 (tokio use-after-free, CVSS 8.1 High) scoped to stream rhtpa-2.1. The vulnerability affects tokio versions before 1.42.0, with the fix available in 1.42.0.

A prior triage of TC-8020 (the same CVE for stream rhtpa-2.2) had already identified that the 2.1.x stream was also affected. At that time, no PSIRT-created CVE Jira existed for stream rhtpa-2.1, so Step 8 Case A (cross-stream impact) created a preemptive remediation task:

- **TC-8022** -- "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)"
  - Status: Open
  - Labels: ai-generated-jira, Security, CVE-2026-55123, security-preemptive
  - Links: Related to TC-8020 (originating CVE from rhtpa-2.2)

### Step 4.4 Reconciliation

When triage reached Step 4.4, the JQL search for preemptive tasks matching the current CVE returned TC-8022. The summary contained "(rhtpa-2.1)" matching the current issue's stream scope, confirming it as a valid reconciliation target.

The reconciliation converts TC-8022 from a preemptive task (linked via "Related" to another stream's CVE) into a standard remediation task (linked via "Depend" to this stream's own CVE Jira).

### Proposed Jira Mutations (Requiring Engineer Confirmation)

All actions below are **PROPOSALS** -- they require explicit engineer confirmation before execution.

1. **Link TC-8021 to TC-8022 (Depend)** -- Establishes the standard remediation linkage between the CVE Vulnerability issue and its remediation Task. This is the same link type used when triage-security creates new remediation tasks.

2. **Remove `security-preemptive` label from TC-8022** -- The label is no longer applicable because TC-8022 now has a proper CVE Jira (TC-8021) as its parent tracker. Updated labels: `[ai-generated-jira, Security, CVE-2026-55123]`.

3. **Skip Step 8 remediation task creation** -- Because TC-8022 already covers the remediation for the 2.1.x stream (bump tokio to 1.42.0), no new remediation tasks are created. The reconciled preemptive task serves as the standard remediation task going forward.

### Link Topology After Reconciliation

```
TC-8020 (CVE Jira, rhtpa-2.2)
  |
  +-- Related --> TC-8022 (remediation task, rhtpa-2.1)  [original preemptive link]

TC-8021 (CVE Jira, rhtpa-2.1)  <-- current issue
  |
  +-- Depend --> TC-8022 (remediation task, rhtpa-2.1)   [new standard link from reconciliation]
```

TC-8022 retains its "Related" link to TC-8020 (origin) and gains a "Depend" link from TC-8021 (new authoritative CVE Jira for this stream). The `security-preemptive` label is removed.

### Why This Approach Is Correct

1. **No duplicate tasks**: Creating a new remediation task for stream 2.1.x would duplicate TC-8022's scope. Reconciliation avoids this.
2. **Traceability preserved**: TC-8022 remains linked to both TC-8020 (originating triage) and TC-8021 (authoritative stream CVE), maintaining a complete audit trail.
3. **Label hygiene**: Removing `security-preemptive` signals that TC-8022 is now a standard remediation task with a proper CVE Jira backing it.
4. **Standard link type**: The "Depend" link from TC-8021 to TC-8022 follows the same pattern used for all remediation tasks, ensuring consistency in Jira queries and release tracking.

### Remaining Triage Steps

After reconciliation, the triage would continue with:

- **Step 5 (Version Lifecycle Check)**: Verify that RHTPA 2.1.0 and 2.1.1 are still within support lifecycle.
- **Step 6 (Already Fixed Check)**: Cross-reference resolved siblings. No resolved siblings are known.
- **Step 7 (Concurrent Triage Detection)**: Check for other in-progress triages on the same upstream component (tokio).
- **Step 7.5 (Release Jira Orchestration)**: Find or create release Epic/Task for the 2.1.x stream. Since the reconciled preemptive task replaces standard remediation, it should be linked to the release Task if one is active.
- **Step 8 (Remediation)**: Task creation is **skipped** for stream 2.1.x because reconciliation recorded that TC-8022 already covers this stream.
- **Post-Triage Summary**: Add `ai-cve-triaged` label to TC-8021 and post a summary comment documenting the reconciliation outcome, version impact, and link to TC-8022.
