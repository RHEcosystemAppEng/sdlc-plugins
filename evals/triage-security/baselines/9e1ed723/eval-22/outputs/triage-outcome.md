# Triage Outcome: TC-8021 (CVE-2026-31812, quinn-proto < 0.11.14) [rhtpa-2.2]

## Decision

**Affected. Remediation is needed (Case A + Case B). Do not close.**

The issue is scoped to 2.2.x. Lock file evidence shows that supported 2.2.x versions **RHTPA 2.2.0, 2.2.1 and 2.2.2** ship a vulnerable quinn-proto (0.11.9 / 0.11.12 / retag of 0.11.12). The other stream, 2.1.x, is also affected (2.1.0 and 2.1.1 ship 0.11.9). That triggers the Case A cross-stream path. Case C (Not a Bug) does not apply, because some supported versions ship a version inside the affected range.

## Step-by-step summary

| Step | Result |
|---|---|
| 0 Config | Valid. Upstream Affected Component = customfield_10632. PS Component and Stream fields not configured. No embargo URL. VEX = customfield_12345 |
| 0.3 Staleness | Matrices last updated 2026-06-28, 148 days old (limit is 14). Warned; proceeding anyway for the eval. Releases after 2026-05-04 may be missing |
| 0.6/0.7 | Interactive mode. No Fullsend input |
| 0.8 | Proposed: assign to current user and transition New → Assigned |
| 1 Extraction | CVE-2026-31812, quinn-proto, < 0.11.14, fixed in 0.11.14, CVSS 7.5. Scope: 2.2.x. Ecosystem: Cargo |
| 1.5 Enrichment | External APIs not queried, so Jira description data is used with reduced confidence |
| 1.7 Embargo | Skipped (no policy URL configured) |
| 2 Impact | 2.2.0 YES, 2.2.1 YES, 2.2.2 YES (retag of 2.2.1), 2.2.3 NO, 2.2.4 NO. 2.1.0 YES, 2.1.1 YES. Dev stream could not be determined (no data) |
| 3 Affects Versions | Change needed (see below) |
| 4 Siblings/overlap | No sibling or preemptive-task data was provided, so no siblings are assumed. 4.3 skipped because PS Component and Stream fields are not configured |
| 5 Lifecycle | The product pages URL was not fetched. All versions are treated as supported, so this needs engineer confirmation |
| 6 Already fixed | No resolved siblings, so it does not apply |
| 7 Concurrent triage | JQL returned 0 results, so the step proceeds silently with no overlap label |
| 7.5 Release Jira | Find or create a release Epic and Task for the next 2.2.x release. The version choice (e.g. 2.2.5) needs individual engineer confirmation |
| 8 Remediation | Case A + Case B (below) |

## Step 3 – Affects Versions correction (proposed, needs confirmation)

The PSIRT value is wrong: no RHTPA 2.0.0 stream exists. The correction is scoped to stream 2.2.x:

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

RHTPA 2.2.3 and 2.2.4 are excluded because they ship 0.11.14. 2.1.0 and 2.1.1 are excluded because they belong to the 2.1.x stream. Jira version IDs would come from `getJiraIssueTypeMetaWithFields`, not hardcoded values. A correction comment with the Comment Footnote goes on the issue. There is no ProdSec @mention because none is configured.

## Step 8 – Remediation

### Important nuance for 2.2.x (fix already available)

Upstream branch `release/0.4.z` already ships quinn-proto 0.11.14, and has since tag v0.4.11 (RHTPA 2.2.3, 2026-03-23). The 2.2.x stream is therefore on the **"Source dependency (fix available)"** path. No upstream backport is needed. Customers on 2.2.0–2.2.2 are fixed by moving to RHTPA 2.2.3 or later. The engineer should confirm whether the 2.2.x tasks below are still wanted, or whether the dependency-bump task can be closed straight away once release/0.4.z HEAD is confirmed at ≥ 0.11.14.

### Case B: stream 2.2.x (in scope), 2 tasks

1. **Dependency bump** in rhtpa-backend on `release/0.4.z`: make sure `Cargo.lock` pins quinn-proto ≥ 0.11.14. This is expected to be already satisfied; check HEAD.
2. **Downstream propagation** in rhtpa-release.0.4.z: make sure the backend tag referenced in `artifacts.lock.yaml` is ≥ v0.4.11. This task is blocked by task 1.

Links: both tasks Depend-linked to TC-8021. Task 1 Blocks task 2. Both tasks Block the 2.2.x release Task, and TC-8021 is Related to that release Task. Each task gets a description digest comment.

### Case A: stream 2.1.x (outside scope), preemptive tasks

- Post a cross-stream impact comment on TC-8021:
  "Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x (RHTPA 2.1.0, 2.1.1 ship 0.11.9) based on lock file analysis. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage." The comment includes the Comment Footnote.
- No sibling CVE Jira for 2.1.x was found in the provided data, so create **2 preemptive tasks** for 2.1.x. Each carries the `security-preemptive` label and is linked to TC-8021 as "Related" (not Depend):
  1. Upstream backport on rhtpa-backend `release/0.3.z`: bump quinn-proto to ≥ 0.11.14. Upstream fix status on release/0.3.z is unknown, and the latest tag v0.3.12 still ships 0.11.9. Coordinate with upstream PR quinn-rs/quinn#2048.
  2. Downstream propagation in rhtpa-release.0.3.z. This task is blocked by task 1.
- Post a comment listing the preemptive tasks.

### Not taken

- Case C (Not a Bug) does not apply. VEX Justification is not set.
- No Vulnerability issues are created.

## Post-triage (after confirmation)

- Add the label `ai-cve-triaged` to TC-8021.
- Post a summary comment with: the impact table, the Affects Versions correction, the outcome, task links, release Epic and Task keys, dedup results (none), an @mention of the reporter, and the Comment Footnote.

## Caveats for the engineer

- The matrix is 148 days stale. A refresh is recommended before running the mutations.
- The due date (2026-07-15) has passed.
- The development stream and the release-branch HEAD versions could not be checked with the provided evidence.
- The mock issue key (TC-8001) differs from the requested key (TC-8021).
