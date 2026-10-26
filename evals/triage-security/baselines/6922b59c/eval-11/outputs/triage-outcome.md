# Triage Outcome: TC-8021

## Summary

**Issue**: TC-8021 -- CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1]
**Outcome**: Preemptive task reconciled -- no new remediation tasks created
**Stream**: 2.1.x (scoped via summary suffix [rhtpa-2.1])

## How the Existing Preemptive Task Was Reconciled

### Background

When TC-8020 (the same CVE-2026-55123, scoped to stream rhtpa-2.2) was triaged
earlier, the triage skill's Step 8 Case A (cross-stream impact) detected that
stream 2.1.x was also affected by the vulnerability. Since no CVE Jira existed
yet for stream 2.1.x, a **preemptive remediation task** (TC-8022) was created:

- **TC-8022**: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)"
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
- Linked to TC-8020 via "Related" (cross-stream originating CVE)

### Reconciliation (Step 4.4)

When TC-8021 arrived as the proper stream-specific CVE Jira for rhtpa-2.1, the
Step 4.4 preemptive task reconciliation detected TC-8022 via JQL search:

```
labels = 'security-preemptive' AND labels = 'CVE-2026-55123'
```

TC-8022's summary contains `(rhtpa-2.1)`, matching TC-8021's stream scope. The
reconciliation performed three actions:

1. **Linked TC-8021 to TC-8022 with "Depend"** -- This establishes the standard
   remediation task linkage, identical to what would exist if TC-8022 had been
   created fresh during this triage.

2. **Removed the `security-preemptive` label from TC-8022** -- This promotes
   TC-8022 from a preemptive task (created speculatively from another stream's
   triage) to a standard remediation task that is properly linked to its own
   stream's CVE Jira.

3. **Recorded that remediation exists for stream 2.1.x** -- This prevents Step 8
   from creating duplicate remediation tasks. The existing TC-8022 already contains
   the correct remediation instructions (bump tokio to 1.42.0).

### Effect on Step 8

Because Step 4.4 recorded that remediation already exists for stream 2.1.x,
Step 8 (Remediation) skips task creation entirely for this stream. No new
upstream backport task or downstream propagation task is created -- TC-8022
already serves that purpose.

### Final State

| Issue | Role | Status | Labels | Links |
|-------|------|--------|--------|-------|
| TC-8020 | CVE Jira (stream rhtpa-2.2) | (previously triaged) | CVE-2026-55123, ai-cve-triaged | Related: TC-8022 |
| TC-8021 | CVE Jira (stream rhtpa-2.1) | Assigned (after Step 0.8) | CVE-2026-55123, ai-cve-triaged | Depend: TC-8022 |
| TC-8022 | Remediation task (stream rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123 | Related: TC-8020, Depend from: TC-8021 |

Key observations:
- TC-8022's `security-preemptive` label has been removed
- TC-8022 now has a proper "Depend" link from TC-8021 (its own stream's CVE Jira)
- TC-8022 retains its "Related" link to TC-8020 (the originating cross-stream CVE)
- No duplicate remediation tasks were created
- The post-triage summary comment on TC-8021 documents the reconciliation
