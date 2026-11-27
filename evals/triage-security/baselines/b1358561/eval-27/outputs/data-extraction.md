# Step 1 – Data Extraction: TC-8051

Source: mock Jira issue (`vuln-issue-feature-gated.md`). No Jira MCP calls were made. The fixture stands in for `jira.get_issue` and `jira.get_issue_remote_links`.

## Step 0 – Configuration check (from claude-md-security-config.md)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 (configured) |
| Upstream Affected Component field | not configured (Steps 4.3 and 7 skipped) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

Result: all required sections are present, so triage proceeds.

## Parsed CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8051 | Issue |
| Issue status | New (full triage path) | Issue `status` |
| CVE ID | CVE-2026-99002 | Label `CVE-2026-99002`, summary |
| Affected component | `pscomponent:org/rhtpa-server` | Component label |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | rustls | Description |
| Affected version range | < 0.23.5 ("versions before 0.23.5") | Description |
| Fixed version | 0.23.5 | Description |
| CVSS / severity | 8.1 (High) | Description |
| Vulnerability summary | Improper server certificate validation with custom certificate verifiers. Allows MITM with an invalid certificate chain. | Description |
| Upstream fix PR | https://github.com/rustls/rustls/pull/2100 (rustls/rustls#2100) | Remote links |
| Advisory URL | none (no GHSA/advisory link present) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99002 | Remote links |
| Due date | 2026-08-01 | `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | none | Comment history |

All critical fields (CVE ID, library, affected range) were parsed.

## Stream scope resolution

| Item | Value |
|------|-------|
| Summary suffix | `[rhtpa-2.2]` |
| Mapped stream | **2.2.x** (Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.4.z`) |
| Match against Version Streams table | Matched |
| Issue stream scope | **Scoped: 2.2.x only** (Steps 3–8 are limited to 2.2.x. Other streams are reported only for cross-stream context.) |

## Ecosystem detection

| Item | Value |
|------|-------|
| Ecosystem | Cargo (Rust crate `rustls`) |
| Category | Source dependency. This would normally mean 2 remediation tasks per stream, but the feature gate (see version-impact.md) changes that. |
| Lock file / check command | `Cargo.lock` / `git show <tag>:Cargo.lock` (from the 2.2.x Ecosystem Mappings) |
| Upstream branch | `release/0.4.z` |
| Affected repository | backend (rhtpa-backend) |
| Deployment context | `upstream` (default; no Deployment Context column configured) |

## Step 0.8 – Assign / transition (not executed)

Proposed action: assign TC-8051 to the current user and move it from New to Assigned. It was not executed because Jira calls are prohibited in this eval.

## Step 1.5 – External CVE enrichment (not executed)

MITRE and OSV.dev were not queried because external calls are prohibited in this eval. Both sources count as unavailable, so the Jira description data is used.

> ⚠ External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used for Step 2: **rustls < 0.23.5 is affected; 0.23.5 is the fixed version.**

## Step 1.7 – Embargo check

Skipped because no Embargo policy URL is configured. CVSS 8.1 would otherwise have triggered the gate.
