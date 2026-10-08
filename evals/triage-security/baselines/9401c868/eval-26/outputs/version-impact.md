# Step 2 -- Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-99001 (criterion versions before 0.5.2):

| Version | criterion | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.2.0 | 0.5.1 | YES | |
| 2.2.1 | 0.5.1 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 0.5.1 | YES | |
| 2.2.4 | 0.5.1 | YES | |

All 2.2.x versions ship criterion 0.5.1, which is within the affected range (< 0.5.2).

## Cross-Stream Impact (Case A)

The 2.1.x stream is also affected:

| Version | criterion | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.1.0 | 0.5.1 | YES | |
| 2.1.1 | 0.5.1 | YES | |

Cross-stream impact: criterion versions before 0.5.2 also affects stream 2.1.x
based on lock file analysis.

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

**Dependency scope assessment**: criterion is declared in `[dev-dependencies]`
in `backend/Cargo.toml`. It is used for benchmarks only and is NOT shipped in
production container images. Per the dependency scope decision tree:

- Dev-only dependencies still represent a supply chain risk (compromised dev deps
  can inject malicious code during builds)
- Remediation tasks will carry the `dev-dependency` label
- Priority is overridden to **Normal** regardless of CVE severity (CVSS 5.3 Medium)
- Remediation task descriptions will include the note: "This dependency is
  dev/build-only and is not shipped in production. Remediation priority is
  Normal (supply chain risk only)."

## Upstream Fix Status (Step 2.5)

The fix version (0.5.2) is a released version of the criterion crate. All 2.2.x
versions currently pin criterion 0.5.1 in Cargo.lock. A `cargo update -p criterion`
on the upstream branch (`release/0.4.z`) would pull in the fix.

| Stream | Ecosystem | Upstream Branch | criterion at HEAD | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.5.1 (in lock) | NO -- lock file still pins 0.5.1 |

Since the upstream branch lock file still pins the vulnerable version, the
remediation path is: dependency bump (`cargo update -p criterion`) on the
upstream branch, then downstream propagation to the Konflux release repo.
