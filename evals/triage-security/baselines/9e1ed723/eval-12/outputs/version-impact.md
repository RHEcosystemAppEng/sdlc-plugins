# Step 2 – Version Impact Analysis: CVE-2026-48901 (h2 < 0.4.8)

## 2.1 – Supportability matrix

Both streams enumerated directly from the Version Streams table (no forward-pointer
chaining). Matrix format: required sections (Supportability Matrix, Ecosystem Mappings,
Source Pinning Method, Forward Pointer) present; Ecosystem Mappings columns
`Ecosystem | Repository | Lock File | Check Command | Upstream Branch` match the
template → **Pass**. Staleness warning (148 days old) recorded in Step 0.3.

| Stream | Konflux repo | Versions |
|--------|--------------|----------|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0, 2.1.1 |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0, 2.2.1, 2.2.2 (retag), 2.2.3, 2.2.4 |

## 2.2 – Development stream

Unreleased Jira versions could not be queried (no Jira access in this eval). The 2.2.x
stream is the latest configured stream (no forward pointer). Development-head evidence
(`git show HEAD:Cargo.lock` on the dev branch) is **not available in the fixture** and
is reported as not determined rather than assumed.

## 2.3 – Dependency versions (Cargo.lock at pinned backend tags)

Comparison uses the **enriched fix threshold from Step 1.5** (`h2 < 0.4.8` affected,
`0.4.8` fixed), not the imprecise Jira prose ("versions prior to the fix").

Version Impact for CVE-2026-48901 (h2 < 0.4.8, fixed 0.4.8):

| Stream | Version | Backend tag | h2 | Affected? | Notes |
|--------|---------|-------------|----|-----------|-------|
| 2.1.x | 2.1.0 | `v0.3.8`  | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.x | 2.1.1 | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.x | 2.2.0 | `v0.4.5`  | 0.4.8 | NO | exactly the fixed version (boundary: `lessThan 0.4.8` excludes 0.4.8) |
| 2.2.x | 2.2.1 | `v0.4.8`  | 0.4.8 | NO | fixed version |
| 2.2.x | 2.2.2 | `v0.4.8`  | —     | NO | same as 2.2.1 (backend retag of 2.2.1; lock check skipped, result carried forward) |
| 2.2.x | 2.2.3 | `v0.4.11` | 0.4.9 | NO | > 0.4.8 |
| 2.2.x | 2.2.4 | `v0.4.12` | 0.4.9 | NO | > 0.4.8 |
| 2.2.x | dev (HEAD) | release/0.4.z HEAD | not determined | — | no HEAD evidence in fixture; every released 2.2.x build already ships >= 0.4.8 |

### Summary

- **Issue scope stream 2.2.x: NOT affected** — every released 2.2.x version ships h2 >= 0.4.8.
- **Other stream 2.1.x: AFFECTED** — 2.1.0 and 2.1.1 ship h2 0.4.5.
- PSIRT-assigned Affects Versions `RHTPA 2.2.0` is **incorrect**: 2.2.0 ships h2 0.4.8, the fixed version.

### Why enrichment mattered

The Jira description gives no numeric threshold. Without Step 1.5, the 2.2.0 build
(h2 0.4.8) could not be classified at all, and a guessed threshold could easily have
flagged it as affected (matching PSIRT's Affects Versions). The cross-validated MITRE
`lessThan 0.4.8` / OSV `fixed 0.4.8` shows 0.4.8 is the first fixed release, so 2.2.0
is not affected.

## 2.3.5 – Dependency chain context (2.1.x, affected)

```
Dependency chain for h2:
  backend (workspace) → ... → h2 0.4.5
  Type: not determined from fixture — the mock provides only the resolved h2 version
        per tag, not the Cargo.lock dependency graph or Cargo.toml manifests.
        (h2 is commonly pulled in transitively via hyper/reqwest/tonic, but this is
        NOT asserted — must be confirmed by inspecting Cargo.lock "dependencies" arrays
        and Cargo.toml at v0.3.12.)
  Profile: assumed production pending confirmation (h2 is an HTTP/2 runtime crate)
  Introduction point: present in all versions analyzed; 2.1.x pins 0.4.5,
        2.2.0 (v0.4.5) was the first build to ship 0.4.8.
```

Remediation tasks therefore include both direct and transitive remediation approaches.

## 2.5 – Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | not determined (no HEAD evidence in fixture) | Unknown → treated as **not fixed upstream** |
| 2.2.x | Cargo | release/0.4.z | not determined (latest pinned tag v0.4.12 ships 0.4.9) | N/A — stream not affected |

Since the fix cannot be confirmed on `release/0.3.z`, the 2.1.x remediation uses the
**upstream backport + downstream propagation** pair (not the dependency-bump variant).
The implementer should first check `git show release/0.3.z:Cargo.lock`; if it already
ships h2 >= 0.4.8, the upstream task reduces to a no-op and only downstream propagation
is required.

## Engineer confirmation

In a live run the skill waits here for the engineer to confirm the table before Step 3.
