# Triage Outcome: TC-8020 (CVE-2026-31812, quinn-proto)

## Decision

**PAUSED at Step 7 (Concurrent Triage Detection) — awaiting engineer choice.**

TC-8020 is **affected** (it would otherwise proceed to Case A + Case B), but a
concurrent triage on the same upstream component was found:
**TC-8019** (In Progress, assigned to engineer-b@example.com, Upstream Affected
Component `quinn-proto`). Per the skill protocol, remediation task creation must
not proceed until the engineer picks Wait / Skip / Proceed.

**Recommended choice: Wait.** Re-run triage after TC-8019 completes so Step 4.3
(cross-CVE overlap) and Step 7.5.3 (cross-CVE dedup) can reuse TC-8019's
remediation tasks if they already bring quinn-proto to >= 0.11.14.

## Version impact (fix threshold 0.11.14)

| Stream | Version | quinn-proto | Affected |
|--------|---------|-------------|----------|
| 2.1.x | 2.1.0 | 0.11.9 | YES |
| 2.1.x | 2.1.1 | 0.11.9 | YES |
| 2.2.x | 2.2.0 | 0.11.9 | YES |
| 2.2.x | 2.2.1 | 0.11.12 | YES |
| 2.2.x | 2.2.2 | 0.11.12 (same as 2.2.1, retag) | YES |
| 2.2.x | 2.2.3 | 0.11.14 | NO |
| 2.2.x | 2.2.4 | 0.11.14 | NO |

## Actions completed or proposed before the gate (simulated, no Jira calls)

1. **Step 0.3** – Matrix staleness warning: matrix last updated 2026-06-28
   (151 days old). Proceeded with current matrix for this eval; a refresh is advisable.
2. **Step 0.8** – Assign TC-8020 to current user; transition New -> Assigned.
3. **Step 1.5** – External enrichment not performed (no external calls); Jira
   description data used, reduced confidence.
4. **Step 1.7** – Skipped (no embargo policy URL configured).
5. **Step 3** – Affects Versions correction (scoped to 2.2.x): replace
   `RHTPA 2.0.0` with `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2` (requires confirmation;
   comment with footnote).
6. **Steps 4–6** – No duplicates, lifecycle exclusions, or resolved siblings
   identified from available data.
7. **Step 7** – Concurrent triage detected (TC-8019). **Execution stops here.**

## What happens next, by engineer choice

- **Wait**: stop now. No remediation tasks, no labels. Re-run
  `/sdlc-workflow:triage-security TC-8020` after TC-8019 completes.
- **Skip**: no remediation tasks for TC-8020. Post a comment (with the
  triage-security footnote) explaining that task creation was skipped because of
  concurrent triage TC-8019 on quinn-proto. Then do the post-triage summary.
- **Proceed**: add the `concurrent-triage-overlap` label to TC-8020, then continue:
  - **Step 7.5** – find/create release Epic + release Task for the affected
    release(s); run 7.5.3 dedup against existing quinn-proto remediation Tasks
    (TC-8019's tasks, if already created, would trigger dedup -> link instead of create).
  - **Step 8, Case A** (scoped issue, other stream affected): post cross-stream
    impact comment noting 2.1.x (2.1.0, 2.1.1) is affected; create preemptive
    Cargo tasks for 2.1.x (label `security-preemptive`, link type Related) if no
    2.1.x sibling CVE Jira exists.
  - **Step 8, Case B** (2.2.x): Cargo source dependency, fix available upstream
    (2.2.3+ already ship 0.11.14) -> 2 tasks: dependency bump in rhtpa-backend
    `release/0.4.z` + downstream propagation (blocked by the bump), linked Depend
    to TC-8020 and Blocks to the release Task. Note: if `release/0.4.z` HEAD already
    ships 0.11.14, the bump may already be done and only z-stream delivery remains.
  - Not Case C: supported versions are affected, so close-as-Not-a-Bug does not apply.

## Post-triage (deferred until gate is resolved)

- Add label `ai-cve-triaged` to TC-8020.
- Post summary comment: version impact table, Affects Versions correction,
  concurrent-triage decision and TC-8019 reference, any tasks/release Jira/dedup
  results, @mention of the PSIRT reporter, and the triage-security Comment Footnote.
