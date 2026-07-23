# Step 1 -- Data Extraction

## Issue: TC-8001

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels: `CVE-2026-31812`; Summary text |
| Affected component | `pscomponent:org/rhtpa-server` | Labels (matches component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description: "A vulnerability was found in quinn-proto" |
| Affected version range | < 0.11.14 (versions before 0.11.14) | Description: "before version 0.11.14" |
| Fixed version | 0.11.14 | Description: "Fixed version: 0.11.14" |
| CVSS score | 7.5 (High) | Description: "CVSS: 7.5 (High)" |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote Links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote Links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote Links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | (none) | Issue comment history |
| Status | New | Issue `status` field |
| Assignee | Unassigned | Issue `assignee` field |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`.

- Parsed suffix: `rhtpa-2.2` -> stream **2.2.x**
- Matched to Version Streams table: **2.2.x** at `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Issue stream scope: **2.2.x** (scoped issue -- Steps 3-4 apply only to this stream)

## Ecosystem Detection

- Vulnerable library: `quinn-proto` (a Rust crate)
- Detected ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock` (per Ecosystem Mappings in security-matrix.md)
- Upstream branch: `release/0.4.z` (for stream 2.2.x)

## Vulnerability Summary

quinn-proto (Rust crate) before version 0.11.14 allows a remote attacker to cause a denial of service (DoS) by sending a QUIC transport frame that creates an excessive number of streams. The server panics when stream allocation exceeds internal limits.

- **Type**: Denial of Service (DoS)
- **Attack vector**: Remote (network-accessible QUIC endpoint)
- **Severity**: High (CVSS 7.5)
- **Fix**: Upgrade quinn-proto to >= 0.11.14

## Affects Versions Observation

The PSIRT-assigned Affects Version is `RHTPA 2.0.0`. There is no `2.0.x` stream configured in the Version Streams table. This is likely incorrect and will need correction in Step 3 after the version impact analysis determines which 2.2.x versions actually ship a vulnerable version of quinn-proto.

## References

- [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) -- GitHub Advisory
- [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) -- CVE Record
- [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) -- Upstream fix PR
- [RUSTSEC-2026-0042](https://rustsec.org/advisories/RUSTSEC-2026-0042.html) -- RustSec Advisory
