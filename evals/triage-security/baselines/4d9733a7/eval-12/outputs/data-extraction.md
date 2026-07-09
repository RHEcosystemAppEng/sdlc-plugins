# Step 0.7 -- Early Assignment

**Proposed actions:**

1. **Assign TC-8030** to the current user via `jira.edit_issue(TC-8030, assignee=<current-user-account-id>)`
2. **Transition TC-8030 to Assigned** via `jira.transition_issue(TC-8030, <assigned-transition-id>)` (discovered dynamically from `jira.get_transitions(TC-8030)`)

---

# Step 1 -- Data Extraction

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | **versions prior to the fix** (imprecise -- no specific threshold given) |
| Fixed version | **see advisory** (imprecise -- no specific version given) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| Due date | 2026-08-01 |
| Existing comments | None |
| CVSS | 7.5 (High) |

### Stream scope resolution

Issue summary contains stream suffix `[rhtpa-2.2]` -- mapped to stream **2.2.x** from the Version Streams table.

### Ecosystem detection

The library **h2** is a Rust crate. Ecosystem: **Cargo**.

### Note on imprecise data

The Jira description does **not** provide a specific fix threshold. The affected versions field says "versions prior to the fix" and the fixed version says "see advisory." This imprecise data requires Step 1.5 external CVE data enrichment to obtain a precise fix threshold for version impact analysis.
