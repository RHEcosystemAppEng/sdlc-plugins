# Discovery Mode — Security Vulnerability Listing (Project TC)

Invoked without an issue key, so discovery mode ran. Configuration comes from the project CLAUDE.md (Security Configuration):
- Project key: TC
- Vulnerability issue type ID: 10024
- Jira version prefix: RHTPA

---

## 1. Untriaged (4 issues)

Query: `project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC`

### Status: New

1. **TC-9001** | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | Created 2026-06-08
2. **TC-9002** | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | Created 2026-06-07
3. **TC-9004** | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | Created 2026-06-04

### Status: In Progress

4. **TC-9003** | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | Created 2026-06-05
   - Note: already In Progress and may be actively worked on. If you select it, you'll be asked whether to triage it anyway or skip it.

---

## 2. Triaged but still New (1 issue)

Query: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC`

> **Flagged:** these issues were triaged (`ai-cve-triaged`) but never moved forward. They may need follow-up or re-triage.

1. **TC-9010** | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | Created 2026-05-28

---

## 3. Ready for QA (1 issue)

Query: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC`

Triaged CVEs where every linked remediation Task is completed. The query returned 3 candidates. After checking their Depend links, 1 qualified (see ready-for-qa.md for details).

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

- **TC-9020**: Consider transitioning to ON_QA.

Excluded candidates:
- TC-9023 (CVE-2026-39102, rustls): remediation is still in progress because TC-9025 is In Progress.
- TC-9026 (CVE-2026-39330, openssl): has no Depend-linked remediation Tasks, so there is nothing to verify.

---

## 4. Release Jira Summary

Query: `project = TC AND issuetype = Task AND summary ~ 'RHTPA' AND summary ~ 'CVE triage' ORDER BY created DESC`

The eval input files have no release Task results, so this summary could not be filled in.

---

**Next step:** pick an issue from the Untriaged list (or the Triaged-but-still-New list) to start triage, e.g. `/sdlc-workflow:triage-security TC-9001`.
