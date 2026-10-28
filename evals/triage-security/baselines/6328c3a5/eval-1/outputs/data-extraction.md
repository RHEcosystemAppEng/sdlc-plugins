# Step 0.7 -- Early Assignment Actions

## Assignment

TC-8001 is currently **Unassigned** and in **New** status.

**Actions (would be performed via Jira MCP):**

1. **Assign TC-8001 to the current user:**
   ```
   jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
   ```
   This records who is actively triaging the issue and enables concurrent triage detection (Step 7).

2. **Discover the Assigned transition:**
   ```
   jira.get_transitions("TC-8001")
   ```
   Select the transition whose target status name is "Assigned". Do not hardcode a transition ID.

3. **Transition TC-8001 from New to Assigned:**
   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```
   The issue is currently in New status, so the transition proceeds.

No Jira operations were performed (eval-only mode).

---

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| **CVE ID** | CVE-2026-31812 |
| **Affected component** | `pscomponent:org/rhtpa-server` (from labels) |
| **Product version (PSIRT-claimed)** | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| **Affects Versions (Jira field)** | RHTPA 2.0.0 |
| **Vulnerable library** | quinn-proto |
| **Affected version range** | versions before 0.11.14 (< 0.11.14) |
| **Fixed version** | 0.11.14 |
| **CVSS** | 7.5 (High) |
| **Due date** | 2026-07-15 |
| **Upstream fix PR** | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| **Advisory URL** | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| **CVE record URL** | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| **Existing comments** | None |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **scoped** to the 2.2.x stream. Steps 3 and 4 will apply only to versions within the 2.2.x stream.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The ecosystem is **Cargo**, which is a source dependency ecosystem. The lock file is `Cargo.lock`, and the check command is `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`.

Per the ecosystem classification table:
- Source dependency ecosystem (Cargo) produces **2 tasks per stream**: upstream backport + downstream propagation (or dependency bump + downstream propagation when the upstream fix is available).

## Deployment Context

The affected repository `rhtpa-backend` has deployment context **upstream** (from Source Repositories table in Security Configuration).
