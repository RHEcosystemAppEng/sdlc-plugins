# Triage Outcome: TC-8011 (CVE-2026-45678, webpack < 5.98.0, [rhtpa-2.2])

## Decision

**Do NOT close as covered by an existing remediation.** The cross-CVE overlap check found that TC-8013 bumps webpack only to 5.96.1. That is below this CVE's fix threshold of 5.98.0. TC-8011 stays open and needs **new remediation** for stream 2.2.x, a Case B dependency bump to webpack >= 5.98.0. Before any tasks are created, an npm version-impact assessment is required (see blockers).

## Step-by-step summary

| Step | Result |
|---|---|
| 0 Config | Valid. TC / 10024 / RHTPA. Overlap fields (10632/10669/10832) available from the scenario. |
| 0.3 Staleness | Matrix 128 days old (Last-Updated 2026-06-28). Warned; assumed "Proceed anyway". |
| 0.8 Assign | Proposed: assign to current user, transition New to Assigned. |
| 1 Extraction | CVE-2026-45678, webpack, < 5.98.0, fixed 5.98.0, CVSS 7.8, scoped to 2.2.x, component pscomponent:org/rhtpa-ui. |
| 1.5 Enrichment | External APIs not queried (eval constraint). Jira threshold 5.98.0 used, with reduced confidence. |
| 1.7 Embargo | Skipped (no embargo policy URL configured). |
| 2 Version impact | **Blocked for automated analysis.** npm/rhtpa-ui is not in the 2.2.x Ecosystem Mappings, and the mock matrix has no webpack lock-file data. Manual assessment is required. Versions were not guessed. |
| 3 Affects Versions | No correction proposed without lock-file evidence. RHTPA 2.2.0 stays as PSIRT set it, pending manual assessment. |
| 4.1/4.2 Siblings | None for CVE-2026-45678. |
| **4.3 Cross-CVE overlap** | TC-8012 (CVE-2026-43210) matches component, PS component, and stream. Its remediation TC-8013 bumps webpack to **5.96.1**, which is **< 5.98.0**. **Not covered.** No links, no overlap comment, no closure. |
| 4.4 Preemptive | No preemptive tasks found. |
| 5 Lifecycle | Not fetched (no external calls). Matrix lists 2.2.0–2.2.4 as supported. |
| 6 Already fixed | No resolved same-CVE siblings. TC-8012 is a different CVE and does not count as "already fixed". |
| 7 Concurrent triage | The search for In Progress/Code Review webpack CVEs would run. TC-8012 is Closed, so no concurrent triage is known. |
| 7.5 Release Jira | Would find or create "RHTPA 2.2.x Release Tasks" Epic / "CVE triage" Task. 7.5.3 dedup: TC-8013 does **not** count as an existing covering task (5.96.1 < 5.98.0), so this CVE is not deduplicated. |
| 8 Remediation | Case B (scoped, 2.2.x affected pending confirmation). Case A cross-stream: the 2.1.x matrix has no npm mapping either, so cross-stream impact can't be determined automatically. |

## Why the overlap does not cover this CVE

- TC-8013 targeted CVE-2026-43210, which requires webpack >= 5.96.0, and moved webpack from 5.95.0 to 5.96.1.
- CVE-2026-45678 requires webpack >= 5.98.0.
- 5.96.1 < 5.98.0 (minor version 96 < 98), so webpack 5.96.1 is still vulnerable to CVE-2026-45678.
- Closing TC-8011 or Depend-linking it to TC-8013 would falsely mark the CVE as remediated.

## Proposed remediation (after the npm impact is confirmed), stream 2.2.x

Source dependency (npm). If webpack 5.98.0+ is available upstream, which is likely, this is the fix-available variant with 2 tasks:

1. **Dependency bump**: "Bump webpack to >= 5.98.0 in rhtpa-ui [rhtpa-2.2]" (CVE-2026-45678). Bump from the current version (expected 5.96.1 after TC-8013, to be verified) to >= 5.98.0 with `npm update webpack` / a package-lock.json update. Labels: `CVE-2026-45678`, security. Deployment context: `upstream` (default). webpack is usually a build-time/dev dependency. If Step 2.3.5 confirms that, add the `dev-dependency` label and set priority to Normal.
2. **Downstream propagation**: propagate the bumped rhtpa-ui into the rhtpa-release.0.4.z Konflux release. Task 1 Blocks it.

Links: TC-8011 Depend on both tasks, task 1 Blocks task 2, both tasks Block the release Task, and TC-8011 is Related to the release Task. Each task gets a description digest comment. Every comment carries the triage-security Comment Footnote.

An informational Related link TC-8011 to TC-8012 (same upstream component) may be proposed for traceability. It is optional, and Step 4.3 does not require it in the not-covered case.

## Blockers / engineer actions required

1. **Unsupported ecosystem (npm)**: add an npm/rhtpa-ui row to the Ecosystem Mappings (lock file `package-lock.json`, upstream branch) and add rhtpa-ui to Source Repositories, or assess webpack versions per 2.2.x release by hand.
2. **Stale matrix** (128 days): refresh it through setup Step 10.6.
3. **Overdue**: the due date 2026-08-15 has passed.
4. All Jira mutations above are proposals and need explicit engineer confirmation. None were executed.

## Post-triage (proposed)

- Add the `ai-cve-triaged` label to TC-8011.
- Post a summary comment with the impact table (once assessed), the overlap finding (TC-8013 at 5.96.1 does not cover 5.98.0), the remediation task links, the release Jira references, and an @mention of the reporter, plus the Comment Footnote.
