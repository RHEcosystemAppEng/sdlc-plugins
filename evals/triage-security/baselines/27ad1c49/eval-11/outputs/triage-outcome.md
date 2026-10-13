# Triage Outcome -- TC-8021 (CVE-2026-55123, tokio, stream rhtpa-2.1)

## Summary

TC-8021 was triaged with the outcome that an **existing preemptive remediation task (TC-8022) was reconciled** to become the standard remediation task for this CVE and stream. No new remediation tasks were created.

## How the Preemptive Task Was Reconciled

### Background

1. **TC-8020** was a prior Vulnerability issue for CVE-2026-55123 scoped to stream `[rhtpa-2.2]`.
2. During triage of TC-8020, Step 8 Case A (cross-stream impact) detected that stream 2.1.x was also affected by the same CVE (tokio < 1.42.0).
3. At that time, no stream-specific CVE Jira existed for stream 2.1.x.
4. Per Case A, a **preemptive remediation task TC-8022** was created for stream rhtpa-2.1 with:
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
   - Link: Related to TC-8020 (the originating CVE Jira from stream rhtpa-2.2)
   - Summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)"

### Reconciliation (Step 4.4)

When TC-8021 arrived as the PSIRT-created CVE Jira for stream `[rhtpa-2.1]`, Step 4.4 (Preemptive task reconciliation) was triggered:

1. **Search**: JQL query for tasks with labels `security-preemptive` and `CVE-2026-55123` returned TC-8022.
2. **Stream match**: TC-8022's summary contains `(rhtpa-2.1)`, matching TC-8021's stream suffix `[rhtpa-2.1]`.
3. **Reconciliation actions**:
   - **Linked TC-8021 to TC-8022 with "Depend"**: This establishes the standard remediation linkage (CVE inward, remediation task outward), the same relationship used for non-preemptive tasks created directly during triage.
   - **Removed `security-preemptive` label from TC-8022**: With a proper CVE Jira now linked, TC-8022 is no longer preemptive. Its updated labels are: `ai-generated-jira`, `Security`, `CVE-2026-55123`.
   - **Recorded reconciliation for Step 8**: The 2.1.x stream is marked as already having remediation coverage, so Step 8 skips task creation for this stream.

### Link Topology After Reconciliation

```
TC-8020 (CVE, stream rhtpa-2.2)
  |
  +-- Related --> TC-8022 (remediation task, stream rhtpa-2.1)
                    ^
                    |
TC-8021 (CVE, stream rhtpa-2.1)
  |
  +-- Depend ---> TC-8022 (remediation task, stream rhtpa-2.1)
```

TC-8022 is now:
- Linked to its own stream's CVE Jira (TC-8021) via **Depend** (standard remediation link)
- Still linked to the originating cross-stream CVE (TC-8020) via **Related** (historical provenance)
- No longer carrying the `security-preemptive` label

## Impact on Step 8 (Remediation)

Because Step 4.4 found and reconciled an existing preemptive task:

- **No new upstream backport task** is created for stream 2.1.x -- TC-8022 already covers "bump tokio to >= 1.42.0 on release/0.3.z".
- **No new downstream propagation task** is created -- a downstream propagation task would have been created alongside TC-8022 during the original preemptive creation from TC-8020's triage (if the ecosystem is Cargo/source dependency, 2 tasks are created per stream).
- Step 8 proceeds to post-triage summary and labeling without creating additional remediation tasks for the 2.1.x stream.

## Post-Triage Actions

Following reconciliation, the remaining triage steps complete as follows:

1. **ai-cve-triaged label**: Added to TC-8021 to mark it as triaged.
2. **Post-triage summary comment**: Posted on TC-8021 documenting the version impact analysis, the Affects Versions status, and the reconciliation outcome (TC-8022 reconciled from preemptive to standard remediation, no new tasks created).
3. **Reporter mention**: The summary comment includes an @mention of TC-8021's reporter (the PSIRT analyst) per the post-triage summary requirements.

## Key Principle

The reconciliation mechanism prevents duplicate remediation work. When PSIRT eventually creates a stream-specific CVE Jira (TC-8021) for a stream that already has preemptive coverage (TC-8022), the preemptive task is promoted to a standard task rather than creating a second, redundant remediation task. The `security-preemptive` label serves as the marker that enables this discovery, and its removal signals that the task is now anchored to a proper CVE Jira.
