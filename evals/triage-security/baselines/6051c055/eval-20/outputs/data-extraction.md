# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches Component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 | Description ("versions before 0.11.14") |
| Fixed version | 0.11.14 | Description |
| CVSS score | 7.5 (High) | Description |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Due date | 2026-07-15 | Jira `duedate` field |
| Existing comments | None | Issue comment history |
| Issue status | New | Jira `status` field |
| Assignee | Unassigned | Jira `assignee` field |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`).

| Summary suffix | Mapped stream | Konflux release repo |
|----------------|---------------|----------------------|
| `[rhtpa-2.2]` | 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z |

This is a **stream-scoped** issue. Steps 3-4 will apply to the 2.2.x stream. Cross-stream impact (Case B) will check the 2.1.x stream for proactive remediation.

## Ecosystem Detection

| Field | Value |
|-------|-------|
| Ecosystem | Cargo |
| Rationale | quinn-proto is a Rust crate; the ecosystem mappings table for both streams lists Cargo with `Cargo.lock` as the lock file |
| Lock file | `Cargo.lock` |
| Check command | `git show <tag>:Cargo.lock` |

As a source dependency (Cargo ecosystem), remediation will produce two tasks per affected stream: an upstream backport task (source repo fix) and a downstream propagation subtask (Konflux release repo update).

## Deployment Context Lookup

| Repository | Source | Deployment Context |
|------------|--------|--------------------|
| rhtpa-backend | Source Repositories table in CLAUDE.md | upstream (default -- no Deployment Context column present) |

## Affects Versions Discrepancy (Noted for Step 3)

The PSIRT-assigned Affects Versions field shows **RHTPA 2.0.0**, but there is no 2.0.x stream configured in the Version Streams table. The configured streams are 2.1.x and 2.2.x. This will need correction in Step 3 after the version impact analysis in Step 2 determines which versions actually ship the vulnerable dependency.

## Critical Fields Validation

All critical fields were successfully parsed:

- CVE ID: CVE-2026-31812 (present)
- Vulnerable library: quinn-proto (present)
- Affected version range: < 0.11.14 (present)

No missing critical fields. Proceeding to Step 1.5 (External CVE Data Enrichment).
