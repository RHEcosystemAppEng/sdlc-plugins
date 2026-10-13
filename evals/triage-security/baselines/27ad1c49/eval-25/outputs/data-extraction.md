# Step 1 -- Data Extraction for TC-8040

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Match found in Version Streams table: Yes (stream `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue stream scope: **scoped to 2.2.x**

## Ecosystem Detection

- Vulnerable library: quinn-proto
- Component context: pscomponent:org/rhtpa-server
- **Detected ecosystem: Go modules**

### Ecosystem Mappings Check

Checked the Ecosystem Mappings table for stream 2.2.x (rhtpa-release.0.4.z):

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

**Result: Go modules is NOT listed in the Ecosystem Mappings table.**

The supported ecosystems for this stream are Cargo and RPM. The detected ecosystem (Go modules) does not match any configured ecosystem mapping. Automated triage cannot proceed for this ecosystem because there is no configured lock file path, check command, or upstream branch mapping.

## Deployment Context Lookup

- Affected repository (from component label): org/rhtpa-server
- Source Repositories table lookup: no Deployment Context column present
- Deployment context: **upstream** (default)
