# Discovery Mode — Vulnerability Issues in Project TC

Invoked without an issue key, so discovery mode ran. Configuration came from the project CLAUDE.md:
- Project key: TC
- Vulnerability issue type ID: 10024
- Jira version prefix: RHTPA

Jira MCP was not called. Results come from the mock JQL output in `discovery-mode-results.md`.

---

## 1. Untriaged (4 issues)

JQL: `project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC`

### New

1. **TC-9001** | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | Created 2026-06-08
2. **TC-9002** | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | Created 2026-06-07
3. **TC-9004** | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | Created 2026-06-04

### In Progress

4. **TC-9003** | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | Created 2026-06-05
   - Note: this issue is already In Progress, so someone may be working on it. If you select it, I will ask whether to triage anyway or skip it.

---

## 2. Triaged but still New (1 issue)

JQL: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC`

5. **TC-9010** | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | Created 2026-05-28
   - **Flag:** this issue has the `ai-cve-triaged` label but is still in New. It may need follow-up or re-triage.

---

## 3. Ready for QA (1 issue)

JQL: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC`

The query returned 3 candidates. Only issues whose "Depend" remediation Tasks are all Done or Closed are listed here. See `ready-for-qa.md` for the full filtering analysis.

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

- **TC-9020:** Consider transitioning to ON_QA.

Candidates excluded:
- TC-9023 (CVE-2026-39102, rustls): remediation is still in progress because TC-9025 is In Progress.
- TC-9026 (CVE-2026-39330, openssl): it has no "Depend" remediation Tasks, so there is nothing to verify.

---

## 4. Release Jira Summary

JQL: `project = TC AND issuetype = Task AND summary ~ 'RHTPA' AND summary ~ 'CVE triage' ORDER BY created DESC`

The eval inputs include no mock results for this query, so this table cannot be filled in.

| Release Epic | Release Task | CVEs Tracked | Remediation Done | Remediation Pending |
|-------------|-------------|-------------|-----------------|-------------------|
| (no data provided) | — | — | — | — |

---

## Next step

Choose an issue to triage by number or key, for example `TC-9001`. You can also act on a Ready for QA item, for example by transitioning TC-9020 to ON_QA.
