# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Issue Key | TC-8011 |
| Summary | CVE-2026-45678 webpack - Arbitrary Code Execution via loader chain [rhtpa-2.2] |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-ui |
| Product Version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable Library | webpack |
| Affected Version Range | < 5.98.0 (versions before 5.98.0) |
| Fixed Version | 5.98.0 |
| CVSS | 7.8 (High) |
| Upstream Fix PR | N/A |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due Date | 2026-08-15 |
| Upstream Affected Component (customfield_10632) | webpack |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui |
| Stream (customfield_10832) | rhtpa-2.2 |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Version Streams table. Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library is **webpack**, a JavaScript/TypeScript build tool distributed via npm. Based on the library name and component context, the ecosystem is **npm** (not Cargo or RPM).

The npm ecosystem uses `package-lock.json` as its lock file. The Check Command from the Ecosystem Mappings table determines how to extract the dependency version at each pinned commit.

## Issue Links

No existing issue links on TC-8011.

## Remote Links

- [GHSA-2026-wk55-m3rr](https://github.com/advisories/GHSA-2026-wk55-m3rr) -- GitHub Advisory
- [CVE-2026-45678](https://www.cve.org/CVERecord?id=CVE-2026-45678) -- CVE Record

## Comments

No existing comments.
