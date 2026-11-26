# Step 2 – Version Impact Analysis: CVE-2026-31812 (quinn-proto < 0.11.14)

## 2.1 – Supportability matrix (aggregated)

Two streams come from the Version Streams table: 2.1.x (rhtpa-release.0.3.z) and 2.2.x (rhtpa-release.0.4.z). Both matrices have all required sections (Supportability Matrix, Ecosystem Mappings with the canonical columns, Source Pinning Method, Forward Pointer), so format validation passes.

## 2.2 – Development stream

The development stream could not be determined. That requires unreleased RHTPA Jira versions from `getJiraIssueTypeMetaWithFields`, and Jira was not called in this eval. 2.2.x is the latest configured stream and has no forward pointer. The engineer should confirm whether an unreleased version (for example RHTPA 2.3 / 3.0) exists and needs a branch-HEAD check.

## 2.3 – Lock file evidence

Simulated `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` (Cargo, repo `backend`), using the mock lock file data:

| Tag | quinn-proto |
|-----|-------------|
| v0.3.8 | 0.11.9 |
| v0.3.12 | 0.11.9 |
| v0.4.5 | 0.11.9 |
| v0.4.8 | 0.11.12 |
| v0.4.11 | 0.11.14 |
| v0.4.12 | 0.11.14 |

## 2.4 – Version Impact Table

```
Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):
```

| Version | Stream | Backend tag (pinned) | quinn-proto | Affected? | Notes |
|---------|--------|----------------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | outside issue scope (cross-stream) |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | outside issue scope (cross-stream) |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | in scope |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | in scope |
| 2.2.2 | 2.2.x | v0.4.8 | — | YES | same as 2.2.1 (backend retag of 2.2.1; lock file check skipped and result carried forward) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | fixed version shipped |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | fixed version shipped |
| dev | — | branch HEAD | not determined | UNKNOWN | development stream not identified (needs a Jira versions query) |

Summary:
- **In-scope stream 2.2.x:** 2.2.0, 2.2.1, and 2.2.2 are affected. 2.2.3 and 2.2.4 are not, because the fix (0.11.14) has shipped since 2.2.3.
- **Out-of-scope stream 2.1.x:** 2.1.0 and 2.1.1 are affected (0.11.9). Every released 2.1.x version is vulnerable.

### 2.3.5 – Dependency chain context

```
Dependency chain for quinn-proto:
  backend (workspace) → ... → quinn → quinn-proto   (expected path via QUIC/HTTP3 stack)
  Type: transitive (assumed; quinn-proto is normally pulled in via quinn)
  Profile: production (runtime networking dependency) — not dev-only
  Introduction point: present in all inspected tags (v0.3.8 onward)
```

Limitation: the mock data has only the resolved quinn-proto version, not the `Cargo.toml` manifests or the full `Cargo.lock` dependency graph. So direct vs. transitive and the exact chain are unverified. The engineer should confirm them with `git show <tag>:Cargo.lock` and the workspace `Cargo.toml` before the tasks are finalized. Nothing points to a dev-only or build-only scope, so the `dev-dependency` label and Normal priority override do not apply.

## 2.5 – Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | not available (latest released tag v0.3.12 = 0.11.9) | NO (by latest tag evidence) |
| 2.2.x | Cargo | release/0.4.z | not available (latest released tags v0.4.11 / v0.4.12 = 0.11.14) | YES (by latest tag evidence) |

The branch-HEAD lock files (`git show release/0.x.z:Cargo.lock`) are not in the mock data, so the latest pinned release tag on each branch is used as a proxy. The engineer should verify HEAD.

Remediation path implications:
- **2.2.x**: the fix is already upstream on release/0.4.z and already shipped in 2.2.3 and later. Affected 2.2.0 through 2.2.2 are fixed by upgrading to 2.2.3 or 2.2.4. No new backport is needed.
- **2.1.x**: not fixed upstream. An upstream backport (bump quinn-proto to >= 0.11.14 on release/0.3.z) is needed, then Konflux propagation in rhtpa-release.0.3.z.

## Step 3 preview – Affects Versions correction (scoped to 2.2.x)

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

RHTPA 2.0.0 matches no configured stream (no 2.0.x stream exists), so the PSIRT-assigned value is wrong. The 2.1.x versions are left out because the issue is scoped to 2.2.x; they are handled as cross-stream impact. The version IDs would be resolved dynamically through `getJiraIssueTypeMetaWithFields`, and the change needs engineer confirmation.

Waiting for the engineer to review and confirm this table before Step 3.
