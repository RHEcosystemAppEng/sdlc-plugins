# Step 1 -- Data Extraction for TC-8006

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels: `CVE-2026-31812`; Summary text |
| Affected component | `pscomponent:org/rhtpa-server` | Labels (matches Component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | `[rhtpa-2.1]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.1.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description: "A vulnerability was found in quinn-proto" |
| Affected version range | versions before 0.11.14 (i.e., < 0.11.14) | Description: "before version 0.11.14" |
| Fixed version | 0.11.14 | Description: "Fixed version: 0.11.14" |
| Upstream fix PR | Not provided | No GitHub PR URL in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| CVSS | 7.5 (High) | Description |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |
| Issue status | New | Jira status field |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x** (matches Version Streams table row: Stream `2.1.x`, Konflux Release Repo `git.example.com/rhtpa/rhtpa-release.0.3.z`)
- Issue stream scope: **2.1.x only**

This is a stream-scoped issue. Steps 3-4 will apply only to the 2.1.x stream for Affects Versions and remediation scoping. Cross-stream impact on the 2.2.x stream will be handled via Step 4.2 (companion tracking) and Case B (proactive remediation) if applicable.

## Ecosystem Detection

- Library: quinn-proto (a Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- This is a source dependency ecosystem, so remediation would require two tasks (upstream backport + downstream propagation)

## Existing Issue Links

The issue already has the following links:

| Link Type | Direction | Linked Issue | Linked Issue Summary |
|-----------|-----------|--------------|----------------------|
| Related | outward (TC-8006 -> TC-8001) | TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |

Link ID: 1990401

## Version Impact (from mock lock file data)

For the 2.1.x stream (issue scope):

| Version | Tag | quinn-proto version | Affected? (< 0.11.14) | Notes |
|---------|-----|---------------------|-----------------------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | |

For the 2.2.x stream (cross-stream analysis):

| Version | Tag | quinn-proto version | Affected? (< 0.11.14) | Notes |
|---------|-----|---------------------|-----------------------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | ships fixed version |

All 2.1.x versions ship quinn-proto 0.11.9, which is within the affected range (< 0.11.14). Both versions in the issue's stream scope are affected.
