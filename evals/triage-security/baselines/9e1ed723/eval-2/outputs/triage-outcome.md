# TC-8002 — Triage Outcome (Steps 3–8 and Post-Triage)

## Decision

**Case C: no supported versions are affected. Recommend closing TC-8002 as "Not a Bug"
with VEX Justification "Component not Present".**

CVE-2026-28940 affects serde_json < 1.0.135. Lock file evidence at every pinned backend
commit shows serde_json 1.0.137–1.0.139 in all supported RHTPA versions (2.1.0–2.2.4). The
fix (recursion limit, default 128) is already shipped everywhere. The PSIRT assignment of
RHTPA 2.2.0 is a false positive: it most likely comes from scanning for the package name
without comparing versions. No remediation tasks are needed.

## Step-by-step results

### Step 3 – Affects Versions correction
- Jira version discovery (`getJiraIssueTypeMetaWithFields`, project TC, issue type 10024)
  was not run in this eval. Version IDs would be resolved at runtime and never hardcoded.
- The issue is scoped to stream 2.2.x. Affected 2.2.x versions according to lock files: **none**.
- Diff: `Current: [RHTPA 2.2.0] → Proposed: []` (no versions affected).
- Because the outcome is closure as not affected, the correction goes into the closure
  comment. RHTPA 2.2.0 is shown as incorrectly attributed. Clearing the field is optional
  and needs engineer confirmation. Many workflows keep the PSIRT-reported version on
  Not-a-Bug closures for VEX traceability, so the engineer should choose.
- No ProdSec @mention (ProdSec Jira account ID not configured).

### Step 4 – Duplicate / sibling / overlap / reconciliation
- Sibling JQL (would run): `project = TC AND labels = 'CVE-2026-28940' AND issuetype = 10024 AND key != TC-8002`.
  It was not run in this eval and no sibling data was provided, so I assume there are no
  siblings. In a real run, any 2.1.x companion would get a Related link. Since 2.1.x is also
  not affected, that companion would get the same not-affected closure.
- 4.3 Cross-CVE overlap: **skipped** (Upstream Affected Component field not configured).
- 4.4 Preemptive task reconciliation (would run): `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-28940'`.
  No data, so I assume none exist. If one existed, it would be obsolete because nothing is
  affected, and the engineer should be told.

### Step 5 – Version lifecycle
Not needed: there are no affected versions to check against the product pages URL. It was
not fetched.

### Step 6 – Already fixed check
- No resolved sibling issues are known, so the sibling-based "already fixed" closure does
  not apply.
- The issue is effectively "already fixed" in a different sense: every shipped build
  already contains the upstream fix version or newer. Under the skill's rules this is a
  **not-affected** finding (Case C, VEX applies). It is not a sibling-resolution closure,
  which would set no VEX.

### Step 7 – Concurrent triage detection
**Skipped** (Upstream Affected Component field not configured).

### Step 7.5 – Release Jira orchestration
Not applicable. No stream needs remediation, so no release Epic or Task is found or created,
and no cross-CVE dedup runs.

### Step 8 – Remediation branching
- No supported versions are affected → **Case C**.
- Case A (cross-stream impact comment): not triggered, because 2.1.x is also not affected.
- Case B (remediation tasks): not triggered. **0 tasks created.**
- VEX Justification: **Component not Present**. This is the skill's default when lock file
  analysis shows the vulnerable package version is not included. serde_json is shipped, but
  only at patched versions; no vulnerable version is present.

## Proposed Jira actions (each needs engineer confirmation; none were executed)

| # | Step | Operation | Details |
|---|---|---|---|
| 1 | 0.8 | Assign | `edit_issue(TC-8002, assignee=<current-user-account-id>)` (from `user_info()`) |
| 2 | 0.8 | Transition | New → **Assigned** (transition ID found dynamically via `get_transitions(TC-8002)`) |
| 3 | 3 | (Optional) Affects Versions | `RHTPA 2.2.0` → none. Engineer decides; documented in comment #4 either way |
| 4 | 8 Case C | Add comment | Not-affected closure comment (draft below), with Comment Footnote |
| 5 | 8 Case C | Set VEX field | `customfield_12345` = "Component not Present" |
| 6 | 8 Case C | Transition | → **Closed**, resolution **"Not a Bug"** |
| 7 | Post-triage | Add label | `ai-cve-triaged`, keeping existing labels `CVE-2026-28940` and `pscomponent:org/rhtpa-server` |
| 8 | Post-triage | Summary comment | Audit-trail summary (draft below), @mention of the issue reporter, Comment Footnote |

No links, no remediation Tasks, no release Epic/Task, and no Vulnerability issues are created.

### Draft comment #4 — Case C closure

> No supported versions ship a vulnerable version of serde_json.
>
> Version impact analysis (Cargo.lock at pinned backend commits from security-matrix.md):
>
> | Version | serde_json | Affected? |
> |---|---|---|
> | 2.1.0 | 1.0.137 | NO |
> | 2.1.1 | 1.0.137 | NO |
> | 2.2.0 | 1.0.138 | NO |
> | 2.2.1 | 1.0.138 | NO |
> | 2.2.2 | — (retag of 2.2.1) | NO |
> | 2.2.3 | 1.0.139 | NO |
> | 2.2.4 | 1.0.139 | NO |
>
> All supported versions ship serde_json 1.0.137–1.0.139, which is outside the affected range
> (< 1.0.135; fixed in 1.0.135). The PSIRT-assigned Affects Version RHTPA 2.2.0 ships
> serde_json 1.0.138 and is not affected. Closing as Not a Bug, VEX: Component not Present.
>
> ---
> This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.

### Draft comment #8 — Post-triage summary

> **Triage summary for CVE-2026-28940 (serde_json < 1.0.135)**, scoped to stream 2.2.x
>
> 1. Version impact: 0/7 supported versions affected (see table above). 2.1.x was also checked and is not affected.
> 2. Affects Versions: RHTPA 2.2.0 was attributed incorrectly. It ships serde_json 1.0.138.
> 3. Outcome: Closed, Not a Bug. VEX Justification: Component not Present.
> 4. Remediation tasks: none (not required).
> 5. Release Jira: none (no remediation needed).
> 6. Dedup: not applicable.
>
> @<reporter> (ADF mention node using the reporter accountId from the issue data. The reporter
> was not in the mock input, so it must be resolved from `get_issue` at runtime.)
>
> ---
> This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.

## Caveats / limitations of this eval run
- Security matrix is 148 days old (stale). I proceeded anyway; a refresh is advisable.
- MITRE/OSV enrichment was not done, so the fix threshold comes only from the Jira
  description. The 2-patch-version margin (1.0.137 vs 1.0.135) makes the result robust.
- Development stream HEAD and upstream branch HEADs were not checked (no data). They were
  marked not verified rather than assumed.
- Sibling, preemptive-task and Jira version lookups were not run. The results above assume
  none exist.
