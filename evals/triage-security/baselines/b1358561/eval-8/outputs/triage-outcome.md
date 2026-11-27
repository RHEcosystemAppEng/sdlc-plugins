# Triage Outcome: TC-8010 (CVE-2026-44492, axios SSRF, [rhtpa-2.2])

## Decision

**Do not create new remediation tasks.** An existing remediation already covers this
CVE: TC-8009, which was created for CVE-2026-42035 / TC-8008. Record the overlap
through links and a comment. Then **recommend closing TC-8010**, because the fix is
already covered by TC-8009. The engineer confirms the closure.

## Rationale

1. TC-8010 is scoped to stream **2.2.x** (`[rhtpa-2.2]`). It affects axios versions `< 1.8.2`, with the fix in **1.8.2**.
2. The Step 4.3 search on `cf[10632] ~ 'axios'` returned **TC-8008** (CVE-2026-42035). It
   has the same Upstream Affected Component (axios), the same PS Component
   (`pscomponent:org/rhtpa-ui`) and the same Stream (`rhtpa-2.2`).
3. TC-8008 has a Depend link to remediation task **TC-8009**: "Bump axios to 1.9.0 in rhtpa-ui [rhtpa-2.2]" (In Progress).
4. **1.9.0 >= 1.8.2.** The bump target is above this CVE's fix threshold, so finishing
   TC-8009 also remediates CVE-2026-44492 in rhtpa-ui for the 2.2.x stream. (TC-8009's
   own stated requirement of `>= 1.8.0` is not what decides this; its bump target is.)
5. Creating the usual Case B pair (dependency bump plus downstream propagation) would
   duplicate TC-8009. Step 7.5.3 cross-CVE dedup would also detect this, because the
   component matches, and skip task creation.

## Proposed Jira actions (each needs engineer confirmation; none were executed)

| # | Action | Target | Step |
|---|--------|--------|------|
| 1 | Assign to current user and transition New → Assigned | TC-8010 | 0.8 |
| 2 | Create a **Related** link TC-8010 ↔ TC-8008 (idempotent; no existing links) | TC-8010 | 4.3.6a |
| 3 | Create a **Depend** link TC-8010 → TC-8009 (covering remediation) | TC-8010 | 4.3.6b |
| 4 | Post a cross-CVE overlap comment with the Comment Footnote (no ProdSec @mention because none is configured) | TC-8010 | 4.3.6c |
| 5 | Add label `CVE-2026-44492` to TC-8009 so the covering task tracks both CVEs | TC-8009 | 7.5.3d (dedup) |
| 6 | If a release Task for RHTPA 2.2.x exists, create a **Related** link from the release Task to TC-8010. No new remediation tasks will be linked. | release Task | 7.5.3c |
| 7 | **Do not create** remediation tasks (Case B skipped because of dedup/overlap) | — | 8 |
| 8 | Add label `ai-cve-triaged` | TC-8010 | Post-triage |
| 9 | Post a summary comment: overlap finding, covering task TC-8009, dedup result, @mention of the reporter, Comment Footnote | TC-8010 | Post-triage |
| 10 | **Recommendation:** close TC-8010 because the fix is already covered by TC-8009. Alternatively, keep it open (Depend-linked) until TC-8009 is Done and then move it to ON_QA. The engineer decides. | TC-8010 | 4.3 recommendation |

The traceability links and the overlap comment (actions 2–4) are recorded as soon as the
overlap is confirmed. They are not deferred until the engineer decides on closure.

## Caveats and follow-ups

- **Remediation is still in flight.** TC-8009 is In Progress, not Done. Until it merges
  and ships, RHTPA 2.2.x is still vulnerable to CVE-2026-44492. If TC-8010 is closed now,
  the Depend link to TC-8009 is the audit trail. If the bump target in TC-8009 is ever
  lowered below 1.8.2 (for example, pinned at 1.8.0 or 1.8.1), this overlap no longer holds
  and TC-8010 must be re-triaged.
- **Version impact (Step 2) could not be verified from lock files.** The 2.2.x
  security-matrix has no npm Ecosystem Mapping and no axios data, so it cannot say which
  RHTPA 2.2.x releases ship axios `< 1.8.2`. TC-8009's description says rhtpa-ui is
  currently on axios **1.7.4**, which falls inside the affected range. That is
  task-description evidence, not lock-file evidence. Affects Versions (RHTPA 2.2.0) were
  left unchanged (Step 3 was not run on unverified data).
- **Cross-stream (Case A).** Step 4.3 is limited to stream `rhtpa-2.2`. If the 2.1.x
  stream also ships rhtpa-ui with a vulnerable axios, it needs its own triage or a
  preemptive task. The matrix data available here cannot determine this.
- **Configuration gaps to fix via `/setup`:**
  - Add the Upstream Affected Component (`customfield_10632`), PS Component
    (`customfield_10669`) and Stream (`customfield_10832`) field IDs to Security Configuration.
  - Add `rhtpa-ui` to Source Repositories.
  - Add an npm Ecosystem Mapping to the security matrices.
  - Refresh the matrix (stale since 2026-06-28).
- No external services were contacted: Jira, git show, MITRE and OSV.dev were all skipped. Every action listed above is a proposal.
