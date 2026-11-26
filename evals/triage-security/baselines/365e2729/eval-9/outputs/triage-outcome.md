# Triage Outcome: TC-8011 (CVE-2026-45678, webpack, [rhtpa-2.2])

## Decision

**Do not close. Proceed with new remediation (Step 8 Case B) for stream 2.2.x.**
The cross-CVE overlap check (Step 4.3) found a related webpack CVE in the same
stream and component, TC-8012 / CVE-2026-43210. Its remediation task TC-8013
bumps webpack only to **5.96.1**. That's below this CVE's fix threshold of
**5.98.0** (5.96.1 < 5.98.0), so the existing remediation doesn't cover
CVE-2026-45678 and a new bump to >= 5.98.0 is required.

## Step-by-step summary

| Step | Result |
|------|--------|
| 0 Config | Valid. Assumption: the Upstream Affected Component, PS Component, and Stream fields (10632/10669/10832) are treated as configured per the task context; the mock CLAUDE.md doesn't list them. |
| 0.3 Staleness | Matrices last updated 2026-06-28, now 151 days old (threshold 14). Warning raised; the eval continues with "Proceed anyway". A refresh is recommended. |
| 0.8 Assign | Would assign TC-8011 to the current user and move it New to Assigned (after confirmation; not executed). |
| 1 Extraction | CVE-2026-45678, webpack (npm), affected < 5.98.0, fixed 5.98.0, CVSS 7.8, scoped to 2.2.x. |
| 1.5 Enrichment | Skipped (no external calls). Uses the Jira description only, with reduced confidence. |
| 1.7 Embargo | No policy URL configured, so skipped. |
| 2 Version impact | **Can't be established from the provided evidence.** The 2.2.x Ecosystem Mappings list only Cargo and RPM: no npm entry, no `rhtpa-ui` repo, no webpack lock-file data. No versions were invented. |
| 3 Affects Versions | Not corrected. RHTPA 2.2.0 stays as is until lock-file evidence exists. |
| 4.1 / 4.2 Siblings | No same-CVE siblings. |
| 4.3 Cross-CVE overlap | TC-8012 matches (webpack / rhtpa-ui / rhtpa-2.2). TC-8013 bumps to 5.96.1, **below** 5.98.0, so **NOT COVERED**. No Related/Depend links or overlap comment are created, and closure isn't recommended. |
| 4.4 Preemptive | None found. |
| 5 Lifecycle | Not fetched (external call). Assumed to need verification. |
| 6 Already fixed | No resolved same-CVE siblings. TC-8012 is a different CVE, and its fix doesn't reach 5.98.0. Not already fixed. |
| 7 Concurrent triage | No In Progress / Code Review webpack CVEs in the mock data (TC-8012 is Closed). Proceed. |
| 7.5 Release Jira | Find or create the RHTPA 2.2.x release Epic/Task (the latest released version in the matrix is 2.2.4, so the default proposal is 2.2.5; needs confirmation). **7.5.3 dedup must not match TC-8013**: it shares the `webpack` component but was shown in 4.3 not to meet the threshold, and it's already Closed. |
| 8 Remediation | Case B for 2.2.x (see below). Case A doesn't apply: only the 2.2.x stream ships rhtpa-ui as far as the provided data shows, and 2.1.x has no npm mapping either. |

## Why the overlap does not short-circuit the triage

- Step 4.3 short-circuits to "close, covered by existing task" only when the
  existing bump version **meets or exceeds** the current CVE's fix threshold.
- TC-8013's target is 5.96.1. It was sized for CVE-2026-43210 (needs >= 5.96.0),
  not for CVE-2026-45678 (needs >= 5.98.0).
- After TC-8013, rhtpa-ui is expected to be on webpack 5.96.1, which is still in
  the vulnerable range `< 5.98.0`.
- Linking TC-8011 to TC-8013 with Depend would wrongly mark this CVE as
  remediated by a closed task that doesn't fix it. That link is intentionally
  not created.

## Proposed remediation (subject to engineer confirmation and Step 2 evidence)

Ecosystem npm is a source dependency, so there are **2 tasks** for stream 2.2.x,
each linked to TC-8011 with **Depend**:

1. **Dependency bump / upstream task**: "Bump webpack to >= 5.98.0 in rhtpa-ui (rhtpa-2.2)"
   - Labels: `ai-generated-jira`, `CVE-2026-45678` (plus `dev-dependency` and priority Normal if Step 2.3.5 confirms webpack is build-only, which is likely for webpack)
   - Notes: the current baseline is probably 5.96.1 from TC-8013; target >= 5.98.0. Use the dependency-bump variant if Step 2.5 confirms 5.98.0 is available upstream, otherwise the upstream-backport variant. Deployment context is `upstream` (default).
2. **Downstream propagation task**: propagate the fixed rhtpa-ui build into the rhtpa-release.0.4.z Konflux release repo. Blocked by task 1 (**Blocks**).
- Release linking: both tasks Block the RHTPA 2.2.x release Task, and TC-8011 is Related to the release Task.
- Post-triage: add the `ai-cve-triaged` label and post a summary comment with the version impact, the overlap finding (TC-8012/TC-8013 not covering), the task links, release Jira references, a reporter @mention, and the comment footnote.

## Blockers / items requiring engineer action

1. **Version impact evidence missing (Step 2).** Add an npm Ecosystem Mapping
   (rhtpa-ui, `package-lock.json`) to the 2.2.x security-matrix.md and add
   rhtpa-ui to Source Repositories. Then confirm which webpack version each 2.2.x
   release (2.2.0 to 2.2.4) and the development HEAD actually ship. Under the
   skill's rules, an ecosystem missing from the Ecosystem Mappings table means
   "Unsupported ecosystem: manual assessment required." Task creation should
   wait for that evidence.
2. **Stale matrix.** 151 days since the last update. Refresh it before relying on
   the version list.
3. **Config gap.** Add the Upstream Affected Component (customfield_10632), PS
   Component (customfield_10669), and Stream (customfield_10832) fields to
   Security Configuration so Step 4.3 and Step 7 run without assumptions.
4. **Due date passed** (2026-08-15). Flag this to ProdSec.

No Jira mutations were executed. All proposed changes need explicit engineer
confirmation.
