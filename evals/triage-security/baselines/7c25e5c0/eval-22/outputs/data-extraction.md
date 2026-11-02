# Step 0.7 — Early Assignment

- **Action**: Assign TC-8021 to the current user
- **Action**: Transition TC-8021 from New → Assigned status (discover transition dynamically via `jira.get_transitions(TC-8021)`, select the transition whose target status name is "Assigned")

These actions provide immediate visibility into who is actively triaging the issue and enable Step 7 (Concurrent Triage Detection) to reliably identify active work.

# Step 1 — Data Extraction

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] → stream 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| CVSS | 7.5 (High) |
| Ecosystem | Cargo (detected from quinn-proto — Rust crate, mapped via Ecosystem Mappings) |
| Stream scope | 2.2.x (from summary suffix [rhtpa-2.2]) |
| Upstream Affected Component | quinn-proto (customfield_10632 as specified in eval prompt) |
