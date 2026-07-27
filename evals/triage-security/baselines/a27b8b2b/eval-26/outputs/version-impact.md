# Step 2 -- Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-99001 (criterion < 0.5.2):

| Version | criterion | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.2.0 | 0.5.1 | YES | Pinned commit: v0.4.5 |
| 2.2.1 | 0.5.1 | YES | Pinned commit: v0.4.8 |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.5.1 | YES | Pinned commit: v0.4.11 |
| 2.2.4 | 0.5.1 | YES | Pinned commit: v0.4.12 |

All versions in the 2.2.x stream ship criterion 0.5.1, which is within the affected range (< 0.5.2). All versions are affected.

---

## Step 2.3.5 -- Dependency Chain Context

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

### Dependency Scope Decision Tree

criterion is declared in `[dev-dependencies]` in backend/Cargo.toml. This means:

- **Classification**: dev-only -- not shipped in production
- **Risk**: Supply chain risk only (compromised dev deps can inject malicious code during builds), but the package does not appear in the production binary or container image
- **Remediation handling**:
  - Remediation tasks are still created (supply chain risk justifies remediation)
  - Add the `dev-dependency` label to remediation tasks
  - Set priority to **Normal** regardless of the CVE severity (CVSS 5.3 Medium)
  - Include a note in remediation task descriptions: "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."

### SBOM Verification

SBOM verification is not applicable for source dependency ecosystems (Cargo). SBOM verification applies to RPM/system package ecosystems only.

---

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | Proposed: check `git show release/0.4.z:Cargo.lock` for criterion version |

The upstream fix status would be verified by inspecting the criterion version at the upstream branch HEAD (`release/0.4.z`) in the backend repository.
