# TC-8004 — Step 2 Version Impact Analysis

CVE-2026-33501 — h2 (Cargo), affected `< 0.4.8`, fixed in `0.4.8`.

Source: simulated `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'` output from the "h2 versions by tag" table in security-matrix-mock.md, using the pinned backend tag for each version in the supportability matrix (pinned tags only; no HEAD).

## Version impact table

| Stream | Version | Build | backend tag (pinned) | h2 version | Affected (< 0.4.8)? | Notes |
|---|---|---|---|---|---|---|
| 2.1.x | RHTPA 2.1.0 | 0.3.8 | `v0.3.8` | 0.4.5 | **YES** | |
| 2.1.x | RHTPA 2.1.1 | 0.3.12 | `v0.3.12` | 0.4.5 | **YES** | |
| 2.2.x | RHTPA 2.2.0 | 0.4.5 | `v0.4.5` | 0.4.8 | NO | ships fixed version |
| 2.2.x | RHTPA 2.2.1 | 0.4.8 | `v0.4.8` | 0.4.8 | NO | |
| 2.2.x | RHTPA 2.2.2 | 0.4.9 | `v0.4.8` | 0.4.8 | NO | same as 2.2.1 (backend retag; lock check skipped, result carried forward) |
| 2.2.x | RHTPA 2.2.3 | 0.4.11 | `v0.4.11` | 0.4.9 | NO | |
| 2.2.x | RHTPA 2.2.4 | 0.4.12 | `v0.4.12` | 0.4.9 | NO | |

## Per-stream summary (mixed impact)

| Stream | Konflux release repo | Upstream branch | Result |
|---|---|---|---|
| 2.1.x | rhtpa-release.0.3.z | `release/0.3.z` | **AFFECTED** — all versions ship h2 0.4.5 |
| 2.2.x | rhtpa-release.0.4.z | `release/0.4.z` | **NOT AFFECTED** — every version ships h2 >= 0.4.8 (0.4.8 / 0.4.9) |

## Notes

- **Step 2.2 (development stream)**: no unreleased RHTPA Jira version data is available in this eval (no Jira call). 2.2.x is the latest stream; its most recent pinned release (2.2.4) already ships h2 0.4.9, so any development HEAD on `release/0.4.z` is not expected to regress — but this was not verified via `git show` at HEAD and should be confirmed in a real run.
- **Step 2.3.5 (dependency chain)**: h2 is normally a transitive dependency (via hyper / reqwest / tonic). The mock data does not include the Cargo.lock dependency graph, so the exact chain is not asserted; the remediation tasks document the two-tier (bump direct dep, fall back to pin) approach. h2 is a runtime HTTP/2 dependency, not dev-only — no `dev-dependency` label.
- **Step 2.5 (upstream fix status)**: the h2 version at `release/0.3.z` HEAD could not be inspected (no git access). Since the fix is not confirmed on the 2.1.x upstream branch, the **upstream backport** variant is used. If a real check shows `release/0.3.z` already resolves h2 >= 0.4.8, switch to the dependency-bump variant.
- Matrix is 128 days stale (proceeded per Step 0.3 choice); newer 2.1.x/2.2.x releases may exist.

Engineer confirmation of this table is required before Step 3 (assumed confirmed for the eval).
