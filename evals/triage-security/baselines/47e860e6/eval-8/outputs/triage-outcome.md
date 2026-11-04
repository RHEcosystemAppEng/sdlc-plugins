# TC-8010 — Triage Outcome

## Decision

**Covered by existing cross-CVE remediation. No new remediation tasks will be created.**

CVE-2026-44492 (axios SSRF, fixed in **1.8.2**) on stream **2.2.x** (`pscomponent:org/rhtpa-ui`) is already handled by remediation task **TC-8009**. That task belongs to CVE-2026-42035 / **TC-8008** and bumps axios from 1.7.4 to **1.9.0**. Since 1.9.0 >= 1.8.2, the existing bump fixes this CVE too. Creating more tasks would duplicate the same axios bump in the same component and stream.

Following Step 4.3, the recommendation is to **close TC-8010, because the fix is already covered by TC-8009**. Every action below waits for engineer confirmation; nothing has been executed.

## Rationale (step by step)

| Step | Result |
|---|---|
| 0 Config | Security Configuration is present. Gap: the Upstream Affected Component, PS Component, and Stream fields are not declared in the mock CLAUDE.md. Step 4.3 ran because the task says so and the issue has those fields set |
| 0.3 Staleness | The matrix is 129 days old (last updated 2026-06-28). Staleness warning raised; proceeded |
| 0.6 Mode | Interactive (`FULLSEND_OUTPUT_DIR` not set) |
| 0.8 Assign | Proposed: assign to the triager and move New to Assigned |
| 1 Extraction | CVE-2026-44492, axios, < 1.8.2, fixed in 1.8.2, CVSS 8.1, scoped `[rhtpa-2.2]` → 2.2.x, Affects Versions RHTPA 2.2.0 |
| 1.5 Enrichment | Not run (no external calls). Used the Jira description threshold 1.8.2, with lower confidence |
| 1.7 Embargo | Skipped (no embargo policy URL configured) |
| 2 Version impact | **Not verifiable.** npm/axios is not in the 2.2.x Ecosystem Mappings (only Cargo and RPM), `rhtpa-ui` is not a configured source repo, and there is no axios lock-file data. No per-version axios table was produced, because that would mean inventing data. TC-8009's description says the current axios is 1.7.4 (vulnerable). This is supporting evidence only |
| 3 Affects Versions | No correction proposed. Without lock-file evidence, PSIRT's RHTPA 2.2.0 is kept as is |
| 4.1/4.2 Siblings | No other issues carry the CVE-2026-44492 label |
| **4.3 Cross-CVE overlap** | **TC-8008 matches on component, PS component, and stream. Its Depend task TC-8009 bumps to 1.9.0 >= 1.8.2, so this CVE is COVERED** |
| 4.4 Preemptive | No preemptive task for CVE-2026-44492 |
| 5 Lifecycle | Not queried (external). 2.2.x is the latest stream in the matrix |
| 6 Already fixed | No resolved siblings. TC-8009 is still **In Progress**, so the fix has not shipped yet |
| 7 Concurrent triage | TC-8008 (In Progress) is active work on the same component. It is the remediation being reused, not a competing triage |
| 7.5.3 Cross-CVE dedup | Agrees with 4.3: an existing axios remediation covers 2.2.x. Skip task creation and link instead |
| 8 Remediation | No Case B tasks (dedup'd / covered). No Case A (2.1.x has no npm mapping and no evidence that it is affected). Not Case C (the component is shipped and vulnerable until TC-8009 lands) |

## Proposed Jira actions (each requires engineer confirmation)

1. Assign TC-8010 to the current user and move it to **Assigned**.
2. Create a **Related** link: TC-8010 ↔ TC-8008 (same upstream component axios).
3. Create a **Depend** link: TC-8010 → TC-8009 (covering remediation).
4. Post the **cross-CVE overlap comment** (text in overlap-check.md, with the Comment Footnote v0.13.10, no ProdSec @mention because none is configured).
5. If a release Task "RHTPA 2.2.x CVE triage" exists (Step 7.5), link TC-8010 to it with **Related**. TC-8009 should already block it.
6. Add the label **`ai-cve-triaged`** to TC-8010.
7. Post the **post-triage summary comment**. It covers: the overlap finding, the reason the version impact table is missing (no npm lock-file mapping), no change to Affects Versions, no new tasks with dedup to TC-8009, release Jira references if any, an @mention of the reporter (account ID from the issue's reporter field, which the mock does not include), and the Comment Footnote.
8. **Closure (recommended by Step 4.3, needs engineer confirmation).** Close TC-8010 because it is covered by TC-8009.
   - Caveat for the engineer: TC-8009 is still **In Progress**, so the vulnerable axios 1.7.4 may still be shipping. Closing as "Not a Bug" / VEX "Component not Present" would be **wrong**, because the product is affected.
   - A safer alternative is to keep TC-8010 open with the Depend link to TC-8009. It then follows the normal lifecycle and becomes "Ready for QA" (Discovery query 3) once TC-8009 is Done.
   - If the engineer still chooses to close now, use a resolution that refers to TC-8009 (for example "Duplicate"-style coverage) rather than Not a Bug, and leave the VEX Justification field unset.

## Not created

- No upstream backport or dependency-bump task, and no downstream propagation task, for 2.2.x. TC-8009 already bumps axios to 1.9.0.
- No preemptive tasks for other streams.
- No Vulnerability issues.

## Follow-ups for the engineer

- Refresh the 2.2.x security matrix (129 days stale).
- Add an npm Ecosystem Mapping for `rhtpa-ui` (package-lock.json) and add `rhtpa-ui` to Source Repositories, so axios exposure can be checked from lock files.
- Declare the Upstream Affected Component (customfield_10632), PS Component (customfield_10669), and Stream (customfield_10832) fields in Security Configuration, so Step 4.3 and Step 7 run without being told to.
- Note that the due date (2026-08-01) has passed.
