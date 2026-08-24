# Step 1 -- Data Extraction for TC-8021

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`) and summary text |
| Affected component | pscomponent:org/rhtpa-server | Label matching `pscomponent:` pattern |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links (quinn-rs/quinn#2048) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links (GitHub Advisory) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links (CVE Record) |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |
| Upstream Affected Component | quinn-proto | customfield_10632 |
| Issue status | New | Jira status field |
| Assignee | Unassigned | Jira assignee field |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`.

- Parsed suffix: `rhtpa-2.2` maps to stream **2.2.x**
- Matched to Version Streams table entry: `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`
- **Issue stream scope**: 2.2.x (scoped issue -- Steps 3 and 4 apply only to this stream)

## Ecosystem Detection

- Vulnerable library: **quinn-proto** -- this is a Rust crate
- Ecosystem: **Cargo**
- Category: **Source dependency** (per ecosystem classification table)
- Remediation tasks per stream: **2** (upstream backport + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`

## Deployment Context Lookup

- Affected repository: rhtpa-backend (from pscomponent:org/rhtpa-server)
- Deployment context: **upstream** (default -- no Deployment Context column in Source Repositories table)

## Version Impact Analysis (Step 2)

Using mock lock file data from security-matrix-mock.md:

### quinn-proto versions by pinned tag

| Stream | Version | Build Tag | quinn-proto version | Affected? | Notes |
|--------|---------|-----------|---------------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.x | 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed version) |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed version) |

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Status |
|--------|-----------|-----------------|------------|
| 2.1.x | Cargo | release/0.3.z | Unknown -- would need git show to verify |
| 2.2.x | Cargo | release/0.4.z | Fixed (v0.4.11+ ships 0.11.14) |

### Affects Versions Mismatch

The PSIRT-assigned Affects Versions is `RHTPA 2.0.0`, which does not correspond to any version in the supportability matrix. The issue is scoped to stream 2.2.x, and the actual affected versions in that stream are:

- RHTPA 2.2.0 (quinn-proto 0.11.9 -- AFFECTED)
- RHTPA 2.2.1 (quinn-proto 0.11.12 -- AFFECTED)
- RHTPA 2.2.2 (retag of 2.2.1 -- AFFECTED)

Proposed correction (scoped to 2.2.x only):
- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are NOT affected (ship quinn-proto 0.11.14, the fixed version).

### Cross-Stream Impact (Case A)

Stream 2.1.x is also affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9), but this issue is scoped to 2.2.x. Cross-stream impact would be reported via comment and preemptive remediation tasks for 2.1.x (if no sibling CVE Jira exists for that stream).
