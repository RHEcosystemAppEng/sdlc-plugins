# Step 0.7 — Early Assignment

Before data extraction, perform early assignment actions:

1. **Assign TC-8006** to the current user via `jira.edit_issue(TC-8006, assignee=<current-user-account-id>)`.
2. **Discover the Assigned transition** via `jira.get_transitions(TC-8006)` — select the transition whose target status name is `"Assigned"`.
3. **Transition TC-8006 to Assigned** via `jira.transition_issue(TC-8006, <assigned-transition-id>)` — the issue is currently in New status, so the transition proceeds.

These actions provide immediate visibility into who is actively triaging the issue and enable Step 7 (Concurrent Triage Detection).

---

# Step 1 — Data Extraction

## Parsed CVE Data

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
| Upstream fix PR | _(not provided)_ |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.1]`, which maps to the configured **2.1.x** version stream (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.3.z`). Triage is **scoped** to stream 2.1.x only.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem Mappings in the 2.1.x stream's `security-matrix.md`, this maps to the **Cargo** ecosystem.

- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.3.z`

Cargo is a source dependency ecosystem, so remediation would produce **2 tasks** per stream (upstream backport + downstream propagation).

## Existing Issue Links

The issue already has the following links:

- **Related**: TC-8001 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2])
  - Link ID: 1990401
  - Type: Related
  - Direction: outward (TC-8006 → TC-8001)
