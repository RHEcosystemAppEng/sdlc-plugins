# TC-8002 — Version Impact Analysis (Step 2)

## 2.1 – Supportability matrix (loaded from security-matrix-mock.md)

Format validation (2.1.1): both stream matrices have `## Supportability Matrix`,
`## Ecosystem Mappings` (with columns `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`),
`### Source Pinning Method` and `## Forward Pointer`, and their tables parse. Result: **Pass**.

Aggregated working matrix:

| Stream | Version | Build | Build Date | backend tag | Notes |
|---|---|---|---|---|---|
| 2.1.x | 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.x | 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |
| 2.2.x | 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.x | 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.x | 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.x | 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.x | 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.2 – Development stream

You find the development stream by querying Jira for unreleased `RHTPA` versions
(`getJiraIssueTypeMetaWithFields`, project TC, issue type 10024). This eval allows no
Jira calls, so the development version and its branch HEAD **could not be determined**.
2.2.x is the latest configured stream (no forward pointer). Its newest release, 2.2.4,
ships serde_json 1.0.139, so development HEAD will most likely be at or above that.
This is an inference, not evidence. The engineer should confirm it with
`git -C /home/dev/repos/rhtpa-backend show release/0.4.z:Cargo.lock | grep -A2 'name = "serde_json"'`
(and the same check on `main` if a 3.x development stream exists).

## 2.3 – Dependency versions at pinned commits

Ecosystem: Cargo, lock file `Cargo.lock`, repository `backend`. Simulated command per tag:
`git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`. The output comes from the
"serde_json versions by tag" section of security-matrix-mock.md.

| Tag | serde_json (Cargo.lock) |
|---|---|
| `v0.3.8` | 1.0.137 |
| `v0.3.12` | 1.0.137 |
| `v0.4.5` | 1.0.138 |
| `v0.4.8` | 1.0.138 |
| `v0.4.9` | retag of v0.4.8 (not checked; 2.2.2 pins backend `v0.4.8`) |
| `v0.4.11` | 1.0.139 |
| `v0.4.12` | 1.0.139 |

Fix threshold: affected if `< 1.0.135`, fixed in `1.0.135` (Jira description; external
enrichment unavailable).

## 2.4 – Version impact table

```
Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Version     | Stream | serde_json | Affected? | Notes                                  |
|-------------|--------|------------|-----------|----------------------------------------|
| 2.1.0       | 2.1.x  | 1.0.137    | NO        | >= 1.0.135 (out of issue scope)        |
| 2.1.1       | 2.1.x  | 1.0.137    | NO        | >= 1.0.135 (out of issue scope)        |
| 2.2.0       | 2.2.x  | 1.0.138    | NO        | >= 1.0.135; PSIRT-claimed version      |
| 2.2.1       | 2.2.x  | 1.0.138    | NO        | >= 1.0.135                             |
| 2.2.2       | 2.2.x  | —          | NO        | same as 2.2.1 (backend retag of v0.4.8)|
| 2.2.3       | 2.2.x  | 1.0.139    | NO        | >= 1.0.135                             |
| 2.2.4       | 2.2.x  | 1.0.139    | NO        | >= 1.0.135                             |
| dev (HEAD)  | ?      | unverified | (likely NO) | Jira/git unavailable in eval; see 2.2 |
```

**Summary:** no supported released version ships a vulnerable serde_json. Every version,
including 2.2.0 (the one PSIRT named), already ships the patched dependency (1.0.137 to
1.0.139, all at or above the 1.0.135 fix version). Even the oldest supported build
(2.1.0, September 2025) was already patched.

### 2.3.5 – Dependency chain context

No version is affected, so no dependency-chain trace is needed for remediation. The
direct/transitive and profile analysis needs the manifest (`Cargo.toml`) files, which
are not in the eval inputs, so it was not done. serde_json is almost certainly a
runtime dependency of the backend, but that has no bearing on the decision.

## 2.5 – Upstream fix status

No stream is affected, so no stream needs an upstream fix check. For reference:

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|---|---|---|---|---|
| 2.1.x | Cargo | `release/0.3.z` | not checked (no git access) | N/A (not affected) |
| 2.2.x | Cargo | `release/0.4.z` | not checked (no git access) | N/A (not affected) |

## Cross-stream impact

The issue is scoped to 2.2.x. The other stream (2.1.x) is **not affected** either
(serde_json 1.0.137), so Case A (cross-stream comment / preemptive tasks) does not apply.
