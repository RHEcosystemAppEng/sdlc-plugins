# TC-8021 — Triage Outcome

## Summary

**Outcome: remediation already exists. The preemptive task TC-8022 was reconciled. No new remediation tasks are created.**

CVE-2026-55123 (tokio < 1.42.0, use-after-free, CVSS 8.1) arrived as TC-8021 for stream `[rhtpa-2.1]`. An earlier cross-stream triage of TC-8020 (`[rhtpa-2.2]`) found 2.1.x affected. No 2.1 CVE Jira existed then, so it created TC-8022 as a **preemptive** task: labeled `security-preemptive` and linked to TC-8020 with **Related**. Now that PSIRT has created the stream-specific CVE Jira (TC-8021), Step 4.4 turns TC-8022 into this CVE's standard remediation task.

## How the preemptive task was reconciled

1. **Found:** the Step 4.4 JQL (`labels = 'security-preemptive' AND labels = 'CVE-2026-55123'`) returned TC-8022.
2. **Matched to the stream:** TC-8022's summary contains `(rhtpa-2.1)`, the same as TC-8021's suffix `[rhtpa-2.1]`. The task is Open and not yet linked to TC-8021.
3. **Linked:** TC-8021 → TC-8022 with **Depend**, the standard CVE-to-remediation link type. This replaces "preemptive" status with a real CVE dependency.
4. **Relabeled:** `security-preemptive` is removed from TC-8022. The remaining labels are `ai-generated-jira`, `Security`, `CVE-2026-55123`.
5. **History kept:** TC-8022's **Related** link to TC-8020 stays as a record of where it came from.
6. **Recorded:** 2.1.x is marked as having remediation (TC-8022). Step 8 does **not** create new upstream or bump tasks for 2.1.x, which avoids a duplicate.

## Remaining steps (simulated)

| Step | Result |
|---|---|
| 0.3 Matrix staleness | Matrix 145 days old (Last-Updated 2026-06-28). Proceeded with a warning; a refresh is recommended |
| 0.8 Assign/transition | Proposed: assign to triager, New → Assigned |
| 1.5 Enrichment | MITRE/OSV not queried in the eval; Jira threshold 1.42.0 used (reduced confidence) |
| 1.7 Embargo | Skipped (no policy URL configured) |
| 2 Version impact | tokio versions at v0.3.8 / v0.3.12 are **not in the mock lock data** and were not invented. Must be checked with `git show <tag>:Cargo.lock` |
| 3 Affects Versions | No correction proposed. RHTPA 2.1.0, 2.1.1 kept but unverified |
| 4.1 Duplicates | None |
| 4.2 Cross-stream | Related link TC-8021 ↔ TC-8020 proposed (companion tracker) |
| 4.3 Cross-CVE overlap | Skipped (Upstream Affected Component field not configured) |
| 4.4 Reconciliation | **TC-8022 reconciled** (Depend link + label removal) |
| 5 Lifecycle | Not fetched in the eval. 2.1.0 / 2.1.1 support status must be checked on the product pages |
| 6 Already fixed | No resolved siblings known, so not already fixed |
| 7 Concurrent triage | Skipped (Upstream Affected Component field not configured) |
| 7.5 Release Jira | Find or create "RHTPA <next 2.1.z> CVE triage". Link TC-8022 → release Task (**Blocks**) now that it is non-preemptive, and TC-8021 → release Task (**Related**). Needs engineer confirmation of the release version |
| 8 Remediation | Case B for 2.1.x **satisfied by TC-8022**, so no new tasks. Case A (cross-stream): 2.2.x already has its own CVE Jira (TC-8020), so no preemptive tasks are needed |

## Open items for the engineer

- Confirm with a real lock-file check that 2.1.0 / 2.1.1 ship tokio < 1.42.0. If neither is affected, TC-8022 and TC-8021 should be revisited (Case C).
- Confirm whether a preemptive **downstream propagation** task exists for 2.1.x. Only TC-8022 was returned. If one exists, reconcile it the same way; if not, consider creating one.
- The due date of 2026-08-15 has passed. Prioritise accordingly.

## Proposed Jira mutations (all need confirmation; none executed)

1. TC-8021: assign to triager; transition New → Assigned.
2. Link TC-8021 ↔ TC-8020 (Related).
3. Link TC-8021 → TC-8022 (Depend).
4. TC-8022: labels → `ai-generated-jira, Security, CVE-2026-55123` (remove `security-preemptive`).
5. Release Jira links (Step 7.5): TC-8022 Blocks release Task; TC-8021 Related to release Task.
6. TC-8021: add label `ai-cve-triaged`.
7. TC-8021: post-triage summary comment containing the impact table (pending lock-file verification), the reconciliation of TC-8022, the release Jira refs, an @mention of the reporter, and the Comment Footnote (`triage-security`).
