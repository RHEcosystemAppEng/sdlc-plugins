# Step 0.7 -- Early Assignment

**Proposed actions (before data extraction):**

1. **Assign TC-8051 to the current user:**
   ```
   jira.edit_issue("TC-8051", assignee=<current-user-account-id>)
   ```

2. **Discover the Assigned transition:**
   ```
   jira.get_transitions("TC-8051")
   ```
   Select the transition whose target status name is "Assigned".

3. **Transition TC-8051 from New to Assigned:**
   ```
   jira.transition_issue("TC-8051", <assigned-transition-id>)
   ```
   The issue is currently in New status, so the transition proceeds.

These actions provide immediate visibility into who is actively triaging
TC-8051 and enable Step 7 (Concurrent Triage Detection) to reliably
identify active work.

---

# Step 1 -- Data Extraction

## Parsed CVE Data Table

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99002 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Stream scope | **2.2.x** (scoped -- analyze only the 2.2.x stream) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | rustls |
| Affected version range | versions before 0.23.5 (< 0.23.5) |
| Fixed version | 0.23.5 |
| CVSS | 8.1 (High) |
| Upstream fix PR | https://github.com/rustls/rustls/pull/2100 |
| Advisory URL | -- |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99002 |
| Due date | 2026-08-01 |
| Existing comments | None |
| Reporter | (from Jira issue reporter field) |
| Deployment context | upstream (default -- no Deployment Context column in Source Repositories table) |

### Ecosystem Detection

The vulnerable library is **rustls**, a Rust crate. Based on the Ecosystem
Mappings table in the 2.2.x stream's security-matrix.md, the ecosystem is
**Cargo** (source dependency ecosystem).

Per the ecosystem classification table:
- **Category**: Source dependency
- **Remediation tasks per stream**: 2 (upstream backport + downstream propagation)

### Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to
the **2.2.x** stream in the Version Streams table. Triage is scoped to
this stream only.
