# Triage Outcome -- TC-8021

## Summary

CVE-2026-55123 (tokio use-after-free in task abort, CVSS 8.1 High) was triaged for stream `rhtpa-2.1`. The triage found that a preemptive remediation task (TC-8022) already existed for this CVE and stream, created during prior cross-stream analysis of TC-8020 (stream `rhtpa-2.2`). The preemptive task was reconciled into a standard remediation task -- no new tasks were created.

## Preemptive Task Reconciliation

### What happened

1. TC-8020 was the first CVE Jira created by PSIRT for CVE-2026-55123, scoped to stream `[rhtpa-2.2]`.
2. During triage of TC-8020, Step 7 Case B identified that stream `2.1.x` was also affected by the vulnerable tokio version (versions before 1.42.0) but had no CVE Jira yet.
3. A preemptive remediation task TC-8022 was created with:
   - Labels: `ai-generated-jira, Security, CVE-2026-55123, security-preemptive`
   - Link: "Related" to TC-8020 (the originating CVE Jira)
   - Summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)"
4. Later, PSIRT created TC-8021 as the stream-specific CVE Jira for `[rhtpa-2.1]`.
5. During triage of TC-8021, Step 4.4 searched for preemptive tasks matching `security-preemptive` and `CVE-2026-55123`, found TC-8022, and confirmed it targets the same stream (`rhtpa-2.1`).

### Reconciliation actions

| Action | Detail |
|--------|--------|
| Link created | TC-8021 -> TC-8022 with link type "Depend" |
| Label removed | `security-preemptive` removed from TC-8022 |
| Task reuse | TC-8022 is now a standard remediation task for TC-8021 |
| Step 7 skip | No new remediation tasks created for stream 2.1.x |

### TC-8022 state after reconciliation

| Field | Before | After |
|-------|--------|-------|
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | ai-generated-jira, Security, CVE-2026-55123 |
| Links | Related: TC-8020 | Related: TC-8020, Depend (inward from TC-8021) |
| Role | Preemptive task (no owning CVE Jira) | Standard remediation task for TC-8021 |

## Triage Decision

**Outcome**: Remediation already exists (reconciled preemptive task).

- TC-8021 remains open with corrected Affects Versions for stream `2.1.x` (RHTPA 2.1.0, RHTPA 2.1.1).
- TC-8022 is the remediation task: bump tokio to >= 1.42.0 on branch `release/0.3.z` of the backend repository.
- No new Jira tasks were created because TC-8022 already covers the required remediation work.
- The `ai-cve-triaged` label would be added to TC-8021 to mark it as triaged.

## Version Impact (Stream 2.1.x)

| Version | Build Tag | tokio | Affected? | Notes |
|---------|-----------|-------|-----------|-------|
| 2.1.0 | v0.3.8 | (before 1.42.0) | YES | Vulnerable |
| 2.1.1 | v0.3.12 | (before 1.42.0) | YES | Vulnerable |

Both versions in the 2.1.x stream ship a tokio version below the fix threshold of 1.42.0 and are therefore affected.

## Cross-Stream Context

| Stream | CVE Jira | Remediation Task | Status |
|--------|----------|------------------|--------|
| rhtpa-2.2 (2.2.x) | TC-8020 | (created during TC-8020 triage) | Triaged separately |
| rhtpa-2.1 (2.1.x) | TC-8021 | TC-8022 (reconciled from preemptive) | Reconciled |
