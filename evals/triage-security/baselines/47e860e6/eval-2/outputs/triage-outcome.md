# TC-8002 — Triage Outcome

## Decision

**Case C: no supported versions are affected. Recommend closing TC-8002 as "Not a Bug", with VEX Justification set to "Component not Present".**

Every supported RHTPA version ships serde_json 1.0.137, 1.0.138 or 1.0.139. All of these are at or above the fixed version 1.0.135. The PSIRT-assigned Affects Version (RHTPA 2.2.0) is wrong: that release ships serde_json 1.0.138 (pinned tag `v0.4.5`). PSIRT most likely assigned it from scan time or a range, not from lock-file evidence. This skill does not trust that assignment without checking (Important Rule 3).

**No remediation Tasks are created.** No Release Epic or Task is found or created (Step 7.5 only applies to affected streams).

## Step-by-step summary

| Step | Result |
|---|---|
| 0 Config | Valid. VEX field `customfield_12345` is configured. Overlap and concurrency fields, ProdSec, and Embargo are not configured. |
| 0.3 Staleness | Both matrices last updated 2026-06-28 (129 days ago, threshold 14). Warning raised. Eval proceeds with "Proceed anyway". |
| 0.8 Assign | Proposed: assign to the current user, transition New → Assigned (discovered dynamically). |
| 1 Extraction | CVE-2026-28940, serde_json < 1.0.135, fixed in 1.0.135, Cargo, scoped to 2.2.x (`[rhtpa-2.2]`). |
| 1.5 Enrichment | MITRE and OSV not queried (eval). Jira description threshold used, with reduced confidence. |
| 1.7 Embargo | Skipped. Not configured, and CVSS 5.3 is below 7.0. |
| 2 Version impact | 0 of 7 released versions affected across 2.1.x and 2.2.x. 2.2.2 carried forward as a retag of 2.2.1. |
| 3 Affects Versions | Correction needed: `[RHTPA 2.2.0]` → `[]` (no affected version in stream 2.2.x). |
| 4 Duplicates/siblings | JQL not run (eval). Proposed query below. Step 4.3 skipped (fields not configured). Step 4.4 preemptive-task search proposed. |
| 5 Lifecycle | Not applicable. No affected versions to check. |
| 6 Already fixed (sibling) | Not the deciding factor. The issue is "already fixed" because every shipped version already contains the patched dependency (version evidence), not because a resolved sibling covers it. VEX is therefore set. |
| 7 Concurrent triage | Skipped. Upstream Affected Component field is not configured. |
| 7.5 Release Jira | Skipped. No affected stream. |
| 8 Remediation | **Case C: close as Not a Bug.** |

## Proposed Jira actions (each needs engineer confirmation, none executed)

1. **Assign and transition (Step 0.8)**
   - `jira.edit_issue("TC-8002", assignee=<current-user-account-id>)`
   - `jira.get_transitions("TC-8002")`, then pick the transition whose target is "Assigned" (e.g. `ASSIGNED`), then `jira.transition_issue("TC-8002", <id>)`

2. **Sibling and preemptive checks (Steps 4, 4.4, 6) to run before closing**
   - `project = TC AND labels = 'CVE-2026-28940' AND issuetype = 10024 AND key != TC-8002`
     - Same-stream (`[rhtpa-2.2]`) open sibling: close as Duplicate instead.
     - Different-stream sibling (e.g. `[rhtpa-2.1]`): add a Related link (if none exists). That issue is also not affected per the 2.1.x lock data (serde_json 1.0.137), so recommend the same Not a Bug closure when it is triaged.
   - `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-28940'`. Not expected to match.

3. **Affects Versions correction (Step 3)**
   - Discover versions with `getJiraIssueTypeMetaWithFields(projectIdOrKey="TC", issueTypeId="10024")`, filtered by the `RHTPA` prefix. No hard-coded IDs.
   - Diff: `Current: [RHTPA 2.2.0] → Proposed: []`. RHTPA 2.2.0 ships serde_json 1.0.138, which is not affected.
   - Comment (ADF, with footnote):
     > Corrected Affects Versions: [RHTPA 2.2.0] → [] (none affected).
     > Based on lock file analysis at pinned commits from security-matrix.md:
     > RHTPA 2.2.0 (backend `v0.4.5`) ships serde_json 1.0.138, which is outside the affected range (< 1.0.135).
     > Scoped to stream 2.2.x per issue suffix.
     >
     > _Comment footnote per `shared/comment-footnote.md` (skill: triage-security)_
   - If Jira requires a non-empty Affects Versions on a Not-a-Bug closure, keep the field unchanged and let the closure comment document the correction.

4. **Case C closure comment (Step 8)**
   > No supported versions ship a vulnerable version of serde_json (CVE-2026-28940, affected < 1.0.135, fixed in 1.0.135).
   >
   > | Version | Pinned tag | serde_json | Affected? |
   > |---|---|---|---|
   > | 2.1.0 | v0.3.8 | 1.0.137 | NO |
   > | 2.1.1 | v0.3.12 | 1.0.137 | NO |
   > | 2.2.0 | v0.4.5 | 1.0.138 | NO |
   > | 2.2.1 | v0.4.8 | 1.0.138 | NO |
   > | 2.2.2 | v0.4.8 | (same as 2.2.1) | NO |
   > | 2.2.3 | v0.4.11 | 1.0.139 | NO |
   > | 2.2.4 | v0.4.12 | 1.0.139 | NO |
   >
   > All supported versions ship serde_json 1.0.137–1.0.139, which is outside the affected range (< 1.0.135).
   >
   > _Comment footnote per `shared/comment-footnote.md` (skill: triage-security)_

5. **Transition to Closed with resolution "Not a Bug"**. Target status comes from `jira.get_transitions`.

6. **Set VEX Justification**: `jira.edit_issue("TC-8002", fields={"customfield_12345": {"value": "Component not Present"}})`. This is the default when the lock-file analysis shows no vulnerable package version is included in any shipped version. A plausible alternative is "Vulnerable Code not Present", since the shipped serde_json contains the recursion-limit fix. The engineer should confirm which one.

7. **Post-triage summary**
   - Add label `ai-cve-triaged` to TC-8002.
   - Summary comment (ADF, with footnote) containing: the version impact table, the Affects Versions correction (`[RHTPA 2.2.0] → []`), the outcome (closed as Not a Bug, VEX = Component not Present), no remediation tasks, no release Jira, no dedup, and an ADF mention of the issue reporter (PSIRT analyst; account ID from the issue's `reporter` field):
     `{ "type": "mention", "attrs": { "id": "<reporter-account-id>", "text": "@<reporter-name>" } }`

## Caveats for the engineer

- **Stale matrix (129 days old).** Releases after 2.2.4 (2026-05-04) are not in the matrix. Before closing, refresh the matrix or confirm that newer releases and the development branch HEAD (`release/0.4.z`) also ship serde_json >= 1.0.135. A regression is very unlikely, since all tags are at 1.0.137 or later.
- **External enrichment not done.** MITRE and OSV did not cross-validate the 1.0.135 threshold. The decision has margin anyway: the lowest shipped version is 1.0.137.
- **Due date 2026-07-30 has passed.** Closing as Not a Bug resolves the SLA item.
- The dependency evidence comes from the eval's simulated `git show` output (mock lock-file data), not from live repositories.
