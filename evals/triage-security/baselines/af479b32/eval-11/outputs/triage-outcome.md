# Triage Outcome: TC-8021

## Summary

CVE-2026-55123 (tokio use-after-free, versions before 1.42.0) for stream rhtpa-2.1 was triaged with a **preemptive task reconciliation** outcome. An existing preemptive remediation task (TC-8022) was found and adopted as the standard remediation task for this CVE Jira.

## How the Preemptive Task Was Reconciled

### Background

1. **TC-8020** was the first CVE Jira created by PSIRT for CVE-2026-55123, scoped to stream **rhtpa-2.2** (suffix `[rhtpa-2.2]`).
2. During triage of TC-8020, Step 8 Case B (cross-stream impact) identified that stream **rhtpa-2.1** was also affected by the same vulnerability.
3. Since no CVE Jira existed for rhtpa-2.1 at that time, Case B proactively created **TC-8022** as a preemptive remediation task with:
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
   - Link: Related to TC-8020 (the originating CVE Jira)
4. Later, PSIRT created **TC-8021** as the stream-specific CVE Jira for rhtpa-2.1.

### Reconciliation (Step 4.4)

When triaging TC-8021, Step 4.4 searched for preemptive tasks matching this CVE and stream:

- **JQL**: `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123'`
- **Result**: TC-8022 matched (summary contains `(rhtpa-2.1)`)

Three reconciliation actions were performed:

1. **Created "Depend" link**: TC-8021 -> TC-8022. This is the standard remediation linkage, making TC-8022 a proper remediation task for TC-8021 (just as if it had been created fresh in Step 8 Case A).

2. **Removed `security-preemptive` label** from TC-8022. The label's purpose is to mark tasks that lack a proper CVE Jira parent. Now that TC-8021 exists and is linked, the label is no longer applicable.

3. **Recorded reconciliation**: Step 8 skips new remediation task creation for stream rhtpa-2.1 because TC-8022 already covers it.

### Final State

**TC-8022** transitions from a preemptive task to a standard remediation task:

- Before reconciliation: preemptive task with `security-preemptive` label, linked only via "Related" to TC-8020 (a different stream's CVE)
- After reconciliation: standard remediation task without `security-preemptive` label, linked via "Depend" to TC-8021 (its own stream's CVE) and retaining "Related" to TC-8020 for provenance

**TC-8021** links after triage:

| Link Type | Target | Purpose |
|-----------|--------|---------|
| Depend | TC-8022 | Remediation task (reconciled from preemptive) |

**TC-8022** links after triage:

| Link Type | Target | Purpose |
|-----------|--------|---------|
| Depend (inward) | TC-8021 | CVE Jira for this stream (from reconciliation) |
| Related | TC-8020 | Originating CVE Jira for stream rhtpa-2.2 (from original creation) |

## Step 8 Outcome

**No new remediation tasks were created.** The preemptive task TC-8022 already covers the remediation for stream rhtpa-2.1 (bump tokio to >= 1.42.0). The reconciliation promoted TC-8022 from a preemptive task to a standard remediation task linked to TC-8021.

This is the expected behavior of Step 4.4: when PSIRT creates a stream-specific CVE Jira after a preemptive task already exists, the triage skill adopts the existing task rather than creating a duplicate.

## Post-Triage Actions

1. **Label TC-8021 with `ai-cve-triaged`** to mark it as triaged.
2. **Post summary comment** on TC-8021 documenting:
   - Version impact analysis for stream rhtpa-2.1
   - Preemptive task reconciliation with TC-8022
   - No new remediation tasks created (TC-8022 adopted)
   - @mention of TC-8021's reporter (PSIRT analyst)
   - Comment Footnote per skill requirements
