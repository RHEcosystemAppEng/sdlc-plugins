# Step 1 -- Data Extraction: TC-8060

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99010 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions before 0.4.5 |
| Fixed version | 0.4.5 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [hyperium/h2#800](https://github.com/hyperium/h2/pull/800) |
| CVE record URL | [CVE-2026-99010](https://www.cve.org/CVERecord?id=CVE-2026-99010) |
| Advisory URL | -- |
| Due date | 2026-08-15 |
| Reporter | psirt-analyst (account ID: 557058:psirt-analyst-mock-id) |
| Existing comments | None |
| Issue status | New |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local path: /home/dev/repos/rhtpa-release.0.4.z
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Library: h2 (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`
- Upstream branch: `release/0.4.z`
- Remediation tasks per stream: 2 (dependency bump + downstream propagation)

## Deployment Context

- Affected repository: rhtpa-backend
- Deployment context: `upstream` (default -- no Deployment Context column in Source Repositories table)

## Vulnerability Description

A vulnerability was found in h2. The h2 crate before version 0.4.5 allows a remote
attacker to cause memory exhaustion by sending a large number of CONTINUATION frames.
This vulnerability is classified as a denial of service (DoS). The vulnerability exists
because h2 does not properly limit the number of CONTINUATION frames that can be received
for a single HEADERS frame, allowing an attacker to send an unbounded sequence that
consumes server memory.
