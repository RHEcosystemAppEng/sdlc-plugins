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
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99010 |
| Due date | 2026-08-15 |
| Reporter | psirt-analyst (account ID: 557058:psirt-analyst-mock-id) |
| Status | New |
| Existing comments | None |

## Ecosystem Detection

- **Ecosystem**: Cargo (h2 is a Rust crate)
- **Category**: Source dependency
- **Remediation tasks per stream**: 2 (dependency bump + downstream propagation)

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in Security Configuration. Triage is scoped to this stream only.

Configured version streams:
- 2.1.x -- Konflux release repo: rhtpa-release.0.3.z
- 2.2.x -- Konflux release repo: rhtpa-release.0.4.z (SCOPED)

## Dependency Type

h2 is a **transitive** dependency (3 levels deep). It is NOT a direct dependency of the backend workspace. The dependency chain is:

```
backend (workspace) -> reqwest -> hyper -> h2
```

This was determined from manifest inspection:
```toml
# backend/Cargo.toml (all versions)
[dependencies]
reqwest = { version = "0.12", features = ["json"] }
# h2 is NOT a direct dependency -- it comes through reqwest -> hyper -> h2
```

## Vulnerability Summary

A vulnerability was found in h2. The h2 crate before version 0.4.5 allows a remote attacker to cause memory exhaustion by sending a large number of CONTINUATION frames. This vulnerability is classified as a denial of service (DoS). The h2 crate does not properly limit the number of CONTINUATION frames that can be received for a single HEADERS frame, allowing an attacker to send an unbounded sequence that consumes server memory.
