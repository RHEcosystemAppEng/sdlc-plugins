# Step 2 – Version Impact Analysis: TC-8004

Issue scope: **unscoped** -> all streams analyzed. Lock file evidence taken from the mock `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'` data in the security matrix (simulated output; pinned commits only).

## 2.1 – Supportability matrix (aggregated)

| Stream | Version | Build | backend pin | Notes |
|---|---|---|---|---|
| 2.1.x | 2.1.0 | 0.3.8 | `v0.3.8` | |
| 2.1.x | 2.1.1 | 0.3.12 | `v0.3.12` | |
| 2.2.x | 2.2.0 | 0.4.5 | `v0.4.5` | |
| 2.2.x | 2.2.1 | 0.4.8 | `v0.4.8` | |
| 2.2.x | 2.2.2 | 0.4.9 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.x | 2.2.3 | 0.4.11 | `v0.4.11` | |
| 2.2.x | 2.2.4 | 0.4.12 | `v0.4.12` | |

Format validation (2.1.1): both stream sections contain Supportability Matrix, Source Pinning Method, Ecosystem Mappings (correct 5 columns), Forward Pointer -> PASS.

## 2.2 – Development stream

Requires Jira `getJiraIssueTypeMetaWithFields` (unreleased RHTPA versions) - not callable in this eval. No unreleased-version data supplied, and no development-branch HEAD lock data exists in the inputs. 2.2.x is the latest stream (no forward pointer); its newest pins (`v0.4.11`, `v0.4.12`) ship h2 0.4.9 (fixed). Development stream HEAD check: **not performed - no data** (would be `git show HEAD:Cargo.lock` in rhtpa-backend).

## 2.4 – Version impact table

Version Impact for CVE-2026-33501 (h2 < 0.4.8):

| Version | Stream | backend tag | h2 | Affected? | Notes |
|---------|--------|-------------|----|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | **YES** | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | **YES** | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.4.8 | NO | ships fixed version (0.4.8 = fix threshold) |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.4.8 | NO | |
| 2.2.2 | 2.2.x | `v0.4.8` | — | NO | same as 2.2.1 (retag; lock check skipped, result carried forward) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.9 | NO | |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.9 | NO | |

### Stream summary — MIXED IMPACT

| Stream | Affected versions | Not affected versions | Stream status |
|---|---|---|---|
| 2.1.x | 2.1.0, 2.1.1 | — | **AFFECTED** (all versions ship h2 0.4.5) |
| 2.2.x | — | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | **NOT AFFECTED** (all versions ship h2 >= 0.4.8) |

Key finding: PSIRT's Affects Versions includes RHTPA 2.2.0, but 2.2.0 already ships the patched h2 0.4.8 — a false positive. 2.1.1 is affected but missing from Affects Versions.

## 2.3.5 – Dependency chain context (2.1.x)

```
Dependency chain for h2 (Cargo):
  backend (workspace) → ... → h2 0.4.5
  Type: NOT DETERMINED — the eval data provides only the h2 package version
        from Cargo.lock; Cargo.toml manifests / full lock graph were not supplied.
        (h2 is commonly pulled transitively via hyper/reqwest/tonic, but this is
        NOT asserted without evidence.)
  Profile: assumed production (HTTP/2 server library in rhtpa-server image);
           not verified as dev/build-only — no dev-dependency label applied.
  Introduction point: h2 0.4.5 present at v0.3.8 and v0.3.12; 2.2.x moved to
           0.4.8 by v0.4.5 and 0.4.9 by v0.4.11.

Remediation: if direct, bump h2 to >= 0.4.8 in Cargo.toml/Cargo.lock; if
transitive, prefer bumping the direct dependency (e.g. hyper), fall back to
`cargo add h2@0.4.8` pin. Engineer must confirm chain with
`cargo tree -i h2` on release/0.3.z.
```

## 2.5 – Upstream fix status

| Stream | Ecosystem | Repository | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|------------|-----------------|-----------------|--------|
| 2.1.x | Cargo | backend | `release/0.3.z` | unknown (no data) | **UNKNOWN — treat as not fixed** |
| 2.2.x | Cargo | backend | `release/0.4.z` | n/a (stream not affected) | — |

No branch-HEAD data for `release/0.3.z` was supplied; the skill forbids guessing. Without confirmation that the upstream branch already ships h2 >= 0.4.8, the 2.1.x remediation uses the **upstream backport + downstream propagation** path. If the engineer confirms `git -C /home/dev/repos/rhtpa-backend show release/0.3.z:Cargo.lock` already shows h2 >= 0.4.8, switch the first task to the dependency-bump variant.

## Steps 4–7 (summary)

- **Step 4**: JQL `project = TC AND labels = 'CVE-2026-33501' AND issuetype = 10024 AND key != TC-8004` -> empty (per eval). No duplicates, no companions, no links needed. 4.3 skipped (Upstream Affected Component field not configured). 4.4 preemptive search (`labels = 'security-preemptive' AND labels = 'CVE-2026-33501'`) -> assumed empty; no reconciliation.
- **Step 5**: Lifecycle page not fetched (external calls prohibited). 2.1.0/2.1.1 are listed in the active supportability matrix; assumed supported — engineer should confirm against https://access.example.com/product-life-cycle/rhtpa.
- **Step 6**: No resolved siblings -> not already fixed.
- **Step 7**: Skipped (Upstream Affected Component field not configured).
