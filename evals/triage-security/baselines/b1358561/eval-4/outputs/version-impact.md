# TC-8004 — Step 2 Version Impact Analysis

## 2.1 Supportability matrix (aggregated from both Version Streams)

| Stream | Konflux release repo | Versions | Cargo lock file | Upstream branch |
|---|---|---|---|---|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0, 2.1.1 | backend `Cargo.lock` | `release/0.3.z` |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | backend `Cargo.lock` | `release/0.4.z` |

Format validation: both matrices contain Supportability Matrix, Source Pinning Method,
Ecosystem Mappings (columns `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`)
and Forward Pointer. Result: **Pass**.

## 2.2 Development stream

The development stream could not be determined. That requires
`getJiraIssueTypeMetaWithFields` to find unreleased `RHTPA` versions, and Jira access is
not allowed in this eval. The Version Streams table has no stream beyond 2.2.x, and 2.2.x
HEAD evidence is not available. **No dev-stream row is included.** In a live run, look up
the earliest unreleased RHTPA version and check that stream's branch HEAD with
`git show HEAD:Cargo.lock`.

## 2.3 Dependency versions at pinned commits

Ecosystem: Cargo. Check command `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`.
Values come from the simulated lock-file output in `security-matrix-mock.md` (h2 table).

## 2.4 Version Impact for CVE-2026-33501 (h2 < 0.4.8)

| Version | Stream | Pinned backend tag | h2 | Affected? | Notes |
|---------|--------|--------------------|----|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8`  | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | `v0.4.5`  | 0.4.8 | NO | ships the fixed version 0.4.8 |
| 2.2.1 | 2.2.x | `v0.4.8`  | 0.4.8 | NO | ships the fixed version 0.4.8 |
| 2.2.2 | 2.2.x | `v0.4.8`  | —     | NO | backend retag of 2.2.1, same as 2.2.1 (lock check skipped) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.9 | NO | |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.9 | NO | |

### Mixed impact across streams

| Stream | Affected versions | Unaffected versions | Stream verdict |
|---|---|---|---|
| **2.1.x** | 2.1.0, 2.1.1 | — | **AFFECTED** (every version ships h2 0.4.5) |
| **2.2.x** | — | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | **NOT AFFECTED** (every version ships h2 >= 0.4.8) |

PSIRT's claim that RHTPA 2.2.0 is affected is **not supported** by the lock-file
evidence. 2.2.0 already ships h2 0.4.8, the fixed release. PSIRT also missed RHTPA 2.1.1,
which ships the vulnerable 0.4.5.

## 2.3.5 Dependency chain context (2.1.x)

```
Dependency chain for h2 (2.1.x, tags v0.3.8 / v0.3.12):
  backend (workspace) → ... → h2 0.4.5
  Type: NOT DETERMINED from available evidence
  Profile: NOT DETERMINED from available evidence
  Introduction point: present in every 2.1.x version, 0.4.5 throughout
```

The simulated data contains only the h2 version line from `Cargo.lock`. It has no
`Cargo.toml` manifests and no `[[package]] dependencies` blocks, so I cannot say whether
h2 is direct or transitive, or which build profile pulls it in. I did not guess. In a
live run, inspect `git show v0.3.12:Cargo.lock` (look for packages that list `h2` among
their dependencies, typically `hyper`/`reqwest`/`tonic`) and the workspace `Cargo.toml`
files. If h2 turns out to be dev-only or build-only, add the `dev-dependency` label and
set priority to Normal. The remediation tasks include both the direct and the transitive
remediation approaches.

## 2.5 Upstream fix status

| Stream | Ecosystem | Repository | Upstream Branch | h2 at HEAD | Fixed? |
|--------|-----------|------------|-----------------|------------|--------|
| 2.1.x | Cargo | rhtpa-backend | `release/0.3.z` | not available | **UNKNOWN** |
| 2.2.x | Cargo | rhtpa-backend | `release/0.4.z` | not checked | not needed (stream not affected) |

`git -C /home/dev/repos/rhtpa-backend show release/0.3.z:Cargo.lock | grep -A2 'name = "h2"'`
was not run (eval constraint), and the mock data has no branch-HEAD value. Because the
fix is **not confirmed** upstream, the 2.1.x remediation uses the **upstream backport +
downstream propagation** pair. If a live check shows `release/0.3.z` already at
h2 >= 0.4.8, switch task 1 to the dependency-bump variant (`cargo update -p h2`).

## Engineer confirmation

Simulated: version impact table confirmed. Proceed to Step 3.
