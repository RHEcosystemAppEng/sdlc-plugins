# Step 0.8 -- Assign and Transition to Assigned

Before data extraction, the following early assignment actions are proposed:

1. **Assign TC-8001 to the current user** -- ensures visibility into who is actively triaging the issue.
2. **Transition TC-8001 from New to Assigned** -- discovered dynamically via `jira.get_transitions(TC-8001)`, selecting the transition whose target status name is "Assigned".

These actions are proposed but not executed (eval prohibits external tool calls).

---

# Step 1 -- Data Extraction

## Parsed CVE Data

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
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

- **Summary suffix:** [rhtpa-2.2]
- **Mapped stream:** 2.2.x
- **Issue stream scope:** Scoped to 2.2.x stream only

## Ecosystem Detection

- **Library:** quinn-proto (Rust crate)
- **Ecosystem:** Cargo
- **Classification:** Source dependency ecosystem
- **Remediation task structure:** 2 tasks per stream (upstream backport + downstream propagation)

## Deployment Context Lookup

- **Affected repository:** rhtpa-backend (matched from component label pscomponent:org/rhtpa-server)
- **Deployment Context column:** Not present in Source Repositories table
- **Default:** upstream (backward compatibility -- no Coordination Guidance subsection will be included in remediation tasks)
