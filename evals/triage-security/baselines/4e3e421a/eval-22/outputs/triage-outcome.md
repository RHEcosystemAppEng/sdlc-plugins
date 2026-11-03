# Triage Outcome: TC-8021 (CVE-2026-31812, quinn-proto)

## Decision: AFFECTED — remediation required (Case A + Case B)

The issue is scoped to stream 2.2.x (`[rhtpa-2.2]`). Lock file evidence shows supported
2.2.x versions ship quinn-proto below the 0.11.14 fix threshold, so the issue is **not**
closed. The 2.1.x stream (outside this issue's scope) is also affected, triggering the
cross-stream (Case A) path.

## Basis

| Version | quinn-proto | Affected |
|---|---|---|
| 2.1.0 | 0.11.9 | YES (out of scope) |
| 2.1.1 | 0.11.9 | YES (out of scope) |
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | same as 2.2.1 (retag) | YES |
| 2.2.3 | 0.11.14 | NO |
| 2.2.4 | 0.11.14 | NO |

## Step-by-step outcome

1. **Step 0.3** – Matrix is 128 days old (> 14-day threshold); staleness warning raised; proceeded with current matrix.
2. **Step 0.8** – Assign TC-8021 to current user; transition New -> Assigned (requires confirmation).
3. **Step 1.7** – Embargo check skipped (no embargo policy URL configured).
4. **Step 3** – Correct Affects Versions from `RHTPA 2.0.0` to `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2`
   (comment with Comment Footnote; ProdSec @mention skipped – not configured).
5. **Step 4** – Sibling/duplicate search for `CVE-2026-31812` (no sibling data supplied; assumed none,
   so no 2.1.x companion CVE Jira known). Step 4.3 cross-CVE overlap on `quinn-proto` would run
   (field configured).
6. **Step 5** – Lifecycle check of 2.2.0–2.2.2 against product pages (not fetched in eval; assumed supported).
7. **Step 6** – No resolved siblings -> not already fixed.
8. **Step 7** – Concurrent triage JQL (`cf[10632] ~ 'quinn-proto'`, In Progress/Code Review, `key != TC-8021`)
   returned **zero results** -> proceed silently; no `concurrent-triage-overlap` label.
9. **Step 7.5** – Find/create release Epic + release Task for the 2.2.x release family
   (`RHTPA <version> Release Tasks` / `RHTPA <version> CVE triage`); cross-CVE dedup on `quinn-proto`
   — no existing remediation task known, so no dedup.
10. **Step 8** – Remediation:
    - **Case A (cross-stream):** post comment on TC-8021:
      "Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x based on lock file
      analysis..." Create **preemptive** 2-task set for 2.1.x (label `security-preemptive`,
      link type "Related" to TC-8021), then a comment listing the preemptive tasks.
    - **Case B (in scope, 2.2.x):** Cargo = source dependency -> **2 tasks**. Since the stream's
      latest releases (2.2.3 / 2.2.4, tag v0.4.11+) already ship quinn-proto 0.11.14, the fix is
      present on `release/0.4.z` (to be confirmed by Step 2.5) -> **dependency bump variant**:
      1. Dependency bump of quinn-proto to >= 0.11.14 on backend `release/0.4.z` (confirm already
         satisfied at HEAD)
      2. Downstream propagation in rhtpa-release.0.4.z (Blocked by task 1)
      Link both to TC-8021 with "Depend"; task 1 Blocks task 2; both Block the release Task;
      TC-8021 Related to the release Task. Post description digest comment per task.
    - Each task's Implementation Notes uses `upstream` deployment-context coordination guidance.
11. **Post-triage** – Add label `ai-cve-triaged`; post summary comment (impact table, Affects Versions
    correction, outcome, task links, release Jira keys, dedup result: none, @mention of reporter,
    Comment Footnote).

All Jira mutations above are proposals requiring engineer confirmation; none were executed in this eval.

## Not chosen

- **Case C (close as Not a Bug)** — rejected: 2.2.0, 2.2.1, 2.2.2 are affected.
- **VEX Justification** — not set (issue not closed).
