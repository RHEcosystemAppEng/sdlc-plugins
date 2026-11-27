# Version Impact — CVE-2026-28940 (serde_json < 1.0.135)

Source: the supportability matrices for both streams (`security-matrix-mock.md`), plus simulated `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'` output from the mock lock-file data. The released versions use the pinned backend tags from the matrix.

## Step 2.1 – Supportability matrix (aggregated)

| Stream | Konflux repo | Versions | Cargo upstream branch |
|---|---|---|---|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0 (`v0.3.8`), 2.1.1 (`v0.3.12`) | release/0.3.z |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0 (`v0.4.5`), 2.2.1 (`v0.4.8`), 2.2.2 (`v0.4.8`, retag), 2.2.3 (`v0.4.11`), 2.2.4 (`v0.4.12`) | release/0.4.z |

## Step 2.2 – Development stream

Finding the development stream needs `getJiraIssueTypeMetaWithFields` (unreleased RHTPA versions). That call was not made (no Jira access in the eval), and the mock data has no branch-HEAD lock file. **The development stream could not be determined or checked.** This gap is flagged in the triage outcome. Every pinned 2.2.x release since 2.2.0 already ships serde_json >= 1.0.138, and the versions only increase over time. A regression to < 1.0.135 at HEAD is therefore very unlikely, but it is not proven.

## Step 2.4 – Version Impact Table

| Version | Stream | Backend tag | serde_json | Affected? | Notes |
|---------|--------|-------------|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8`  | 1.0.137 | NO | >= 1.0.135 |
| 2.1.1 | 2.1.x | `v0.3.12` | 1.0.137 | NO | >= 1.0.135 |
| 2.2.0 | 2.2.x | `v0.4.5`  | 1.0.138 | NO | >= 1.0.135; PSIRT-assigned Affects Version |
| 2.2.1 | 2.2.x | `v0.4.8`  | 1.0.138 | NO | >= 1.0.135 |
| 2.2.2 | 2.2.x | `v0.4.8`  | —       | NO | same as 2.2.1 (backend retag; lock check skipped) |
| 2.2.3 | 2.2.x | `v0.4.11` | 1.0.139 | NO | >= 1.0.135 |
| 2.2.4 | 2.2.x | `v0.4.12` | 1.0.139 | NO | >= 1.0.135 |
| dev   | —     | branch HEAD | not available | UNKNOWN | no Jira unreleased-version data or HEAD lock file in eval inputs |

**Result: 0 of 7 supported released versions are affected.** Every shipped build pins serde_json 1.0.137 or later, which already includes the 1.0.135 fix (the configurable recursion limit).

## Step 2.3.5 – Dependency chain context

Not computed. The mock data gives only the resolved `Cargo.lock` version, not the dependency path. Because no version is affected, there is no remediation path to document. serde_json is very likely a direct or near-direct runtime dependency of the backend, but this was not verified.

## Step 2.5 – Upstream fix status

Not needed for remediation, because no stream is affected. The upstream branches (`release/0.3.z`, `release/0.4.z`) were not inspected (no `git show` allowed in the eval).

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | not inspected | n/a (released builds already fixed) |
| 2.2.x | Cargo | release/0.4.z | not inspected | n/a (released builds already fixed) |
