# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0   | 2.1.x  | v0.3.8    | 0.11.9      | YES       |       |
| 2.1.1   | 2.1.x  | v0.3.12   | 0.11.9      | YES       |       |
| 2.2.0   | 2.2.x  | v0.4.5    | 0.11.9      | YES       |       |
| 2.2.1   | 2.2.x  | v0.4.8    | 0.11.12     | YES       |       |
| 2.2.2   | 2.2.x  | v0.4.9    | 0.11.12     | YES       | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3   | 2.2.x  | v0.4.11   | 0.11.14     | NO        | meets fix threshold |
| 2.2.4   | 2.2.x  | v0.4.12   | 0.11.14     | NO        | meets fix threshold |

## Summary

- **Fix threshold**: quinn-proto >= 0.11.14 (from CVE description, confirmed by advisory)
- **Affected versions**: 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2
- **Not affected versions**: 2.2.3, 2.2.4
- **Issue stream scope**: 2.2.x -- within this stream, versions 2.2.0, 2.2.1, and 2.2.2 are affected
- **Cross-stream impact**: 2.1.x stream is also affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9)

## Lock File Evidence

All dependency versions were extracted using `git show <tag>:Cargo.lock` at the pinned commits from the supportability matrix:

- `git show v0.3.8:Cargo.lock` -> quinn-proto 0.11.9
- `git show v0.3.12:Cargo.lock` -> quinn-proto 0.11.9
- `git show v0.4.5:Cargo.lock` -> quinn-proto 0.11.9
- `git show v0.4.8:Cargo.lock` -> quinn-proto 0.11.12
- `v0.4.9` -> retag of v0.4.8, carrying forward result: quinn-proto 0.11.12
- `git show v0.4.11:Cargo.lock` -> quinn-proto 0.11.14
- `git show v0.4.12:Cargo.lock` -> quinn-proto 0.11.14
