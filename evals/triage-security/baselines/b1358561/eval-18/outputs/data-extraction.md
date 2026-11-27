# Step 1 – Data Extraction: TC-8001

Source: simulated `jira.get_issue(TC-8001)` + `jira.get_issue_remote_links(TC-8001)`
(read from `vuln-issue-standard-already-triaged.md`; no Jira call made).

## Pre-step gates

| Gate | Result |
|------|--------|
| Step 0 – Configuration | Valid. Project key TC, Cloud ID 2b9e35e3-..., Security Configuration present (prefix `RHTPA`, Vulnerability type 10024, component pattern `pscomponent:`, VEX field customfield_12345, 2 Version Streams, 1 Source Repository). |
| Step 0.3 – Matrix staleness | Mock matrices have no `<!-- Last-Updated -->` header, so the skill warns ("no Last-Updated timestamp, consider `/setup`") and continues. |
| Step 0.5 – Jira access | Simulated. No MCP or REST calls made (eval constraint). |
| Step 0.6 – Fullsend mode | `FULLSEND_OUTPUT_DIR` absent, so interactive mode. |
| Status-aware handling | Status is **In Progress**. The skill warns: "This issue is already in In Progress. It may be actively worked on." It runs as option 1 ("Proceed with triage anyway") because the task explicitly asks for a re-run. |
| Step 0.8 – Assign / transition | Transition **skipped** because In Progress is later than Assigned. Assignee is already `engineer-a@example.com`. If the engineer re-running triage is engineer-a, assignment is a no-op. Otherwise the skill would propose reassignment, which needs explicit confirmation and was not executed. |

## Extracted CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` + summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label (pattern `pscomponent:`) / customfield_10669 |
| Upstream Affected Component | quinn-proto | customfield_10632 |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]`, which maps to stream **2.2.x** (scoped) | Summary suffix / customfield_10832 |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 | `versions` field (already corrected by prior run) |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| Severity | CVSS 7.5 (High), DoS | Description |
| Ecosystem | Cargo (Rust crate), a source dependency, so 2 remediation tasks per stream | Library name + Ecosystem Mappings |
| Lock file / check command | `Cargo.lock` / `git show <tag>:Cargo.lock` | security-matrix.md (2.2.x) |
| Upstream branch | `release/0.4.z` (repo: backend) | security-matrix.md (2.2.x) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | `duedate` |
| Status | In Progress | Issue |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server, **ai-cve-triaged** | Issue |
| Assignee | engineer-a@example.com | Issue |
| Deployment context | `upstream` (default, because Source Repositories has no Deployment Context column) | CLAUDE.md |
| Existing comments | (1) `[sdlc-workflow] Description digest: sha256-md:a1b2...a1b2` (2026-07-01T10:00Z); (2) Post-triage summary from triage-security v0.11.1 (2026-07-01T10:01Z) | Comment history |
| Existing links | Depend: TC-8100 (upstream backport, In Progress); Depend: TC-8101 (downstream propagation, Open, blocked by TC-8100) | `issuelinks` |

All critical fields (CVE ID, library, affected range) parsed. No engineer input needed.

## Stream scope resolution

`[rhtpa-2.2]` maps to `2.2.x`, which matches the configured Version Stream `git.example.com/rhtpa/rhtpa-release.0.4.z`. The issue is **scoped to 2.2.x**.

## Step 1.5 / 1.7

- External enrichment (MITRE/OSV): not queried (eval constraint, no external tools). The skill falls back to the Jira description threshold `< 0.11.14` with reduced confidence.
- Embargo check: no Embargo policy URL configured, so Step 1.7 is skipped silently even though CVSS is 7.5.

## Step 2 – Version impact (simulated `git show` from mock lock data)

| Version | backend tag | quinn-proto | Affected? | Notes |
|---------|-------------|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | out of scope (2.1.x stream) |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | out of scope (2.1.x stream) |
| 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | v0.4.8 | (0.11.12) | **YES** | backend retag of 2.2.1, so the 2.2.1 result carries forward (Rule 5) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | |

Development stream: no unreleased Jira version data available (Step 2.2 not resolvable offline). 2.2.x is the latest configured stream.
Upstream fix (Step 2.5): `release/0.4.z` HEAD was not inspected (no git). The latest released tag v0.4.12 already ships 0.11.14, which suggests the fix is upstream.
