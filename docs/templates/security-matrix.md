<!-- Last-Updated: {{last-updated-timestamp}} -->

# Security Matrix Template

<!-- TODO: Copy this template into the project working directory at the path specified in
     your Security Configuration's Version Streams table (e.g., docs/security-matrix-2.2.x.md)
     and fill in the sections below. Each file covers one version stream's supportability matrix.

     The triage-security skill reads this file to determine which product versions ship a given
     dependency version, enabling automated CVE impact analysis across supported releases. -->

## Version Stream

This Konflux release repo covers the **{{version-stream}}** product version stream.

## Supportability Matrix

<!-- TODO: Add one row per product version built from this release stream.
     Add one column per source repository listed in your Security
     Configuration's Source Repositories table, using the repo short name.

     - Version: the product version label (e.g., 2.2.0, 2.2.1)
     - Build: the Konflux build identifier (e.g., 0.4.12)
     - Build Date: the date Konflux built the image
     - <repo>: one column per source repo, containing the tag or commit hash
       pinned in the build (e.g., `v0.4.12` or `9e03dca1`)
     - Notes: free-form; note retags here (e.g., "frontend-ui retag of 2.2.1")

     This matrix can be populated during /setup or filled in on demand by
     /triage-security when investigating a CVE. -->

| Version | Build | Build Date | {{source-repo-name}} | Notes |
|---------|-------|------------|----------------------|-------|
| {{version}} | {{build}} | {{build-date}} | {{source-ref}} | |

### Source Pinning Method

<!-- TODO: Describe how each source repository's commit or tag is pinned in this
     release repo. Common methods:
     - git submodule at `components/<repo>`
     - `artifacts.lock.yaml` (download URL contains the tag)
     - tag reference in a build config file -->

- **{{source-repo-name}}**: {{pinning-method}}

## Ecosystem Mappings

<!-- TODO: List every ecosystem whose dependencies are tracked in this stream.
     - Ecosystem: the package ecosystem name (e.g., Cargo, npm, RPM)
     - Repository: the source repo short name that owns the lock file (from
       Source Repositories in your Security Configuration), or "—" if N/A
     - Lock File: the lock file name within the source repo (e.g., Cargo.lock);
       leave empty if no lock file exists
     - Check Command: the command to inspect a specific dependency at a given commit
       (use `git show <commit>:<lock-file>` as the base pattern)
     - Upstream Branch: the branch in the source repository that feeds this stream.
       Used during triage to check if a vulnerability is already fixed upstream
       (e.g., "main" for the dev stream, "release/0.4.z" for a release stream). -->

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| {{ecosystem}} | {{repository}} | {{lock-file}} | `git show <commit>:{{lock-file}}` | {{upstream-branch}} |

---

## Worked Example: MYPRODUCT 2.2.x in the 0.4.z Stream

<!-- This example shows a completed security-matrix.md for a product-release.0.4.z
     repo, covering the 2.2.x version stream. Use it as a reference when filling
     in the template sections above. -->

### Version Stream

This Konflux release repo covers the **2.2.x** product version stream.

### Supportability Matrix

| Version | Build | Build Date | backend | frontend-ui | Notes |
|---------|-------|------------|---------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | `bb447eeb` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | `40874efb` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.9` | `40874efb` | frontend-ui retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | `bf9fc536` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | `9e03dca1` | |

#### Source Pinning Method

- **backend**: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **frontend-ui**: git submodule at `components/frontend-ui`

### Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| npm | frontend-ui | `package-lock.json` | `git show <commit>:package-lock.json` | `release/0.4.z` |

### Forward Pointer

Next stream: `3.0.x` at `git.downstream.example.com/my-org/product-release.0.5.z`
