# Step 2 — Version Impact Analysis for CVE-2026-31812

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | — | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | at fix threshold |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | at fix threshold |

## Summary

- **Affected versions**: 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2
- **Not affected versions**: 2.2.3, 2.2.4
- **Fix threshold**: quinn-proto >= 0.11.14
- **First fixed in**: 2.2.3 (build 0.4.11, build date 2026-03-23)

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Check Command | Notes |
|--------|-----------|-----------------|---------------|-------|
| 2.1.x | Cargo | release/0.3.z | `git show <tag>:Cargo.lock` | All released versions affected |
| 2.2.x | Cargo | release/0.4.z | `git show <tag>:Cargo.lock` | Fixed from 2.2.3 onward |
