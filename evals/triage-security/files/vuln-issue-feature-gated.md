<!-- SYNTHETIC TEST DATA — Vulnerability issue for a feature-gated optional dependency for triage-security eval testing -->

# Mock Jira Vulnerability Issue

**Key**: TC-8051
**Summary**: CVE-2026-99002 rustls - Certificate validation bypass [rhtpa-2.2]
**Issue Type**: Vulnerability
**Status**: New
**Labels**: CVE-2026-99002, pscomponent:org/rhtpa-server
**Affects Versions**: RHTPA 2.2.0
**Due Date**: 2026-08-01
**Assignee**: Unassigned

## Remote Links

- [CVE-2026-99002](https://www.cve.org/CVERecord?id=CVE-2026-99002) — CVE Record
- [rustls/rustls#2100](https://github.com/rustls/rustls/pull/2100) — Upstream fix PR

## Comments

_(no comments)_

---

## Description

A vulnerability was found in rustls. The rustls crate before version 0.23.5 improperly validates server certificates when using custom certificate verifiers, allowing a man-in-the-middle attacker to present an invalid certificate chain.

**Affected package**: rustls
**Affected versions**: versions before 0.23.5
**Fixed version**: 0.23.5
**CVSS**: 8.1 (High)

### References

- https://www.cve.org/CVERecord?id=CVE-2026-99002

---

## Mock Dependency Chain Data

The following data simulates what Step 2.3.5 would discover when inspecting
the Cargo.toml manifest files. In a real triage, the skill reads manifests
via `git show`; in this eval, use this data as the simulated output.

### rustls dependency chain for backend

```
Dependency chain for rustls:
  backend (workspace) → rustls (direct optional dependency)
  Profile: feature-gated (optional = true, behind non-default feature "tls-rustls")
  Default features do NOT include "tls-rustls" — the product ships with
  the "tls-native" feature enabled by default

Feature declaration:
  [features]
  default = ["tls-native"]
  tls-native = ["dep:native-tls"]
  tls-rustls = ["dep:rustls"]

First appeared: 2.2.0 (added as alternative TLS backend)
Not present in: 2.1.x (only native-tls was available)
```

**Manifest evidence:**
```toml
# backend/Cargo.toml (v0.4.5+)
[dependencies]
rustls = { version = "0.23.4", optional = true }

[features]
default = ["tls-native"]
tls-native = ["dep:native-tls"]
tls-rustls = ["dep:rustls"]
```
