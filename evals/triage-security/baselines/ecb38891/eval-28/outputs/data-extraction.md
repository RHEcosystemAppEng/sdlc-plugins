# Step 0.7 -- Early Assignment

Before extracting CVE data, assign the Vulnerability issue and transition it to Assigned status for triage visibility and concurrent triage detection (Step 7).

1. **Retrieve current user's Jira account ID:**
   ```
   jira.user_info()
   ```
   Result: current user account ID retrieved.

2. **Assign the issue to the current user:**
   ```
   jira.edit_issue("TC-8060", assignee=<current-user-account-id>)
   ```
   Proposed action: assign TC-8060 to the current user.

3. **Discover the target transition dynamically:**
   ```
   jira.get_transitions("TC-8060")
   ```
   Select the transition whose target status name is "Assigned". The transition ID is discovered at runtime from the Vulnerability workflow -- not hardcoded.

4. **Transition to Assigned:**
   ```
   jira.transition_issue("TC-8060", <assigned-transition-id>)
   ```
   Proposed action: transition TC-8060 from New to Assigned status.

The issue is currently in New status, so both the assignment and the transition proceed.

---

# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99010 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | < 0.4.5 |
| Fixed version | 0.4.5 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | -- |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99010 |
| Due date | 2026-08-15 |
| Reporter | psirt-analyst (account ID: 557058:psirt-analyst-mock-id) |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. Mapping to configured Version Streams:

- `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)

**Issue stream scope**: 2.2.x (scoped -- analysis targets 2.2.x versions only; other streams checked for cross-stream impact in Case A)

## Ecosystem Detection

The vulnerable library `h2` is a Rust crate. Based on the component context (pscomponent:org/rhtpa-server, a Rust backend service) and the library name, the ecosystem is **Cargo**.

Cargo is a **source dependency** ecosystem per the classification table. Remediation produces **two tasks** per affected stream: upstream backport + downstream propagation.

## Deployment Context Lookup

The Source Repositories table does not include a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream`. No Coordination Guidance subsection will be included in remediation task descriptions.
