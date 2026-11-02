# Step 0.7 — Early Assignment

**Proposed actions (eval — no Jira calls executed):**

1. **Assign TC-8051** to the current user.
2. **Transition TC-8051** to Assigned status (current status: New → discover the "Assigned" transition dynamically via `jira.get_transitions(TC-8051)`).

---

# Step 1 — Data Extraction

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99002 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] → stream 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | rustls |
| Affected version range | < 0.23.5 |
| Fixed version | 0.23.5 |
| Upstream fix PR | https://github.com/rustls/rustls/pull/2100 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99002 |
| Due date | 2026-08-01 |
| CVSS | 8.1 (High) |
| Existing comments | None |
| Ecosystem | Cargo (rustls is a Rust crate — read from Ecosystem Mappings in security-matrix.md) |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to the 2.2.x stream only.

## Deployment Context Lookup

The Source Repositories table does not include a Deployment Context column. Per backward compatibility, all repositories default to `upstream`.
