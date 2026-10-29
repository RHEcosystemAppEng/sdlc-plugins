# Step 1 -- Data Extraction: TC-8021

## Extracted CVE Metadata

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-55123 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Label (matches component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.1 | Summary suffix `[rhtpa-2.1]` |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 | Jira `versions` field |
| Vulnerable library | tokio | Description text |
| Affected version range | versions before 1.42.0 | Description text |
| Fixed version | 1.42.0 | Description text |
| CVSS | 8.1 (High) | Description text |
| Due date | 2026-08-15 | Issue `duedate` field |
| Upstream fix PR | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) | Remote links |
| Advisory URL | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) | Remote links |
| CVE Record URL | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) | Remote links |
| Existing comments | (none) | Issue comment history |
| Existing issue links | (none) | Issue `issuelinks` field |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Parsed stream: `rhtpa-2.1` maps to **2.1.x** version stream
- Matched Version Stream: `2.1.x` at Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.3.z` (local path `/home/dev/repos/rhtpa-release.0.3.z`)
- Issue stream scope: **2.1.x only** (scoped issue)

## Ecosystem Detection

- Library: tokio (Rust crate)
- Ecosystem: **Cargo** (source dependency)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`
- Classification: Source dependency ecosystem -- standard remediation produces 2 tasks per stream (upstream backport or dependency bump + downstream propagation)

## Deployment Context Lookup

- Affected repository: rhtpa-backend (from component label `pscomponent:org/rhtpa-server`)
- Deployment context: `upstream` (from Source Repositories table in Security Configuration)

## Upstream Affected Component (Custom Field)

- Field: `customfield_10632`
- Value: `tokio`

## PS Component (Custom Field)

- Field: `customfield_10669`
- Value: `pscomponent:org/rhtpa-server`

## Stream (Custom Field)

- Field: `customfield_10832`
- Value: `rhtpa-2.1`

## Existing Preemptive Task Context

The issue description notes that a proactive remediation task (TC-8022) already exists for this stream, created by a prior cross-stream triage of TC-8020 (stream [rhtpa-2.2]). This will be evaluated in Step 4.4 (Preemptive Task Reconciliation).
