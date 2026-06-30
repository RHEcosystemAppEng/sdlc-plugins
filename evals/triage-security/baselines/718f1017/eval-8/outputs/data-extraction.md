# Data Extraction — TC-8010

## Step 1: Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | axios |
| Affected version range | versions before 1.8.2 |
| Fixed version | 1.8.2 |
| Upstream fix PR | (none found in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Due date | 2026-08-01 |
| Existing comments | (none) |
| CVSS | 8.1 (High) |

## Custom Fields

| Field ID | Field Name | Value |
|----------|-----------|-------|
| customfield_10632 | Upstream Affected Component | axios |
| customfield_10669 | PS Component | pscomponent:org/rhtpa-ui |
| customfield_10832 | Stream | rhtpa-2.2 |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. Mapping this to the
configured Version Streams table:

- `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)

This issue is **stream-scoped** to the 2.2.x stream. Steps 3-7 will apply only
to versions within the 2.2.x stream.

## Ecosystem Detection

The vulnerable library is **axios**, which is a JavaScript/TypeScript npm package.
The ecosystem is **npm**.

Note: The security-matrix.md for stream 2.2.x (rhtpa-release.0.4.z) lists Cargo
and RPM ecosystems but does not include an npm ecosystem mapping. This means there
is no configured lock file path or check command for npm dependencies in this stream.
The mock lock file data does not include axios version data by tag either.

However, based on the CVE description:
- **Affected package**: axios
- **Affected versions**: versions before 1.8.2
- **Fixed version (fix threshold)**: 1.8.2

## Issue Links

No existing issue links on TC-8010.

## Remote Links

- [GHSA-2026-ax91-r7pp](https://github.com/advisories/GHSA-2026-ax91-r7pp) -- GitHub Advisory
- [CVE-2026-44492](https://www.cve.org/CVERecord?id=CVE-2026-44492) -- CVE Record
