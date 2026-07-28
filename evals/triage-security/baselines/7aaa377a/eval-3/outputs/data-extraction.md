# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Version Streams**: 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z)
- **Source Repositories**: rhtpa-backend (upstream -- no Deployment Context column, defaulting to upstream)

## Step 0.3 -- Matrix Staleness Check

Security matrix Last-Updated timestamp: 2026-06-28T10:00:00Z
Days since last update: 30 days (as of 2026-07-28)

The matrix is older than the 14-day default threshold. In a live triage, the
engineer would be prompted to refresh, proceed anyway, or stop. For this eval,
proceeding with the current matrix.

## Step 0.7 -- Assign and Transition to Assigned

**Proposed actions:**
1. Assign TC-8003 to the current user
2. Retrieve available transitions via `jira.get_transitions(TC-8003)`
3. Select the transition whose target status name is "Assigned"
4. Transition TC-8003 from New to Assigned

These actions provide immediate visibility into who is actively triaging the
issue and enable Step 7 (Concurrent Triage Detection).

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | _(not available from remote links)_ |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the
**2.2.x** stream in the Version Streams table. Triage is scoped to the 2.2.x
stream only.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem
Mappings table in the 2.2.x stream's security-matrix.md, this maps to the
**Cargo** ecosystem.

Cargo is a **source dependency** ecosystem, which would normally produce two
remediation tasks per stream (upstream backport + downstream propagation).
However, duplicate detection (Step 4) will determine whether remediation tasks
are needed at all.
