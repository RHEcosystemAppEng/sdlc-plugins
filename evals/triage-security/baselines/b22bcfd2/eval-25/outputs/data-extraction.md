# Step 1 -- Data Extraction

## Issue: TC-8040

Data extracted from Vulnerability issue TC-8040 (using issue details from TC-8001 fixture as the base issue data).

### Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (Component label pattern: `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | < 0.11.14 | Description: "versions before 0.11.14" |
| Fixed version | 0.11.14 | Description: "Fixed version: 0.11.14" |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | _(none)_ | Issue comment history |

### Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Issue stream scope: **scoped to 2.2.x**

### Ecosystem Detection

The ecosystem detection for the vulnerable library resolved to **Go modules**.

**Ecosystem Mappings check**: The security-matrix.md Ecosystem Mappings tables for the configured version streams list the following supported ecosystems:

- Stream 2.1.x: **Cargo**, **RPM**
- Stream 2.2.x: **Cargo**, **RPM**

**Result**: Go modules is **NOT** listed in any stream's Ecosystem Mappings table.

Automated triage cannot proceed for this ecosystem. See `unsupported-ecosystem.md` for the notification presented to the user.
