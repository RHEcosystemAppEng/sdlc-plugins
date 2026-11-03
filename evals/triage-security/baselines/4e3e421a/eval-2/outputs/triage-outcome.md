# TC-8002 — Triage Outcome

## Decision

**Case C: no supported versions are affected. Recommend closing TC-8002 as "Not a Bug" with VEX Justification "Component not Present".**

CVE-2026-28940 affects serde_json **< 1.0.135**. Every supported RHTPA release, in both the 2.1.x and 2.2.x streams, ships serde_json **1.0.137, 1.0.138, or 1.0.139** at its pinned backend tag. All of these are at or above the fixed version 1.0.135. PSIRT's Affects Versions value (RHTPA 2.2.0) is wrong: 2.2.0 ships serde_json 1.0.138, which is already patched.

No remediation Tasks will be created. No Vulnerability issues will be created.

## Step-by-step results (Steps 3–8)

### Step 3 – Affects Versions correction (scoped to 2.2.x)

- Current: `[RHTPA 2.2.0]`
- Proposed: `[]`. Remove RHTPA 2.2.0, because no 2.2.x version is affected.
- Rationale: at `v0.4.5` (2.2.0), Cargo.lock pins serde_json 1.0.138, which is ≥ 1.0.135.
- Version IDs would be discovered at runtime via `getJiraIssueTypeMetaWithFields(projectIdOrKey="TC", issueTypeId="10024")`, filtered by prefix `RHTPA`. No IDs are hardcoded.
- Note: when an issue is closed as Not a Bug / Component not Present, some teams keep the PSIRT value for audit purposes instead of clearing it. The skill's lock-file evidence says the correct affected set is empty, so clearing is the proposal. The engineer should confirm.

### Step 4 – Duplicate / sibling / overlap / reconciliation

- 4.1 / 4.2: proposed JQL `project = TC AND labels = 'CVE-2026-28940' AND issuetype = 10024 AND key != TC-8002`. The eval inputs provide no sibling issues, so no same-stream duplicate or cross-stream companion is known. If a 2.1.x companion such as `[rhtpa-2.1]` exists, it is also not affected (2.1.0 and 2.1.1 ship 1.0.137) and should receive the same Case C closure through its own triage.
- 4.3 Cross-CVE overlap: **skipped** because the Upstream Affected Component custom field is not configured.
- 4.4 Preemptive reconciliation: proposed JQL `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-28940'`. No preemptive tasks are present in the eval inputs.

### Step 5 – Version lifecycle

- This step is not needed for the decision because no version is affected. The product pages URL was not fetched because external calls are forbidden.

### Step 6 – Already fixed check

- The eval inputs contain no resolved siblings, so the issue is not "already fixed by sibling". The non-impact comes from the shipped dependency versions themselves, not from a sibling's fix. That is why this is Case C (not affected, with VEX) rather than an already-fixed closure (no VEX).

### Step 7 – Concurrent triage detection

- **Skipped** because the Upstream Affected Component custom field is not configured.

### Step 7.5 – Release Jira orchestration

- **Not applicable.** No stream is affected and no remediation Tasks are needed, so no release Epic or Task is found or created and nothing is linked.

### Step 8 – Remediation branching

- Any supported versions affected? **No**, so the decision is **Case C**.
- Case A (cross-stream impact): not triggered, because 2.1.x is also not affected.
- Case B (remediation tasks): not triggered.

## Proposed Jira actions (each needs engineer confirmation; none were executed)

| # | Action | Details |
|---|---|---|
| 1 | Assign | `jira.edit_issue(TC-8002, assignee=<current-user-account-id>)` (Step 0.8) |
| 2 | Transition to Assigned | Find the target status "Assigned" dynamically via `jira.get_transitions(TC-8002)` (current status is New) |
| 3 | Correct Affects Versions | `jira.edit_issue(TC-8002, fields={"versions": []})`, removing RHTPA 2.2.0 |
| 4 | Comment: Affects Versions correction | See Comment A below. No ProdSec @mention, because none is configured |
| 5 | Comment: Case C close rationale | See Comment B below |
| 6 | Set VEX Justification | `jira.edit_issue(TC-8002, fields={"customfield_12345": {"value": "Component not Present"}})` |
| 7 | Transition to Closed | Find the "Closed" transition dynamically. Resolution is **Not a Bug** |
| 8 | Add label | Add `ai-cve-triaged` to the issue's existing labels: `CVE-2026-28940`, `pscomponent:org/rhtpa-server`, `ai-cve-triaged` |
| 9 | Post-triage summary comment | See Comment C below. Includes an @mention of the reporter |

