# Security Vulnerability Discovery — Project TC

Discovery mode: no issue key provided. Listing untriaged, stale, and ready-for-QA Vulnerability issues.

**Configuration extracted from CLAUDE.md:**
- Project key: TC
- Vulnerability issue type ID: 10024
- Component label pattern: `pscomponent:`
- Jira version prefix: RHTPA

---

## 1. Untriaged Issues

**JQL:** `project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC`

4 issues found.

### Status: New (3 issues)

1. **TC-9001** | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | Created: 2026-06-08
2. **TC-9002** | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | Created: 2026-06-07
3. **TC-9004** | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | Created: 2026-06-04

### Status: In Progress (1 issue)

4. **TC-9003** | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | Created: 2026-06-05

---

## 2. Triaged but still New (stale)

**JQL:** `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC`

1 issue found. These issues were triaged but never moved forward and may need follow-up or re-triage.

1. **TC-9010** | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | Created: 2026-05-28 | Labels: ai-cve-triaged

---

## 3. Ready for QA

**JQL:** `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC`

3 candidates evaluated; **1 qualifies** for ON_QA transition.

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

**Excluded from Ready for QA:**
- **TC-9023** (In Progress, CVE-2026-39102) — remediation task TC-9025 still In Progress
- **TC-9026** (Modified, CVE-2026-39330) — no linked remediation Tasks (no Depend links)

### Recommendation

- **TC-9020**: All linked remediation Tasks are completed. Consider transitioning to ON_QA.

---

To triage a specific issue, run: `/sdlc-workflow:triage-security TC-XXXX`
