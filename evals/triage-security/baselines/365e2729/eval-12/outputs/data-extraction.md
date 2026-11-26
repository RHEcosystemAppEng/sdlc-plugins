# Step 1 – Data Extraction: TC-8030

Source: mock Jira issue `vuln-issue-enrichment.md` (no live Jira call made).

## Pre-flight (Steps 0 – 0.8)

| Check | Result |
|---|---|
| Step 0 – Configuration | PASS. Repository Registry, Jira Configuration (Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence and Security Configuration (Product Lifecycle, Version Streams, Source Repositories) all present. |
| Jira version prefix | `RHTPA` |
| Vulnerability issue type ID | `10024` |
| Component label pattern | `pscomponent:` |
| VEX Justification field | `customfield_12345` (configured) |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |
| Upstream Affected Component field | Not configured, so Steps 4.3 and 7 are skipped |
| ProdSec contact / account ID | Not configured, so @mentions are skipped |
| Source Repositories deployment context | Column absent, so default is `upstream` (coordination guidance omitted, per backward-compat rule) |
| Step 0.3 – Matrix staleness | WARNING. `Last-Updated: 2026-06-28T10:00:00Z` is 151 days old (threshold 14 days). Options: Refresh now / Proceed anyway / Stop. For this eval: **proceed anyway** with the current matrix. |
| Step 0.6 – Mode | Interactive (no `FULLSEND_OUTPUT_DIR`). Jira writes are simulated in output files. |
| Step 0.8 – Assign/transition | Proposed: assign TC-8030 to the current user and transition New -> Assigned (not executed; eval mode). |

## Extracted CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8030 | Issue |
| Status | New, so the full triage path applies | Issue |
| CVE ID | **CVE-2026-48901** | Label `CVE-2026-48901` + summary |
| Summary | CVE-2026-48901 h2 - HTTP/2 CONTINUATION flood [rhtpa-2.2] | Issue |
| Affected component | `pscomponent:org/rhtpa-server`, which maps to repository `rhtpa-backend` (Ecosystem Mappings repo `backend`) | Labels |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | **h2** (Rust crate, hyperium/h2) | Description |
| Affected version range | **"versions prior to the fix"**. This is imprecise: the text gives no numeric threshold | Description |
| Fixed version | **"see advisory"**. The description gives no numeric value | Description |
| CVSS | 7.5 (High) | Description |
| Vulnerability | HTTP/2 CONTINUATION flood: h2 does not limit CONTINUATION frames after HEADERS, which causes memory/CPU exhaustion (DoS) | Description |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p ; https://rustsec.org/advisories/RUSTSEC-2026-0089.html | Remote links / References |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 | Remote links |
| Due date | 2026-08-01 | `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | None | Issue |

## Critical-field assessment

- CVE ID: parsed.
- Library: parsed (`h2`).
- Affected range: **not precisely parseable from the Jira description** ("versions prior to the fix"). Normally the skill would stop here and ask the engineer. Step 1.5 enrichment is always run, though, and the MITRE and OSV.dev records give a machine-readable threshold (`< 0.4.8`, fixed `0.4.8`). That resolves the gap (see `enrichment.md`), so triage continues using the external data.

## Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to stream **2.2.x**, which matches Version Streams row `2.2.x` (`git.example.com/rhtpa/rhtpa-release.0.4.z`).
- **Issue stream scope: 2.2.x (scoped).** Steps 3, 4 and 8 are limited to 2.2.x. Other streams are handled via Case A (cross-stream impact).

## Ecosystem detection

- `h2` is a Rust crate, so the ecosystem is **Cargo**, which is listed in both streams' Ecosystem Mappings.
- Category: **source dependency**, so each affected stream gets 2 remediation tasks.
- Lock file: `Cargo.lock`. Check command: `git show <tag>:Cargo.lock`. Upstream branches: `release/0.3.z` (2.1.x) and `release/0.4.z` (2.2.x).

## Deployment context

- `rhtpa-backend` has no Deployment Context column in Source Repositories, so the default is `upstream`. Because the column is absent, the Coordination Guidance subsection is omitted from task descriptions.
