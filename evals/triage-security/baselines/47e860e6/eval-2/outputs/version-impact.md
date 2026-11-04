# TC-8002 — Version Impact Analysis (Step 2)

## 2.1 – Supportability matrix (all configured streams)

The skill reads both streams from the Version Streams table (Important Rule 14). It does not follow forward pointers. Source: `security-matrix-mock.md`.

| Stream | Version | Build | backend pinned tag | Notes |
|---|---|---|---|---|
| 2.1.x | 2.1.0 | 0.3.8 | `v0.3.8` | |
| 2.1.x | 2.1.1 | 0.3.12 | `v0.3.12` | |
| 2.2.x | 2.2.0 | 0.4.5 | `v0.4.5` | |
| 2.2.x | 2.2.1 | 0.4.8 | `v0.4.8` | |
| 2.2.x | 2.2.2 | 0.4.9 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.x | 2.2.3 | 0.4.11 | `v0.4.11` | |
| 2.2.x | 2.2.4 | 0.4.12 | `v0.4.12` | |

Ecosystem mapping (both streams): Cargo, repository `backend`, lock file `Cargo.lock`, check command `git show <tag>:Cargo.lock`. Upstream branches are `release/0.3.z` (2.1.x) and `release/0.4.z` (2.2.x).

Matrix format is valid: all required sections are present (Version Stream, Supportability Matrix, Source Pinning Method, Ecosystem Mappings). The matrix is 129 days old. See the staleness warning in data-extraction.md.

## 2.2 – Development stream

Unreleased Jira versions come from `getJiraIssueTypeMetaWithFields`, which was not called in this eval, so no development version was identified. 2.2.x is the latest configured stream (no forward pointer). In a live run, check any unreleased `RHTPA` version, such as a 2.2.5 or 2.3/3.0, at the HEAD of its source branch.

## 2.3 – serde_json versions at pinned commits

Simulated output of `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`, taken from the mock lock file data:

Fix threshold: affected when serde_json < 1.0.135; fixed when serde_json >= 1.0.135 (Jira description only, Step 1.5 not available).

## 2.4 – Version impact table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Version | Stream | Pinned tag | serde_json | Affected? | Notes |
|---------|--------|-----------|-----------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 1.0.137 | NO | 1.0.137 >= 1.0.135 |
| 2.1.1 | 2.1.x | `v0.3.12` | 1.0.137 | NO | 1.0.137 >= 1.0.135 |
| 2.2.0 | 2.2.x | `v0.4.5` | 1.0.138 | NO | 1.0.138 >= 1.0.135. **PSIRT listed this version as affected.** |
| 2.2.1 | 2.2.x | `v0.4.8` | 1.0.138 | NO | 1.0.138 >= 1.0.135 |
| 2.2.2 | 2.2.x | `v0.4.8` | — | NO | same as 2.2.1 (backend retag of `v0.4.8`, lock check skipped) |
| 2.2.3 | 2.2.x | `v0.4.11` | 1.0.139 | NO | 1.0.139 >= 1.0.135 |
| 2.2.4 | 2.2.x | `v0.4.12` | 1.0.139 | NO | 1.0.139 >= 1.0.135 |
| dev | — | branch HEAD | not determined | — | No unreleased Jira version could be discovered in the eval (see 2.2) |

**Result: no supported version ships a vulnerable serde_json.** The oldest version shipped in any supported release is 1.0.137, which is already 2 patch releases past the fix (1.0.135).

- Issue-scoped stream (2.2.x): 0 of 5 versions affected.
- Other stream (2.1.x): 0 of 2 versions affected. There is no cross-stream impact.

### 2.3.5 – Dependency chain context

Not needed. Chain tracing only runs for affected versions, and none are affected. serde_json is present in `Cargo.lock` at every tag, but always at a fixed version.

## 2.5 – Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | not inspected (no git access in eval) | n/a, no released version is affected |
| 2.2.x | Cargo | release/0.4.z | not inspected (no git access in eval) | n/a, no released version is affected |

No affected stream exists, so no remediation path is needed. Every released tag is already at or above 1.0.137, so a regression at branch HEAD is unlikely. A live run would still confirm it with `git -C /home/dev/repos/rhtpa-backend show release/0.4.z:Cargo.lock | grep -A2 'serde_json'`.
