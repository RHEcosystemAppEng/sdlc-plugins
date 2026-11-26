# Step 2 – Version Impact Analysis: CVE-2026-48901 (h2 < 0.4.8)

Fix threshold: **enriched from Step 1.5** (MITRE `lessThan: 0.4.8` + OSV `fixed: 0.4.8`).
Affected means h2 < 0.4.8. h2 0.4.8 and later is NOT affected. Lock file data comes from the
fixture's mock `git show <tag>:Cargo.lock` output (h2 versions by tag).

## 2.1 Matrix load

Streams enumerated from the Version Streams table: **2.1.x** (rhtpa-release.0.3.z) and
**2.2.x** (rhtpa-release.0.4.z). Matrix format: required sections present
(Supportability Matrix, Source Pinning Method, Ecosystem Mappings, Forward Pointer). Result: Pass.
(Staleness warning from Step 0.3: last updated 2026-06-28, 151 days old. Proceeded anyway.)

## 2.2 Development stream

The fixture has no Jira unreleased-version metadata and no branch-HEAD lock data, so no
development stream could be identified. 2.2.x is the latest configured stream
("no forward pointer"). In a live run, check `getJiraIssueTypeMetaWithFields` for
unreleased `RHTPA` versions and inspect `release/0.4.z` HEAD (see 2.5).

## 2.4 Version impact table

Version Impact for CVE-2026-48901 (h2 < 0.4.8, fixed 0.4.8):

| Version | Stream | backend tag | h2 | Affected? | Notes |
|---------|--------|-------------|----|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | **YES** | 0.4.5 < 0.4.8. Out of issue scope (cross-stream) |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8. Out of issue scope (cross-stream) |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.4.8 | NO | 0.4.8 = fixed version (boundary, not affected) |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.4.8 | NO | 0.4.8 = fixed version |
| 2.2.2 | 2.2.x | `v0.4.8` | — | NO | same as 2.2.1 (backend retag of 2.2.1; lock check skipped) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.9 | NO | 0.4.9 > 0.4.8 |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.9 | NO | 0.4.9 > 0.4.8 |

**Summary**
- **Issue stream scope (2.2.x): NOT affected.** Every 2.2.x release ships h2 >= 0.4.8.
- **Other stream (2.1.x): AFFECTED.** 2.1.0 and 2.1.1 ship h2 0.4.5.
- Pin notes: the 2.2.0 row's backend tag `v0.4.5` must not be confused with h2 0.4.5. The
  matrix "Build" column (0.4.x) is the product build number, not the h2 crate version.

## 2.3.5 Dependency chain context (2.1.x affected versions)

```
Dependency chain for h2 (Cargo):
  backend (workspace) -> ? -> h2 0.4.5
  Type: NOT DETERMINED from fixture data (only Cargo.lock version lines were provided;
        no manifest / dependency-graph output). h2 is usually pulled in transitively
        via hyper (HTTP/2), but this is unverified and must be confirmed with
        `git show v0.3.12:Cargo.lock` (reverse dependency lookup) before remediation.
  Profile: assumed production (HTTP/2 server stack). Verify no dev-only scope.
  Introduction point: present in all versions of both streams. 2.2.x picked up
                      h2 0.4.8 starting at 2.2.0 (backend v0.4.5).
```

## 2.5 Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | not in fixture (needs `git -C rhtpa-backend show release/0.3.z:Cargo.lock`) | UNKNOWN |
| 2.2.x | Cargo | `release/0.4.z` | not in fixture | n/a (stream not affected at any released pin; latest pin v0.4.12 ships 0.4.9) |

Because the 2.1.x upstream fix status cannot be confirmed from the evidence, remediation for
2.1.x uses the **upstream backport** variant. If `release/0.3.z` HEAD already ships
h2 >= 0.4.8, switch to the dependency-bump variant.

## Step 3 – Affects Versions Correction (scoped to 2.2.x)

- Current: `[RHTPA 2.2.0]`, then Proposed: `[]` (none). RHTPA 2.2.0 ships h2 0.4.8, which is the
  fixed version, so the PSIRT assignment is wrong.
- 2.1.0 and 2.1.1 are **not** added. They belong to the 2.1.x stream (sibling/companion scope).
- Proposed comment (with footnote): "Corrected Affects Versions: [RHTPA 2.2.0] -> [].
  Based on lock file analysis at pinned commits from security-matrix.md, all 2.2.x
  releases ship h2 >= 0.4.8 (fixed per MITRE/OSV). Scoped to stream 2.2.x per issue suffix."

## Steps 4–7 (notes)

- Step 4: search siblings with `labels = CVE-2026-48901`. The fixture shows no sibling data, so
  assume there is no `[rhtpa-2.1]` companion issue. Step 4.3 is skipped (Upstream Affected
  Component field not configured).
- Step 5: 2.1.x lifecycle status must be checked at the Product pages URL. The fixture has no
  lifecycle data, so 2.1.x is assumed supported.
- Step 6: no resolved siblings in the fixture, so nothing is already fixed.
- Step 7: skipped (Upstream Affected Component field not configured).
