# Step 2 -- Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto versions before 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Analysis

- **Fix threshold**: quinn-proto >= 0.11.14 (from Jira description; would be
  cross-validated with MITRE and OSV.dev in a live triage)
- **Affected versions**: 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2 (all ship quinn-proto < 0.11.14)
- **Not affected versions**: 2.2.3, 2.2.4 (ship quinn-proto 0.11.14, the fixed version)
- **Retag handling**: Version 2.2.2 is a retag of 2.2.1 (build tag v0.4.9 is a
  retag of v0.4.8). The lock file check was skipped and the result carried forward
  from 2.2.1 (quinn-proto 0.11.12, affected).

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | YES |

- **Stream 2.2.x**: The upstream branch `release/0.4.z` already ships quinn-proto 0.11.14
  (as seen in tags v0.4.11 and v0.4.12). Remediation path: **dependency bump** (cargo
  update) + downstream propagation.
- **Stream 2.1.x**: The upstream branch `release/0.3.z` still ships quinn-proto 0.11.9
  (latest tag v0.3.12). Remediation path: **upstream backport** (bump quinn-proto on
  the release branch) + downstream propagation.
