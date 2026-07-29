# Feature-Gate VEX Justification Prompt: TC-8051

## Context

- **CVE**: CVE-2026-99002
- **Library**: rustls
- **Affected range**: versions before 0.23.5
- **Version in product**: 0.23.4 (all 2.2.x versions)
- **Feature flag**: `tls-rustls`
- **Default features**: `["tls-native"]` (does NOT include `tls-rustls`)
- **Dependency declaration**: `rustls = { version = "0.23.4", optional = true }`

## VEX Justification Prompt

The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. The default feature set is `["tls-native"]`, meaning production builds use `native-tls` as the TLS backend and do not compile or link `rustls`. Recommended VEX justification: **Vulnerable Code not in Execute Path**.

Options:
1. **Skip remediation** -- apply VEX justification "Vulnerable Code not in Execute Path" and close as not affected
2. **Proceed with remediation** -- create tasks despite the feature gate

Choose (1/2):

## Rationale

If option 1 is selected:
- The Vulnerability issue TC-8051 would be closed as "Not a Bug" with resolution indicating the product is not affected.
- The VEX Justification custom field (`customfield_12345`) would be set to **Vulnerable Code not in Execute Path**.
- Justification: rustls is an optional dependency that is only included when the non-default `tls-rustls` feature is explicitly enabled. The product's default build configuration uses `tls-native` and does not compile, link, or execute any rustls code. The vulnerable certificate validation code path in rustls is therefore not present in default production builds.

If option 2 is selected:
- Standard remediation tasks would be created for the 2.2.x stream (2 tasks: upstream backport + downstream propagation) without any label or priority modifications.
- The tasks would target bumping rustls from 0.23.4 to >= 0.23.5 in the backend Cargo.toml manifest.
