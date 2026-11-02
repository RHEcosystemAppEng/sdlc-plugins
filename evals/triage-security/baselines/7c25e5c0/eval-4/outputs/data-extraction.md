# Step 0.7 — Early Assignment

**Proposed actions (not executed — eval mode):**

1. Assign TC-8004 to the current user
2. Transition TC-8004 from New → Assigned

These actions would be performed before data extraction to provide visibility into active triage.

---

# Step 1 — Data Extraction

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | _(no stream suffix — unscoped)_ |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | < 0.4.8 |
| Fixed version | 0.4.8 |
| Upstream fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |
| Advisory URL | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| CVE record URL | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |
| Due date | 2026-08-01 |
| CVSS | 7.5 (High) |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" has **no stream suffix** in brackets.

**Result**: This issue is **unscoped** — it covers all configured streams. Version impact analysis will check ALL versions across all streams (2.1.x and 2.2.x).

## Ecosystem Detection

Library `h2` is a Rust crate. The Ecosystem Mappings tables for both streams list **Cargo** as a supported ecosystem with repository `backend`, lock file `Cargo.lock`, and check command `git show <tag>:Cargo.lock`.

**Ecosystem**: Cargo (source dependency)
**Remediation task structure**: 2 tasks per affected stream — upstream backport + downstream propagation
