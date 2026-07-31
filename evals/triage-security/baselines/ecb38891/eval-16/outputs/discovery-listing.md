# Discovery Mode — Vulnerability Issue Listing

## Step 0 — Configuration Extraction

Extracted from project CLAUDE.md (Security Configuration):

- **Project key**: TC
- **Vulnerability issue type ID**: 10024
- **Jira version prefix**: RHTPA

These values are used to construct all three JQL queries below.

---

## Query 1: Untriaged Issues

**JQL query constructed from Security Configuration:**

```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Results** (4 issues):

### New

1. **TC-9001** — `New` — CVE-2026-40112 — CVE-2026-40112 h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] — Created: 2026-06-08
2. **TC-9002** — `New` — CVE-2026-40297 — CVE-2026-40297 serde_json - Stack overflow on deeply nested input [rhtpa-2.1] — Created: 2026-06-07
3. **TC-9004** — `New` — CVE-2026-40518 — CVE-2026-40518 ring - Timing side-channel in RSA verification [rhtpa-2.2] — Created: 2026-06-04

### In Progress

4. **TC-9003** — `In Progress` — CVE-2026-40455 — CVE-2026-40455 tokio - Race condition in task cancellation [rhtpa-2.2] — Created: 2026-06-05
   > **Warning**: This issue is already in `In Progress`. It may be actively worked on. Selecting this issue will prompt whether to proceed with triage anyway or skip.

### Status-aware handling

- **TC-9001, TC-9002, TC-9004** (New): Ready for full triage (default path).
- **TC-9003** (In Progress): Warning — this issue may be actively worked on. If selected, the engineer will be asked whether to proceed with triage or skip.

---

## Query 2: Triaged but still New

**JQL query constructed from Security Configuration:**

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**Results** (1 issue):

1. **TC-9010** — `New` — CVE-2026-39874 — CVE-2026-39874 quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] — Created: 2026-05-28

These issues were triaged (have the `ai-cve-triaged` label) but remain in `New` status. They may need follow-up or re-triage.

---

## Query 3: Ready for QA Candidates

**JQL query constructed from Security Configuration:**

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query finds triaged CVEs that are still in a pre-QA state (not yet Closed, Verified, or ON_QA). For each result, the skill checks the issue's `issuelinks` for linked Tasks with link type "Depend" and fetches each linked Task's status to determine whether all remediation work is complete.

**Filtering criteria:**
- ALL linked remediation Tasks (via Depend link type) must be Done or Closed to qualify.
- If ANY linked Task is still open (not Done/Closed), the issue is excluded — remediation is still in progress.
- If NO linked Tasks with type "Depend" exist, the issue is excluded — there is no remediation to verify.

**Results** (3 candidates evaluated, 1 qualified):

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

> Consider transitioning TC-9020 to ON_QA.

**Excluded issues:**

- **TC-9023** (CVE-2026-39102, In Progress) — Excluded: TC-9025 is still In Progress. Remediation is not yet complete.
- **TC-9026** (CVE-2026-39330, Modified) — Excluded: No linked Tasks with type "Depend". No remediation to verify.

---

Select an issue key to begin triage, or choose a Ready for QA issue to transition to ON_QA.
