# Step 1 -- Data Extraction for TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
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

Summary suffix `[rhtpa-2.2]` maps to stream **2.2.x** in the Version Streams table.

Issue stream scope: **2.2.x** (scoped -- only 2.2.x remediation tasks are created directly; other streams are handled via Case B cross-stream impact).

## Ecosystem Detection

- Vulnerable library: quinn-proto (Rust crate)
- Detected ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Cargo ecosystem is listed in the Ecosystem Mappings table for both 2.1.x and 2.2.x streams

## Deployment Context

The Source Repositories table does not include a Deployment Context column. Default: `upstream`. Coordination guidance subsection is omitted from remediation task descriptions (backward compatibility).

## Affects Versions Mismatch

The PSIRT-assigned Affects Versions field contains **RHTPA 2.0.0**, which does not correspond to any configured version stream (2.1.x or 2.2.x). This will be corrected in Step 3 based on lock file evidence from Step 2.
