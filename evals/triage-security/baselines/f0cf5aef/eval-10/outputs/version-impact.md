# Step 2 -- Version Impact Analysis

## CVE-2026-55123: tokio (versions before 1.42.0)

### Version Impact Table

| Version     | Stream    | tokio version | Affected? | Notes |
|-------------|-----------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0        | YES       |       |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0        | YES       |       |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1        | YES       |       |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1        | YES       |       |

Fix threshold: 1.42.0 (from Jira description; cross-validated with external CVE databases).

### Cross-Stream Impact Summary

The issue is scoped to stream **rhtpa-2.2** (suffix `[rhtpa-2.2]`).

**Streams within issue scope (rhtpa-2.2):**
- RHTPA 2.2.0: tokio 1.41.1 -- AFFECTED (< 1.42.0)
- RHTPA 2.2.1: tokio 1.41.1 -- AFFECTED (< 1.42.0)

**Streams outside issue scope (cross-stream):**
- rhtpa-2.1: RHTPA 2.1.0 ships tokio 1.40.0, RHTPA 2.1.1 ships tokio 1.40.0 -- AFFECTED (< 1.42.0)

### Ecosystem Mappings

**Stream rhtpa-2.2 (2.2.x / rhtpa-release.0.4.z):**

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

**Stream rhtpa-2.1 (2.1.x / rhtpa-release.0.3.z):**

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Upstream Fix PR | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x  | Cargo     | release/0.4.z   | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) | Requires verification via `git show` |
| 2.1.x  | Cargo     | release/0.3.z   | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) | Requires verification via `git show` |

### Sibling CVE Jira Search Results

JQL: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020`

- **Stream rhtpa-2.2**: TC-8020 (the current issue)
- **Stream rhtpa-2.1**: No sibling Vulnerability issue found

This means rhtpa-2.1 has no CVE Jira for CVE-2026-55123. Case A preemptive remediation applies for this stream.
