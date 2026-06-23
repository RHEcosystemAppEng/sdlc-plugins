# Version Impact Analysis - TC-8004

## Step 2 - Version Impact Table

CVE-2026-33501 affects h2 versions before 0.4.8. The fix version is 0.4.8.

### Version Impact for CVE-2026-33501 (h2 < 0.4.8):

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | YES | < 0.4.8 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | YES | < 0.4.8 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | = 0.4.8 (fixed version) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | = 0.4.8 (fixed version) |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | > 0.4.8 |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | > 0.4.8 |

### Summary by Stream

| Stream | Affected? | Details |
|--------|-----------|---------|
| 2.1.x | YES | All versions (2.1.0, 2.1.1) ship h2 0.4.5, which is vulnerable |
| 2.2.x | NO | All versions ship h2 >= 0.4.8, which includes the fix |

### Dependency Chain Context

Dependency chain for h2 (Cargo):
- h2 is a Rust crate used for HTTP/2 protocol support
- Ecosystem: Cargo (source dependency in `Cargo.lock`)
- Lock file: `Cargo.lock` in the backend repository
- Source pinning method: `artifacts.lock.yaml` (download URL contains tag)

The 2.1.x stream ships h2 0.4.5 across both released versions (2.1.0 and 2.1.1), both pinned via tags v0.3.8 and v0.3.12 respectively. The 2.2.x stream already ships h2 >= 0.4.8 starting from its first version (2.2.0, tag v0.4.5).

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 version at branch HEAD | Fixed? |
|--------|-----------|-----------------|---------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.4.5 (latest tag v0.3.12) | NO -- upstream branch still has vulnerable version |
| 2.2.x | Cargo | release/0.4.z | 0.4.9 (latest tag v0.4.12) | YES -- already ships fixed version |

The 2.1.x upstream branch (`release/0.3.z`) has NOT been fixed -- the latest pinned tag (v0.3.12) still ships h2 0.4.5. Remediation requires an upstream PR to bump h2 to >= 0.4.8 on `release/0.3.z`, followed by a downstream Konflux release repo update.
