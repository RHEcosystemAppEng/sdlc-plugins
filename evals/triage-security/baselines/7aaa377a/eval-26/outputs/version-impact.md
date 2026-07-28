# Step 2 -- Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-99001 (criterion < 0.5.2):

| Version | criterion | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.2.0 | 0.5.1 | YES | |
| 2.2.1 | 0.5.1 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.5.1 | YES | |
| 2.2.4 | 0.5.1 | YES | |

All versions in the 2.2.x stream ship criterion 0.5.1, which is within the
affected range (< 0.5.2). All versions are affected.

**Source commits used** (from supportability matrix pinned commits):
- 2.2.0: `v0.4.5`
- 2.2.1: `v0.4.8`
- 2.2.2: `v0.4.9` (retag of v0.4.8 -- skipped, carried forward from 2.2.1)
- 2.2.3: `v0.4.11`
- 2.2.4: `v0.4.12`

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

criterion is declared in `[dev-dependencies]` in the Cargo manifest. This means:

- **Classification**: dev-only -- not shipped in production
- **Risk**: Supply chain risk only (compromised dev deps can inject malicious
  code during builds), but the vulnerable code is NOT present in the production
  binary or container image
- **Remediation handling**:
  - Still create remediation tasks (supply chain risk justifies remediation)
  - Add the `dev-dependency` label to remediation tasks
  - Override priority to **Normal** regardless of CVE severity (CVSS 5.3 Medium)
  - Include a note in the remediation task description: "This dependency is
    dev/build-only and is not shipped in production. Remediation priority is
    Normal (supply chain risk only)."

---

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | (would check via git show) | (to be determined) |

Note: In this eval, external tools are not invoked. In a real triage, the skill
would run `git show release/0.4.z:Cargo.lock | grep -A2 'name = "criterion"'`
to determine the upstream fix status.
