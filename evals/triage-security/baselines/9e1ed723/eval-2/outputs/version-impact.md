# TC-8002 — Version Impact Analysis (Step 2)

Source of dependency versions: the "serde_json versions by tag" mock data in
`security-matrix-mock.md`, standing in for
`git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'` run in the backend repo at each
pinned commit from the supportability matrix. No versions were invented.

## 2.1 – Supportability matrix (aggregated)

| Stream | Konflux repo | Versions | Backend pin |
|---|---|---|---|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0, 2.1.1 | v0.3.8, v0.3.12 |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0, 2.2.1, 2.2.2 (retag), 2.2.3, 2.2.4 | v0.4.5, v0.4.8, v0.4.8, v0.4.11, v0.4.12 |

Format validation (2.1.1): both stream sections have Supportability Matrix, Source Pinning
Method, Ecosystem Mappings (expected 5 columns, in order) and Forward Pointer → **Pass**.

## 2.2 – Development stream

Unreleased Jira versions could not be queried (no Jira access in this eval), and the mock
data contains no branch-HEAD lock file. 2.2.x is the latest stream (no forward pointer).
The development stream is therefore **not verified** — see note under 2.5.

## 2.3 / 2.4 – Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135, fixed in 1.0.135):

| Version | Stream | Backend tag | serde_json | Affected? | Notes |
|---------|--------|-------------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 1.0.137 | NO | outside scope of TC-8002 (cross-stream check) |
| 2.1.1 | 2.1.x | v0.3.12 | 1.0.137 | NO | outside scope of TC-8002 (cross-stream check) |
| 2.2.0 | 2.2.x | v0.4.5 | 1.0.138 | NO | PSIRT-assigned Affects Version — incorrect |
| 2.2.1 | 2.2.x | v0.4.8 | 1.0.138 | NO | |
| 2.2.2 | 2.2.x | v0.4.8 | — | NO | retag of 2.2.1 — same as 2.2.1 (lock file check skipped) |
| 2.2.3 | 2.2.x | v0.4.11 | 1.0.139 | NO | |
| 2.2.4 | 2.2.x | v0.4.12 | 1.0.139 | NO | |
| dev (HEAD) | — | — | not available | not verified | no Jira unreleased-version data or branch-HEAD lock file in mock input |

**Result: 0 of 7 supported released versions are affected.** Every released build
already ships serde_json ≥ 1.0.137, which is newer than the fixed version 1.0.135. This
holds for the issue's scoped stream (2.2.x) and for the other stream (2.1.x).

## 2.3.5 – Dependency chain context

No affected versions → chain tracing for remediation is not required. serde_json is present
in `Cargo.lock` at every pinned tag (so the package is a dependency of backend), but at
patched versions only. Direct vs. transitive classification was not determined (no
Cargo.toml content in mock data) and is not needed for a not-affected outcome.

## 2.5 – Upstream fix status

Not required — no stream is affected, so no remediation path has to be chosen. For
information: the Cargo Upstream Branch is `release/0.3.z` for 2.1.x and `release/0.4.z` for
2.2.x. Their HEAD lock files were not available in the mock data. The newest pinned tags
(v0.3.12 → 1.0.137, v0.4.12 → 1.0.139) are already past the fix, so those branches are
expected to stay fixed unless serde_json were downgraded.

## Engineer confirmation gate

In a real run, the table above is shown to the engineer for confirmation before Step 3.
For this eval, it is taken as confirmed.
