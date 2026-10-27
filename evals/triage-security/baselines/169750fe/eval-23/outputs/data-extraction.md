# Step 1 -- Data Extraction: TC-8001

## Step 0 -- Configuration Extraction

The following configuration was extracted from the project CLAUDE.md:

| Setting | Value |
|---------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | customer-shipped |

## CVE Metadata

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | (none) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream. This issue is **scoped** to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The ecosystem is **Cargo**, which is a source dependency ecosystem. Per the Ecosystem Mappings in the security matrix:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` (2.2.x) / `release/0.3.z` (2.1.x) |

Source dependency ecosystems produce 2 tasks per affected stream: upstream backport (or dependency bump if fix is available) + downstream propagation.

## Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` maps to the source repository **rhtpa-backend**. Looking up the deployment context from the Source Repositories table:

| Repository | Deployment Context |
|------------|--------------------|
| rhtpa-backend | **customer-shipped** |

The deployment context `customer-shipped` is recorded as part of the CVE metadata. This will be used in Step 8 (Remediation) to generate coordination guidance in remediation task descriptions. Customer-shipped components require coordination with Product Security for CVE assignment, advisory preparation, and formal disclosure.

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | Fixed: ships >= 0.11.14 |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | Fixed: ships >= 0.11.14 |

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD (latest tag) | Fixed? |
|--------|-----------|-----------------|------------------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |

### Summary

- **2.2.x stream** (scoped): Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 are already fixed. The upstream branch `release/0.4.z` already ships the fix (0.11.14 at v0.4.11+).
- **2.1.x stream** (cross-stream): All versions (2.1.0, 2.1.1) are affected. The upstream branch `release/0.3.z` does NOT yet ship the fix (0.11.9 at latest tag v0.3.12).
- **Affects Versions correction needed**: PSIRT set "RHTPA 2.0.0" but the actual affected versions are RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (within the scoped 2.2.x stream). RHTPA 2.0.0 does not exist in the configured version streams.
