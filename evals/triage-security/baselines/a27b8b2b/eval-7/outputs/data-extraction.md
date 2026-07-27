# Step 1 -- Data Extraction

## Step 0.7 -- Early Assignment Actions

Before extracting CVE data, assign the issue and transition to Assigned status:

1. **Retrieve current user account ID**: `jira.user_info()` -- retrieves the current user's Jira account ID.
2. **Assign TC-8006 to current user**: `jira.edit_issue("TC-8006", assignee=<current-user-account-id>)` -- assigns the CVE issue to the active triage engineer.
3. **Discover Assigned transition**: `jira.get_transitions("TC-8006")` -- dynamically discover the transition whose target status name is "Assigned". Do NOT hardcode a transition ID.
4. **Transition to Assigned**: `jira.transition_issue("TC-8006", <assigned-transition-id>)` -- TC-8006 is currently in New status, so this transition proceeds.

These actions provide immediate visibility into who is actively triaging the issue and enable Step 7 (Concurrent Triage Detection) to reliably identify active work.

---

## Step 1 -- Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | (not provided in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | (none) |
| Ecosystem | Cargo (Rust crate -- quinn-proto is a Cargo package) |

### Stream Scope Resolution

- Issue summary contains stream suffix: `[rhtpa-2.1]`
- Mapped to Version Streams table: stream **2.1.x** (Konflux release repo: rhtpa-release.0.3.z)
- Issue stream scope: **2.1.x only**

### Existing Issue Links

| Link Type | Direction | Linked Issue | Summary |
|-----------|-----------|--------------|---------|
| Related | outward (TC-8006 -> TC-8001) | TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |

### Deployment Context Lookup

- Affected repository: rhtpa-backend (from component label pscomponent:org/rhtpa-server)
- Source Repositories table has no Deployment Context column -- defaulting to `upstream`
