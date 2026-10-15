# Step 2 -- Version Impact Analysis for TC-8001

## CVE-2026-31812 (quinn-proto < 0.11.14)

### Matrix Staleness Check (Step 0.3)

The security matrix `Last-Updated` timestamp is `2026-06-28T10:00:00Z`. Assuming a current date of 2026-10-15, the matrix is approximately 109 days old, which exceeds the 14-day staleness threshold. In a live triage, the engineer would be warned and given the option to refresh, proceed, or stop. For this eval, we proceed with the current matrix data.

### Loaded Supportability Matrix

**Stream 2.1.x (rhtpa-release.0.3.z)**

| Version | Build | Build Date | backend Tag |
|---------|-------|------------|-------------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 |

**Stream 2.2.x (rhtpa-release.0.4.z)**

| Version | Build | Build Date | backend Tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

### Ecosystem Mappings

Both streams use the same ecosystems:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.3.z (2.1.x) / release/0.4.z (2.2.x) |
| RPM | -- | rpms.lock.yaml | `git show <tag>:rpms.lock.yaml` | -- |

### Dependency Version Extraction (Step 2.3)

Extracted quinn-proto versions from `Cargo.lock` at each pinned backend tag:

| Tag | Command (simulated) | quinn-proto version |
|-----|---------------------|---------------------|
| v0.3.8 | `git show v0.3.8:Cargo.lock \| grep -A2 'name = "quinn-proto"'` | 0.11.9 |
| v0.3.12 | `git show v0.3.12:Cargo.lock \| grep -A2 'name = "quinn-proto"'` | 0.11.9 |
| v0.4.5 | `git show v0.4.5:Cargo.lock \| grep -A2 'name = "quinn-proto"'` | 0.11.9 |
| v0.4.8 | `git show v0.4.8:Cargo.lock \| grep -A2 'name = "quinn-proto"'` | 0.11.12 |
| v0.4.9 | Skipped -- retag of v0.4.8 | (same as v0.4.8: 0.11.12) |
| v0.4.11 | `git show v0.4.11:Cargo.lock \| grep -A2 'name = "quinn-proto"'` | 0.11.14 |
| v0.4.12 | `git show v0.4.12:Cargo.lock \| grep -A2 'name = "quinn-proto"'` | 0.11.14 |

### Version Impact Table (Step 2.4)

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

### Dependency Chain Context (Step 2.3.5)

quinn-proto is a Rust crate present in `Cargo.lock`. Based on the component label `pscomponent:org/rhtpa-server` and the library name, quinn-proto is used for QUIC protocol support in the backend service. The exact dependency chain (direct vs. transitive) would be determined by inspecting the workspace `Cargo.toml` and the lock file's dependency graph at each pinned commit. For this eval, we note that the chain investigation would be performed via:

```
git show <tag>:Cargo.toml | grep quinn-proto
```

If quinn-proto is a direct dependency, remediation is a straightforward version bump. If transitive (e.g., via a QUIC client library like `quinn`), the two-tier approach applies: bump the direct dependency first, fall back to pinning quinn-proto directly.

### Upstream Fix Check (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Latest Tag Version at Branch | Fixed? |
|--------|-----------|-----------------|------------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (at v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (at v0.4.12) | YES |

**Analysis**:
- **2.2.x (release/0.4.z)**: The fix is already available on this upstream branch. Version 0.11.14 (the fix threshold) is shipped by the latest tags (v0.4.11, v0.4.12). Remediation uses the **dependency bump** variant -- `cargo update -p quinn-proto` is sufficient, followed by downstream propagation.
- **2.1.x (release/0.3.z)**: The fix is NOT available on this upstream branch. All tags still ship 0.11.9. Remediation requires an **upstream backport** (PR to bump quinn-proto on `release/0.3.z`), followed by downstream propagation.

### Summary

- **In-scope stream (2.2.x)**: 3 versions affected (2.2.0, 2.2.1, 2.2.2), 2 versions not affected (2.2.3, 2.2.4). Upstream fix is available -- use dependency bump variant.
- **Cross-stream (2.1.x)**: 2 versions affected (2.1.0, 2.1.1). Upstream fix is NOT available -- requires upstream backport. This will be handled via Case A (cross-stream impact) since the issue is scoped to 2.2.x.
