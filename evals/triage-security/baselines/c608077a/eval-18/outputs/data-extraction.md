# Step 1 – Data Extraction: TC-8001 (re-run)

Mode: interactive (`FULLSEND_OUTPUT_DIR` absent). Jira was not called. Every value below
comes from the provided mock issue (`vuln-issue-standard-already-triaged.md`), which stands in for
`jira.get_issue(TC-8001)` and `jira.get_issue_remote_links(TC-8001)`.

## Step 0 – Configuration (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component / PS Component / Stream fields | Not configured in Security Configuration, so Steps 4.3, 7 and 7.5.3 are skipped |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |
| ProdSec contact / account ID | Not configured (no @mentions) |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

All required sections are present, so validation passes.

## Step 0.3 – Matrix Staleness

`<!-- Last-Updated: 2026-06-28T10:00:00Z -->` was 145 days before today (2026-11-20). That is past the
14-day threshold, so a **staleness warning applies** and the engineer would choose between Refresh, Proceed and Stop.
This eval assumes "Proceed anyway". The skill does not write any matrix file.

## Status-aware handling

The current status is **In Progress**. The skill warns: "This issue is already in `In Progress`. It may be
actively worked on." This eval assumes the engineer chose "Proceed with triage anyway (verify)".

## Extracted CVE Data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8001 | Issue |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` (also customfield_10669) |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Issue stream scope | **2.2.x** (rhtpa-release.0.4.z), scoped | Suffix `rhtpa-2.2` mapped to Version Streams `2.2.x` |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 | `versions` field (already corrected by the prior run) |
| Vulnerable library | quinn-proto | Description; customfield_10632 = quinn-proto |
| Ecosystem | Cargo (source dependency, so 2 remediation tasks per stream) | Library type and Ecosystem Mappings |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS / severity | 7.5 (High) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links and description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | `duedate` |
| Assignee | engineer-a@example.com | `assignee` |
| Status | In Progress | `status` |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server, **ai-cve-triaged** | `labels` |
| Existing links | Depend: TC-8100 (upstream backport, In Progress); Depend: TC-8101 (downstream propagation, Open; TC-8101 is blocked by TC-8100) | `issuelinks` |
| Existing comments | (1) `[sdlc-workflow] Description digest: sha256-md:a1b2...a1b2` (2026-07-01T10:00Z); (2) Post-triage summary with footnote v0.11.1 (2026-07-01T10:01Z) | Comment history |
| Deployment context | upstream (default) | Source Repositories |

All critical fields (CVE ID, library, affected range) were parsed, so the skill proceeds.

## Step 1.5 / 1.7

- Step 1.5: MITRE and OSV were not queried because this eval allows no external calls. The fix threshold comes from the Jira
  description (< 0.11.14 / 0.11.14), with reduced confidence noted.
- Step 1.7: skipped because no Embargo policy URL is configured. CVSS 7.5 would otherwise trigger the gate.

## Step 2 – Version Impact (2.2.x stream, simulated `git show <tag>:Cargo.lock`)

| Version | Build | backend tag | quinn-proto | Affected (< 0.11.14)? |
|---|---|---|---|---|
| RHTPA 2.2.0 | 0.4.5 | v0.4.5 | 0.11.9 | YES |
| RHTPA 2.2.1 | 0.4.8 | v0.4.8 | 0.11.12 | YES |
| RHTPA 2.2.2 | 0.4.9 | v0.4.8 (retag) | 0.11.12 (same as 2.2.1) | **YES** |
| RHTPA 2.2.3 | 0.4.11 | v0.4.11 | 0.11.14 | NO |
| RHTPA 2.2.4 | 0.4.12 | v0.4.12 | 0.11.14 | NO |

Out-of-scope stream 2.1.x (for cross-stream awareness only): 2.1.0 (v0.3.8) and 2.1.1 (v0.3.12) both ship
0.11.9, so they are **affected**.

Step 2.5: the upstream branch `release/0.4.z` already ships 0.11.14 from v0.4.11 onward. The current dev HEAD was not
inspected because this eval allows no git calls.
