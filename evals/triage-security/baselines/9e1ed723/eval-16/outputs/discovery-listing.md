# Discovery Mode: Vulnerability Issues in TC

Project key: `TC` | Vulnerability issue type ID: `10024` (from Security Configuration)

No issue key was provided, so discovery mode ran the Query 1, Query 2 and Query 3 searches from SKILL.md (Discovery mode). These are mock results; Jira was not called.

---

## 1. Untriaged (4 issues)

JQL: `project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC`

### Status: In Progress

1. **TC-9003**: In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | Created 2026-06-05
   - Note: this issue is already In Progress and may be actively worked on. If you select it, you'll be asked whether to triage it anyway or skip it.

### Status: New

2. **TC-9001**: New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | Created 2026-06-08
3. **TC-9002**: New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | Created 2026-06-07
4. **TC-9004**: New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | Created 2026-06-04

---

## 2. Triaged but still New (1 issue) -- FLAGGED

JQL: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC`

These issues have the `ai-cve-triaged` label but are still in New status. They were triaged but never moved forward and may need follow-up or re-triage.

1. **TC-9010** [STALE]: New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | Created 2026-05-28

---

## 3. Ready for QA (1 issue)

JQL: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC`

These are triaged CVEs where every linked remediation Task ("Depend" links) is Done or Closed. Query 3 returned 3 candidates. Only 1 passed the filter; see `ready-for-qa.md` for the full analysis.

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

- **TC-9020**: Consider transitioning to ON_QA.

Candidates that did not qualify:
- TC-9023 (In Progress, CVE-2026-39102): TC-9025 is still In Progress, so remediation is not finished.
- TC-9026 (Modified, CVE-2026-39330): has no "Depend" links, so there is no remediation to verify.

---

## 4. Release Jira Summary

No mock results were provided for the release Task query (`project = TC AND issuetype = Task AND summary ~ 'RHTPA' AND summary ~ 'CVE triage'`), so this summary could not be produced in the eval.

---

## Next step

Pick an issue number from the Untriaged or Triaged-but-still-New list to start triage, or give an issue key directly (e.g. `/sdlc-workflow:triage-security TC-9001`).
