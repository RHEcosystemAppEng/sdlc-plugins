# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| Issue Key | TC-8040 |
| CVE ID | CVE-2026-31812 |
| Affected Component | pscomponent:org/rhtpa-server |
| Product Version (PSIRT-claimed) | rhtpa-2.2 |
| Stream Scope | 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable Library | quinn-proto |
| Affected Version Range | versions before 0.11.14 |
| Fixed Version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream Fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due Date | 2026-07-15 |
| Assignee | Unassigned |
| Status | New |
| Existing Comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the configured Version Stream **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

## Ecosystem Detection

| Detection Input | Value |
|-----------------|-------|
| Library Name | quinn-proto |
| Component Label | pscomponent:org/rhtpa-server |
| Detected Ecosystem | Go modules |

### Ecosystem Mappings (from security-matrix.md)

The 2.2.x stream's Ecosystem Mappings table lists the following supported ecosystems:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

**Result**: The detected ecosystem **Go modules** is NOT listed in the Ecosystem Mappings table. Automated triage cannot proceed for this ecosystem.