The VEX choice is **Component not Present**, the skill's default when lock-file analysis shows the vulnerable package version is not included in any shipped version. serde_json itself is present, but only at patched versions. The vulnerable component version is absent, so the code-path justifications do not apply.

### Comment A – Affects Versions correction

```
Corrected Affects Versions: [RHTPA 2.2.0] → [] (none).
Based on lock file analysis at pinned commits from security-matrix.md:
RHTPA 2.2.0 (backend v0.4.5) ships serde_json 1.0.138, which is outside the
affected range (< 1.0.135). No 2.2.x version is affected.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

---
This comment was AI-generated by sdlc-workflow/triage-security v0.13.10.
```

### Comment B – Case C close rationale

```
No supported versions ship a vulnerable version of serde_json.

Version impact analysis (CVE-2026-28940, serde_json < 1.0.135):

| Version | serde_json | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.1.0   | 1.0.137    | NO        | backend v0.3.8 |
| 2.1.1   | 1.0.137    | NO        | backend v0.3.12 |
| 2.2.0   | 1.0.138    | NO        | backend v0.4.5 |
| 2.2.1   | 1.0.138    | NO        | backend v0.4.8 |
| 2.2.2   | —          | NO        | retag of 2.2.1 |
| 2.2.3   | 1.0.139    | NO        | backend v0.4.11 |
| 2.2.4   | 1.0.139    | NO        | backend v0.4.12 |

All supported versions ship serde_json 1.0.137–1.0.139, which is outside the
affected range (< 1.0.135; fixed in 1.0.135).

Closing as Not a Bug. VEX Justification: Component not Present.

---
This comment was AI-generated by sdlc-workflow/triage-security v0.13.10.
```

### Comment C – Post-triage summary

```
Triage summary for CVE-2026-28940 (serde_json stack overflow on deeply nested input)

1. Version impact: no supported RHTPA version is affected (table above);
   all ship serde_json >= 1.0.137 (fix: 1.0.135).
2. Affects Versions correction: [RHTPA 2.2.0] → [] (none).
3. Outcome: Closed as Not a Bug; VEX Justification = Component not Present.
4. Remediation tasks: none created (not affected).
5. Release Jira: none (no remediation required).
6. Dedup: none (no cross-CVE overlap check — Upstream Affected Component field not configured).

@<reporter>  (ADF mention node: {"type":"mention","attrs":{"id":"<reporter-account-id>","text":"@<reporter-name>"}})

---
This comment was AI-generated by sdlc-workflow/triage-security v0.13.10.
```

In each comment, the footnote is rendered as an ADF `rule` node followed by a paragraph that links "sdlc-workflow/triage-security" to https://github.com/RHEcosystemAppEng/sdlc-plugins.

## Caveats for the engineer

1. **Stale matrix (128 days, last updated 2026-06-28).** Releases after 2.2.4, or a newer stream, may be missing from the matrix. Consider refreshing it (setup Step 10.6) before you confirm the closure.
2. **External enrichment unavailable.** MITRE and OSV were not queried, so the fix threshold comes from the Jira description only. The 1.0.137 minimum leaves a margin of two patch releases.
3. **Development stream not assessed.** No unreleased Jira version data or HEAD lock data was available. Confirm with `git show HEAD:Cargo.lock` in rhtpa-backend before closing.
4. **Due date 2026-07-30 has passed.** Closing as Not a Bug resolves the overdue item.
5. **Reporter identity is not in the mock data.** The reporter's account ID must be pulled from the live issue for the mandatory @mention.
