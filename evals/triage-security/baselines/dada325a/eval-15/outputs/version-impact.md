# Step 2 – Version Impact Analysis: TC-8001

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14). Fixed in 0.11.14.

Evidence: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` at each pinned backend tag from security-matrix.md. In this eval, the output is simulated by the mock lock file data.

| Stream | Version | Build | backend tag (pinned) | quinn-proto | Affected? | Notes |
|--------|---------|-------|----------------------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.3.8 | `v0.3.8` | 0.11.9 | YES | Outside issue scope (cross-stream) |
| 2.1.x | 2.1.1 | 0.3.12 | `v0.3.12` | 0.11.9 | YES | Outside issue scope (cross-stream) |
| 2.2.x | 2.2.0 | 0.4.5 | `v0.4.5` | 0.11.9 | YES | In scope |
| 2.2.x | 2.2.1 | 0.4.8 | `v0.4.8` | 0.11.12 | YES | In scope |
| 2.2.x | 2.2.2 | 0.4.9 | `v0.4.8` | — | YES | Same as 2.2.1 (backend retag of 2.2.1); lock file check skipped |
| 2.2.x | 2.2.3 | 0.4.11 | `v0.4.11` | 0.11.14 | NO | Fixed version shipped |
| 2.2.x | 2.2.4 | 0.4.12 | `v0.4.12` | 0.11.14 | NO | Fixed version shipped |
| dev | — | — | branch HEAD | not determined | — | Step 2.2 needs Jira unreleased versions, which this eval did not query, so no development stream was identified. 2.2.x is the latest configured stream. |

**Summary**
- Scoped stream 2.2.x: **2.2.0, 2.2.1 and 2.2.2 are affected**. 2.2.3 and 2.2.4 are not affected, because the fix (quinn-proto 0.11.14) first shipped in 2.2.3.
- Cross-stream: **2.1.x (2.1.0, 2.1.1) is also affected**, with quinn-proto 0.11.9.
- RHTPA 2.0.0 (the PSIRT-assigned version) does not exist in any configured stream or supportability matrix.

## Step 2.3.5 – Dependency chain context

```
Dependency chain for quinn-proto (Cargo):
  Ecosystem: Cargo (source dependency), repository backend (rhtpa-backend)
  Type: not determined. The workspace Cargo.toml and the Cargo.lock dependents
        were not inspected in this eval. quinn-proto is normally a transitive
        dependency, pulled in through quinn by an HTTP/3 or QUIC-capable client
        such as reqwest with the http3 feature. Verify this with
        `git show <tag>:Cargo.lock` reverse-dependency inspection before
        implementation.
  Profile: assumed production (runtime networking). Not confirmed as dev-only.
  Present in: all released versions of 2.1.x and 2.2.x
  Fixed from: 2.2.3 (backend v0.4.11), where quinn-proto moved from 0.11.12 to 0.11.14
```

## Step 2.5 – Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | not available (git not run in this eval) | UNKNOWN. The latest 0.3.z tag (`v0.3.12`) ships 0.11.9 |
| 2.2.x | Cargo | release/0.4.z | not available (git not run in this eval) | YES for released tags: `v0.4.11` and `v0.4.12` ship 0.11.14 |

Remediation paths:
- **2.2.x**: the fix is already shipped in RHTPA 2.2.3 and 2.2.4. No new upstream or Konflux change is needed for the stream.
- **2.1.x**: the fix is not confirmed on release/0.3.z. An upstream backport (bump quinn-proto to >= 0.11.14 on release/0.3.z) and then downstream propagation in rhtpa-release.0.3.z are required.

The engineer reviews and confirms the table before Step 3 (simulated confirmation).
