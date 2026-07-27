# Version Impact Analysis — CVE-2026-55123 (tokio < 1.42.0)

## Version Impact Table

| Version     | Stream    | tokio version | Affected? | Notes |
|-------------|-----------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0        | YES       |       |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0        | YES       |       |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1        | YES       |       |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1        | YES       |       |

All supported versions across both streams ship tokio < 1.42.0 and are affected by CVE-2026-55123.

## Cross-Stream Impact

The issue is scoped to stream **rhtpa-2.2** (suffix `[rhtpa-2.2]`).

Cross-stream version impact analysis reveals that stream **rhtpa-2.1** is also affected:

| Stream    | Versions Affected       | tokio version | Fix Threshold |
|-----------|-------------------------|---------------|---------------|
| rhtpa-2.1 | RHTPA 2.1.0, RHTPA 2.1.1 | 1.40.0      | 1.42.0        |
| rhtpa-2.2 | RHTPA 2.2.0, RHTPA 2.2.1 | 1.41.1      | 1.42.0        |

## Stream Scope Classification

- **In-scope stream (rhtpa-2.2)**: RHTPA 2.2.0, RHTPA 2.2.1 -- both affected (tokio 1.41.1 < 1.42.0)
- **Out-of-scope stream (rhtpa-2.1)**: RHTPA 2.1.0, RHTPA 2.1.1 -- both affected (tokio 1.40.0 < 1.42.0)

## Sibling CVE Jira Search

JQL search for sibling Vulnerability issues with label `CVE-2026-55123` in stream `rhtpa-2.1`:

**Result: No sibling CVE Jiras found for stream rhtpa-2.1.**

This triggers Case A (cross-stream impact with preemptive remediation) for the rhtpa-2.1 stream.

## Ecosystem Mappings

### Stream rhtpa-2.1 (rhtpa-release.0.3.z)

| Ecosystem | Repository | Lock File    | Check Command                                  | Upstream Branch |
|-----------|------------|--------------|-------------------------------------------------|-----------------|
| Cargo     | backend    | `Cargo.lock` | `git show <tag>:Cargo.lock \| grep -A2 'name = "<library>"'` | `release/0.3.z` |

### Stream rhtpa-2.2 (rhtpa-release.0.4.z)

| Ecosystem | Repository | Lock File    | Check Command                                  | Upstream Branch |
|-----------|------------|--------------|-------------------------------------------------|-----------------|
| Cargo     | backend    | `Cargo.lock` | `git show <tag>:Cargo.lock \| grep -A2 'name = "<library>"'` | `release/0.4.z` |
