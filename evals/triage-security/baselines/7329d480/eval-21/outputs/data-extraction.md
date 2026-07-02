# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue Key | TC-8020 | Jira issue key |
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected Component | pscomponent:org/rhtpa-server | Labels (matches `pscomponent:` pattern) |
| Product Version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable Library | quinn-proto | Description |
| Affected Version Range | versions before 0.11.14 (< 0.11.14) | Description |
| Fixed Version | 0.11.14 | Description |
| CVSS Score | 7.5 (High) | Description |
| Upstream Fix PR | quinn-rs/quinn#2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due Date | 2026-07-15 | Jira `duedate` field |
| Existing Comments | None | Jira comments |
| Upstream Affected Component | quinn-proto | customfield_10632 |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream configured in Security Configuration (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This issue is **stream-scoped** to **2.2.x**. Steps 3 and 4 will apply only to versions within the 2.2.x stream. Cross-stream impact on 2.1.x will be handled via Case B (cross-stream impact comment).

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The 2.2.x stream's Ecosystem Mappings table lists **Cargo** as a supported ecosystem with:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

Ecosystem: **Cargo** (source dependency)

This means remediation will require two tasks: an upstream backport task (fix in the source repo) and a downstream propagation subtask (update the reference in the Konflux release repo).

## Deployment Context Lookup

The affected repository `rhtpa-backend` is listed in the Source Repositories table. No explicit Deployment Context column is present, so the default context of `upstream` applies.

## Version Impact Analysis (Step 2)

Using the mock lock file data from security-matrix, the quinn-proto versions by build tag are:

### Stream 2.2.x (in-scope)

| Product Version | Build Tag | quinn-proto Version | Affected? | Rationale |
|----------------|-----------|---------------------|-----------|-----------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 (fix threshold) |
| 2.2.2 | v0.4.9 | 0.11.12 | YES | Same as v0.4.8 (retag of 2.2.1) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fix threshold) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fix threshold) |

### Stream 2.1.x (cross-stream, out of scope for this issue)

| Product Version | Build Tag | quinn-proto Version | Affected? | Rationale |
|----------------|-----------|---------------------|-----------|-----------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |

## Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, which is incorrect -- there is no 2.0.x stream configured. Based on lock file analysis scoped to the 2.2.x stream, the correct Affects Versions are:

- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are NOT affected (they ship quinn-proto 0.11.14, which is at or above the fix threshold).

## Configuration Extracted (Step 0)

| Parameter | Value |
|-----------|-------|
| Project Key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira Version Prefix | RHTPA |
| Vulnerability Issue Type ID | 10024 |
| Product Pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component Label Pattern | pscomponent: |
| VEX Justification Custom Field | customfield_12345 |
| Upstream Affected Component Custom Field | customfield_10632 |
