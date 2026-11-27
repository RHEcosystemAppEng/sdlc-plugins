# Step 2 – Version Impact Analysis: CVE-2026-31812 (TC-8001)

Analysis continues after the Step 1.7 embargo gate, assuming the engineer answers "Yes".

## 2.1 – Supportability matrix (aggregated)

Both streams come from the Version Streams table. Matrix data comes from
`security-matrix-mock.md`. Both matrices have the required sections (Supportability
Matrix, Source Pinning Method, Ecosystem Mappings, Forward Pointer) and parsable
tables, so format validation passes. Staleness warning: both matrices were last
updated 2026-06-28, 152 days ago (see data-extraction.md).

| Stream | Version | Build | Build Date | backend pinned tag | Notes |
|--------|---------|-------|------------|--------------------|-------|
| 2.1.x | 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.x | 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |
| 2.2.x | 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.x | 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.x | 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.x | 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.x | 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.2 – Development stream

The unreleased Jira versions could not be retrieved (Jira calls are forbidden in this
eval), so no development stream could be identified. The 2.2.x matrix says it is the
latest stream (no forward pointer). **Development-stream (branch HEAD) status is
UNDETERMINED.** The engineer should check the dev branch HEAD `Cargo.lock` before
closing out triage.

## 2.3 – Dependency versions (Cargo, `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`)

These are simulated lock-file outputs from the mock data. The fix threshold is
quinn-proto < 0.11.14 (from the Jira description; Step 1.5 enrichment was unavailable).

## 2.4 – Version Impact Table

```
Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):
```

| Version | Stream | Pinned tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | **YES** | outside issue scope (cross-stream) |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | **YES** | outside issue scope (cross-stream) |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | **YES** | in scope |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | **YES** | in scope |
| 2.2.2 | 2.2.x | `v0.4.8` | — | **YES** | same as 2.2.1 (backend retag of 2.2.1; lock file check skipped) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | ships fixed version |
| dev (unknown) | — | branch HEAD | not checked | UNDETERMINED | no Jira/repo access in this eval |

### Dependency chain context (Step 2.3.5)

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) → ? → quinn-proto
  Type: NOT DETERMINED. Only lock-file version data was provided; Cargo.toml /
        Cargo.lock dependency graphs were not available. quinn-proto is usually
        pulled in transitively through `quinn` (for example via reqwest's http3
        feature), but this has NOT been verified.
  Profile: NOT DETERMINED (assume production until shown otherwise; no
        dev-dependency label applied)
  Introduction point: present in every release from 2.1.0 (v0.3.8) onward
  Version history: 0.11.9 (2.1.0–2.2.0) → 0.11.12 (2.2.1/2.2.2) → 0.11.14 (2.2.3+)
```

Action for the engineer: run
`git -C /home/dev/repos/rhtpa-backend show v0.3.12:Cargo.lock` and run `cargo tree -i
quinn-proto` on `release/0.3.z` to confirm direct vs transitive before implementation.

## 2.5 – Upstream fix status

| Stream | Ecosystem | Repository | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|------------|-----------------|-----------------|--------|
| 2.1.x | Cargo | backend | `release/0.3.z` | not checked (latest release tag `v0.3.12` has 0.11.9) | **NOT CONFIRMED**, so treat as not fixed |
| 2.2.x | Cargo | backend | `release/0.4.z` | not checked (latest release tag `v0.4.12` has 0.11.14) | **YES in shipped releases**: fixed since 2.2.3 (`v0.4.11`) |

## Summary of impact

- **In-scope stream 2.2.x**: 2.2.0, 2.2.1, and 2.2.2 are affected. 2.2.3 and 2.2.4 already
  ship quinn-proto 0.11.14 and are **not affected**. The fix is already in the latest
  2.2.x release.
- **Out-of-scope stream 2.1.x**: 2.1.0 and 2.1.1 are affected (quinn-proto 0.11.9). No
  fixed 2.1.x release exists, so this is **cross-stream impact (Case A)**.
- **PSIRT Affects Versions is wrong**: the issue has `RHTPA 2.0.0`, but no 2.0.x stream
  exists.

### Step 3 preview – Affects Versions correction (scoped to 2.2.x)

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

The 2.1.x versions (RHTPA 2.1.0, 2.1.1) belong to a 2.1.x companion issue and are not
added to TC-8001. Jira version IDs must come from
`getJiraIssueTypeMetaWithFields(TC, 10024)` at execution time. If any of these versions
are not registered in Jira, flag it to the project admin. Proposed correction comment:

> Corrected Affects Versions: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
> Based on lock file analysis at pinned commits from security-matrix.md.
> Scoped to stream 2.2.x per issue suffix.
> (Comment Footnote per shared/comment-footnote.md, skill `triage-security`.)

The ProdSec @mention is omitted because it is not configured.

**Engineer confirmation of this table is required before Step 3.**
