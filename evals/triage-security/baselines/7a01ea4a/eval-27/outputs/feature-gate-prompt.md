# Feature-Gated Dependency -- VEX Justification Prompt

The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. Recommended VEX justification: **Vulnerable Code not in Execute Path**.

Options:
1. Skip remediation -- apply VEX justification and close as not affected
2. Proceed with remediation -- create tasks despite the feature gate

Choose (1/2):

---

## Context

- **Library**: rustls
- **CVE**: CVE-2026-99002
- **Affected range**: versions before 0.23.5
- **Shipped version**: 0.23.4 (all 2.2.x versions)
- **Feature flag**: `tls-rustls` (non-default, optional)
- **Default features**: `["tls-native"]` -- does NOT include `tls-rustls`
- **Manifest declaration**: `rustls = { version = "0.23.4", optional = true }`

The `rustls` crate is an optional dependency in `backend/Cargo.toml`. It is only compiled into the binary when a consumer explicitly enables the `tls-rustls` feature flag. Under the default build configuration (`default = ["tls-native"]`), the product uses `native-tls` as its TLS backend and the rustls code is not present in the compiled binary.

## VEX Justification

**Vulnerable Code not in Execute Path** -- The package is shipped in the lock file but the vulnerable code path is not included in the default build. The `tls-rustls` feature must be explicitly enabled by a downstream consumer for the rustls code to be compiled and executed.

## If Option 1 (Skip remediation)

- Close the Vulnerability issue as "Not a Bug" with VEX justification field (`customfield_12345`) set to "Vulnerable Code not in Execute Path"
- Post triage summary comment documenting the feature-gate analysis

## If Option 2 (Proceed with remediation)

- Create standard remediation tasks (upstream backport + downstream propagation) for the 2.2.x stream
- No label or priority modifications (standard remediation despite feature gate)
