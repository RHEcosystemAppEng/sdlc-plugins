# Step 1 — Data Extraction for TC-8001

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary text |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches Component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | [rhtpa-2.2] | Summary suffix in brackets |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`.

1. Parsed suffix: `rhtpa-2.2` maps to stream `2.2.x`
2. Matched to Version Streams table: stream `2.2.x` is configured with Konflux Release Repo `git.example.com/rhtpa/rhtpa-release.0.4.z`
3. **Issue stream scope: 2.2.x** — Steps 3 and 7 are scoped to this stream only

## Ecosystem Detection

- **Ecosystem**: Cargo (Rust crate)
- quinn-proto is a Rust crate, identified from the library name and the Cargo ecosystem mapping in the stream's security-matrix.md
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- Upstream branch (2.2.x stream): `release/0.4.z`
- Repository: backend (rhtpa-backend)

## Observations

- The PSIRT-assigned Affects Versions (`RHTPA 2.0.0`) does not match any configured Version Stream (2.1.x or 2.2.x). There is no 2.0.x stream. This will be corrected in Step 3.
- CVSS 7.5 (High) meets the embargo check threshold (>= 7.0). If an Embargo policy URL were configured, an embargo warning gate would be presented. No Embargo policy URL is configured in this project's Security Configuration, so Step 1.7 is skipped.
