# Step 2 -- Version Impact Analysis: TC-8020

## CVE-2026-55123 (tokio < 1.42.0)

Fix threshold: **1.42.0** (from Jira description; would be cross-validated with MITRE/OSV in Step 1.5)

## Version Impact Table

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | **YES** | `git show v0.3.8:Cargo.lock` |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | **YES** | `git show v0.3.12:Cargo.lock` |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | **YES** | `git show v0.4.5:Cargo.lock` |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | **YES** | `git show v0.4.8:Cargo.lock` |
| RHTPA 2.2.2 | rhtpa-2.2 | -- | **YES** | retag of 2.2.1 (same as RHTPA 2.2.1) |

All versions across both streams ship tokio < 1.42.0 and are affected.

## Cross-Stream Impact Summary

This issue is **scoped** to stream rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`).

Cross-stream analysis reveals that stream **rhtpa-2.1** is also affected:

| Stream | Versions Affected | tokio version | Within issue scope? |
|--------|-------------------|---------------|---------------------|
| rhtpa-2.2 | RHTPA 2.2.0, 2.2.1, 2.2.2 | 1.41.1 | **YES** (issue stream) |
| rhtpa-2.1 | RHTPA 2.1.0, 2.1.1 | 1.40.0 | **NO** (cross-stream) |

Stream rhtpa-2.1 ships tokio 1.40.0, which is below the fix threshold of 1.42.0.

## Affects Versions Correction (Step 3)

Issue is scoped to stream rhtpa-2.2. Only rhtpa-2.2 versions should be in Affects Versions.

- Current Affects Versions: `[RHTPA 2.2.0, RHTPA 2.2.1]`
- Proposed Affects Versions: `[RHTPA 2.2.0, RHTPA 2.2.1]`
- **No correction needed** -- PSIRT-assigned Affects Versions are correct for the issue's stream scope.

Note: RHTPA 2.2.2 is a retag of 2.2.1 and may not have a separate Jira version entry. If it does exist as a Jira version, it should also be included in Affects Versions.

## Sibling CVE Jira Search (Step 4)

JQL: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020`

**Result: No sibling Vulnerability issues found.**

- No sibling CVE Jira exists for stream rhtpa-2.1.
- No same-stream duplicate exists for rhtpa-2.2.

This triggers **Case A** (cross-stream impact with preemptive remediation) for stream rhtpa-2.1.

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| rhtpa-2.2 | Cargo | release/0.4.z | Would need to check via `git -C /home/dev/repos/rhtpa-backend show release/0.4.z:Cargo.lock` |
| rhtpa-2.1 | Cargo | release/0.3.z | Would need to check via `git -C /home/dev/repos/rhtpa-backend show release/0.3.z:Cargo.lock` |

Note: In a live triage, upstream fix status would be checked via git show on the upstream branch HEAD. The upstream fix PR (tokio-rs/tokio#7001) exists, and the fixed version is 1.42.0. If the upstream branch already ships tokio >= 1.42.0, the dependency bump variant would be used instead of the upstream backport variant.
