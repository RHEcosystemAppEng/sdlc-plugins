# Step 2 – Version Impact Analysis: CVE-2026-31812 (quinn-proto < 0.11.14)

Evidence: the simulated `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` output from security-matrix-mock.md ("Mock Lock File Data"). Each released version uses its pinned `backend` tag from its stream's Supportability Matrix. No real git commands were run.

## 2.1 Supportability matrix

| Stream | Konflux repo | Versions | Cargo lock file | Upstream branch |
|--------|--------------|----------|-----------------|-----------------|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0, 2.1.1 | backend `Cargo.lock` | release/0.3.z |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | backend `Cargo.lock` | release/0.4.z |

Both matrices pass the format check: the required sections are present and the Ecosystem Mappings columns match the template. The matrix files have no `Last-Updated` timestamp, so Step 0.3 only advises running `/setup` to add one. That does not block triage.

## 2.4 Version impact table

```
Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):
```

| Version | Stream | backend tag | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | Outside issue scope |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | Outside issue scope |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.8 | — | YES | Same as 2.2.1 (backend retag of 2.2.1; lock file check skipped) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | Fixed version shipped |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | Fixed version shipped |
| Dev stream | — | branch HEAD | not determined | not determined | Step 2.2 needs Jira unreleased-version metadata and HEAD lock file reads, which are not available in this eval. No version is assumed |

**Summary**
- Issue scope (2.2.x): **2.2.0, 2.2.1, 2.2.2 are affected.** 2.2.3 and 2.2.4 are not, because they already ship 0.11.14.
- Outside scope (2.1.x): **2.1.0 and 2.1.1 are affected.** This is cross-stream impact (Case A).

## 2.3.5 Dependency chain context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) → ... → quinn → quinn-proto   (expected path via the quinn QUIC crate)
  Type: not verified. The mock data provides only the Cargo.lock version line,
        with no dependency graph or Cargo.toml content. Confirm direct versus
        transitive during implementation (e.g., `cargo tree -i quinn-proto`).
  Profile: assumed production (no dev/build-only evidence). No dev-dependency label.
  Introduction: present in all inspected tags from v0.3.8 onwards.
```

## 2.5 Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | not available (latest released tag v0.3.12 = 0.11.9) | Not confirmed. Treated as **not fixed** |
| 2.2.x | Cargo | release/0.4.z | not available (released tags v0.4.11 and v0.4.12 = 0.11.14) | **Fix already on branch.** Released tags cut from release/0.4.z ship 0.11.14 |

Remediation paths that follow from this:
- 2.1.x: an upstream backport (bump quinn-proto on release/0.3.z), then downstream propagation in rhtpa-release.0.3.z.
- 2.2.x: the fix is already available upstream and shipped from 2.2.3 onwards. This is the dependency-bump variant. The downstream work is verifying or keeping the rhtpa-release.0.4.z pin at v0.4.11 or later.

## Step 3 preview – Affects Versions correction (stream-scoped)

`Current: [RHTPA 2.0.0] → Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

RHTPA 2.0.0 does not correspond to any supported stream. Jira version IDs must be discovered at runtime through `getJiraIssueTypeMetaWithFields`; they were not available in this eval. The correction needs engineer confirmation.
