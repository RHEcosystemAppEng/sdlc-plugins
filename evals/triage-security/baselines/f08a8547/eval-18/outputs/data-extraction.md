# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data Table

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`) and summary text |
| Affected component | pscomponent:org/rhtpa-server | Label matching `pscomponent:` pattern |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | quinn-rs/quinn#2048 | Remote link: https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | GHSA-2026-qp73-x4mq | Remote link: https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | CVE-2026-31812 | Remote link: https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 | Issue `duedate` field |
| Assignee | engineer-a@example.com | Issue `assignee` field |
| Issue status | In Progress | Issue `status` field |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server, ai-cve-triaged | Issue `labels` field |
| Upstream Affected Component (customfield_10632) | quinn-proto | Custom field |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-server | Custom field |
| Stream (customfield_10832) | rhtpa-2.2 | Custom field |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams row: `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to 2.2.x

## Ecosystem Detection

- Vulnerable library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Classification: **Source dependency** -- produces 2 remediation tasks per stream (upstream backport + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`

## Existing Comments Detected

1. **Description digest comment**: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2` -- posted by sdlc-workflow/triage-security on 2026-07-01T10:00:00Z
2. **Post-triage summary comment**: Documents completed triage including version impact, actions taken (Affects Versions corrected, ai-cve-triaged label added, remediation tasks TC-8100 and TC-8101 created, transitioned to In Progress) -- posted by sdlc-workflow/triage-security on 2026-07-01T10:01:00Z

## Existing Issue Links Detected

- **Depend**: TC-8100 (upstream backport task) -- Status: In Progress, Labels: ai-generated-jira, Security, CVE-2026-31812
- **Depend**: TC-8101 (downstream propagation task) -- Status: Open, Labels: ai-generated-jira, Security, CVE-2026-31812; Blocks TC-8100

## Version Impact (from security-matrix mock data)

Using quinn-proto versions by tag for stream 2.2.x (rhtpa-release.0.4.z):

| Version | Build Tag | quinn-proto Version | Affected? (< 0.11.14) |
|---------|-----------|--------------------|-----------------------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES |
| 2.2.1 | v0.4.8 | 0.11.12 | YES |
| 2.2.2 | v0.4.9 | (retag of v0.4.8) = 0.11.12 | YES |
| 2.2.3 | v0.4.11 | 0.11.14 | NO (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO (fixed) |

Cross-stream check (stream 2.1.x, rhtpa-release.0.3.z):

| Version | Build Tag | quinn-proto Version | Affected? (< 0.11.14) |
|---------|-----------|--------------------|-----------------------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.1 | v0.3.12 | 0.11.9 | YES |
