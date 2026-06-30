# Step 1 -- Data Extraction for TC-8020

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 |
| Existing comments | None |
| CVSS | 8.1 (High) |
| Vulnerability type | Use-after-free in task abort |

## Custom Fields

| Field | ID | Value |
|-------|----|-------|
| Upstream Affected Component | customfield_10632 | tokio |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-server |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. This maps to the **2.2.x** stream in Version Streams configuration, which corresponds to the Konflux release repo `rhtpa-release.0.4.z`.

**Issue stream scope**: 2.2.x (rhtpa-2.2)

## Ecosystem Detection

The vulnerable library is **tokio**, a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, the ecosystem is **Cargo**.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`
- Repository: backend

Since this is a source dependency ecosystem (Cargo), remediation will require **two tasks**: an upstream backport task (fix in the source repo) and a downstream propagation subtask (update the reference in the Konflux release repo).

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |

## Step 1.5 -- External CVE Data Enrichment

Fix threshold from Jira description: tokio < 1.42.0 (fixed in 1.42.0)

External sources would be queried:
- MITRE CVE API: `https://cveawg.mitre.org/api/cve/CVE-2026-55123`
- OSV.dev API: `https://api.osv.dev/v1/vulns/CVE-2026-55123`

Cross-validated fix threshold: **1.42.0** (used for version impact comparisons in Step 2.3)

## Step 1.7 -- Embargo Check

CVSS is 8.1 (High severity, >= 7.0 threshold). The Security Configuration does not include an Embargo policy URL, so this step is skipped.
