# Ready for QA — Filtering Analysis

**Query 3 JQL:**
`project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC`
Fields: summary, labels, status, created, issuelinks (maxResults 20)

**Filtering rules (SKILL.md, Discovery mode, Query 3):**
1. For each candidate, collect `issuelinks` entries where `type.name == "Depend"` and
   fetch each linked Task's status (taken from the mock data here; no live fetch).
2. ALL linked Depend Tasks are Done or Closed → **include** (Ready for QA).
3. ANY linked Depend Task is still open → **exclude** (remediation in progress).
4. NO Depend links → **exclude** (no remediation to verify).

## Candidate evaluation

| Issue | CVE | Status | Depend-linked Tasks | Rule applied | Result |
|-------|-----|--------|---------------------|--------------|--------|
| TC-9020 | CVE-2026-38901 (hyper) | Modified | TC-9021 (Done), TC-9022 (Closed) | 2 — every Task is Done/Closed | **Ready for QA** |
| TC-9023 | CVE-2026-39102 (rustls) | In Progress | TC-9024 (Done), TC-9025 (In Progress) | 3 — TC-9025 still open | **Excluded** |
| TC-9026 | CVE-2026-39330 (openssl) | Modified | none | 4 — no Depend links | **Excluded** |

### TC-9020 — QUALIFIES
- Depend links: 2 found.
  - TC-9021: Done (complete)
  - TC-9022: Closed (complete)
- 2 of 2 remediation Tasks complete, so remediation is finished.
- **Recommendation:** Consider transitioning to ON_QA. This needs explicit engineer
  confirmation before any Jira write; none was made here.

### TC-9023 — EXCLUDED
- Depend links: 2 found.
  - TC-9024: Done (complete)
  - TC-9025: In Progress (open)
- 1 of 2 complete. One open Task is enough to exclude the issue: remediation is still in progress.
- Revisit once TC-9025 is Done or Closed.

### TC-9026 — EXCLUDED
- Depend links: none.
- With no linked remediation Tasks there is nothing to verify. Status Modified is not
  enough on its own to qualify.
- Possible follow-up: check whether remediation was tracked outside Depend links,
  or whether the issue needs re-triage.

## Summary
- Candidates evaluated: 3
- Ready for QA: 1 (TC-9020)
- Excluded: 2 (TC-9023 — open Task; TC-9026 — no Depend links)

No Jira, git, or external tools were called. All statuses come from the provided mock results.
