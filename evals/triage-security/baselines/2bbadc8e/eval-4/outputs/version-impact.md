# Version Impact Analysis -- TC-8004

## Step 2: Version Impact Table

CVE-2026-33501 (h2 < 0.4.8 -- memory exhaustion via CONTINUATION frames)

| Stream | Version | Build Tag | h2 version | Affected? | Notes |
|--------|---------|-----------|------------|-----------|-------|
| 2.1.x | 2.1.0 | `v0.3.8` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.x | 2.1.1 | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.x | 2.2.0 | `v0.4.5` | 0.4.8 | NO | 0.4.8 >= 0.4.8 (ships fixed version) |
| 2.2.x | 2.2.1 | `v0.4.8` | 0.4.8 | NO | 0.4.8 >= 0.4.8 |
| 2.2.x | 2.2.2 | `v0.4.9` | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | `v0.4.11` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.x | 2.2.4 | `v0.4.12` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

## Stream Impact Summary

| Stream | Affected Versions | Unaffected Versions | Overall |
|--------|-------------------|---------------------|---------|
| **2.1.x** | 2.1.0, 2.1.1 | _(none)_ | **AFFECTED** -- all versions ship h2 0.4.5 |
| **2.2.x** | _(none)_ | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | **NOT AFFECTED** -- all versions ship h2 >= 0.4.8 |

## Mixed Impact Across Streams

This CVE exhibits **mixed impact** across version streams:

- The **2.1.x stream** ships h2 0.4.5 in both released versions (2.1.0, 2.1.1), which
  falls within the vulnerable range (< 0.4.8). Both versions are **affected**.

- The **2.2.x stream** ships h2 0.4.8 or later in all released versions. Version 2.2.0
  ships the exact fix version (h2 0.4.8), and later versions ship h2 0.4.9. All 2.2.x
  versions are **not affected**.

## Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: source dependency (Cargo crate)
  Ecosystem: Cargo
  Lock file: Cargo.lock
  Profile: production (h2 is a runtime dependency -- HTTP/2 protocol implementation)
```

The h2 crate is used for HTTP/2 protocol support in the backend service. It is a
production runtime dependency, not dev-only or build-only.

## Upstream Fix Status

The h2 crate fix (version 0.4.8) has been released upstream. The 2.2.x stream already
ships h2 >= 0.4.8, confirming the fix is available as a published crate version.

For the 2.1.x stream (upstream branch `release/0.3.z`), the fix can be applied via
`cargo update -p h2` to pull in h2 >= 0.4.8, since the fixed version is published
in the crate registry. This qualifies for the **dependency bump** remediation variant
rather than an upstream backport.

| Stream | Ecosystem | Upstream Branch | Fix Available? | Remediation Path |
|--------|-----------|-----------------|----------------|------------------|
| 2.1.x | Cargo | `release/0.3.z` | YES (h2 0.4.8 published) | Dependency bump + downstream propagation |
| 2.2.x | Cargo | `release/0.4.z` | N/A (not affected) | No remediation needed |
