# Step 2 – Version Impact Analysis: CVE-2026-31812

The lock file data comes from the mock `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` output in security-matrix-mock.md.

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | backend tag | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | outside issue scope |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | outside issue scope |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.8 | — | YES | same as 2.2.1 (backend retag of 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships the fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships the fixed version |
| dev stream | — | branch HEAD | not determined | — | Unreleased Jira versions could not be fetched (no Jira call allowed), so no development stream was identified |

**Summary:**
- Affected in issue scope (2.2.x): 2.2.0, 2.2.1 and 2.2.2.
- Already fixed in 2.2.x: 2.2.3 and 2.2.4, which ship quinn-proto 0.11.14.
- Affected outside issue scope (2.1.x): 2.1.0 and 2.1.1. This is cross-stream impact.

## Dependency chain context (Step 2.3.5)

```
Dependency chain for quinn-proto:
  backend (rhtpa-backend workspace) → ... → quinn-proto
  Type: not determined (the mock data has no Cargo.toml or full Cargo.lock dependency graph)
  Profile: assumed production (QUIC transport crate; no dev-dependency evidence)
  Introduction point: present in all inspected tags (v0.3.8 onward)
  Fix introduced in 2.2.x at: v0.4.11 (2.2.3)
```

## Upstream fix status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | not available in mock data (latest tag v0.3.12 = 0.11.9) | NO (unverified) |
| 2.2.x | Cargo | release/0.4.z | not available in mock data (latest tag v0.4.12 = 0.11.14) | YES (based on latest release tag) |

Remediation path:
- **2.2.x**: the fix already shipped in 2.2.3 and later. The affected versions 2.2.0–2.2.2 are superseded by 2.2.3/2.2.4, so no new code change is needed in this stream.
- **2.1.x**: no fix is shipped. This needs an upstream backport (bump quinn-proto to >= 0.11.14 on `release/0.3.z`), then downstream propagation in rhtpa-release.0.3.z.
