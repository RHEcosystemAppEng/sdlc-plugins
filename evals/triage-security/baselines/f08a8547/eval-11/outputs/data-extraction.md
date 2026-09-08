# Step 1 -- Data Extraction: TC-8021

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Upstream fix PR | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE record URL | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| Due date | 2026-08-15 |
| Existing comments | (none) |
| Issue status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.1]`.

- Parsed suffix: `rhtpa-2.1` maps to stream **2.1.x**
- Matched Version Stream: `2.1.x` at Konflux Release Repo `git.example.com/rhtpa/rhtpa-release.0.3.z` (local path: `/home/dev/repos/rhtpa-release.0.3.z`)
- Issue stream scope: **2.1.x only** (scoped issue -- Steps 3-4 apply to this stream only)

## Ecosystem Detection

- Vulnerable library: **tokio** (Rust crate)
- Detected ecosystem: **Cargo**
- Category: **Source dependency**
- Remediation tasks per stream: **2** (upstream backport + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`

## Deployment Context Lookup

- Affected repository from component label: rhtpa-server (matched via `pscomponent:org/rhtpa-server`)
- Source Repositories table entry: rhtpa-backend at `https://github.com/rhtpa/rhtpa-backend`
- Deployment context: **upstream** (default -- no Deployment Context column present in Source Repositories table)

## Existing Issue Links

No existing issue links on TC-8021.

## Remote Links

- [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) -- GitHub Advisory
- [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) -- CVE Record
- [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) -- Upstream fix PR

## Additional Context from Issue Description

The issue description notes: "A proactive remediation task (TC-8022) already exists for this stream, created by a prior cross-stream triage of TC-8020 (stream [rhtpa-2.2])."

This is relevant to Step 4.4 (preemptive task reconciliation).
