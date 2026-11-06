# triage-security — Discovery Mode Results

Invoked without an issue key, so the skill ran in discovery mode.

## Step 0: Configuration check

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Vulnerability issue type ID | 10024 |
| Jira version prefix | RHTPA |
| Component label pattern | `pscomponent:` |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| VEX Justification custom field | customfield_12345 |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend |

All required sections are present: Repository Registry, Jira Configuration, Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories). Discovery can go ahead.

Execution mode: interactive (`FULLSEND_OUTPUT_DIR` is not set).

---

## 1. Untriaged (4 issues)

JQL: `project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC`

### Status: New

1. **TC-9001** | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | Created 2026-06-08
2. **TC-9002** | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | Created 2026-06-07
3. **TC-9004** | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | Created 2026-06-04

### Status: In Progress

4. **TC-9003** | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | Created 2026-06-05
   - Note: this issue is already In Progress and may be in active work. If you select it, the skill will ask whether to proceed or skip.

---

## 2. Triaged but still New (1 issue)

JQL: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC`

> These issues carry the `ai-cve-triaged` label but are still in New status. They were triaged but never moved forward and may need follow-up or re-triage.

5. **TC-9010** | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | Created 2026-05-28 | **STALE: triaged, not actioned**

---

## 3. Ready for QA (1 issue)

JQL: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC`

These are triaged CVEs whose linked remediation Tasks (link type "Depend") are all Done or Closed.

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

- **TC-9020**: Consider transitioning to ON_QA.

Excluded candidates (details in `ready-for-qa.md`):
- TC-9023 (CVE-2026-39102, rustls): remediation is still in progress, because TC-9025 is In Progress.
- TC-9026 (CVE-2026-39330, openssl): no "Depend" remediation Tasks are linked, so there is nothing to verify.

---

## 4. Release Jira Summary

JQL: `project = TC AND issuetype = Task AND summary ~ 'RHTPA' AND summary ~ 'CVE triage' ORDER BY created DESC`

The provided search results contain no data for this query, so there is no release Jira summary to show. In a live run, this section would list each release Epic and release Task with counts of CVEs tracked and remediation done or pending.

---

## Next step

Choose an issue to triage, for example `/sdlc-workflow:triage-security TC-9001`, or reply with its number from the lists above. No Jira changes were made during discovery.
