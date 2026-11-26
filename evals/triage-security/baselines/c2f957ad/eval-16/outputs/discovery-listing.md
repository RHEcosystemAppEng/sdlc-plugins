# triage-security — Discovery Mode Listing

No issue key was given, so the skill ran in **discovery mode** (interactive; `FULLSEND_OUTPUT_DIR` not set).

**Configuration checked (Step 0):**
- Project key: `TC`
- Cloud ID: `2b9e35e3-6bd3-4cec-b838-f4249ee02432`
- Vulnerability issue type ID: `10024`
- Jira version prefix: `RHTPA`
- Component label pattern: `pscomponent:`
- Version Streams: 2.1.x (`rhtpa-release.0.3.z`), 2.2.x (`rhtpa-release.0.4.z`)
- Source Repositories: rhtpa-backend

Every required Security Configuration section is present.

---

## 1. Untriaged (4 issues)

JQL: `project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC`

### Status: New

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 1 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

### Status: In Progress

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 4 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

Note: TC-9003 is already **In Progress**, so someone may be working on it. If you pick it, the skill will warn you and ask whether to go ahead with triage or skip it.

---

## 2. Triaged but still New (1 issue) — needs follow-up

JQL: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC`

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 5 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

**Flag:** TC-9010 has the `ai-cve-triaged` label but is still in **New** status. It was triaged and then never moved forward. It may need follow-up or re-triage.

---

## 3. Ready for QA (1 issue)

JQL: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC`

The query returned 3 candidates. Only 1 passed the Depend-link filter. In the passing issue, every linked remediation Task is Done or Closed:

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

- **TC-9020**: Consider transitioning to ON_QA.

Excluded candidates (see `ready-for-qa.md` for details):
- TC-9023 (rustls, CVE-2026-39102): TC-9025 is still In Progress, so remediation is not finished.
- TC-9026 (openssl, CVE-2026-39330): it has no Depend-linked Tasks, so there is no remediation to verify.

---

## 4. Release Jira Summary

The eval input files contain no results for the release Task search (`summary ~ 'RHTPA' AND summary ~ 'CVE triage'`). No release Jira summary rows can be shown, and none were made up.

---

## Next step

Choose an issue number from the Untriaged or Triaged-but-still-New lists to start the full 8-step triage. You can also act on the Ready for QA suggestion for TC-9020. The skill made no Jira changes; any transition needs your explicit confirmation.
