# Step 1 -- Data Extraction: TC-8040

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (Component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links (GHSA) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links (cve.org) |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |
| Issue status | New | Jira status field |
| Assignee | Unassigned | Jira assignee field |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for stream `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to 2.2.x

## Ecosystem Detection

- Library: quinn-proto
- Component: org/rhtpa-server
- **Detected ecosystem: Go modules**

### Ecosystem Mappings Check

The Ecosystem Mappings tables in the configured security matrices were consulted:

**Stream 2.1.x (rhtpa-release.0.3.z):**

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

**Stream 2.2.x (rhtpa-release.0.4.z):**

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

**Result: "Go modules" is NOT listed in any stream's Ecosystem Mappings table.**

The supported ecosystems across all configured streams are: Cargo, RPM. The detected ecosystem "Go modules" does not match any of these entries. Automated triage cannot proceed for this ecosystem.

## Deployment Context Lookup

- Affected repository (from component label `pscomponent:org/rhtpa-server`): rhtpa-backend
- Deployment context: `upstream` (from Source Repositories table)
