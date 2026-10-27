# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99010 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions before 0.4.5 |
| Fixed version | 0.4.5 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99010 |
| Due date | 2026-08-15 |
| Reporter | psirt-analyst (account ID: 557058:psirt-analyst-mock-id) |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local path: /home/dev/repos/rhtpa-release.0.4.z
- Scope: Triage is scoped to the 2.2.x stream only

## Ecosystem Detection

- Ecosystem: **Cargo** (Rust crate -- h2 is a Rust HTTP/2 library)
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`
- Upstream branch: `release/0.4.z`
- Remediation tasks per stream: 2 (dependency bump + downstream propagation)

## Vulnerability Description

A vulnerability was found in h2. The h2 crate before version 0.4.5 allows a remote attacker to cause memory exhaustion by sending a large number of CONTINUATION frames. This vulnerability is classified as a denial of service (DoS). The vulnerability exists because h2 does not properly limit the number of CONTINUATION frames that can be received for a single HEADERS frame, allowing an attacker to send an unbounded sequence that consumes server memory.
