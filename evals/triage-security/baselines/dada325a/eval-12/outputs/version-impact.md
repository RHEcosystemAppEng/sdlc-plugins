# Step 2 – Version Impact Analysis: CVE-2026-48901 (h2 < 0.4.8)

Fix threshold: **affected `< 0.4.8`, fixed `0.4.8`**. This is the enriched threshold from Step 1.5, cross-validated by MITRE and OSV.dev. The Jira description had no numeric threshold.

Dependency versions come from the mock lock-file data in `security-matrix-mock.md` ("h2 versions by tag"), which simulates `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'` at each pinned tag.

## 2.1 Supportability matrix

Both streams from the Version Streams table were enumerated directly (2.1.x and 2.2.x). Both matrices contain Supportability Matrix, Source Pinning Method, Ecosystem Mappings, and Forward Pointer sections, so format validation passes. Staleness warning from Step 0.3: the matrix was last updated 2026-06-28 (131 days old). Releases after 2.2.4 / 2.1.1 may not be listed.

## 2.2 Development stream

No Jira unreleased-version data is available in the fixture, so no separate development stream could be identified and no branch HEAD evidence exists. The upstream branch HEADs (`release/0.3.z`, `release/0.4.z`) are also absent from the mock data. They are marked as not determined rather than assumed.

## 2.4 Version impact table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

| Stream | Version | Build | backend tag (pinned) | h2 | Affected? | Notes |
|--------|---------|-------|----------------------|----|-----------|-------|
| 2.1.x | 2.1.0 | 0.3.8  | `v0.3.8`  | 0.4.5 | **YES** | 0.4.5 < 0.4.8. Cross-stream (outside issue scope) |
| 2.1.x | 2.1.1 | 0.3.12 | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8. Cross-stream (outside issue scope) |
| 2.2.x | 2.2.0 | 0.4.5  | `v0.4.5`  | 0.4.8 | NO | 0.4.8 equals the fixed version, so not affected. PSIRT-claimed Affects Version |
| 2.2.x | 2.2.1 | 0.4.8  | `v0.4.8`  | 0.4.8 | NO | 0.4.8 equals the fixed version |
| 2.2.x | 2.2.2 | 0.4.9  | `v0.4.8`  | —     | NO | Retag of 2.2.1 (backend `v0.4.8`), same as 2.2.1. Lock check skipped |
| 2.2.x | 2.2.3 | 0.4.11 | `v0.4.11` | 0.4.9 | NO | 0.4.9 > 0.4.8 |
| 2.2.x | 2.2.4 | 0.4.12 | `v0.4.12` | 0.4.9 | NO | 0.4.9 > 0.4.8 |
| dev | — | — | branch HEAD | not determined | not determined | No dev-stream or HEAD evidence in the fixture |

### Summary

- **Issue scope (2.2.x): NOT affected.** Every 2.2.x release ships h2 >= 0.4.8.
- **Cross-stream (2.1.x): AFFECTED.** 2.1.0 and 2.1.1 ship h2 0.4.5.
- Using the enriched threshold matters here. The boundary case is 2.2.0, which PSIRT flagged and which ships exactly 0.4.8. With the precise `< 0.4.8` threshold it is correctly classified as NOT affected. The Jira prose ("versions prior to the fix") could not decide this boundary.

## 2.3.5 Dependency chain context (affected versions: 2.1.0, 2.1.1)

```
Dependency chain for h2 (Cargo):
  backend (workspace) → ... → h2 0.4.5
  Type: not determined from available evidence. The mock data supplies only
        the Cargo.lock version line, not the dependency graph or Cargo.toml.
        h2 is commonly pulled in transitively via hyper/reqwest/tonic, but
        that is not verified here and must be confirmed with
        `git show v0.3.12:Cargo.lock` (reverse deps) / `cargo tree -i h2`.
  Profile: not determined (no manifest evidence). Treated as production
        until shown otherwise.
  Introduction point: h2 is present in all versions. 2.1.x pins 0.4.5;
        2.2.0 (v0.4.5) already moved to 0.4.8.
```

## 2.5 Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | not determined (no HEAD lock data in fixture) | Unknown |
| 2.2.x | Cargo | `release/0.4.z` | not determined. All released tags are >= 0.4.8 | N/A (stream not affected) |

Because a fix on `release/0.3.z` cannot be confirmed, 2.1.x remediation uses the **upstream backport + downstream propagation** pair. If the engineer confirms that `release/0.3.z` HEAD already has h2 >= 0.4.8, switch to the dependency-bump variant.

## Step 3 – Affects Versions correction (scoped to 2.2.x)

- Current: `[RHTPA 2.2.0]` → Proposed: `[]` (no 2.2.x version is affected)
- RHTPA 2.2.0 ships h2 0.4.8, the fixed version, so PSIRT's assignment is incorrect.
- The 2.1.x versions are **not** added, because they are outside this issue's `[rhtpa-2.2]` scope and belong to a sibling or companion tracker.
- Comment (would be posted after confirmation): "Corrected Affects Versions: [RHTPA 2.2.0] → [] (none). Based on lock file analysis at pinned commits from security-matrix.md: all 2.2.x releases ship h2 >= 0.4.8 (fixed version per MITRE/OSV). Scoped to stream 2.2.x per issue suffix." The comment includes the triage-security Comment Footnote. No ProdSec @mention, since none is configured.
