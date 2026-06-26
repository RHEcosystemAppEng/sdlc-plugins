# Step 2 -- Version Impact Analysis: TC-8004

## CVE-2026-33501 (h2 -- versions before 0.4.8)

Fix threshold: h2 >= 0.4.8

## Version Impact Table

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | YES | < 0.4.8 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | YES | < 0.4.8 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.2 | 2.2.x | v0.4.9 | 0.4.8 | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | >= 0.4.8 (fixed) |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | >= 0.4.8 (fixed) |

## Stream-Level Summary

| Stream | Affected? | Affected Versions | h2 range shipped |
|--------|-----------|-------------------|------------------|
| 2.1.x | YES | 2.1.0, 2.1.1 | 0.4.5 (all versions) |
| 2.2.x | NO | (none) | 0.4.8 -- 0.4.9 (all at or above fix threshold) |

## Dependency Chain Context

Dependency chain for h2 (Cargo ecosystem):

The h2 crate is a Rust HTTP/2 implementation used as a transitive dependency through the hyper HTTP library. Typical dependency path:

  backend (workspace) -> hyper -> h2

Profile: production (hyper is a runtime dependency for the backend service)

The vulnerability (memory exhaustion via CONTINUATION frames) affects h2 versions before 0.4.8. The fix adds a configurable maximum header list size defaulting to 16 KiB.

In the 2.1.x stream, h2 0.4.5 is shipped in both released versions (2.1.0 and 2.1.1), confirming the stream is vulnerable.

In the 2.2.x stream, the earliest version (2.2.0) already ships h2 0.4.8 (the fixed version), so no version in this stream is affected.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.1.x | Cargo | release/0.3.z | Upstream fix PR: hyperium/h2#812. The fix (h2 0.4.8) needs to be backported or the dependency bumped on this branch. |
| 2.2.x | Cargo | release/0.4.z | Already ships h2 >= 0.4.8 -- no action needed. |

## Conclusion

**Mixed impact across streams**: The 2.1.x stream is affected (ships h2 0.4.5), while the 2.2.x stream is not affected (ships h2 >= 0.4.8). Remediation is required only for the 2.1.x stream. Since the issue is unscoped, no cross-stream impact notice is needed -- the issue already covers all streams by definition.
