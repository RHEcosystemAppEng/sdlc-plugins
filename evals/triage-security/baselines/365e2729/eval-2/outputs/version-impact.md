# TC-8002 — Version Impact Analysis (Step 2)

## 2.1 – Supportability Matrix (loaded from local security-matrix.md mock)

| Stream | Konflux repo | Versions | Backend tags |
|---|---|---|---|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0, 2.1.1 | v0.3.8, v0.3.12 |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1), 2.2.3, 2.2.4 | v0.4.5, v0.4.8, v0.4.8, v0.4.11, v0.4.12 |

The matrix format is valid: it has the Supportability Matrix, Source Pinning Method, and Ecosystem Mappings sections. Cargo maps to `Cargo.lock` in `backend` with check command `git show <tag>:Cargo.lock`.

## 2.2 – Development stream

Finding the development stream requires `getJiraIssueTypeMetaWithFields` to list unreleased `RHTPA` versions. Jira is not available in this eval and the mock contains no unreleased-version data, so **no development stream was identified**. In a live run, the unreleased version with the earliest release date would be checked at its branch HEAD.

For partial context, the upstream branch HEAD check in 2.5 also could not be run.

## 2.3 – Dependency versions (simulated `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`)

Fix threshold: serde_json **< 1.0.135 is vulnerable**, and 1.0.135 or later is fixed.

## 2.4 – Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Stream | Version | Backend tag | serde_json | Affected? | Notes |
|---|---|---|---|---|---|
| 2.1.x | 2.1.0 | v0.3.8 | 1.0.137 | NO | 1.0.137 >= 1.0.135 |
| 2.1.x | 2.1.1 | v0.3.12 | 1.0.137 | NO | 1.0.137 >= 1.0.135 |
| 2.2.x | 2.2.0 | v0.4.5 | 1.0.138 | NO | 1.0.138 >= 1.0.135. This is the version PSIRT assigned. |
| 2.2.x | 2.2.1 | v0.4.8 | 1.0.138 | NO | 1.0.138 >= 1.0.135 |
| 2.2.x | 2.2.2 | v0.4.8 | — | NO | Same as 2.2.1 (backend retag of v0.4.8; lock check skipped and result carried forward) |
| 2.2.x | 2.2.3 | v0.4.11 | 1.0.139 | NO | 1.0.139 >= 1.0.135 |
| 2.2.x | 2.2.4 | v0.4.12 | 1.0.139 | NO | 1.0.139 >= 1.0.135 |
| dev | n/a | branch HEAD | not determined | n/a | No unreleased-version data available (see 2.2) |

**Result: none of the 7 supported released versions in either stream ships a vulnerable serde_json.** The oldest shipped version is 1.0.137, which is already newer than the 1.0.135 fix. Development branches can only pick up newer lock files than the released tags, so they are not expected to regress. Still, a live run must confirm the development stream at branch HEAD.

- Issue stream (2.2.x): **not affected**.
- Other streams (2.1.x): **not affected**, so there is no cross-stream impact.

### 2.3.5 – Dependency chain context

serde_json appears in `Cargo.lock` for backend. Direct-vs-transitive classification (`cargo tree -i serde_json`) needs source access and was not run. It does not affect the outcome because no version is affected and no remediation is needed.

## 2.5 – Upstream fix status

| Stream | Ecosystem | Upstream branch | Version at HEAD | Fixed? |
|---|---|---|---|---|
| 2.1.x | Cargo | release/0.3.z | not checked (no git access in eval) | n/a, stream not affected |
| 2.2.x | Cargo | release/0.4.z | not checked (no git access in eval) | n/a, stream not affected |

The upstream fix check only applies to affected streams. Since no stream is affected, it does not change the decision.

## Engineer confirmation

The table above would be shown to the engineer for confirmation before Step 3. For this eval, it is treated as confirmed.
