# Version Impact Analysis — CVE-2026-55123 (tokio < 1.42.0)

## Step 2 — Version Impact Table

Fix threshold: **1.42.0** (versions before 1.42.0 are vulnerable).

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES | |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES | |

### Cross-stream summary

- **rhtpa-2.2** (issue scope): all versions affected (tokio 1.41.1 < 1.42.0)
- **rhtpa-2.1** (outside issue scope): all versions affected (tokio 1.40.0 < 1.42.0)

### Dependency chain context

```
Dependency chain for tokio:
  backend (workspace) -> tokio
  Type: direct dependency (Cargo)
  Profile: production (tokio is a runtime dependency)

Remediation: bump tokio to >= 1.42.0 in Cargo.toml
```

### Ecosystem Mappings Used

**Stream 2.1.x (rhtpa-release.0.3.z):**

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.3.z |

**Stream 2.2.x (rhtpa-release.0.4.z):**

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.4.z |

### Upstream fix status

| Stream | Ecosystem | Upstream Branch | Upstream Fix PR | Status |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) | Upstream fix available |
| 2.2.x | Cargo | release/0.4.z | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) | Upstream fix available |

### Affects Versions Correction (Step 3)

- **Current (PSIRT-assigned):** RHTPA 2.2.0, RHTPA 2.2.1
- **Proposed (scoped to rhtpa-2.2):** RHTPA 2.2.0, RHTPA 2.2.1
- **Result:** Affects Versions are already correct for the issue's stream scope. No correction needed.

### Duplicate / Sibling Check (Step 4)

- JQL search for sibling Vulnerability issues with label `CVE-2026-55123` (excluding TC-8020): **no results**
- No same-stream duplicates found.
- No cross-stream companion CVE Jiras found.
- Specifically, **no CVE Jira exists for stream rhtpa-2.1**.
