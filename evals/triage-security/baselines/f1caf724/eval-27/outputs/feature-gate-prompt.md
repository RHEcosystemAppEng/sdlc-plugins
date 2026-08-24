# Feature-Gated Dependency -- VEX Justification Prompt

## Context

The vulnerable dependency `rustls` (CVE-2026-99002, CVSS 8.1 High) is gated behind the `tls-rustls` feature, which is not enabled by default. The product ships with the `tls-native` feature enabled by default, meaning rustls code is not compiled into or executed by the default product build.

Manifest evidence:

```toml
# backend/Cargo.toml (v0.4.5+)
[dependencies]
rustls = { version = "0.23.4", optional = true }

[features]
default = ["tls-native"]
tls-native = ["dep:native-tls"]
tls-rustls = ["dep:rustls"]
```

## VEX Justification Prompt

The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. Recommended VEX justification: **Vulnerable Code not in Execute Path**.

Options:
1. **Skip remediation** -- apply VEX justification and close as not affected
2. **Proceed with remediation** -- create tasks despite the feature gate

Choose (1/2):

## Option 1 Details (Skip remediation)

If the user chooses option 1:
- Close the Vulnerability issue as "Not a Bug" (not affected)
- Set VEX Justification custom field (`customfield_12345`) to: **Vulnerable Code not in Execute Path**
- Rationale: The rustls dependency is declared as `optional = true` and gated behind the non-default `tls-rustls` feature flag. The default product build enables `tls-native` instead, so rustls code is not compiled into or executed by the shipped product. The vulnerable code path (certificate validation bypass in rustls < 0.23.5) cannot be reached in the default configuration.
- Add comment: "No supported versions ship rustls in the default build configuration. The rustls crate is an optional dependency gated behind the non-default `tls-rustls` feature flag. The default build uses `tls-native` (native-tls). Version impact analysis confirms rustls 0.23.4 is present in Cargo.lock but not activated by default features. VEX justification: Vulnerable Code not in Execute Path."

## Option 2 Details (Proceed with remediation)

If the user chooses option 2:
- Create standard remediation tasks (upstream backport + downstream propagation) for the 2.2.x stream without any label or priority modifications
- The upstream task would bump rustls from 0.23.4 to >= 0.23.5 in the `backend` repository on the `release/0.4.z` branch
- The downstream task would update the backend source reference in the Konflux release repo `rhtpa-release.0.4.z`
