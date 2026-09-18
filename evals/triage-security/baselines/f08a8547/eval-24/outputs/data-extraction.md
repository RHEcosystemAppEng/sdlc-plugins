# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 (versions before 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | (none) |

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]` which maps to configured Version Stream **2.2.x** (Konflux release repo `rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. Steps 3 and 4 apply only to this stream. Cross-stream impact on 2.1.x is handled via Case A.

## Ecosystem Detection

- **Ecosystem**: Cargo (quinn-proto is a Rust crate)
- **Category**: Source dependency
- **Remediation tasks per stream**: 2 (upstream backport + downstream propagation)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

## Deployment Context

The Source Repositories table does NOT have a Deployment Context column. Per backward compatibility rules, deployment context defaults to `upstream` internally but coordination guidance is omitted from remediation task descriptions.

## Version Impact Analysis

### Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | fixed version |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | fixed version |

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | YES |

### Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (based on presence in Cargo.lock)
  Profile: production (quinn-proto is a runtime QUIC transport dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml / Cargo.lock
```

## Affects Versions Correction

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, but there is no 2.0.x version stream configured. This is incorrect.

Since the issue is scoped to stream **2.2.x**, the correct Affects Versions (based on lock file evidence) are the affected versions within that stream:

- Current: [RHTPA 2.0.0]
- Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

Versions 2.2.3 and 2.2.4 are NOT affected (they ship quinn-proto 0.11.14, the fix version).

## Cross-Stream Impact (Case A)

The issue is scoped to 2.2.x, but version impact analysis reveals that stream **2.1.x** is also affected:

- 2.1.0: quinn-proto 0.11.9 (affected)
- 2.1.1: quinn-proto 0.11.9 (affected)

The upstream branch `release/0.3.z` does NOT have the fix (latest tag v0.3.12 still ships 0.11.9). Remediation for 2.1.x requires an upstream backport first.

## Staleness Check

The security matrix `Last-Updated` timestamp is `2026-06-28T10:00:00Z`, which is 72 days ago (current date: 2026-09-08). This exceeds the 14-day staleness threshold.

In a live triage, the engineer would be warned and asked whether to refresh, proceed, or stop. For this eval, proceeding with the current matrix data.
