# Step 0.7 -- Early Assignment

Before extracting CVE data, assign the issue and transition to Assigned status.

## Proposed Actions

1. **Retrieve current user's Jira account ID:**

   ```
   jira.user_info()
   ```

2. **Assign TC-8001 to the current user:**

   ```
   jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
   ```

3. **Discover the Assigned transition dynamically:**

   ```
   jira.get_transitions("TC-8001")
   ```

   Select the transition whose target status name is `"Assigned"`.

4. **Transition TC-8001 to Assigned** (issue is currently in New status):

   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```

These actions provide immediate visibility into who is actively triaging TC-8001 and
enable Step 7 (Concurrent Triage Detection) to reliably identify active work.

---

# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x (mapped from suffix `[rhtpa-2.2]` to Version Streams table) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | _(none)_ |
| Reporter | psirt-analyst (account ID: `557058:psirt-analyst-mock-id`) |
| Ecosystem | Cargo (quinn-proto is a Rust crate -- identified from library name and Ecosystem Mappings table in security-matrix.md) |
| Deployment context | upstream (default -- Source Repositories table has no Deployment Context column) |

## Ecosystem Detection

The library `quinn-proto` is a Rust crate. The Ecosystem Mappings table in the 2.2.x
stream's security-matrix.md lists **Cargo** as a configured ecosystem with:

- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

Cargo is classified as a **source dependency** ecosystem. Per the ecosystem classification
table, this means remediation produces **2 tasks per stream**: upstream backport +
downstream propagation (with the downstream subtask blocked by the upstream task).

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream
in the Version Streams table. Steps 3 and 8 will be scoped to this stream only.
Cross-stream impact on the 2.1.x stream will be assessed via Case A.

## Configuration Extracted (Step 0)

| Config Item | Value |
|-------------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| ProdSec contact email | prodsec-team@example.com |
| ProdSec Jira account ID | 557058:prodsec-mock-account-id |
