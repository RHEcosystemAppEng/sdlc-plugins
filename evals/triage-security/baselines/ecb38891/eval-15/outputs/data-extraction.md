# Step 0.7 -- Early Assignment

Before extracting CVE data, assign the issue and transition to Assigned status:

1. **Retrieve current user's Jira account ID:**
   ```
   jira.user_info()
   ```
   Result: current user account ID retrieved.

2. **Assign the issue to the current user:**
   ```
   jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
   ```
   Proposed action: Assign TC-8001 to the current user.

3. **Discover the target transition dynamically:**
   ```
   jira.get_transitions("TC-8001")
   ```
   Select the transition whose target status name is "Assigned". Do NOT hardcode a transition ID.

4. **Transition to Assigned (issue is in New status):**
   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```
   Proposed action: Transition TC-8001 from New to Assigned.

---

# Step 0 -- Configuration Extraction

Extracted from claude-md-security-config-prodsec.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **ProdSec contact email**: prodsec-team@example.com
- **ProdSec Jira account ID**: 557058:prodsec-mock-account-id
- **Version Streams**: 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z)
- **Source Repositories**: rhtpa-backend (no Deployment Context column -- defaulting all repos to upstream)

---

# Step 1 -- Data Extraction

**Issue**: TC-8001
**Reporter**: psirt-analyst (account ID: 557058:psirt-analyst-mock-id)

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Ecosystem | Cargo (source dependency -- Rust crate) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

### Stream scope resolution

Issue summary contains stream suffix `[rhtpa-2.2]` -- mapped to stream **2.2.x** (rhtpa-release.0.4.z). Triage is scoped to the 2.2.x stream.

### Ecosystem detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings table for the 2.2.x stream lists **Cargo** as a configured ecosystem with lock file `Cargo.lock`. Ecosystem classification: **source dependency** -- produces 2 tasks per stream (upstream backport + downstream propagation).

### Deployment context lookup

Repository rhtpa-backend: no Deployment Context column in Source Repositories table -- defaults to `upstream`.
