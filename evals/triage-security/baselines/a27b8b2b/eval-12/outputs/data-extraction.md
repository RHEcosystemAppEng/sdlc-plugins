# Step 0.7 -- Early Assignment

Before extracting CVE data, assign the issue and transition to Assigned status:

1. **Retrieve current user's Jira account ID**: `jira.user_info()`
2. **Assign TC-8030 to current user**: `jira.edit_issue("TC-8030", assignee=<current-user-account-id>)`
3. **Discover Assigned transition**: `jira.get_transitions("TC-8030")` -- select the transition whose target status name is "Assigned"
4. **Transition to Assigned**: `jira.transition_issue("TC-8030", <assigned-transition-id>)`

The issue is currently in New status, so the transition proceeds.

---

# Step 1 -- Data Extraction

**Issue**: TC-8030
**Source**: Jira Vulnerability issue (PSIRT-created)

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-48901 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | h2 | Description text ("A vulnerability was found in h2") |
| Affected version range | **IMPRECISE** -- "versions prior to the fix" | Description text (no specific version threshold provided) |
| Fixed version | **IMPRECISE** -- "see advisory" | Description text (no specific version number provided) |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 | Remote links |
| Due date | 2026-08-01 | Issue `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to the **2.2.x** stream in Version Streams configuration. Triage is scoped to the 2.2.x stream.

## Ecosystem Detection

The vulnerable library **h2** is a Rust crate (part of the crates.io ecosystem). Checking the 2.2.x stream's Ecosystem Mappings table in security-matrix.md:

- **Cargo** is listed with Repository `backend`, Lock File `Cargo.lock`, Check Command `git show <tag>:Cargo.lock`

h2 is a **Cargo** (source dependency) ecosystem package. Per the ecosystem classification table, source dependency ecosystems produce **2 tasks** per stream (upstream backport + downstream propagation).

## Deployment Context Lookup

The Source Repositories table in CLAUDE.md does not include a Deployment Context column. Per backward compatibility rules, all repositories default to **upstream**.

## Critical Note

The Jira description provides **imprecise** version data:
- Affected range: "versions prior to the fix" (no version number)
- Fixed version: "see advisory" (no version number)

**Step 1.5 (External CVE Data Enrichment) is required** to obtain a precise fix threshold for version impact comparison in Step 2.3.
