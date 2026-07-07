# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Stream scope | 2.2.x (scoped -- maps to rhtpa-release.0.4.z) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Ecosystem | Cargo (Rust crate) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Status | New |
| Assignee | Unassigned |

## Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` maps to the source repository `rhtpa-backend`.

Lookup in the Source Repositories table from CLAUDE.md Security Configuration:

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | customer-shipped |

**Deployment context for rhtpa-backend: `customer-shipped`**

This deployment context is recorded as part of the extracted CVE metadata and will be used in Step 8 (Remediation) to generate coordination guidance in the remediation task descriptions.

## Version Impact Analysis

Using the supportability matrix and lock file data for quinn-proto:

### Stream 2.2.x (rhtpa-release.0.4.z) -- issue-scoped stream

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed version) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed version) |

### Stream 2.1.x (rhtpa-release.0.3.z) -- cross-stream analysis

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

### Summary

- **Stream 2.2.x**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 are NOT affected (they ship quinn-proto 0.11.14, the fixed version).
- **Stream 2.1.x**: All versions (2.1.0, 2.1.1) are affected (they ship quinn-proto 0.11.9).
- **Affects Versions correction needed**: The current Jira Affects Versions is `RHTPA 2.0.0`, which does not match any configured version stream. The correct Affects Versions for the scoped stream (2.2.x) should be RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2.
- **Cross-stream impact**: Stream 2.1.x is also fully affected but is outside this issue's scope (Case B).

### Ecosystem Mappings Used

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.3.z (2.1.x) |
| Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.4.z (2.2.x) |
