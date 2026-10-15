# Step 1 -- Data Extraction for TC-8020

## Step 0 -- Configuration Validation

The following configuration was validated from the project CLAUDE.md (Security Configuration):

| Setting | Value |
|---------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component custom field | customfield_10632 (configured per task assumption) |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream (default -- no Deployment Context column) |

## Extracted CVE Data

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
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Status | New |
| Upstream Affected Component (customfield_10632) | quinn-proto |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL (GHSA) | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |

### Additional References

- https://rustsec.org/advisories/RUSTSEC-2026-0042.html

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Version Streams configuration. This issue is **stream-scoped** to 2.2.x only. Steps 3 and 4 will be scoped to versions within the 2.2.x stream, and Case A cross-stream impact analysis will check other streams.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings table for both streams lists **Cargo** as the ecosystem for the `backend` repository, with:
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z` (for 2.2.x stream), `release/0.3.z` (for 2.1.x stream)

Ecosystem classification: **Source dependency (Cargo)** -- produces 2 remediation tasks per stream (upstream fix + downstream propagation), or dependency bump + downstream propagation if the upstream branch already ships the fix.

## Deployment Context Lookup

The affected repository `rhtpa-backend` maps to deployment context **upstream** (default, since no Deployment Context column is present in the Source Repositories table). Coordination guidance for upstream context will be included in remediation task descriptions.

## Step 2 -- Version Impact Analysis

### Version Impact Table

Using the mock lock file data for quinn-proto versions by tag, compared against the fix threshold of 0.11.14:

| Version | Stream | Backend Tag | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.8 | 0.11.12 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

### Upstream Fix Status

The upstream branch `release/0.4.z` for the 2.2.x stream ships quinn-proto 0.11.14 at the latest tags (v0.4.11 and v0.4.12), which meets the fix threshold. The upstream fix is **already available**.

| Stream | Ecosystem | Upstream Branch | Version at HEAD (latest tag) | Fixed? |
|--------|-----------|-----------------|------------------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |

Since the upstream fix is available for the 2.2.x stream, the remediation path is the **dependency bump** variant: `cargo update -p quinn-proto` + downstream propagation. For the 2.1.x stream (if preemptive tasks are created), the upstream fix is NOT available on `release/0.3.z`, so the standard upstream backport + downstream propagation tasks would apply.

## Step 3 -- Affects Versions Correction (Proposed)

Current Affects Versions: `[RHTPA 2.0.0]`
RHTPA 2.0.0 does not correspond to any version in the supportability matrix. The PSIRT-assigned version is incorrect.

Since this issue is **scoped to stream 2.2.x**, only 2.2.x versions should be included:

**Proposed correction**: `[RHTPA 2.0.0]` --> `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are NOT affected (they ship quinn-proto 0.11.14, which is the fixed version) and are excluded.

**Proposed Jira action**: `jira.edit_issue(TC-8020, fields={"versions": [{"id": "<RHTPA-2.2.0-id>"}, {"id": "<RHTPA-2.2.1-id>"}, {"id": "<RHTPA-2.2.2-id>"}]})` (version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields`).

**Proposed comment**: "Corrected Affects Versions: [RHTPA 2.0.0] --> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]. Based on lock file analysis at pinned commits from security-matrix.md. Scoped to stream 2.2.x per issue suffix [rhtpa-2.2]."
