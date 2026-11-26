# Step 1 – Data Extraction: TC-8030

## Pre-flight (Steps 0 – 0.8)

| Check | Result |
|-------|--------|
| Step 0.6 Fullsend mode | `FULLSEND_OUTPUT_DIR` absent → **interactive mode** (eval: Jira/git/WebFetch simulated from fixtures) |
| Step 0 Configuration | PASS — Repository Registry, Jira Configuration (Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence, Security Configuration (Product Lifecycle, Version Streams, Source Repositories) all present |
| Jira version prefix | `RHTPA` |
| Vulnerability issue type ID | `10024` |
| Component label pattern | `pscomponent:` |
| VEX Justification field | `customfield_12345` (configured) |
| Upstream Affected Component field | not configured → Step 4.3 and Step 7 skipped |
| ProdSec account ID / email | not configured → @mentions skipped |
| Embargo policy URL | not configured → Step 1.7 skipped |
| Step 0.3 Matrix staleness | **WARNING** — both stream matrices carry `Last-Updated: 2026-06-28T10:00:00Z`, which is 148 days old (threshold 14 days). In a live run the engineer would be offered Refresh / Proceed / Stop; for this eval we proceed with the current matrix. |
| Step 0.8 Assign + transition | Would assign TC-8030 to the current user and transition New → Assigned (simulated; no Jira call made) |

## Extracted CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8030 | Jira |
| Status | New (full triage path) | Jira `status` |
| CVE ID | **CVE-2026-48901** | Label `CVE-2026-48901` + summary |
| Summary | CVE-2026-48901 h2 - HTTP/2 CONTINUATION flood [rhtpa-2.2] | Jira |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` |
| Vulnerable library | **h2** (hyperium/h2 crate) | Description |
| Affected version range (Jira) | "versions prior to the fix" — **imprecise, no numeric threshold** | Description |
| Fixed version (Jira) | "see advisory" — **not stated** | Description |
| CVSS | 7.5 (High) | Description |
| Vulnerability | Unbounded CONTINUATION frames after HEADERS → excessive memory/CPU → DoS | Description |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p | Remote links |
| Additional advisory | https://rustsec.org/advisories/RUSTSEC-2026-0089.html | Description references |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 | Remote links |
| Due date | 2026-08-01 (already past as of 2026-11-23) | `duedate` |
| Assignee | Unassigned | Jira |
| Existing comments | none | Comment history |

### Critical-field assessment

- CVE ID: parsed.
- Library: parsed (`h2`).
- Affected range: **only qualitatively parsed** from the Jira description ("versions
  prior to the fix"). No numeric threshold can be derived from Jira alone. This gap is
  resolved by Step 1.5 External CVE Data Enrichment (MITRE + OSV both give `< 0.4.8`),
  so execution does not need to stop for engineer input.

## Stream scope resolution

- Suffix `[rhtpa-2.2]` → stream **2.2.x**
- Matches configured Version Stream `2.2.x` → `git.example.com/rhtpa/rhtpa-release.0.4.z`
- **Issue stream scope: 2.2.x (scoped)**. Steps 3–8 scoped to 2.2.x; 2.1.x is "other stream" for cross-stream (Case A) handling.

## Ecosystem detection

- Library `h2` is a Rust crate (OSV ecosystem `crates.io`) → **Cargo**
- Cargo is listed in both streams' Ecosystem Mappings (repository `backend`, lock file `Cargo.lock`, check `git show <tag>:Cargo.lock`)
- Category: **Source dependency** → 2 remediation tasks per affected stream

## Deployment context

- Affected repository: `rhtpa-backend` (backend)
- Source Repositories table has **no Deployment Context column** → defaults to `upstream`
  for metadata; per remediation-templates.md backward-compatibility rule, the
  Coordination Guidance subsection is **omitted** from task descriptions.
