# Step 1 — Data Extraction

## Step 0.7 — Early Assignment

**Proposed actions (not executed — eval mode):**

1. Assign TC-8010 to current user
2. Transition TC-8010 from New → Assigned

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | [rhtpa-2.2] → stream 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | axios |
| Affected version range | < 1.8.2 |
| Fixed version | 1.8.2 |
| CVSS | 8.1 (High) |
| Upstream fix PR | — |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Due date | 2026-08-01 |
| Existing comments | None |

### Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]` → mapped to stream **2.2.x** from Version Streams table.

### Ecosystem Detection

Library: **axios** — detected ecosystem: **npm** (JavaScript/TypeScript package).

npm is a source dependency ecosystem → remediation produces 2 tasks per stream (upstream backport/dependency bump + downstream propagation).

### Custom Fields

- **Upstream Affected Component** (customfield_10632): `axios`
- **PS Component** (customfield_10669): `pscomponent:org/rhtpa-ui`
- **Stream** (customfield_10832): `rhtpa-2.2`

### Deployment Context Lookup

Source Repositories table does not have a Deployment Context column → defaulting all repositories to `upstream`.
