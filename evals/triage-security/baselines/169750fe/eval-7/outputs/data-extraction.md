# Step 1 -- Data Extraction: TC-8006

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Stream scope | 2.1.x |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Status | New |

## Remote Links

| URL | Type |
|-----|------|
| https://github.com/advisories/GHSA-2026-qp73-x4mq | GitHub Advisory |
| https://www.cve.org/CVERecord?id=CVE-2026-31812 | CVE Record |

## Existing Issue Links

| Link Type | Direction | Linked Issue | Link ID |
|-----------|-----------|--------------|---------|
| Related | outward (TC-8006 -> TC-8001) | TC-8001 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]) | 1990401 |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.1]`, which maps to the `2.1.x` version stream configured in Security Configuration. This issue is scoped to the 2.1.x stream only.

## Ecosystem Detection

The vulnerable library is `quinn-proto`, a Rust crate. The ecosystem is **Cargo** (source dependency). Per the Ecosystem Mappings table for the 2.1.x stream, the lock file is `Cargo.lock` and the check command is `git show <tag>:Cargo.lock`.

As a source dependency ecosystem, remediation would produce 2 tasks per stream: upstream backport or dependency bump + downstream propagation.

## Vulnerability Summary

quinn-proto before version 0.11.14 allows a remote attacker to cause a panic by sending a QUIC transport frame that creates an excessive number of streams. This is classified as a denial of service (DoS) vulnerability. The fix is available in quinn-proto version 0.11.14.
