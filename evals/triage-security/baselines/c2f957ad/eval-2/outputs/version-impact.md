# Version Impact Analysis — TC-8002 (CVE-2026-28940, serde_json < 1.0.135)

Source of dependency versions: the "serde_json versions by tag" section of
`security-matrix-mock.md`. It stands in for the output of
`git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'` at each pinned backend tag.
No `git show` was executed.

## Step 2.1 — Supportability Matrix (aggregated)

Both streams in the Version Streams table were enumerated directly, without relying on forward pointers.

Matrix format check: the Supportability Matrix, Ecosystem Mappings, Source Pinning Method
and Forward Pointer sections are present in both streams. The Ecosystem Mappings columns
(`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`) match the template.
Result: Pass.

| Stream | Version | Build | Build Date | backend pinned tag | Notes |
|---|---|---|---|---|---|
| 2.1.x | 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.x | 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |
| 2.2.x | 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.x | 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.x | 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.x | 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.x | 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## Step 2.2 — Development stream

- Jira version metadata (`getJiraIssueTypeMetaWithFields`) was not queried in this eval, so
  no unreleased RHTPA version can be identified.
- 2.2.x is the latest configured stream (its matrix has no forward pointer). No separate
  development stream or branch-HEAD evidence is available in the mock data.
- The upstream branch for 2.2.x is `release/0.4.z`. Its HEAD was not inspected. This does
  not change the outcome, because every released 2.2.x build already ships a patched
  serde_json and the most recent tags show the version moving forward (1.0.138 -> 1.0.139).

## Step 2.3 / 2.4 — Version Impact Table

Fix threshold: serde_json **>= 1.0.135** is fixed. Source: Jira description (external
enrichment unavailable).

### In-scope stream: 2.2.x (issue suffix `[rhtpa-2.2]`)

| Version | serde_json | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.2.0   | 1.0.138    | NO        | `v0.4.5`; 1.0.138 >= 1.0.135 |
| 2.2.1   | 1.0.138    | NO        | `v0.4.8` |
| 2.2.2   | 1.0.138    | NO        | same as 2.2.1 (retag of `v0.4.8`); lock file check skipped |
| 2.2.3   | 1.0.139    | NO        | `v0.4.11` |
| 2.2.4   | 1.0.139    | NO        | `v0.4.12` |

### Other stream (checked for cross-stream impact): 2.1.x

| Version | serde_json | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.1.0   | 1.0.137    | NO        | `v0.3.8`; 1.0.137 >= 1.0.135 |
| 2.1.1   | 1.0.137    | NO        | `v0.3.12` |

### Summary

- **0 of 7** supported released versions ship a vulnerable serde_json.
- The oldest shipped serde_json is 1.0.137, two patch releases above the fix version 1.0.135.
- The PSIRT-assigned Affects Version **RHTPA 2.2.0 is incorrect**. 2.2.0 ships serde_json
  1.0.138, which already contains the fix (the configurable recursion limit that defaults
  to 128 levels).

## Step 2.3.5 — Dependency chain context

Not applicable. The skill traces the dependency chain only for affected versions, and none
are affected. serde_json is present in `Cargo.lock` at every tag, so the component is shipped,
but only in patched versions. Manifest inspection (direct vs. transitive) was not needed.

## Step 2.5 — Upstream fix status

Not required, because no stream is affected and no remediation path needs to be chosen.

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x  | Cargo     | release/0.3.z   | not inspected (eval) | n/a (released 2.1.x already >= 1.0.135) |
| 2.2.x  | Cargo     | release/0.4.z   | not inspected (eval) | n/a (released 2.2.x already >= 1.0.135) |
