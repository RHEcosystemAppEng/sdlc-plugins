# Step 1 – Data Extraction: TC-8051

Source: mock Jira issue (`vuln-issue-feature-gated.md`). No Jira MCP calls were made; the fixture stands in for `jira.get_issue` and `jira.get_issue_remote_links`.

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Jira key | TC-8051 | Issue |
| CVE ID | CVE-2026-99002 | Label `CVE-2026-99002` + summary text |
| Summary | CVE-2026-99002 rustls - Certificate validation bypass [rhtpa-2.2] | Issue summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching the Component label pattern `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → RHTPA 2.2 | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | rustls (Rust crate) | Description |
| Affected version range | < 0.23.5 ("versions before 0.23.5") | Description |
| Fixed version | 0.23.5 | Description |
| CVSS / severity | 8.1 (High) | Description |
| Vulnerability | Improper server certificate validation with custom certificate verifiers allows a MITM attacker to present an invalid certificate chain | Description |
| Upstream fix PR | https://github.com/rustls/rustls/pull/2100 (rustls/rustls#2100) | Remote links |
| Advisory URL | None (no GHSA/advisory remote link) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99002 | Remote links / References |
| Due date | 2026-08-01 | `duedate` |
| Status / Assignee | New / Unassigned | Issue |
| Existing comments | None | Comment history |

All critical fields (CVE ID, library, affected range) were parsed, so triage can continue.

## Stream Scope Resolution

| Item | Value |
|------|-------|
| Summary suffix | `[rhtpa-2.2]` |
| Mapped stream | **2.2.x** |
| Configured stream match | Yes: `2.2.x` → `git.example.com/rhtpa/rhtpa-release.0.4.z` (local: `/home/dev/repos/rhtpa-release.0.4.z`) |
| Issue stream scope | **Scoped to 2.2.x**. Steps 2–8 cover only the 2.2.x stream. 2.1.x is outside the issue scope. |

## Ecosystem Detection

| Item | Value |
|------|-------|
| Ecosystem | **Cargo** (rustls is a Rust crate) |
| Listed in the 2.2.x Ecosystem Mappings? | Yes: Cargo / backend / `Cargo.lock` / `git show <tag>:Cargo.lock` / upstream branch `release/0.4.z` |
| Category | Source dependency (normal remediation is 2 tasks: upstream backport or dependency bump, plus downstream propagation) |

## Deployment Context

| Item | Value |
|------|-------|
| Affected repository | rhtpa-backend (`backend` in the Ecosystem Mappings) |
| Source Repositories entry | https://github.com/rhtpa/rhtpa-backend (`/home/dev/repos/rhtpa-backend`) |
| Deployment context | `upstream` (the default, because the Source Repositories table has no deployment-context column) |

## Notes on Steps 0.3 / 1.5 / 1.7 (simulated)

- **Step 1.5 (external enrichment):** MITRE and OSV were not queried because the eval forbids external calls. Treated as "both external APIs unavailable": the Jira description threshold (fixed in 0.23.5) is used, with reduced confidence in the fix threshold.
- **Step 1.7 (embargo check):** CVSS 8.1 is above the threshold, but no Embargo policy URL is configured in the Security Configuration, so the step is skipped.
- **Step 0.3 (matrix staleness):** the matrix `Last-Updated` is 2026-06-28. Today is 2026-11-20, so the matrix is about 145 days old. In an interactive run the engineer would get a staleness warning with refresh options. Here the fixture matrix is used as-is.
