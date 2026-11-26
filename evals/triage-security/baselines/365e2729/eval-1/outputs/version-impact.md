# TC-8001 — Version Impact Analysis (Step 2)

> **Eval simulation.** The lock file versions come from the "Mock Lock File Data"
> section of `security-matrix-mock.md`, which stands in for the output of
> `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`. No real `git show` was run.
> No Jira operation was performed.

## 2.1 — Supportability matrix (all configured streams)

Both rows of the Version Streams table were enumerated directly, without relying on forward pointers:

- **2.1.x**: `rhtpa-release.0.3.z`, versions 2.1.0 and 2.1.1, Cargo upstream branch `release/0.3.z`
- **2.2.x**: `rhtpa-release.0.4.z`, versions 2.2.0 through 2.2.4, Cargo upstream branch `release/0.4.z`

The matrix format checks pass: Supportability Matrix, Ecosystem Mappings (with the canonical columns), Source Pinning Method, and Forward Pointer are all present.

## 2.2 — Development stream

Development stream detection needs the unreleased `RHTPA` versions from `getJiraIssueTypeMetaWithFields`. Jira was not queried and the inputs contain no unreleased-version data, so **no development stream could be identified**. The branch-HEAD check could not be done either. This is a reported gap, not an assumption.

## 2.3 / 2.4 — Version impact table

**Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):**

| Version | Stream | Build | backend tag (pinned) | quinn-proto | Affected? | Notes |
|---------|--------|-------|----------------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.3.8 | `v0.3.8` | 0.11.9 | **YES** | outside issue scope (cross-stream) |
| 2.1.1 | 2.1.x | 0.3.12 | `v0.3.12` | 0.11.9 | **YES** | outside issue scope (cross-stream) |
| 2.2.0 | 2.2.x | 0.4.5 | `v0.4.5` | 0.11.9 | **YES** | in scope |
| 2.2.1 | 2.2.x | 0.4.8 | `v0.4.8` | 0.11.12 | **YES** | in scope |
| 2.2.2 | 2.2.x | 0.4.9 | `v0.4.8` | — | **YES** | in scope; **same as 2.2.1** (backend retag of 2.2.1, lock file check skipped, result carried forward) |
| 2.2.3 | 2.2.x | 0.4.11 | `v0.4.11` | 0.11.14 | NO | fixed version shipped |
| 2.2.4 | 2.2.x | 0.4.12 | `v0.4.12` | 0.11.14 | NO | fixed version shipped |
| dev | — | — | branch HEAD | not determined | not determined | dev stream could not be identified (see 2.2) |

Summary:
- **In-scope (2.2.x) affected:** 2.2.0, 2.2.1, 2.2.2. Versions 2.2.3 and later already ship quinn-proto 0.11.14.
- **Cross-stream (2.1.x) affected:** 2.1.0, 2.1.1. Every released 2.1.x version ships 0.11.9, so this stream has no fixed release yet.

### 2.3.5 — Dependency chain context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) → ... → quinn-proto
  Type: NOT DETERMINED. The mock data provides only resolved Cargo.lock versions.
        Classifying it as direct or transitive needs Cargo.toml / `cargo tree -i quinn-proto`
        at the pinned tags (for example, a direct dep or pulled in via quinn / reqwest http3).
  Profile: NOT DETERMINED. No evidence that it is dev-only or build-only, so it is
           treated as production (no `dev-dependency` label, no priority override).
  Introduction point: present in every supported tag (v0.3.8 through v0.4.12);
           upgraded to 0.11.12 at v0.4.8 and to 0.11.14 (fixed) at v0.4.11.
```

## 2.5 — Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? | Evidence |
|--------|-----------|-----------------|-----------------|--------|----------|
| 2.2.x | Cargo | `release/0.4.z` | not read (needs `git -C /home/dev/repos/rhtpa-backend show release/0.4.z:Cargo.lock`) | **Likely YES** | Release tags `v0.4.11` and `v0.4.12` cut from this branch already ship 0.11.14 |
| 2.1.x | Cargo | `release/0.3.z` | not read (needs `git -C /home/dev/repos/rhtpa-backend show release/0.3.z:Cargo.lock`) | **Unknown, assume NO** | The latest tag `v0.3.12` ships 0.11.9. No evidence of a fix on this branch |

Remediation path implications:
- **2.2.x:** the fix is available upstream, so the **dependency bump** variant applies, plus downstream propagation. The latest release 2.2.4 already ships the fix.
- **2.1.x:** no fix is known upstream, so the **upstream backport** variant applies, plus downstream propagation.

Before Step 3, the engineer would review and confirm this table.
