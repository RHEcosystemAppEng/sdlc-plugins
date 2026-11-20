# Step 1 – Data Extraction: TC-8001

Source: simulated `jira.get_issue(TC-8001)` + `jira.get_issue_remote_links(TC-8001)` (read from `vuln-issue-standard.md`; no Jira calls made).

## Parsed CVE data

| Field | Value |
|-------|-------|
| Issue key | TC-8001 |
| Issue type / Status | Vulnerability / New |
| CVE ID | CVE-2026-31812 (from label `CVE-2026-31812` and summary) |
| Affected component | `pscomponent:org/rhtpa-server` (matches Component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Ecosystem | Cargo (Rust crate) — source dependency; lock file `Cargo.lock` in `backend` |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) — DoS (panic via excessive STREAMS frame count) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 (quinn-rs/quinn#2048) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (GHSA-2026-qp73-x4mq); also https://rustsec.org/advisories/RUSTSEC-2026-0042.html |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 (already past as of 2026-11-20) |
| Assignee | Unassigned (Step 0.8 would assign to the current triager and transition New -> Assigned) |
| Reporter | psirt-analyst (account ID `557058:psirt-analyst-mock-id`) |
| Existing comments | None |

## Stream scope resolution

| Item | Value |
|------|-------|
| Summary suffix | `[rhtpa-2.2]` |
| Mapped stream | **2.2.x** (`git.example.com/rhtpa/rhtpa-release.0.4.z`) — matches configured Version Streams |
| Scope | **Scoped** to 2.2.x. The 2.1.x stream is out of scope for this issue (cross-stream handling in Step 4 / Case A) |

## Deployment context

Affected repository: `rhtpa-backend` (Cargo / `backend`). The Source Repositories table has no
Deployment Context column, so it defaults to `upstream`; per the template, coordination guidance
is left out when the column is absent.

## Configuration (Step 0) notes

- Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Jira version prefix `RHTPA`, Vulnerability issue type ID 10024.
- VEX Justification field: customfield_12345 (configured).
- ProdSec contact email: prodsec-team@example.com (for reference only).
- ProdSec Jira account ID: 557058:prodsec-mock-account-id (used for the @mention in Step 3).
- Not configured: Upstream Affected Component field (so Steps 4.3 and 7 are skipped), Embargo policy URL (so Step 1.7 is skipped).

## Step 0.3 – Matrix staleness warning

The matrix `Last-Updated` timestamp is 2026-06-28T10:00:00Z, which is **145 days old** as of
2026-11-20 (threshold: 14 days). Releases after 2.2.4 (2026-05-04) may be missing. In interactive
mode the engineer would choose Refresh / Proceed / Stop. For this eval we **proceed with the
current matrix** and record the warning.

## Step 1.5 – External enrichment

The MITRE CVE API and OSV.dev were **not queried** (eval: no external calls). Fix-threshold
confidence is therefore lower. The Jira description threshold applies (< 0.11.14, fixed in 0.11.14).
It agrees with the RustSec/GHSA references listed in the issue, but those were not fetched either.

## Step 1.7 – Embargo check

Skipped: no Embargo policy URL is configured. CVSS 7.5 would otherwise meet the threshold.
