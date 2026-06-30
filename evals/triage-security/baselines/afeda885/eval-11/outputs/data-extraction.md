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
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x** (Konflux release repo: rhtpa-release.0.3.z)
- This issue is **stream-scoped** to 2.1.x only.
- Steps 3 and 4 will apply only to the 2.1.x stream versions.

## Ecosystem Detection

- Library: tokio (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Source repository: backend
- Upstream branch for 2.1.x stream: `release/0.3.z`

## Custom Fields

| Custom Field | Value |
|---|---|
| customfield_10632 (Upstream Affected Component) | tokio |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-server |
| customfield_10832 (Stream) | rhtpa-2.1 |

## Remote Links

- [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) -- GitHub Advisory
- [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) -- CVE Record
- [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) -- Upstream fix PR

## Version Impact Analysis (Step 2)

Since the issue is scoped to stream 2.1.x, the primary analysis targets versions in that stream. However, per Step 2, all supported streams must be checked for a complete version impact picture.

The mock lock file data does not include tokio versions directly. Based on the CVE description, tokio versions before 1.42.0 are vulnerable.

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | tokio version | Affected? | Notes |
|---------|-----------|---------------|-----------|-------|
| 2.1.0 | v0.3.8 | (needs lock file check) | Requires verification | |
| 2.1.1 | v0.3.12 | (needs lock file check) | Requires verification | |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build Tag | tokio version | Affected? | Notes |
|---------|-----------|---------------|-----------|-------|
| 2.2.0 | v0.4.5 | (needs lock file check) | Requires verification | |
| 2.2.1 | v0.4.8 | (needs lock file check) | Requires verification | |
| 2.2.2 | v0.4.9 | N/A | Same as 2.2.1 | retag of 2.2.1 |
| 2.2.3 | v0.4.11 | (needs lock file check) | Requires verification | |
| 2.2.4 | v0.4.12 | (needs lock file check) | Requires verification | |

Note: In a real triage, `git show <tag>:Cargo.lock | grep -A2 'name = "tokio"'` would be run for each tag to determine the exact tokio version shipped. The mock data provides versions for quinn-proto, serde_json, h2, and openssl-libs but not for tokio specifically. In this simulated scenario, we rely on the issue description which states that the vulnerability affects tokio versions before 1.42.0 and that the 2.1.x stream ships a vulnerable version.

## Step 1.7 -- Embargo Check

CVSS is 8.1 (High), which meets the threshold (>= 7.0). However, no Embargo policy URL is configured in the Security Configuration, so this step is skipped.
