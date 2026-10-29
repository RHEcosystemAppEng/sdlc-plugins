# Step 2 -- Version Impact Analysis: TC-8050

## CVE-2026-99001 (criterion < 0.5.2)

Stream scope: **2.2.x only** (from issue suffix `[rhtpa-2.2]`)

## Version Impact Table

| Version | Build Tag | criterion version | Affected? | Notes |
|---------|-----------|-------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.5.1 | YES | 0.5.1 < 0.5.2 fix threshold |
| 2.2.1 | v0.4.8 | 0.5.1 | YES | 0.5.1 < 0.5.2 fix threshold |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.5.1 | YES | 0.5.1 < 0.5.2 fix threshold |
| 2.2.4 | v0.4.12 | 0.5.1 | YES | 0.5.1 < 0.5.2 fix threshold |

**All versions in the 2.2.x stream ship criterion 0.5.1, which is within the affected range (< 0.5.2).**

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for criterion:
  backend (workspace) -> criterion (direct dev-dependency)
  Type: direct dependency
  Profile: dev-only ([dev-dependencies] in backend/Cargo.toml)
  NOT present in production builds -- used for benchmarks only

First appeared: 2.1.0 (initial project setup)
Present in all versions
```

**Manifest evidence:**
```toml
# backend/Cargo.toml (all versions)
[dev-dependencies]
criterion = "0.5.1"
```

### Dependency Scope Assessment

- **Scope**: dev-only (`[dev-dependencies]`)
- **Shipped in production?**: NO -- criterion is used for benchmarks only and is not included in production builds or container images
- **Risk level**: Supply chain risk only -- a compromised dev dependency could inject malicious code during builds, but the vulnerable code itself does not run in production
- **Remediation impact**: Per the dependency scope decision tree in version-impact-analysis.md:
  - Add `dev-dependency` label to remediation tasks
  - Override priority to **Normal** regardless of CVE severity (CVSS 5.3 Medium)
  - Include dev-only note in remediation task description

## Fix Threshold

- Source: Jira description (external CVE databases not queried in this eval)
- Affected range: versions before 0.5.2
- Fix threshold: **>= 0.5.2**

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | Not checked (eval mode -- no git access) |

Note: In a real triage, `git show release/0.4.z:Cargo.lock` would be inspected to determine if the upstream branch already ships criterion >= 0.5.2. Since the fix version 0.5.2 exists as a published crate, the remediation would likely be a dependency bump (`cargo update -p criterion`) rather than an upstream backport.
