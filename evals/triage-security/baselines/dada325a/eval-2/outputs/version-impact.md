# Version Impact Analysis — TC-8002 (CVE-2026-28940, serde_json < 1.0.135)

## 2.1 – Supportability Matrix (aggregated)

Matrix format check: Pass. Both streams contain Supportability Matrix, Source Pinning Method, Ecosystem Mappings (with the canonical 5 columns) and Forward Pointer.

| Stream | Version | Build | Backend pinned tag | Notes |
|--------|---------|-------|--------------------|-------|
| 2.1.x | 2.1.0 | 0.3.8 | `v0.3.8` | |
| 2.1.x | 2.1.1 | 0.3.12 | `v0.3.12` | |
| 2.2.x | 2.2.0 | 0.4.5 | `v0.4.5` | |
| 2.2.x | 2.2.1 | 0.4.8 | `v0.4.8` | |
| 2.2.x | 2.2.2 | 0.4.9 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.x | 2.2.3 | 0.4.11 | `v0.4.11` | |
| 2.2.x | 2.2.4 | 0.4.12 | `v0.4.12` | |

## 2.2 – Development Stream

Jira unreleased-version metadata (`getJiraIssueTypeMetaWithFields`) was not available in this eval, so no development version or branch HEAD lock file data was provided. 2.2.x is the latest configured stream (no forward pointer). Its upstream branch `release/0.4.z` is covered by the upstream check in 2.5, using the latest pinned tag as a proxy. **This is a gap:** in a real run, `git show HEAD:Cargo.lock` on the development branch would be checked.

## 2.3 / 2.4 – Dependency Versions and Version Impact Table

Dependency versions come from the mock lock file data in `security-matrix-mock.md` (simulated output of `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`).

Version Impact for CVE-2026-28940 (serde_json < 1.0.135, fixed in 1.0.135):

| Version | Stream | Pinned tag | serde_json | Affected? | Notes |
|---------|--------|------------|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 1.0.137 | NO | 1.0.137 >= 1.0.135 (patched) |
| 2.1.1 | 2.1.x | `v0.3.12` | 1.0.137 | NO | 1.0.137 >= 1.0.135 (patched) |
| 2.2.0 | 2.2.x | `v0.4.5` | 1.0.138 | NO | 1.0.138 >= 1.0.135 (patched); this is the version PSIRT claimed |
| 2.2.1 | 2.2.x | `v0.4.8` | 1.0.138 | NO | 1.0.138 >= 1.0.135 (patched) |
| 2.2.2 | 2.2.x | `v0.4.8` | — | NO | same as 2.2.1 (backend retag, lock file check skipped) |
| 2.2.3 | 2.2.x | `v0.4.11` | 1.0.139 | NO | 1.0.139 >= 1.0.135 (patched) |
| 2.2.4 | 2.2.x | `v0.4.12` | 1.0.139 | NO | 1.0.139 >= 1.0.135 (patched) |
| dev (HEAD) | — | — | n/a | not checked | no development stream data provided (see 2.2) |

**Result: 0 of 7 supported released versions are affected.** Every shipped version, including the oldest (2.1.0 / `v0.3.8`), already contains a patched serde_json (1.0.137 or later). The vulnerable range (< 1.0.135) is not present in any build.

- Scoped stream (2.2.x, per the `[rhtpa-2.2]` suffix): not affected.
- Other stream (2.1.x): not affected, so no cross-stream impact (Case A does not apply).

### 2.3.5 – Dependency Chain Context

No version is affected, so remediation chain tracing is not needed. serde_json is present in the backend `Cargo.lock` at every pinned tag, so the crate is shipped. It is shipped only at versions that already include the recursion-limit fix.

## 2.5 – Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version (latest pinned tag) | Fixed? |
|--------|-----------|-----------------|-----------------------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | 1.0.137 (`v0.3.12`) | YES |
| 2.2.x | Cargo | `release/0.4.z` | 1.0.139 (`v0.4.12`) | YES |

Branch HEAD was not read in this eval. serde_json versions only increase across tags, so a regression below 1.0.135 at HEAD is very unlikely. In a real run, `git -C /home/dev/repos/rhtpa-backend show release/0.4.z:Cargo.lock` would confirm this.

No remediation path is needed for either stream.
