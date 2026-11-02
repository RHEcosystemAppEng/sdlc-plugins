# Step 1 — Data Extraction

## Step 0.7 — Early Assignment

- **Action**: Assign TC-8040 to the current user
- **Action**: Transition TC-8040 from New → Assigned

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] → stream 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| CVSS | 7.5 (High) |

## Ecosystem Detection

The vulnerable library is quinn-proto. Based on the library name and component context (rhtpa-server), the ecosystem detection resolves to **Go modules**.

### Ecosystem Mappings Check

The configured Ecosystem Mappings tables for the relevant streams list:

**Stream 2.1.x (rhtpa-release.0.3.z):**

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| RPM | — | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | — |

**Stream 2.2.x (rhtpa-release.0.4.z):**

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | — | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | — |

**Result**: Go modules is **not listed** in either stream's Ecosystem Mappings table. The supported ecosystems are Cargo and RPM only.

**Automated triage stops here.** The unsupported ecosystem notification is presented to the user.
