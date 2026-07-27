# Step 1 -- Data Extraction

## Issue: TC-8060

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99010 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions before 0.4.5 |
| Fixed version | 0.4.5 |
| CVSS | 7.5 (High) |
| Ecosystem | Cargo |
| Dependency type | Transitive (3 levels deep) |
| Upstream fix PR | [hyperium/h2#800](https://github.com/hyperium/h2/pull/800) |
| CVE record URL | [CVE-2026-99010](https://www.cve.org/CVERecord?id=CVE-2026-99010) |
| Advisory URL | -- |
| Due date | 2026-08-15 |
| Reporter | psirt-analyst (account ID: 557058:psirt-analyst-mock-id) |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table. Triage is scoped to this stream. The corresponding Konflux release repo is `rhtpa-release.0.4.z`.

## Ecosystem Detection

The vulnerable library `h2` is a Rust crate. The 2.2.x stream's Ecosystem Mappings table lists **Cargo** with lock file `Cargo.lock` and check command `git show <tag>:Cargo.lock`. Cargo is a source dependency ecosystem, which means remediation requires **two tasks** per stream: upstream backport + downstream propagation.

## Vulnerability Description

A vulnerability was found in h2. The h2 crate before version 0.4.5 allows a remote attacker to cause memory exhaustion by sending a large number of CONTINUATION frames. This vulnerability is classified as a denial of service (DoS). The vulnerability exists because h2 does not properly limit the number of CONTINUATION frames that can be received for a single HEADERS frame, allowing an attacker to send an unbounded sequence that consumes server memory.
