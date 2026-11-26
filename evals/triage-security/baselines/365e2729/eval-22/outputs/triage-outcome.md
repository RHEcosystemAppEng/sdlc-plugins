# Triage Outcome: TC-8021 (CVE-2026-31812, quinn-proto < 0.11.14)

## Decision: AFFECTED. Case A (cross-stream impact) + Case B (remediation for 2.2.x)

TC-8021 is scoped to stream **2.2.x**. Lock-file evidence shows RHTPA 2.2.0,
2.2.1, and 2.2.2 (a retag of 2.2.1) ship quinn-proto 0.11.9 or 0.11.12. Both are
below the 0.11.14 fix threshold. 2.2.3 and 2.2.4 ship 0.11.14 and are not affected.
Stream 2.1.x (2.1.0, 2.1.1 at 0.11.9) is also affected, but it is outside this
issue's scope.

## Step-by-step summary

| Step | Result |
|---|---|
| 0 Config | Valid. Upstream Affected Component field = customfield_10632 |
| 0.3 Staleness | Matrix is 151 days old (STALE). Proceeding with a caveat; a refresh is recommended |
| 0.8 Assign | Proposed: assign to the current user and transition New -> Assigned |
| 1 Extraction | CVE-2026-31812, quinn-proto, < 0.11.14, fixed 0.11.14, scoped to 2.2.x, Cargo |
| 1.5 Enrichment | External APIs not queried. Jira description data used; confidence reduced |
| 1.7 Embargo | Skipped (no embargo URL configured) |
| 2 Impact | 2.2.0/2.2.1/2.2.2 YES; 2.2.3/2.2.4 NO; 2.1.0/2.1.1 YES (out of scope); dev stream not determined |
| 3 Affects Versions | Proposed: `[RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]` plus a correction comment (with footnote, no ProdSec @mention because none is configured) |
| 4 Duplicates/siblings | JQL for siblings with label CVE-2026-31812 not executed. No sibling data was provided, so none are assumed. Step 4.3 overlap uses cf[10632] = quinn-proto; no overlap data was provided |
| 5 Lifecycle | Product pages not fetched. 2.2.x is assumed supported (it is in the matrix) |
| 6 Already fixed | No resolved siblings known, so proceed |
| 7 Concurrent triage | JQL returned 0 results, so proceed silently with no `concurrent-triage-overlap` label (see concurrent-triage.md) |
| 7.5 Release Jira | Find or create the "RHTPA 2.2.x Release Tasks" Epic and the "RHTPA 2.2.x CVE triage" Task. Each creation needs individual confirmation; the next patch version (likely 2.2.5) must be confirmed by the engineer. Cross-CVE dedup against existing quinn-proto remediation is not checkable here |
| 8 Remediation | Case A + Case B (below) |

## Case A: Cross-stream impact (scoped issue, other stream affected)

1. Post a comment on TC-8021:
   "Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x
   (RHTPA 2.1.0, 2.1.1 ship 0.11.9) based on lock file analysis. These streams are
   tracked by companion issues (see Related links) or may require separate PSIRT
   triage." The comment includes the Comment Footnote.
2. If the Step 4 sibling search finds no `[rhtpa-2.1]` CVE Jira, create **preemptive**
   tasks for 2.1.x. These carry the `security-preemptive` label and are linked to
   TC-8021 as "Related". Source: backend `release/0.3.z`. The upstream fix status is
   unknown, so treat it as an upstream backport plus downstream propagation in
   rhtpa-release.0.3.z. If a 2.1.x sibling exists, skip this.

## Case B: Remediation tasks for 2.2.x (Cargo, source dependency, 2 tasks)

Released tags v0.4.11 and v0.4.12 already ship quinn-proto 0.11.14, so the
`release/0.4.z` branch very likely already contains the fix. This should be
confirmed with `git show release/0.4.z:Cargo.lock` in a live run. That makes this
the **fix-available** variant:

1. **Dependency bump task (rhtpa-backend, release/0.4.z):** verify that quinn-proto
   is >= 0.11.14 (run `cargo update -p quinn-proto` if needed) and document the
   dependency chain. Since 2.2.3+ already ship the fix, this task may only need to
   verify and record it. Coordination guidance: `upstream` deployment context.
2. **Downstream propagation task (rhtpa-release.0.4.z):** make sure the next 2.2.x
   release pins a backend tag that ships quinn-proto >= 0.11.14 (v0.4.11 or later).
   This task is Blocked by task 1.

Links: both tasks -> TC-8021 (Depend); task 1 -> task 2 (Blocks); both tasks ->
the release Task (Blocks); TC-8021 -> the release Task (Related). After each task is
created, post a description digest comment. Labels follow
`remediation-templates.md`.

Note for the engineer: because current 2.2.x releases (2.2.3, 2.2.4) are already
fixed, the practical remedy for 2.2.0-2.2.2 customers is to upgrade to 2.2.3 or
later. Remediation tasks are still proposed according to the skill's Case B rules,
but the engineer may decide at the confirmation gate that the tasks only need
verification.

Not Case C: supported versions in scope are affected, so closing as Not a Bug and
setting VEX do not apply.

## Post-triage (proposed, pending confirmation)

- Add the label `ai-cve-triaged` to TC-8021.
- Post a summary comment containing: the version impact table, the Affects Versions
  correction, the outcome, the remediation task links, the release Jira refs, dedup
  results (none), an @mention of the reporter, and the Comment Footnote.

## Caveats

- No Jira writes were performed. Every mutation above needs engineer confirmation.
- The issue key in the mock file (TC-8001) differs from the task (TC-8021); TC-8021
  was used.
- The matrix is stale (151 days). The dev stream, the upstream HEAD state, siblings,
  and lifecycle were not verifiable without external calls.
- The due date (2026-07-15) has already passed.
