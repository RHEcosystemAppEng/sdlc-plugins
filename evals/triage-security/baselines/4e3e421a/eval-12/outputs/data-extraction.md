# Step 1 – Data Extraction: TC-8030

Source: mock Jira issue (`vuln-issue-enrichment.md`), project config (`claude-md-security-config.md`).
No Jira MCP calls were made; all data parsed from the fixture.

## Pre-flight notes (Steps 0 – 0.3)

- Project key: TC, Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Security Configuration present: Vulnerability issue type ID 10024, Jira version prefix `RHTPA`,
  component label pattern `pscomponent:`, VEX Justification field `customfield_12345`
- Version Streams: 2.1.x (`rhtpa-release.0.3.z`), 2.2.x (`rhtpa-release.0.4.z`)
- **Matrix staleness warning**: security matrix `Last-Updated: 2026-06-28T10:00:00Z` is 128 days old
  (threshold 14 days). In interactive mode the engineer would be offered Refresh / Proceed / Stop;
  for this eval we **proceed anyway** with the supplied matrix.

## Extracted fields

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8030 | Issue |
| CVE ID | CVE-2026-48901 | Label `CVE-2026-48901` + summary |
| Affected component | `pscomponent:org/rhtpa-server` | Labels |
| Affected repository | rhtpa-backend (`backend` in Ecosystem Mappings) | Component + matrix mapping |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → RHTPA 2.2 | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | h2 (hyperium/h2 Rust crate) | Description |
| Vulnerability | HTTP/2 CONTINUATION flood (unbounded CONTINUATION frames → memory/CPU exhaustion, DoS) | Description |
| Affected version range | **"versions prior to the fix"** — imprecise, no numeric threshold | Description |
| Fixed version | **"see advisory"** — not stated | Description |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p (also RUSTSEC-2026-0089) | Remote links / References |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 | Remote links |
| Due date | 2026-08-01 (**already past** as of 2026-11-03) | `duedate` |
| Status / Assignee | New / Unassigned | Issue |
| Existing comments | none | Comments |

## Critical field check

- CVE ID: parsed
- Library: parsed (h2)
- Affected range: **NOT parseable from Jira description** ("versions prior to the fix").
  Normally this would require asking the engineer. However, Step 1.5 always queries external
  CVE databases, and both the MITRE and OSV mock responses provide a precise machine-readable
  threshold (`< 0.4.8`), which resolves the gap (see `enrichment.md`). Triage proceeds on the
  enriched threshold.

## Stream scope resolution

- Suffix `[rhtpa-2.2]` → stream **2.2.x**, which matches the configured Version Streams table
  (`git.example.com/rhtpa/rhtpa-release.0.4.z`).
- Issue is **scoped** to stream 2.2.x. Steps 3–4 and Case B apply only to 2.2.x; other affected
  streams are handled via Case A (cross-stream impact).

## Ecosystem detection

- h2 is a Rust crate → **Cargo** ecosystem (listed in both streams' Ecosystem Mappings:
  repository `backend`, lock file `Cargo.lock`, check `git show <tag>:Cargo.lock`).
- Category: **Source dependency** → 2 remediation tasks per affected stream
  (upstream backport / dependency bump + downstream propagation).

## Deployment context

- Source Repositories table has no Deployment Context column → per backward-compatibility rule,
  coordination guidance is omitted from remediation tasks (lookup default would be `upstream`,
  but the column is absent so no subsection is added).
