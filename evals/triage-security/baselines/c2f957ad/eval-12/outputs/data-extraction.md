# Step 1 – Data Extraction: TC-8030

## Preliminary checks

- **Step 0.6 Mode**: interactive mode (`FULLSEND_OUTPUT_DIR` not set). Eval constraint: no Jira, git, or WebFetch calls; mock fixture data used.
- **Step 0 Configuration** (from `claude-md-security-config.md`): all required sections are present (Repository Registry, Jira Configuration, Code Intelligence, Security Configuration with Product Lifecycle, Version Streams, Source Repositories).
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Jira version prefix: RHTPA
  - Vulnerability issue type ID: 10024
  - Product pages URL: https://access.example.com/product-life-cycle/rhtpa
  - Component label pattern: `pscomponent:`
  - VEX Justification custom field: customfield_12345
  - Embargo policy URL: not configured, so Step 1.7 is skipped
  - Upstream Affected Component field: not configured, so Steps 4.3 and 7 are skipped
  - Source Repositories: rhtpa-backend. There is no Deployment Context column, so it defaults to `upstream` and coordination guidance is omitted.
- **Step 0.3 Matrix staleness**: `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-26, so the matrix is **151 days old**, which is over the 14-day threshold.
  > Security matrix for streams **2.1.x / 2.2.x** was last updated on 2026-06-28 (151 days ago). The matrix may not reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.
  For this eval: **Proceed anyway** with the current matrix. Releases after 2.2.4 / 2.1.1 may be missing.

## Extracted fields

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8030 | Issue |
| Status | New | Issue. Full triage path applies |
| CVE ID | CVE-2026-48901 | Label `CVE-2026-48901` and summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | h2 (Rust crate, hyperium/h2) | Description |
| Affected version range | "versions prior to the fix". **Imprecise, no numeric threshold** | Description |
| Fixed version | "see advisory". **Not stated** | Description |
| CVSS | 7.5 (High) | Description |
| Vulnerability | HTTP/2 CONTINUATION flood: unbounded CONTINUATION frames after HEADERS cause excessive memory/CPU use (DoS) | Description |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p (also RUSTSEC-2026-0089: https://rustsec.org/advisories/RUSTSEC-2026-0089.html) | Remote links / References |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 | Remote links |
| Due date | 2026-08-01 (**already past**: today is 2026-11-26) | `duedate` |
| Assignee | Unassigned (Step 0.8 would assign to the current user and transition New to Assigned, after confirmation; not run in this eval) | Issue |
| Existing comments | None | Issue |

### Critical-field assessment

- CVE ID: parsed.
- Library: parsed (h2).
- Affected range: **not parseable from the Jira description**. The prose "versions prior to the fix" gives no version to compare against. Normally this would stop execution until the engineer supplies a range. Step 1.5 (External CVE Data Enrichment) always runs, though, and its structured data supplies the missing threshold (`< 0.4.8`). See `enrichment.md`.

## Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to stream **2.2.x**, which matches the configured Version Stream `git.example.com/rhtpa/rhtpa-release.0.4.z`.
- **Issue stream scope: 2.2.x (scoped).** Stream 2.1.x is outside this issue's scope. It is still analyzed for cross-stream impact (Case A).

## Ecosystem detection

- h2 is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in both streams' Ecosystem Mappings (`Cargo.lock`, repository `backend`).
- Category: **source dependency**, which means 2 remediation tasks per affected stream (upstream backport or dependency bump, plus downstream propagation).

## Deployment context

- Affected repository: rhtpa-backend (`backend` in Ecosystem Mappings). The Source Repositories table has no Deployment Context column, so the default is `upstream`. Per backward-compatibility rules, the Coordination Guidance subsection is omitted from remediation tasks.
