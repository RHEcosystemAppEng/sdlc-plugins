# triage-security: Discovery Mode Results (Project TC)

No issue key was given, so the skill ran in discovery mode.

**Configuration check (Step 0):** passed. Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`, Vulnerability issue type ID `10024`, Component label pattern `pscomponent:`, Jira version prefix `RHTPA`. Version Streams: 2.1.x, 2.2.x. Source Repositories: rhtpa-backend.

**Mode (Step 0.6):** interactive. `FULLSEND_OUTPUT_DIR` is not set.

---

## 1. Untriaged (4 issues)

JQL: `project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC`

### Status: New

1. **TC-9001** | New | CVE-2026-40112 | CVE-2026-40112 h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | Created 2026-06-08
2. **TC-9002** | New | CVE-2026-40297 | CVE-2026-40297 serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | Created 2026-06-07
3. **TC-9004** | New | CVE-2026-40518 | CVE-2026-40518 ring - Timing side-channel in RSA verification [rhtpa-2.2] | Created 2026-06-04

### Status: In Progress

4. **TC-9003** | In Progress | CVE-2026-40455 | CVE-2026-40455 tokio - Race condition in task cancellation [rhtpa-2.2] | Created 2026-06-05
   - Note: this issue is already In Progress. If you select it, the skill will warn that someone may be working on it and ask whether to proceed or skip.

---

## 2. Triaged but still New (1 issue)

> **Flag:** these issues have the `ai-cve-triaged` label but are still in New status. They were triaged and never moved forward, so they may need follow-up or re-triage.

JQL: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC`

1. **TC-9010** | New | CVE-2026-39874 | CVE-2026-39874 quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | Created 2026-05-28

---

## 3. Ready for QA (1 issue)

Triaged CVEs whose linked remediation Tasks (link type "Depend") are all Done or Closed.

JQL: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC`

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

- **TC-9020:** Consider transitioning to ON_QA.

Candidates excluded (details in `ready-for-qa.md`):
- TC-9023 (CVE-2026-39102, rustls): TC-9025 is still In Progress, so remediation is not finished.
- TC-9026 (CVE-2026-39330, openssl): has no "Depend" links, so there is no remediation to verify.

---

## 4. Release Jira Summary

JQL: `project = TC AND issuetype = Task AND summary ~ 'RHTPA' AND summary ~ 'CVE triage' ORDER BY created DESC`

The eval input did not include results for this query, so there is no release-progress table to show. Run the query against Jira to fill in this section.

---

**Next step:** pick an issue key from the Untriaged or Triaged-but-still-New lists to start the full 8-step triage, for example `/sdlc-workflow:triage-security TC-9001`. Discovery mode made no Jira changes.
