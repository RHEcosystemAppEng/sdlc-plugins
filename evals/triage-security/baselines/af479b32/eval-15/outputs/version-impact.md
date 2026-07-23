# Step 2 -- Version Impact Analysis: CVE-2026-31812

Version Impact for CVE-2026-31812 (quinn-proto versions before 0.11.14):

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | |

Dependency chain for quinn-proto (Cargo):
  Lock file: Cargo.lock
  Ecosystem: Cargo (source dependency)
  Fix threshold: 0.11.14 (from Jira description, cross-validated with external sources)

Upstream fix status:

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | (to be checked) | TBD |
| 2.2.x | Cargo | release/0.4.z | (to be checked) | TBD |

Summary:
- Stream 2.1.x: ALL versions affected (2.1.0, 2.1.1) -- ships quinn-proto 0.11.9
- Stream 2.2.x: versions 2.2.0, 2.2.1, 2.2.2 affected -- fixed starting from 2.2.3 (ships quinn-proto 0.11.14)
