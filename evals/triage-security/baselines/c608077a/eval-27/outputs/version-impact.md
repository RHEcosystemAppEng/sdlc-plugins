# Step 2 – Version Impact Analysis: CVE-2026-99002 (rustls < 0.23.5)

**Scope:** 2.2.x stream only (issue suffix `[rhtpa-2.2]`).
**Matrix:** `rhtpa-release.0.4.z` security-matrix (Stream 2 in the fixture).
**Ecosystem / lock file:** Cargo, `Cargo.lock` in backend, checked with `git show <tag>:Cargo.lock | grep -A2 'name = "rustls"'` (simulated with the fixture lock data).
**Fix threshold:** 0.23.5, from the Jira description. External enrichment was not run.

## Version Impact Table

```
Version Impact for CVE-2026-99002 (rustls < 0.23.5) — stream 2.2.x:

| Version | Build  | backend tag | rustls (Cargo.lock) | In affected range? | Shipped by default? | Affected? | Notes |
|---------|--------|-------------|---------------------|--------------------|---------------------|-----------|-------|
| 2.2.0   | 0.4.5  | v0.4.5      | 0.23.4              | YES                | NO (feature-gated)  | YES*      | rustls first introduced (optional, `tls-rustls`) |
| 2.2.1   | 0.4.8  | v0.4.8      | 0.23.4              | YES                | NO (feature-gated)  | YES*      | |
| 2.2.2   | 0.4.9  | v0.4.8      | —                   | YES                | NO (feature-gated)  | YES*      | same as 2.2.1 (backend retag) |
| 2.2.3   | 0.4.11 | v0.4.11     | 0.23.4              | YES                | NO (feature-gated)  | YES*      | |
| 2.2.4   | 0.4.12 | v0.4.12     | 0.23.4              | YES                | NO (feature-gated)  | YES*      | |
| dev     | —      | release/0.4.z HEAD | not determined | —                  | —                   | —         | dev stream detection needs Jira unreleased versions (not queried); see upstream fix status below |
```

\* **Conditionally affected.** Every 2.2.x release has rustls 0.23.4 in `Cargo.lock`, which is below the 0.23.5 fix, so the lock-file result is "in affected range". But rustls is an **optional dependency behind the non-default `tls-rustls` feature**. Default builds enable `tls-native` (native-tls), so the vulnerable crate is not compiled into the shipped product unless someone opts in to `tls-rustls`. The engineer decides between a VEX justification and remediation (see `feature-gate-prompt.md`).

Out of scope, for reference only: in the 2.1.x stream (2.1.0 / v0.3.8 and 2.1.1 / v0.3.12), rustls is **not present** in `Cargo.lock`. Not affected (Component not Present). No cross-stream action is needed.

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for rustls:
  backend (workspace) → rustls
  Type: direct dependency (optional)
  Profile: feature-gated — optional = true, enabled only by the
           NON-default feature "tls-rustls"
  Default features: ["tls-native"] → dep:native-tls (rustls NOT enabled)

Feature declaration (backend/Cargo.toml, v0.4.5+):
  [dependencies]
  rustls = { version = "0.23.4", optional = true }

  [features]
  default    = ["tls-native"]
  tls-native = ["dep:native-tls"]
  tls-rustls = ["dep:rustls"]

First appeared: 2.2.0 (backend v0.4.5, added as alternative TLS backend)
Not present in: 2.1.x (only native-tls was available)

Remediation (if pursued): direct dependency, so bump rustls to >= 0.23.5
in backend/Cargo.toml and refresh Cargo.lock on release/0.4.z, then
propagate the new backend tag to rhtpa-release.0.4.z.
```

### Dependency Scope Decision

- **Classification:** feature-gated optional dependency (Cargo `optional = true` behind a non-default feature).
- **Decision-tree outcome:** before creating any remediation tasks, show the engineer the VEX justification prompt. Recommended justification: **Vulnerable Code not in Execute Path**.
- The `dev-dependency` label and the Normal-priority override **do not apply**. Those are for `[dev-dependencies]` and `[build-dependencies]` only. If the engineer chooses to remediate, standard tasks are created with no label or priority changes.
- Risk note: `Cargo.lock` lists rustls because Cargo resolves optional deps into the lock file. Being in the lock file does not mean it is compiled into the default artifact.

## Upstream Fix Status (Step 2.5, simulated)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x  | Cargo     | release/0.4.z   | not determined (no `git -C` run in the eval; no fixture data) | Unknown |

If remediation is chosen and HEAD still has rustls < 0.23.5, an upstream PR to bump rustls is needed first, followed by the Konflux release repo update.

## Engineer Confirmation

Waiting for the engineer to confirm this table and to answer the feature-gate VEX prompt before Step 3 (Affects Versions correction) and Step 8 (remediation or closure).
