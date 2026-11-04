# Step 2 – Version Impact Analysis: CVE-2026-48901 (h2 < 0.4.8)

Fix threshold used: **h2 < 0.4.8 affected; >= 0.4.8 fixed** — the enriched,
cross-validated threshold from Step 1.5 (MITRE `lessThan: 0.4.8`, OSV
`fixed: 0.4.8`). The Jira description ("versions prior to the fix") was not
usable as a threshold.

Lock-file evidence: simulated `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`
output from the "h2 versions by tag" section of the mock matrix fixture. All
released versions use the pinned backend tag from the supportability matrix
(never a branch tip).

## 2.1 – Matrix load and validation

Both streams (2.1.x / rhtpa-release.0.3.z and 2.2.x / rhtpa-release.0.4.z) loaded
from the mock. Required sections present (Supportability Matrix, Source Pinning
Method, Ecosystem Mappings with columns
`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`, Forward
Pointer). Validation: Pass. (Staleness warning from Step 0.3: matrix 129 days old.)

## 2.2 – Development stream

Not determinable in this eval: no Jira version metadata (`released: false`
versions) is available in the fixture, and no branch-HEAD lock-file data is
provided. The 2.2.x stream is the latest configured stream (no forward pointer).
Development-stream impact is **not assessed** — no value is assumed.

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

| Stream | Version | Backend tag | h2 | Affected? | Notes |
|--------|---------|-------------|----|-----------|-------|
| 2.1.x | 2.1.0 | `v0.3.8` | 0.4.5 | **YES** | outside issue scope (cross-stream) |
| 2.1.x | 2.1.1 | `v0.3.12` | 0.4.5 | **YES** | outside issue scope (cross-stream) |
| 2.2.x | 2.2.0 | `v0.4.5` | 0.4.8 | NO | 0.4.8 = fixed version (lessThan is exclusive) |
| 2.2.x | 2.2.1 | `v0.4.8` | 0.4.8 | NO | 0.4.8 = fixed version |
| 2.2.x | 2.2.2 | `v0.4.8` | — | NO | same as 2.2.1 (backend retag of 2.2.1; lock check skipped, result carried forward) |
| 2.2.x | 2.2.3 | `v0.4.11` | 0.4.9 | NO | |
| 2.2.x | 2.2.4 | `v0.4.12` | 0.4.9 | NO | |
| dev | — | branch HEAD | not available | not assessed | no Jira unreleased-version or HEAD lock data in fixture |

### Summary

- **Issue scope (2.2.x): NOT affected.** Every 2.2.x release ships h2 >= 0.4.8.
  Even the earliest release (2.2.0, backend `v0.4.5`) already ships h2 0.4.8,
  the exact fixed version.
- **Cross-stream (2.1.x): AFFECTED.** 2.1.0 and 2.1.1 ship h2 0.4.5 (< 0.4.8).

### Boundary note

The critical comparison is at 2.2.0 / 2.2.1, which ship exactly h2 0.4.8. Both
MITRE (`lessThan`) and OSV (`fixed`) define 0.4.8 as the first non-vulnerable
version, so these are NOT affected. Treating the threshold as `<= 0.4.8` (or
trusting PSIRT's scan-time assignment) would incorrectly mark 2.2.0–2.2.2 as
affected.

## 2.3.5 – Dependency chain context (affected versions: 2.1.0, 2.1.1)

```
Dependency chain for h2:
  backend (workspace) → ? → h2 0.4.5
  Type: not determined — Cargo.toml / full Cargo.lock dependency graph is not in
        the fixture. h2 is commonly pulled in transitively (e.g., via hyper /
        reqwest / tonic), but this must be verified with
        `git show v0.3.12:Cargo.lock` (dependents of h2) and the workspace
        Cargo.toml files before choosing the remediation approach.
  Profile: not determined (assumed production until verified; h2 is an HTTP/2
        runtime library, not a typical dev-only dependency)
  Introduction point: present in all 2.1.x and 2.2.x releases; version moved
        0.4.5 (2.1.x) → 0.4.8 (2.2.0+) → 0.4.9 (2.2.3+)
```

## 2.5 – Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | not available in fixture | unknown |
| 2.2.x | Cargo | `release/0.4.z` | not needed (stream not affected; latest release already ships 0.4.9) | n/a |

Because the 2.1.x upstream branch HEAD version is not available, the fix cannot be
confirmed as already present upstream → the 2.1.x remediation uses the **upstream
backport + downstream propagation** pair (not the dependency-bump variant). If
`git show release/0.3.z:Cargo.lock` later shows h2 >= 0.4.8, switch to the
dependency-bump variant / ref-bump only.

## Step 3 – Affects Versions correction (proposed)

| | Value |
|---|---|
| Current (PSIRT) | RHTPA 2.2.0 |
| Lock-file evidence | 2.2.0 ships h2 0.4.8 (fixed) — not affected; no 2.2.x version affected |
| Proposed | Remove RHTPA 2.2.0. No 2.2.x versions to add (scoped issue — 2.1.x versions are not added to this issue). |

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields`
(not executed). Correction comment would include the Comment Footnote.

## Steps 4–7 (eval notes)

- **Step 4 (siblings/duplicates):** JQL for other `CVE-2026-48901` Vulnerability
  issues (e.g., an `[rhtpa-2.1]` companion) not executed; no sibling data in the
  fixture. Outcome determines whether 2.1.x gets preemptive tasks (see
  remediation.md). Step 4.3 skipped (Upstream Affected Component field not
  configured).
- **Step 5 (lifecycle):** product pages not fetched; 2.1.x lifecycle status must be
  confirmed before creating 2.1.x tasks.
- **Step 6 (already fixed):** no resolved sibling data; not applicable to 2.2.x
  (never affected).
- **Step 7 (concurrent triage):** skipped — Upstream Affected Component field not
  configured.
