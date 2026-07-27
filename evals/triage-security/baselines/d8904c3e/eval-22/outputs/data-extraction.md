# Step 1 -- Data Extraction for TC-8021

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | quinn-rs/quinn#2048 (https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | GHSA-2026-qp73-x4mq (https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Upstream Affected Component (customfield_10632) | quinn-proto |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the configured Version Stream **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. Steps 3 and 4 will be scoped to this stream. Cross-stream impact (Case A) will be evaluated for other streams (2.1.x).

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings table for both streams lists **Cargo** as the ecosystem, with `Cargo.lock` as the lock file and `git show <tag>:Cargo.lock` as the check command.

Cargo is a **source dependency** ecosystem per the classification table. This means remediation requires **2 tasks per affected stream**: upstream backport + downstream propagation.

## Version Impact Analysis (Step 2)

Using quinn-proto version data from security-matrix.md lock file data:

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | quinn-proto Version | Affected? | Rationale |
|---------|-----------|---------------------|-----------|-----------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |

### Stream 2.2.x (rhtpa-release.0.4.z) -- Issue Scope

| Version | Build Tag | quinn-proto Version | Affected? | Rationale |
|---------|-----------|---------------------|-----------|-----------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 (fix threshold) |
| 2.2.2 | v0.4.9 | 0.11.12 | YES | Retag of v0.4.8 -- same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (at or above fix threshold) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (at or above fix threshold) |

## Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, which is incorrect -- there is no 2.0.x stream configured.

Since this issue is scoped to stream 2.2.x, the corrected Affects Versions should include only the affected versions in that stream:

- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are NOT affected (they ship quinn-proto 0.11.14, which is the fixed version) and should be excluded.

## Vulnerability Details

The vulnerability exists because quinn-proto does not properly validate the number of streams requested in a STREAMS frame. An attacker can send a specially crafted frame that causes the server to allocate an unbounded number of stream state objects, leading to a panic when the allocation exceeds internal limits. This is classified as a denial of service (DoS).
