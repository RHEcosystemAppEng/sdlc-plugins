# Feature-Gated Dependency -- VEX Justification Prompt

## Context

The vulnerability CVE-2026-99002 affects `rustls` versions before 0.23.5. In the 2.2.x stream, `rustls` 0.23.4 is present in the Cargo.lock but is an **optional dependency** gated behind the **non-default** `tls-rustls` feature flag.

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

The default features are `["tls-native"]`. The `tls-rustls` feature is not included in the default feature set. The product ships with the `tls-native` feature enabled, meaning `rustls` is **not compiled or linked** in the default build.

## VEX Justification Prompt

The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. Recommended VEX justification: **Vulnerable Code not in Execute Path**.

Options:
1. Skip remediation -- apply VEX justification and close as not affected
2. Proceed with remediation -- create tasks despite the feature gate

Choose (1/2):

## Rationale

If the user chooses **option 1**:
- Set VEX Justification custom field (`customfield_12345`) to: **Vulnerable Code not in Execute Path**
- Close the Vulnerability issue TC-8051 with resolution "Not a Bug"
- Add comment documenting the feature-gate analysis and VEX justification

If the user chooses **option 2**:
- Create standard remediation tasks (dependency bump + downstream propagation) without dev-dependency label or priority override
- The remediation would bump rustls from 0.23.4 to >= 0.23.5 for all affected 2.2.x versions
