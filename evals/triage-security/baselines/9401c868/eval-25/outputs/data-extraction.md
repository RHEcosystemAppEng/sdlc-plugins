# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md (claude-md-security-config.md):

| Setting | Value |
|---------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Embargo policy URL | _(not configured)_ |
| Upstream Affected Component custom field | _(not configured)_ |
| PS Component custom field | _(not configured)_ |
| Stream custom field | _(not configured)_ |
| ProdSec contact email | _(not configured)_ |
| ProdSec Jira account ID | _(not configured)_ |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Local Path |
|------------|-----|------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend |

Configuration validation: PASSED. All required sections present.

---

# Step 1 -- Data Extraction

## Parsed CVE Data from TC-8040

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`) and summary text |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches `pscomponent:` pattern) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Due date | 2026-07-15 | Jira `duedate` field |
| Assignee | Unassigned | Jira `assignee` field |
| Status | New | Jira `status` field |

## Remote Links

| URL | Type |
|-----|------|
| https://github.com/advisories/GHSA-2026-qp73-x4mq | GitHub Advisory |
| https://www.cve.org/CVERecord?id=CVE-2026-31812 | CVE Record |
| https://github.com/quinn-rs/quinn/pull/2048 | Upstream fix PR |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Match found in Version Streams table: Yes (2.2.x -> git.example.com/rhtpa/rhtpa-release.0.4.z)
- Issue stream scope: **scoped to 2.2.x**

## Ecosystem Detection

- Library name: quinn-proto
- Component context: pscomponent:org/rhtpa-server
- **Detected ecosystem: Go modules**

### Ecosystem Mappings Check (from security-matrix.md)

Ecosystems configured in the 2.2.x stream (rhtpa-release.0.4.z):

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

Supported ecosystems: **Cargo**, **RPM**

**Result: "Go modules" is NOT listed in the Ecosystem Mappings table.**

Automated triage cannot proceed for this ecosystem. The skill halts at Step 1 (Ecosystem detection) per the unsupported ecosystem rule.

## Deployment Context Lookup

- Repository: rhtpa-backend (from Source Repositories table)
- Deployment context: `upstream` (default -- no Deployment Context column present)

## Existing Comments

_(no comments on the issue)_
