# Step 1 -- Data Extraction: TC-8040

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table row: 2.2.x -> `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue stream scope: **2.2.x only**

## Ecosystem Detection

- Library: quinn-proto
- Component context: `pscomponent:org/rhtpa-server`
- **Detected ecosystem: Go modules**

### Ecosystem Mappings Check

The Ecosystem Mappings tables in the security-matrix.md for both streams (2.1.x and 2.2.x) list the following ecosystems:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` (2.1.x) / `release/0.4.z` (2.2.x) |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

**Result: Go modules is NOT listed in the Ecosystem Mappings table for any configured stream.**

The detected ecosystem "Go modules" does not appear in the Ecosystem Mappings tables. Automated triage cannot proceed -- the skill does not know which lock file to inspect, which check command to run, or which upstream branch to target for this ecosystem.

## Deployment Context Lookup

- Affected repository (from component label): rhtpa-server
- Source Repositories table entry for rhtpa-backend found (URL: https://github.com/rhtpa/rhtpa-backend)
- Deployment context: `upstream` (default -- no Deployment Context column configured)
