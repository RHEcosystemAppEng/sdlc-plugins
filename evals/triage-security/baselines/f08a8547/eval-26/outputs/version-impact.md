# Step 2 -- Version Impact Analysis

## Stream scope: 2.2.x only

Issue TC-8050 is scoped to the 2.2.x stream per the `[rhtpa-2.2]` suffix.
Only versions from the 2.2.x stream are analyzed below.

## Version Impact Table

Version Impact for CVE-2026-99001 (criterion < 0.5.2):

| Version | Tag | criterion version | Affected? | Notes |
|---------|-----|-------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.5.1 | YES | 0.5.1 < 0.5.2 fix threshold |
| 2.2.1 | v0.4.8 | 0.5.1 | YES | 0.5.1 < 0.5.2 fix threshold |
| 2.2.2 | v0.4.9 | 0.5.1 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.5.1 | YES | 0.5.1 < 0.5.2 fix threshold |
| 2.2.4 | v0.4.12 | 0.5.1 | YES | 0.5.1 < 0.5.2 fix threshold |

All 2.2.x versions ship criterion 0.5.1, which is within the affected range (< 0.5.2).

## Cross-stream note (2.1.x)

The 2.1.x stream is also affected (criterion 0.5.1 at all tags), but this issue
is scoped to 2.2.x only. Cross-stream impact will be handled via Case A in Step 8.

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

Manifest evidence:
```toml
# backend/Cargo.toml (all versions)
[dev-dependencies]
criterion = "0.5.1"
```

### Dependency Scope Assessment

criterion is declared in `[dev-dependencies]` in backend/Cargo.toml.
Dev-dependencies are used for tests and benchmarks only and are NOT shipped
in the production binary or container image.

Per the dependency scope decision tree:

- **Dev-only dependency**: criterion is not shipped in production. It still
  represents a supply chain risk (compromised dev deps can inject malicious
  code during builds), so remediation tasks are still created.
- **Label override**: remediation tasks receive the `dev-dependency` label.
- **Priority override**: priority is set to **Normal** regardless of CVE
  severity (CVSS 5.3 Medium). Do not inherit the CVE's priority.
- **Description note**: "This dependency is dev/build-only and is not shipped
  in production. Remediation priority is Normal (supply chain risk only)."

## Step 2.5 -- Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | criterion at HEAD | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.2.x | Cargo | release/0.4.z | (not checked -- eval mode) | Unknown |

Note: In this eval, upstream fix status was not checked via git show because
external tool calls are disabled. In a real triage, the skill would run:
```
git -C /home/dev/repos/rhtpa-backend show release/0.4.z:Cargo.lock | grep -A2 'name = "criterion"'
```
