# Step 0.8 — Early Assignment

Before data extraction, the following actions are proposed:

1. **Assign TC-8030** to the current user (retrieves account ID via `jira.user_info()`)
2. **Transition TC-8030 to Assigned** — the issue is currently in `New` status, so the transition to `Assigned` is applicable. Discover the target transition dynamically via `jira.get_transitions(TC-8030)` and select the transition whose target status name is `"Assigned"`.

These actions provide immediate visibility into who is actively triaging the issue and enable Step 7 (Concurrent Triage Detection) to reliably identify active work.

---

# Step 1 — Data Extraction

**Issue**: TC-8030

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x (mapped from summary suffix `[rhtpa-2.2]` to Version Streams table) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | "versions prior to the fix" (**imprecise** — no specific version threshold provided in description) |
| Fixed version | "see advisory" (**imprecise** — no specific version provided in description) |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| Due date | 2026-08-01 |
| Existing comments | None |
| Ecosystem | Cargo (h2 is a Rust crate on crates.io) |
| Deployment context | upstream (default — no Deployment Context column in Source Repositories table) |

**Note**: The Jira description does not provide a precise affected version range or fixed version. The affected range is stated as "versions prior to the fix" and the fixed version is "see advisory." Step 1.5 (External CVE Data Enrichment) will query MITRE CVE API and OSV.dev to obtain precise fix thresholds.
