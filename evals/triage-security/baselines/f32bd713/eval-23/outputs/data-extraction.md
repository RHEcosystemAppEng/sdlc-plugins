# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links (quinn-rs/quinn#2048) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links (GHSA) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links (cve.org) |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to configured Version Stream **2.2.x** (Konflux release repo `rhtpa-release.0.4.z`).

Issue stream scope: **2.2.x** (scoped issue -- Steps 3-8 apply only to this stream; Case A cross-stream check applies to other affected streams).

## Ecosystem Detection

- **Library**: quinn-proto (Rust crate)
- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Remediation tasks per stream**: 2 (upstream backport or dependency bump + downstream propagation)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`

## Deployment Context Lookup

- **Component label**: `pscomponent:org/rhtpa-server`
- **Mapped repository**: rhtpa-backend (from Source Repositories table)
- **Deployment context**: **customer-shipped**

The repository `rhtpa-backend` is listed in the Source Repositories table with URL `https://github.com/rhtpa/rhtpa-backend` and Deployment Context value `customer-shipped`. This deployment context will be used in Step 8 (Remediation) to generate coordination guidance in remediation task descriptions.

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | Outside issue scope (cross-stream) |
| 2.1.1 | 2.1.x | 0.11.9 | YES | Outside issue scope (cross-stream) |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | Fixed version shipped |
| 2.2.4 | 2.2.x | 0.11.14 | NO | Fixed version shipped |

### Dependency chain for quinn-proto (Cargo):

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (present in Cargo.lock for all source tags)
  Profile: production (quinn-proto is a runtime dependency for QUIC transport)
```

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |

- **2.2.x**: Upstream branch `release/0.4.z` already ships quinn-proto 0.11.14 (fixed). Remediation is a dependency bump + downstream propagation.
- **2.1.x**: Upstream branch `release/0.3.z` still ships quinn-proto 0.11.9 (vulnerable). Remediation requires an upstream backport + downstream propagation.

## Affects Versions Correction

The PSIRT-assigned Affects Versions (`RHTPA 2.0.0`) is incorrect. There is no `2.0.0` version in any configured stream. Based on lock file evidence, the correct Affects Versions for the 2.2.x stream scope are:

- **Add**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Remove**: RHTPA 2.0.0

Cross-stream impact note: 2.1.x versions (2.1.0, 2.1.1) are also affected but are outside the issue scope.
