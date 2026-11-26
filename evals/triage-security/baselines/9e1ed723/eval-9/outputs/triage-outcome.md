# Triage Outcome: TC-8011 (CVE-2026-45678, webpack, [rhtpa-2.2])

## Decision

**Not covered by existing remediation. New remediation is required (Case B path), but it is blocked on manual version-impact assessment because npm is not a configured ecosystem.**

TC-8011 must **not** be closed as covered by the earlier webpack remediation. The cross-CVE overlap check (Step 4.3) found related CVE TC-8012 (CVE-2026-43210) and its remediation task TC-8013. TC-8013 bumps webpack only to **5.96.1**, which is **below** this CVE's fix threshold of **5.98.0**. rhtpa-ui in the 2.2 stream is therefore still vulnerable after TC-8013. A new bump to webpack >= 5.98.0 is needed.

## Step-by-step summary

| Step | Result |
|---|---|
| 0 Config | Valid. Upstream Affected Component, PS Component, and Stream fields are not declared in Security Configuration (supplied by task/issue data). |
| 0.3 Staleness | Matrix last updated 2026-06-28, 148 days ago, so it is STALE. Refresh recommended. Proceeded for the eval. |
| 0.8 Assign | Proposed: assign to current user and transition New → Assigned (needs confirmation). |
| 1 Extraction | CVE-2026-45678, webpack < 5.98.0, fixed in 5.98.0, CVSS 7.8, scoped to stream 2.2.x, component pscomponent:org/rhtpa-ui. |
| 1.5 Enrichment | Not queried (no external calls allowed). Jira description threshold 5.98.0 used, with reduced confidence. |
| 1.7 Embargo | Skipped because no embargo policy URL is configured. |
| 2 Version impact | **Cannot be automated.** npm is not in either stream's Ecosystem Mappings, rhtpa-ui is not a configured source repository, and the mock matrix has no webpack lock-file data. The skill says: "Unsupported ecosystem: npm is not yet supported for automated triage. Manual assessment is required." No webpack versions per release were invented. |
| 3 Affects Versions | Cannot verify against lock-file evidence. RHTPA 2.2.0 (PSIRT-assigned) is left unchanged until manual assessment. Indirect evidence: TC-8012/TC-8013 show rhtpa-ui 2.2 shipped webpack 5.95.0 and was bumped to 5.96.1, both below 5.98.0. That is consistent with 2.2.x being affected, but it is not a pinned-commit check for each release. |
| 4 / 4.1 / 4.2 Siblings | No same-CVE siblings. |
| 4.3 Cross-CVE overlap | TC-8012 matches on component, PS component, and stream. Its Depend task TC-8013 bumps to 5.96.1, which is less than 5.98.0, so it **does not cover** this CVE. No Related/Depend links or overlap comment are created. Proceed to new remediation. |
| 4.4 Preemptive | No preemptive task found. |
| 5 Lifecycle | Not fetched (no external calls). Needs a check against the product pages URL before task creation. |
| 6 Already fixed | No resolved same-CVE siblings. TC-8012 is a different CVE and its fix is insufficient, so this is not already fixed. |
| 7 Concurrent triage | No other open webpack CVE triage was reported. TC-8012 is Closed. |
| 7.5 Release Jira | Find or create the RHTPA 2.2.x release Epic/Task (needs confirmation; version comes from the matrix). In 7.5.3, TC-8013 must **not** be counted as a dedup match: it matches by component only and its 5.96.1 bump is below the threshold. |
| 8 Remediation | Case B (scoped to 2.2.x, source-dependency ecosystem), once manual assessment confirms impact. |

## Proposed remediation (pending manual version-impact confirmation and engineer approval)

Two tasks for stream 2.2.x (npm is a source dependency):

1. **Upstream task:** bump webpack to >= 5.98.0 in rhtpa-ui on the 2.2 release branch. The title would be something like "Bump webpack to 5.98.0 in rhtpa-ui [rhtpa-2.2]". Use the dependency-bump variant if Step 2.5 confirms 5.98.0 is available upstream, otherwise the upstream-backport variant. Labels: `CVE-2026-45678`, standard security labels. Linked to TC-8011 with **Depend**. Webpack is normally a build-time dependency, so Step 2.3.5 scope analysis may apply the `dev-dependency` label and set priority to Normal.
2. **Downstream propagation task:** propagate the updated rhtpa-ui into the Konflux release repo `rhtpa-release.0.4.z`. It is **Blocked by** the upstream task and linked to TC-8011 with Depend.

Both tasks: link to the release Task with Blocks, link TC-8011 to the release Task with Related, and post a description digest comment after creation. Coordination guidance uses deployment context `upstream` (the default, since rhtpa-ui is not configured).

Optional informational reference only: the new task description may mention that TC-8013 (CVE-2026-43210) previously bumped webpack to 5.96.1 and that this was not enough for CVE-2026-45678.

## Case A (cross-stream)

The 2.1.x stream (rhtpa-release.0.3.z) cannot be assessed for webpack for the same reason (npm is not mapped). The manual assessment should cover 2.1.x as well. If 2.1.x is affected and has no CVE-2026-45678 Jira, post a cross-stream comment and create preemptive tasks (label `security-preemptive`, link type Related).

## Post-triage (after the actions are confirmed)

- Add the `ai-cve-triaged` label to TC-8011.
- Post a summary comment covering: the version impact status (manual assessment required, npm not mapped), the Affects Versions decision, the overlap finding (TC-8012/TC-8013 at 5.96.1 does not cover 5.98.0), the remediation task keys, the release Jira keys, an @mention of the reporter, and the Comment Footnote.

## Follow-ups for the engineer

1. Add an npm ecosystem row (lock file `package-lock.json` or equivalent) and the rhtpa-ui source repo to the security matrices and Security Configuration, so webpack can be assessed automatically.
2. Refresh the stale security matrices (148 days old).
3. Declare the Upstream Affected Component (customfield_10632), PS Component (customfield_10669), and Stream (customfield_10832) fields in Security Configuration.
4. The due date (2026-08-15) has already passed. Prioritize this work.
