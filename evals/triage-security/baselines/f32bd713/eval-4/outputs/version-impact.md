# Version Impact Analysis — TC-8004

## CVE-2026-33501: h2 (versions before 0.4.8)

### Version Impact Table

| Version | Stream | Source Tag | h2 version | Affected? | Notes |
|---------|--------|------------|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | **YES** | < 0.4.8 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | **YES** | < 0.4.8 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.4.8 | NO | = 0.4.8 (fixed version) |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.4.8 | NO | = 0.4.8 (fixed version) |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.9 | NO | > 0.4.8 |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.9 | NO | > 0.4.8 |

### Stream-Level Summary

| Stream | Affected Versions | Unaffected Versions | Overall |
|--------|-------------------|---------------------|---------|
| 2.1.x | 2.1.0, 2.1.1 | _(none)_ | **AFFECTED** |
| 2.2.x | _(none)_ | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | **NOT AFFECTED** |

### Mixed Impact Explanation

This vulnerability shows **mixed impact across streams**:

- **2.1.x stream**: All versions (2.1.0 and 2.1.1) ship h2 0.4.5, which is within the vulnerable range (before 0.4.8). The entire stream is affected and requires remediation.
- **2.2.x stream**: All versions ship h2 >= 0.4.8 (the fixed version). The 2.2.x stream already ships the patched dependency and is not affected. Version 2.2.0 (the earliest in this stream) already ships h2 0.4.8, meaning the fix was present from the start of the 2.2.x stream.

### Dependency Chain Context (Step 2.3.5)

The h2 crate is a Rust HTTP/2 protocol implementation. Based on the ecosystem mappings:

- **Repository**: backend
- **Lock file**: `Cargo.lock`
- **Ecosystem**: Cargo (source dependency)

The h2 crate is typically a transitive dependency pulled in through HTTP libraries such as `hyper` or `reqwest`. The dependency chain would be:

```
backend (workspace) -> hyper/reqwest -> h2
Type: likely transitive dependency
Profile: production (HTTP/2 is a runtime dependency)
```

### Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | Unknown -- requires `git show release/0.3.z:Cargo.lock` to check if h2 >= 0.4.8 on the upstream branch |
| 2.2.x | Cargo | `release/0.4.z` | Not applicable -- stream is not affected |

Since the 2.2.x stream already ships h2 >= 0.4.8 at every released version, the fix is known to be available in the upstream crate ecosystem. The question for remediation is whether the `release/0.3.z` branch of the backend repository has already been updated to use h2 >= 0.4.8. If it has, the remediation is a dependency bump + downstream propagation. If not, an upstream backport is needed first.

For this analysis, since both released 2.1.x versions (v0.3.8 and v0.3.12) ship h2 0.4.5, and the upstream fix (h2 0.4.8) is available as a published crate, the remediation path is an upstream dependency bump on the `release/0.3.z` branch followed by downstream propagation.
